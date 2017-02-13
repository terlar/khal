import re

weekheader = """[1m    Mo Tu We Th Fr Sa Su   [0m"""
today = """[1mToday[0m[0m"""
calendarline = """[1mNov [0m[1;33m31[0m [32m 1[0m [1;33m 2[0m [1;33m 3[0m [1;33m 4[0m [32m 5[0m [32m 6[0m"""

input = """
[1m    Mo Tu We Th Fr Sa Su   [0m    [1mToday[0m[0m
[1mNov [0m[1;33m31[0m [32m 1[0m [1;33m 2[0m [1;33m 3[0m [1;33m 4[0m [32m 5[0m [32m 6[0m [1m44[0m    [32m↔ Anja Asien[0m[0m
    [32m 7[0m  8 [32m 9[0m [32m10[0m [1;33m11[0m [32m12[0m [32m13[0m [1m45[0m    ↔ pyData Cologne[0m[0m
    14 [32m15[0m 16 17 [1;33m18[0m [32m19[0m [32m20[0m [1m46[0m    [1mTomorrow[0m[0m
    21 [32m22[0m [32m23[0m [32m24[0m [1;33m25[0m [32m26[0m [32m27[0m [1m47[0m    [32m↔ Anja Asien[0m[0m
[1mDec [0m[1;33m28[0m [7m29[0m [1;33m30[0m [1;33m 1[0m [1;33m 2[0m [32m 3[0m [32m 4[0m [1m48[0m    ⇥ pyData Cologne[0m[0m
     5  6  7  8 [1;33m 9[0m [32m10[0m 11 [1m49[0m
    12 [34m13[0m [1;33m14[0m 15 [34m16[0m [32m17[0m [32m18[0m [1m50[0m
    19 20 21 22 23 24 25 [1m51[0m
[1mJan [0m26 27 28 29 30 31  1 [1m52[0m
     2  3  4  5  6  7  8 [1m 1[0m
    [1;31m 9[0m 10 [1;33m11[0m 12 [1;33m13[0m 14 15 [1m 2[0m
    16 17 18 [1;31m19[0m [34m20[0m 21 22 [1m 3[0m
    23 24 25 26 [34m27[0m 28 29 [1m 4[0m
[1mFeb [0m30 [1;31m31[0m  1  2 [34m 3[0m  4  5 [1m 5[0m
"""

RESET = '\x1b[0m'

ansi_reset = re.compile(r'(\x1b\[0m)')
ansi_sgr = re.compile(r'(\x1b\[[^0^m]*m)')


def find_last_reset(string):
    for match in re.finditer(ansi_reset, string):
        pass
    try:
        return match.start(), match.end(), match.group(0)
    except UnboundLocalError:
        return -2, -1, ''


def find_last_sgr(string):
    for match in re.finditer(ansi_sgr, string):
        pass
    try:
        return match.start(), match.end(), match.group(0)
    except UnboundLocalError:
        return -2, -1, ''


def find_unmatched_sgr(string):
    reset_pos, _, _ = find_last_reset(string)
    sgr_pos, _, sgr = find_last_sgr(string)
    if sgr_pos > reset_pos:
        return sgr
    else:
        return False


def test_last_reset():
    assert find_last_reset(weekheader) == (31, 35, '\x1b[0m')
    assert find_last_reset(today) == (13, 17, '\x1b[0m')
    assert find_last_reset(calendarline) == (99, 103, '\x1b[0m')
    assert find_last_reset('Hello World') == (-2, -1, '')


def test_last_sgr():
    assert find_last_sgr(weekheader) == (0, 4, '\x1b[1m')
    assert find_last_sgr(today) == (0, 4, '\x1b[1m')
    assert find_last_sgr(calendarline) == (92, 97, '\x1b[32m')
    assert find_last_sgr('Hello World') == (-2, -1, '')


def test_find_unmatched_sgr():
    assert find_unmatched_sgr(weekheader) is False
    assert find_unmatched_sgr(today) is False
    assert find_unmatched_sgr(calendarline) is False
    assert find_unmatched_sgr(calendarline) is False
    assert find_unmatched_sgr('\x1b[31mHello World') == '\x1b[31m'
    assert find_unmatched_sgr('\x1b[31mHello\x1b[0m \x1b[32mWorld') == '\x1b[32m'
    assert find_unmatched_sgr('foo [1;31mbar') == '\x1b[1;31m'
