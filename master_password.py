""" TODO add more types and synonyms:
    TODO update descriptions...
  x, maximum  | 20 characters, contains symbols.
  l, long     | Copy-friendly, 14 characters, symbols.
  m, medium   | Copy-friendly, 8 characters, symbols.
  b, basic    | 8 characters, no symbols.
  s, short    | Copy-friendly, 4 characters, no symbols.
  i, pin      | 4 numbers.
  n, name     | 9 letter name.
  p, phrase   | 20 character sentence.
  K, key      | encryption key (512 bit or -P bits).
  B, longbasic | ...
"""
import scrypt
import hmac
import hashlib
import struct
# TODO implement MP algorithm v0 v1 v2

# authentication scope
# TODO other scopes
scope = b"com.lyndir.masterpassword"

# TODO DOC
N, r, p, dk_len = 32768, 8, 2, 64


# TODO DOC
char_classes = {
    "V": "AEIOU",
    "C": "BCDFGHJKLMNPQRSTVWXYZ",
    "v": "aeiou",
    "c": "bcdfghjklmnpqrstvwxyz",
    "A": "AEIOUBCDFGHJKLMNPQRSTVWXYZ",
    "a": "AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz",
    "n": "0123456789",
    "o": "@&%?,=[]_:-+*$#!'^~;()/.",
    "x": "AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz0123456789!@#$%^&*()",
    "X": "AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz0123456789!@#$%^&*()",
    " ": " "
}


# TODO DOC
template_classes = {
    "maximum": ["anoxxxxxxxxxxxxxxxxx", "axxxxxxxxxxxxxxxxxno"],
    "long": ["CvcvnoCvcvCvcv", "CvcvCvcvnoCvcv", "CvcvCvcvCvcvno",
             "CvccnoCvcvCvcv", "CvccCvcvnoCvcv", "CvccCvcvCvcvno",
             "CvcvnoCvccCvcv", "CvcvCvccnoCvcv", "CvcvCvccCvcvno",
             "CvcvnoCvcvCvcc", "CvcvCvcvnoCvcc", "CvcvCvcvCvccno",
             "CvccnoCvccCvcv", "CvccCvccnoCvcv", "CvccCvccCvcvno",
             "CvcvnoCvccCvcc", "CvcvCvccnoCvcc", "CvcvCvccCvccno",
             "CvccnoCvcvCvcc", "CvccCvcvnoCvcc", "CvccCvcvCvccno"],
    "medium": ["CvcnoCvc", "CvcCvcno"],
    "short": ["Cvcn"],
    "basic": ["aaanaaan", "aannaaan", "aaannaaa"],
    "longbasic": ["aaanaaanaaanaaan", "aannaaanaannaaan", "aaannaaaaaannaaa"],
    "pin": ["nnnn"],
    "name": ["cvccvcvcv"],
    "phrase": ["cvcc cvc cvccvcv cvc", "cvc cvccvcvcv cvcv", "cv cvccv cvc cvcvccv"]
}

synonyms = {
    "maximum": "x",
    "long": "l",
    "medium": "m",
    "basic": "b",
    "short": "s",
    "longbasic": "lb",
    "pin": "#",
    "name": "n",
    "phrase": "ph",
}

tmp = tuple(template_classes.items())
for k, v in tmp:
    template_classes[synonyms[k]] = v


def int2bytes(n):
    # TODO DOC
    # TODO ensure 4 bytes
    if n < 1 or n > 4294967295:
        raise Exception("ERROR!")
    # big-endian integer
    # TODO make sure it's 4 bytes
    return struct.pack('>i', n)


def len2bytes(s):
    # TODO DOC
    return int2bytes(len(s))


def master_key(name, master_pw, scope=scope, N=N, r=r, p=p, dk_len=dk_len, enc='utf8'):
    # TODO DOC
    if type(name) is str:
        name = bytes(name, enc)
    if type(master_pw) is str:
        master_pw = bytes(master_pw, enc)
    salt = seed = b''.join([scope, len2bytes(name), name])
    return scrypt.hash(password=master_pw, salt=salt, N=N, r=r, p=p, buflen=dk_len)


def site_key(site_name, master_key, counter=1, enc='utf8', scope=scope):
    # TODO DOC
    if type(site_name) is str:
        site_name = bytes(site_name, enc)
    site_seed = b''.join([scope, len2bytes(site_name),
                          site_name, int2bytes(counter)])
    return hmac.digest(key=master_key, msg=site_seed, digest=hashlib.sha256)


def site_password(site_name, master_key, template_class="Long", counter=1):
    # TODO DOC
    seed = site_key(site_name, master_key, counter)

    template_class = template_classes[template_class]
    template = template_class[seed[0] % len(template_class)]

    password = ''.join([char_classes[c][seed[i + 1] % len(char_classes[c])]
                        for i, c in enumerate(template)])

    return password
