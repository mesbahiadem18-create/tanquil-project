def showM(M, open, closed):
    print(M[0],M[1],M[2],sep="\n")
    print(f'open:{open}')
    print(f'closed:{closed}')

def find_zero(M):
    for i in range(3):
        for j in range(3):
            if M[i][j]==0:
                return (i,j)
            
#we know that the parity of EF is odd (7) so we need to know if M is odd or not
def is_soluble(M):
    l=0
    A= [x for row in M for x in row if x != 0]
    for i in range(7):#len(A)-1 is equal to 7 because we start at 0 and stop before the last element
        for j in range(i+1,8):#len(A) is equal to 8
            if A[i]>A[j]:
                l+=1
    if l%2==1:
        return True 
    return False
#h(m) is the sum of the distances between the position of the numbers and where they are supposed to be
def heuristic(M):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = M[i][j]
            if value != 0:
                for x in range(3):
                    for y in range(3):
                        if EF[x][y] == value:
                            distance += abs(i-x) + abs(j-y)
    return distance

def move(M,direction):
    i,j = find_zero(M)
    if direction=="up" and i>0:
        M[i][j],M[i-1][j]=M[i-1][j],M[i][j]
    elif direction=="down" and i<2:
        M[i][j],M[i+1][j]=M[i+1][j],M[i][j]
    elif direction=="left" and j>0:
        M[i][j],M[i][j-1]=M[i][j-1],M[i][j]
    elif direction=="right" and j<2:
        M[i][j],M[i][j+1]=M[i][j+1],M[i][j]
    else:
        return False
    return True

def T_tuple(M):
    return tuple(x for row in M for x in row)

def T_matrix(t):
    return [list(t[i:i+3]) for i in range (0, 9, 3)]

def possibilities(M):
    directions = ["up", "down", "left", "right"]
    poss=[]
    for direction in directions:
        newM=[row[:]for row in M]
        if move(newM,direction):
            poss.append(T_tuple(newM))
    return poss
    
EF=[[1,2,3],[8,0,4],[7,6,5]]
N=[0,1,2,3,4,5,6,7,8]
M=[]
for i in range (3):
    row=[]
    for j in range(3):
       while True:
           try:
               num=int(input(f'Enter a number for the place number {3*i+j+1} :'))
               if(num) not in N:
                   raise ValueError
               row.append(num)
               N.remove(num)
               break
           except ValueError:
               print("You entered a wrong value")
    M.append(row)
g=0
h=heuristic(M)
f=g+h
open=[(g,h,f)]
closed=[]
if not is_soluble(M):
    print("The puzzle is not soluble")
else:   
    start=T_tuple(M)
    goal=T_tuple(EF)
    openM=[start]
    closedM=[]
    parent = {start: None}# we store the parent of each state
    best_g = {start: 0}# we store the best g value to visit each state

    while open:
        # we search for the shortest path
        l=0
        for i in range(1,len(open)):
            if open[i][2]<open[l][2]:#we choose the path with the smallest h
                l=i
        scores=open.pop(l)
        curr=openM.pop(l)
        g, h, f = scores    
        if g != best_g.get(curr):
            continue
        currM=T_matrix(curr)  
        showM(currM, open, closed)
        if curr not in closedM:
            closed.append(scores)
            closedM.append(curr)
        
        if curr==goal:
            path=[]
            node=curr
            while node is not None:
                path.append(T_matrix(node))
                node = parent[node] 
            path.reverse()
            for step,M in enumerate(path):
                print(f'Step {step}:')
                showM(M, open, closed)
            break
        #explore the possible moves
        for poss in possibilities(currM):
            newg = g + 1
            if newg >= best_g.get(poss, float("inf")):#in case we didn't visit the cell yet it ll give infinity
                continue
            best_g[poss] = newg
            parent[poss] = curr
            possM=T_matrix(poss)
            newh = heuristic(possM)
            newf = newg + newh
            newscore=(newg, newh, newf)
            #we remove the state from closed because we found a better path to it
            if poss in closedM:
                i = closedM.index(poss)
                closedM.pop(i)
                closed.pop(i)
            #we modify open for the new state
            if poss in openM:
                i = openM.index(poss)
                openM.pop(i)
                open.pop(i)   
            open.append(newscore)
            openM.append(poss)
