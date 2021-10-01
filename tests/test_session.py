import pytest
import random
import string
import time

from airshare import Session
from pyperclip import copy


def test_session_init():
    s = Session()
    s.stop()


def test_session_duplicates():
    with pytest.raises(OSError):
        s1 = Session()
        _ = Session(s1.host)
    s1.stop()


def test_session_connect():
    s1 = Session()
    s2 = Session(None, s1.host)
    s1.stop()
    s2.stop()


def test_session_clipboard():
    data = "".join(random.sample(string.ascii_letters + string.digits, 20))
    s1 = Session()
    s2 = Session(None, s1.host)
    time.sleep(1)
    s1.clipboard = copy(data)
    time.sleep(1)
    assert s2.node.data == data
    s1.stop()
    s2.stop()


def test_session_logging():
    s1 = Session()
    s2 = Session(None, s1.host)
    time.sleep(1)
    for i in range(5):
        data = "".join(random.sample(string.ascii_letters + string.digits, 20))
        session = s1 if i % 2 == 0 else s2
        session.clipboard = copy(data)
        time.sleep(2)
        print(len(s1.log), s1.log)
        print(len(s2.log), s2.log)
    assert len(s1.log) == 5 and len(s2.log) == 5
    s1.stop()
    s2.stop()
