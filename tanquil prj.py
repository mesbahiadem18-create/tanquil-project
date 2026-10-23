
def showM(M):
    print(M[0],M[1],M[2],sep="\n")

def find_zero(M):
    for i in range(3):
        for j in range(3):
            if M[i][j]==0:
                return (i,j)

def is_solved(M):
    for i in range(3):
        for j in range(3):
            if M[i][j]!=EF[i][j]:
                return False
    return True

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
