"""
Basic object to hold an s-expression cargo/list, etc.

Think about using Stackless and channels.
"""



nil = lambda: None

class Node(object):
    def __init__(self, cargo=None, next=nil):
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

    def __getattr__(self, name):
        if name in ['car', 'cdr']:
            name = '_{name}'.format(name=name)
            try:
                return self.__dict__[name]()
            except:
                return self.__dict__[name]
        else:
            raise AttributeError("{name} attribute not found".format(name=name))

    def __iter__(self):
        return self._pre_order()

    def _pre_order(self):
        if type(self.car) != Node:
            yield self.car
        else:
            for cargo in self.car:
                yield cargo
        if type(self.cdr) != Node:
            yield self.cdr
        else:
            for cargo in self.cdr:
                yield cargo

    def next(self):
        return self.cdr


cons = lambda el, lst=nil: Node(el, lst)
car = lambda lst: lst.car()
cdr = lambda lst: lst.next()
nth = lambda n, lst: nth(n-1, cdr(lst)) if n > 0 else car(lst)
length = lambda lst, count=0: len(lst, count)  # could just call len(lst)
