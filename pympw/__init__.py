"""These functions implement the Master Password algorithm v3.

How to use:

1. Call master_key() once with a name and a master password
2. View available password templates in template_classes
3. Pass key, site name, counter, and password template class to site_password()
""" 
import scrypt
import hmac
import hashlib
import struct
# TODO implement MP algorithm v0 v1 v2

# Only use authentication scope
scope = b"com.lyndir.masterpassword"

# TODO Support other scopes
identification_scope = b"com.lyndir.masterpassword.login"
answer_scope = b"com.lyndir.masterpassword.answer"


# SCRYPT parameters for the Master Password algorithm v3 
N, r, p, dk_len = 32768, 8, 2, 64


# Characters in each character class of a template class
# Example: "Voc" could represent "A@b" or "I[x"
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


# All possible password templates
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

# Short names for each password template name
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

template_class_names = sum([[k, v] for k, v in synonyms.items()], [])

def int2bytes(n):
    """Convert a positive 4 byte integer into a big-endian 4-byte array"""
    if n < 1 or n > 4294967295:
        raise ValueError("can only convert positive integers to 4-byte array")
    # big-endian integer
    # TODO how to make sure it's 4 bytes?
    return struct.pack('>i', n)


def len2bytes(s):
    """Convert the length of a string into a big-endian 4-byte array""" 
    return int2bytes(len(s))


def master_key(name, master_pw, scope=scope, N=N, r=r, p=p, dk_len=dk_len, enc='utf8'):
    """Time and memory intensive. Generates master key using a name and password"""
    if len(name) == 0:
        raise ValueError("name should not have length 0")
    if len(master_pw) == 0:
        raise ValueError("master password should not have length 0")

    if type(name) is str:
        name = bytes(name, enc)
    if type(master_pw) is str:
        master_pw = bytes(master_pw, enc)
    salt = seed = b''.join([scope, len2bytes(name), name])
    return scrypt.hash(password=master_pw, salt=salt, N=N, r=r, p=p, buflen=dk_len)


def site_key(master_key, site_name, counter=1, enc='utf8', scope=scope):
    """Quickly generate a site key using password, site name, and parameters"""
    if type(site_name) is str:
        site_name = bytes(site_name, enc)

    site_seed = b''.join([scope, len2bytes(site_name),
                          site_name, int2bytes(counter)])
    return hmac.digest(key=master_key, msg=site_seed, digest=hashlib.sha256)


def site_password(master_key, site_name, template_class="long", counter=1):
    """Quickly generates a password for a site"""

    # Use the site key to generate a password of a given template class 
    seed = site_key(master_key, site_name, counter)

    template_class = template_classes[template_class]
    template = template_class[seed[0] % len(template_class)]

    password = ''.join([char_classes[c][seed[i + 1] % len(char_classes[c])]
                        for i, c in enumerate(template)])

    return password
