from unittest import TestCase

from pympw import master_key, site_password

user = "USER"
password = "PASSWORD"
site_tests = {
    ("google.com", "x"): "i%&yc(sRV7VJqOQK%G0~",
    ("google.com", "pin"): "7002",
    ("google.com", "basic"): "iIh2cLs7",
    ("google.com", "medium"): "KasWik5.",
    ("google.com", "long"): "Kasi2/FipsHonm",
    ("google.com", "phrase"): "kasw kaz segnucu dax",
    ("google.com", "name"): "kaswikazi",
    ("site 42 . !!?", "x"): "S2@TW#$$Bb$5LA0$eDx1",
    ("site 42 . !!?", "pin"): "8287",
    ("site 42 . !!?", "basic"): "SQ87HDd9",
    ("SITE 42 . !!?", "medium"): "YeyMeb8%",
    ("Site 42 . !!?", "long"): "Mosx0/RazuBaje",
    ("Site 42 . !!?", "phrase"): "mosx rem xetjefe wot",
    ("Site 42 . !!?", "name"): "mosxaremi",
}
counter_tests = {
    ("google.com", "x", 2): "O9uoPZJKQPCB^hMYHL6(",
    ("google.com", "x", 20000): "w8^aERdEe5v)WJuLkCM&",
    ("google.com", "name", 2147483647): "megreseva",
    ("google.com", "phrase", 2147483647): "me resva daf kivotmo",
}
long_tests = {("google.com" * 1000, "x", 20000): "j1-@SYRoIclOmZRWNx(F"}


def test_sites():
    key = master_key(user, password)
    for args, known_password in site_tests.items():
        assert site_password(key, *args) == known_password, args


def test_counter():
    key = master_key(user, password)
    for args, known_password in counter_tests.items():
        assert site_password(key, *args) == known_password, args


def test_long_inputs():
    key = master_key(user, password)
    for args, known_password in long_tests.items():
        assert site_password(key, *args) == known_password, args
