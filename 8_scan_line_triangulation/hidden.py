import matplotlib.pyplot as plt

def turn(v1, v2, v3):
    return (v2.x - v1.x) * (v3.y - v1.y) - (v3.x - v1.x) * (v2.y - v1.y)

class Vertex:
    """
    Класс точки с компаратором, подходящим для нашей задачи
    """
    def __init__(self, px, py):
        self.x = px
        self.y = py
        self.hedgelist = []
        self.vtype = None
    
    def __lt__(self, other):
        d = self.y - other.y
        if d == 0: 
            d = other.x - self.x
        return d > 0
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({0};{1})'.format(self.x,self.y)

    
class Hedge:
    """
    Класс half-edge - одностороннего ребра, которое используется в DCEL.
    """
    def __init__(self, v):
        self.origin = v
        self.twin = None
        self.next = None
        self.prev = None
        
    def __lt__(self, other):
        """
        Сравнение для дерева поиска рёбер в сканлайне 
        """
        v1 = self.origin
        v2 = self.twin.origin
        v3 = other.origin
        t = turn(v1, v2, v3)
        return t > 0
        
    def __repr__(self):
        return '{}->{}'.format(self.origin, self.twin.origin)
    

def build_dcel(vert):
    dcel = []
    start = Hedge(vert[0])
    start.twin = Hedge(vert[1])
    vert[1].hedgelist.append(start.twin)
    start.twin.twin = start
    dcel.append(start)
    prev = start
    lis = vert[1:] + [vert[0]]
    for i in range(0, len(lis)-1):
        cur = Hedge(lis[i])
        lis[i].hedgelist.append(cur)
        cur.twin = Hedge(lis[i+1])
        lis[i+1].hedgelist.append(cur.twin)
        cur.twin.twin = cur
        cur.prev = prev
        prev.next = cur
        prev.twin.prev = cur.twin
        cur.twin.next = prev.twin
        prev = cur
        dcel.append(cur)
    cur.next = start
    start.prev = cur
    start.twin.next = cur.twin
    cur.twin.prev = start.twin
    vert[0].hedgelist.append(start)
    return dcel

def add_diagonal(hfrom, hto):
    #print ('[ADD DIAGONAL] from: {} to: {}'.format(hfrom.origin, hto.origin))
    d = Hedge(hfrom.origin)
    d.twin = Hedge(hto.origin)
    """
    hfrom.prev.next = d
    d.prev = hfrom.prev
    hfrom.prev = d.twin
    d.twin.next = hfrom
    hto.prev.next = d.twin
    d.twin.prev = hto.prev
    hto.prev = d
    d.next = hto
    """
    return d

