# coding: utf-8
# TODO PDF: where to find v012 docs?
import scrypt
import hmac
import hashlib
import struct
import math


master_pw = "PASSWORD"  # input()
master_pw = bytes(master_pw, 'utf8')
name = b"USER"


# authentication scope
scope = b"com.lyndir.masterpassword"
N, r, p, dk_len = 32768, 8, 2, 64


char_classes = {
    "V": "AEIOU",
    "C": "BCDFGHJKLMNPQRSTVWXYZ",
    "v": "aeiou",
    "c": "bcdfghjklmnpqrstvwxyz",
    "A": "AEIOUBCDFGHJKLMNPQRSTVWXYZ",
    "a": "AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz",
    "n": "0123456789",
    # TODO PDF: INCORRECTLY DOCUMENTED AS "n": "123456789",
    "o": "@&%?,=[]_:-+*$#!'^~;()/.",
    "x": "AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz0123456789!@#$%^&*()",
    # INCORRECTLY SPECIFIED AS 'X' instead of 'x'
    "X": "AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz0123456789!@#$%^&*()",
    # NOT SPECIFIED?
    " ": " "
}


template_classes = {
    "Maximum": ["anoxxxxxxxxxxxxxxxxx", "axxxxxxxxxxxxxxxxxno"],
    # CAREFUL WITH ORDER!!! COLUMN OR ROW??
    # TODO PDF: MAYBE INCORRECT IN PDF!!!
    "Long": ["CvcvnoCvcvCvcv",
             "CvcvCvcvnoCvcv",
             "CvcvCvcvCvcvno",
             "CvccnoCvcvCvcv",
             "CvccCvcvnoCvcv",
             "CvccCvcvCvcvno",
             "CvcvnoCvccCvcv",
             "CvcvCvccnoCvcv",
             "CvcvCvccCvcvno",
             "CvcvnoCvcvCvcc",
             "CvcvCvcvnoCvcc",
             "CvcvCvcvCvccno",
             "CvccnoCvccCvcv",
             "CvccCvccnoCvcv",
             "CvccCvccCvcvno",
             "CvcvnoCvccCvcc",
             "CvcvCvccnoCvcc",
             "CvcvCvccCvccno",
             "CvccnoCvcvCvcc",
             "CvccCvcvnoCvcc",
             "CvccCvcvCvccno"],
    "Medium": ["CvcnoCvc", "CvcCvcno"],
    "Short": ["Cvcn"],
    "Basic": ["aaanaaan", "aannaaan", "aaannaaa"],
    "PIN": ["nnnn"],
    "Name": ["cvccvcvcv"],
    "Phrase": ["cvcc cvc cvccvcv cvc", "cvc cvccvcvcv cvcv", "cv cvccv cvc cvcvccv"]
}


def INT(n):
    # TODO ensure 4 bytes
    if n < 1 or n > 4294967295:
        raise Exception("ERROR!")
    # big-endian integer
    # TODO make sure it's 4 bytes
    return struct.pack('>i', n)


def LEN(s):
    return INT(len(s))


def master_key(name, master_pw, scope=scope, N=N, r=r, p=p, dk_len=dk_len):
    salt = seed = b''.join([scope, LEN(name), name])
    return scrypt.hash(password=master_pw, salt=salt, N=N, r=r, p=p, buflen=dk_len)


def site_key(site_name, master_key, counter=1):
    site_name = bytes(site_name, 'utf8')
    site_seed = b''.join([scope, LEN(site_name), site_name, INT(counter)])
    return hmac.digest(key=master_key, msg=site_seed, digest=hashlib.sha256)


def site_password(site_name, master_key, template_class="Long", counter=1):
    seed = site_key(site_name, master_key, counter)

    template_class = template_classes[template_class]
    template = template_class[seed[0] % len(template_class)]

    password = ''.join([char_classes[c][seed[i + 1] % len(char_classes[c])] 
                       for i, c in enumerate(template)])

    return password
