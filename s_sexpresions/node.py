"""
Basic object to hold an s-expression cargo/list, etc.

"""
from greenlet import greenlet

nil = lambda: None

class Node(object):
    _nil = nil
    def __init__(self, cargo=None, next=None):
        if next is None:
            next = self._nil  # lets me do some fun things without metaclasisng it yet
        self._car = cargo
        self._cdr = next

    def __unicode__(self):
        return unicode(self.car)

    def __str__(self):
        return self.__unicode__()

    def __len__(self, count=0):
        """assuming i'm just a list."""
        return len(self.next(), count+1) if self.next() else count

    def depth(self, depth=0):
        l_depth = r_depth = 0
        depth += 1
        if type(self.car) == Node:
            l_depth = self.car.depth(depth)
        if type(self.cdr) == Node:
            r_depth = self.cdr.depth(depth)
        return max(l_depth, r_depth, depth)


    def __nonzero__(self):
        return self.car is not None and self.car != nil

    @property
    def car(self):
        try:
            return self._car()
        except:
            return self._car

    @property
    def cdr(self):
        try:
            return self._cdr()
        except:
            return self._cdr

    def __iter__(self):
        return self._pre_order()

    def _pre_order(self):
        if not isinstance(self.car, Node):
            yield self.car
        else:
            for cargo in self.car:
                yield cargo
        if not isinstance(self.cdr, Node):
            yield self.cdr
        else:
            for cargo in self.cdr:
                yield cargo

    def next(self):
        return self.cdr

    @classmethod
    def parse(cls, data):
        parser = Parser(data, cls)
        return parser()


class LazyNode(Node):
    _nil = None
    @property
    def car(self):
        if isinstance(self._car, GreenParser):
            green_parser = self._car
            self._car = green_parser.switch()
        return self._car

    @property
    def cdr(self):
        if isinstance(self._cdr,GreenParser):
            green_parser = self._cdr
            self._cdr = green_parser.switch()
        return self._cdr

    @classmethod
    def parse(cls, data):
        parser = GreenParser(data, cls)
        return parser()


class Parser(object):
    _nil = nil

    def __init__(self, data, node_class):
        self._data = data
        self.node_class = node_class

    def get_node(self):
        """Return a Node with the cargo and a Parser for cdr (or nil if there
        is no remaining data)"""
        split_data = self._data.split(',',1)
        if len(split_data) == 1:
            return self.node_class(split_data[0])
        else:
            return self.node_class(split_data[0], Parser(split_data[1],
                self.node_class))

    def __call__(self):
        return self.get_node()


class GreenParser(greenlet, Parser):
    def __init__(self, data, node_class):
        self._data = data
        self.node_class = node_class

    def parse_data(self):
        """toy parser."""
        split_data = self._data.split(',',1)
        return split_data

    def get_node(self):
        split_data = self.parse_data()
        if len(split_data) == 1:
            return self.node_class(split_data[0])
        else:
            return self.node_class(split_data[0], GreenParser(split_data[1],
                self.node_class))

    def run(self):
        return self.get_node()

    def __call__(self):
        cargo = self.switch()
        return cargo


cons = lambda el, lst=nil: Node(el, lst)
car = lambda lst: lst.car()
cdr = lambda lst: lst.next()
nth = lambda n, lst: nth(n-1, cdr(lst)) if n > 0 else car(lst)
length = lambda lst, count=0: len(lst, count)  # could just call len(lst)
