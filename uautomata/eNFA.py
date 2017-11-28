from __future__ import absolute_import, division, unicode_literals

from intervaltree import IntervalTree

EPSILON = object.__new__(object)


def _to_utf16_code_units(v):
    assert v > 0xFFFF
    offset = v - 0x10000
    high = 0xD800 | (offset >> 10)
    low = 0xDC00 | (offset & 0x3FF)
    return (high, low)


class Node(object):
    def __init__(self):
        self.accepting = False
        self._outgoing_edges = IntervalTree()
        self._outgoing_epsilon = set()

    def eclose(self):
        seen = set()
        search = list([self])
        while search:
            cur = search.pop()
            if cur in seen:
                continue
            seen.add(cur)
            yield cur
            search.extend(cur._outgoing_epsilon)

    def add_edge(self, k, v):
        if k is EPSILON:
            self._outgoing_epsilon.add(v)
            return

        if isinstance(k, tuple):
            if len(k) != 2:
                raise TypeError("add_edge only accepts 2-tuples")
            start, end = k
        elif isinstance(k, slice):
            if k.start > k.end:
                raise ValueError("add_edge only accepts ordered slices")
            if k.step:
                raise ValueError("add_edge only accepts slices without steps")
            start, end = k.start, k.end
        else:
            start = end = k

        self._outgoing_edges[start:end + 1] = v

    def has_epsilon(self):
        for node in self.iter_nodes():
            if self._outgoing_epsilon:
                return True
        return False

    def iter_nodes(self):
        seen = set()
        search = list([self])
        while search:
            cur = search.pop()
            if cur in seen:
                continue
            seen.add(cur)
            yield cur
            search.extend(cur._outgoing_epsilon)
            for v in self._outgoing_edges.items():
                search.append(v.data)

    def remove_epsilon(self):
        pass

    def to_dfa(self):
        pass

    def to_utf16_code_units(self):
        for node in self.iter_nodes():
            # Get the edges
            edges = node._outgoing_edges

            # Split the intervals at the end of the BMP
            edges.slice(0xFFFF)
            edges.chop(0xFFFF, 0x10000)

            # Rewrite all these intervals using UTF-16 code-units
            for iv in edges[0x10000:0x110000]:
                begin, end, out_node = iv
                high_beg, low_beg = _to_utf16_code_units(begin)
                high_end, low_end = _to_utf16_code_units(end)
                if high_beg == high_end:
                    high_node = Node()
                    node.add_edge(high_beg, high_node)
                    node.add_edge((low_beg, low_end), out_node)
                else:
                    assert high_end > high_beg
                    high_start_node = Node()
                    node.add_edge(high_beg, high_start_node)
                    high_start_node.add_edge((low_beg, 0xDFFF), out_node)
                    if high_beg + 1 != high_end:
                        high_mid_node = Node()
                        node.add_edge((high_beg + 1, high_end - 1), high_mid_node)
                        high_mid_node.add_edge((0xDC00, 0xDFFF), out_node)
                    high_end_node = Node()
                    node.add_edge(high_end, high_end_node)
                    high_end_node.add_edge((0xDC00, low_end), out_node)
            edges.remove_overlap(0x10000, 0x110000)

    def match(self, s):
        states = set(self.eclose())
        for c in s:
            c = ord(c)
            old_states = states
            states = set()
            for state in old_states:
                for iv in state._outgoing_edges[c]:
                    states |= set(iv.data.eclose())
        for state in states:
            if state.accepting:
                return True
        return False
