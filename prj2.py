
def showM(M):
    print(M[0],M[1],M[2],sep="\n")

def find_zero(M):
    for i in range(3):
        for j in range(3):
            if M[i][j]==0:
                return (i,j)
            
#we know that the parity of EF is odd (7) so we need to know if M is odd or not
def is_soluble(M):
    l=0
    A= [x for row in M for x in row if x != 0]
    for i in range(7):
        for j in range(i+1,8):
            if A[i]>A[j]:
                l+=1
    if l%2==1:
        return True 
    return False

def h(M):
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
    i,j=find_zero(M)
    if direction=="up" and i>0:
        M[i][j],M[i-1][j]=M[i-1][j],M[i][j]
        return (i-1,j)
    elif direction=="down" and i<2:
        M[i][j],M[i+1][j]=M[i+1][j],M[i][j]
        return (i+1,j)
    elif direction=="left" and j>0:
        M[i][j],M[i][j-1]=M[i][j-1],M[i][j]
        return (i,j-1)
    elif direction=="right" and j<2:
        M[i][j],M[i][j+1]=M[i][j+1],M[i][j]
        return (i,j+1)
    else:
        print("Invalid move")
        return find_zero(M)

def is_solved(M):
    for i in range(3):
        for j in range(3):
            if M[i][j]!=EF[i][j]:
                return False
    return True
    
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
showM(M)
if not is_soluble(M):
    print("The puzzle is not soluble")
