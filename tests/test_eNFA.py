from __future__ import absolute_import, division, unicode_literals

import pytest

from uautomata.eNFA import Node, EPSILON

@pytest.mark.parametrize("s,matches", [
    ("", True),
    ("a", False),
])
def test_empty(s, matches):
    a = Node()
    a.accepting = True
    assert a.match(s) is matches


@pytest.mark.parametrize("s,matches", [
    ("", False),
    ("a", True),
    ("b", False),
    ("ba", False),
    ("aa", False),
])    
def test_single(s, matches):
    a = Node()
    b = Node()
    b.accepting = True
    a.add_edge(ord("a"), b)
    assert a.match(s) is matches


@pytest.mark.parametrize("s,matches", [
    ("", False),
    ("\uDBFF", False),
    ("\uDBFF\uDFFF", True),
    ("\uDBFE\uDFFF", False),
    ("\uDC00\uDFFF", False),
    ("\uDBFF\uDFFE", False),
    ("\uDBFF\uE000", False),
])    
def test_utf16_max(s, matches):
    a = Node()
    b = Node()
    b.accepting = True
    a.add_edge(0x10FFFF, b)
    a.to_utf16_code_units()
    assert a.match(s) is matches
