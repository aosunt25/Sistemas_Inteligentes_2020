#Alfredo Osuna Torres 
#A01339250

#Method to fin if a conflict exists in the current position of the queen
def conflict(mat, current):
    for i in range(current):
        #Checks if the position is not 'null' 
        if mat[current]!=-1:
            #Checks if the position is in the same row or in any diagonal that it should be
            #Returns True if this happens 
            if mat[current]==mat[i] or mat[current]==(mat[i]+current-i) or mat[current]==(mat[i]+i-current):
                return True   
    return False

#Recursive definition to find the solution 
def queenArr(mat, current, pos):
    #Changes de value of the current position on the array to 'pos'
    mat[current]=pos
    #Checks if a conflict exist in that position and if the value of pos is lower or equal to 7
    if conflict(mat,current) == True and pos<=7:
        pos+=1
        queenArr(mat,current,pos)
    #if the pos is bigger than 7 it means that no position was available 
    elif pos>7:
        current-=1
        pos=mat[current]+1
        #it goes back one position on the array 
        queenArr(mat,current,pos)

    else:
        if current<7:
            queenArr(mat,current+1,0)
        

def initState():
    mat = []
    mat.append(0)

    for i in range(7):
        mat.append(-1)
        
    queenArr(mat,0,0)


    print("Solution:")
    print(mat)
    print("")
   
       
def main(): 
    initState()

if __name__ == '__main__':
    main()