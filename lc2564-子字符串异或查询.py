from collections import OrderedDict
from copy import deepcopy

class State:
    def __init__(self, length=None, link=None,trans={},pos=-1):
        self.length = length
        self.link = link
        self.trans = trans
        self.pos=pos
    def __str__(self):
        return f'{str(self.trans)} {self.pos}'
    
class SAM:
    def __init__(self, s=""):
        self.last = 0
        self.sz = 1
        self.st = OrderedDict({0: State(0, -1,OrderedDict(),-1)})
        self(s)

    def _extend(self, c,pos):
        cur = self.sz
        self.st[cur] = State(None, None, OrderedDict(),pos)
        self.st[cur].length = self.st[self.last].length + 1     
        p=self.last
        while p > -1 and self.st[p].trans.get(c) is None:
            self.st[p].trans[c] = cur
            p = self.st[p].link           
        if p == -1:
            self.st[cur].link = 0
        else:
            q = self.st[p].trans[c]           
            if self.st[p].length + 1 == self.st[q].length:
                self.st[cur].link = q
            else:
                self.sz += 1            
                self.st[self.sz] = State(self.st[p].length + 1, self.st[q].link, deepcopy(self.st[q].trans),self.st[q].pos)
                while p > -1 and self.st[p].trans.get(c) == q:
                    self.st[p].trans[c] = self.sz 
                    p = self.st[p].link
                self.st[q].link = self.st[cur].link = self.sz       
        self.sz += 1
        self.last = cur
    
    def __call__(self, s):
        for i,c in enumerate(s):
            self._extend(c,i)
            
            
class Solution:
    def substringXorQueries(self, s: str, queries: List[List[int]]) -> List[List[int]]:
        sam=SAM(s)
        res=[]
        for a,b in queries:
            c=bin(a^b)[2:]
            idx=0
            for ch in c:
                if ch not in sam.st[idx].trans:
                    res.append([-1,-1])
                    break
                idx=sam.st[idx].trans[ch]
            else:
                finish=sam.st[idx].pos
                res.append([finish-len(c)+1,finish])
        return res
