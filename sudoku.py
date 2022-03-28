class Solver:
    def __init__(self,table):
        self.table=table
        self.n=len(table)
        self.smn=int(self.n**0.5+0.2)
        self.tableCandi = [[[] for c in range(self.n)] for r in range(self.n)]
        self.peers = [[self.getPeer(r,c) for c in range(self.n)] for r in range(self.n)]

        for r in range(self.n):
            for c in range(self.n):
                if table[r][c]<1: continue
                self.add(r,c,table[r][c])

        for r in range(self.n):
            for c in range(self.n):
                if table[r][c]>=1: continue
                tmp=[]
                for cand in range(1,self.n+1):
                    if cand in self.tableCandi[r][c]: continue
                    tmp.append(cand)
                self.tableCandi[r][c]=tmp

    def getPeer(self,r,c):
        re=[]
        for i in range(self.n):
            if i!=c: re.append((r,i))
            if i!=r: re.append((i,c))
        rsm,csm=r-r%self.smn,c-c%self.smn
        for ri in range(rsm,rsm+self.smn):
            for ci in range(csm,csm+self.smn):
                if ri==r or ci==c: continue
                re.append((ri,ci))
        return re

    def add(self,r,c,val):
        for ri,ci in self.peers[r][c]:
            if self.table[ri][ci]<1 and not val in self.tableCandi[ri][ci]: 
                self.tableCandi[ri][ci].append(val)

    def remove(self,r,c,val):
        memo,valid=[],True
        for ri,ci in self.peers[r][c]:
            if self.table[ri][ci]<1:
                try:
                    self.tableCandi[ri][ci].remove(val)
                    memo.append((ri,ci))
                    if len(self.tableCandi[ri][ci])==0:
                        valid=False
                        break
                except:pass
        return memo,valid

    def check(self,r,c,val):
        f=True
        for i in range(self.n):
            if self.table[r][i]<1 and val in self.tableCandi[r][i]:
                f=False
                break
        if f: return True
        f=True
        for i in range(self.n):
            if self.table[i][c]<1 and val in self.tableCandi[i][c]:
                f=False
                break
        if f: return True
        f=True
        rsm,csm=r-r%self.smn,c-c%self.smn
        for ri in range(rsm,rsm+self.smn):
            for ci in range(csm,csm+self.smn):
                if self.table[ri][ci]>=1: continue
                if val in self.tableCandi[ri][ci]:
                    return False
        return True

    def getNext(self):
        mr,mc=-1,-1
        for r in range(self.n):
            for c in range(self.n):
                if self.table[r][c]>=1: continue
                if mr==-1 or len(self.tableCandi[r][c])<len(self.tableCandi[mr][mc]):
                    mr=r
                    mc=c
        return mr,mc

    def solve(self,cur=0,func=None):
        for i1 in range(cur,self.n**2):
            i,j=divmod(i1,self.n)
            if self.table[i][j]>=1: continue
            if len(self.tableCandi[i][j])==0: return False
            for cand in self.tableCandi[i][j]:
                self.table[i][j]=cand
                if self.check(i,j,cand) or len(self.tableCandi[i][j])==1:
                    if func:func(i,j)
                    memo,valid=self.remove(i,j,cand)
                    if valid:
                        if self.solve(i1+1,func): return True
                    for ri,ci in memo: self.tableCandi[ri][ci].append(cand)
                    self.table[i][j]=0
                    
                    return False
                self.table[i][j]=0
        r,c=self.getNext()
        if r==-1: return True # solved
        if len(self.tableCandi[r][c])==0: return False # dead end
        for cand in self.tableCandi[r][c]:
            self.table[r][c]=cand
            if func:func(r,c)
            memo,valid=self.remove(r,c,cand)
            if valid:
                if self.solve(0,func): return True
            for ri,ci in memo: self.tableCandi[ri][ci].append(cand)
        self.table[r][c]=0

        return False

    def infoCell(self,r,c):
        print()
        print('Row: %d, Column: %d'%(r+1,c+1))
        print('Possible values:',', '.join(map(str,self.tableCandi[r][c])))

class Solver2:
    def __init__(self,table):
        self.table=table
        self.n=len(table)
        self.smn=int(self.n**0.5+0.2)
        
    def check(self,r,c,val):
        for i in range(self.n):
            if self.table[r][i]==val: return False
            if self.table[i][c]==val: return False
        rsm,csm=r-r%self.smn,c-c%self.smn
        for ri in range(rsm,rsm+self.smn):
            for ci in range(csm,csm+self.smn):
                if self.table[ri][ci]==val: return False
        return True
    
    def solve(self,cur=0,func=None):
        if cur==self.n**2: return True
        r,c=divmod(cur,self.n)
        if self.table[r][c]>=1:
            return self.solve(cur+1,func)
        for cand in range(1,self.n+1):
            if self.check(r,c,cand):
                self.table[r][c]=cand
                if func: func(r,c)
                if self.solve(cur+1,func): return True
        self.table[r][c]=0
        return False
    
    def infoCell(self,r,c):
        print()
        print('Row: %d, Column: %d'%(r+1,c+1))