import numpy as np
from copy import deepcopy

f = open("DIMACS", "r")

literalNum=0
clauseNum=0
while True:
  s=f.readline()
  s=s.split()
  if s[0][0]=='c' :
    continue
  else:   
    literalNum=int(s[2])
    clauseNum=int(s[3])
    break
clauses = []
literalCount=np.zeros(literalNum)
literalSignCount=np.zeros(literalNum)
literalAssignment=np.full(literalNum, -1)
for i in range(clauseNum):
    s=f.readline()
    s=s.split()
    a=np.full(literalNum, -1)
    for j in range(len(s)-1):  
      b=int(s[j])
      if b>0:
       literalCount[abs(b)-1]=literalCount[abs(b)-1]+1
       literalSignCount[abs(b)-1]=literalSignCount[abs(b)-1]+1
       a[abs(b)-1]=1
      elif b<0 :
       literalCount[abs(b)-1]=literalCount[abs(b)-1]+1
       literalSignCount[abs(b)-1]=literalSignCount[abs(b)-1]-1
       a[abs(b)-1]=0
      else: 
       break 
    clauses.append(a)


clauseIndex = []
def clauseSize(c):
    counter=0
    clauseIndex.clear()
    for j in range(literalNum):
        if c[j]==1 or c[j]==0:
         counter=counter+1
         clauseIndex.append(j)
    return counter     


def clauseSizeMin(c):
   for i in range(len(c)):
     if clauseSize(c)==0:
        return 0
   return 1     


def unitResolution(c,literalAssignmentCopy,literalCountCopy):
    if len(c)==0:
      return 1

    i=0         
    while i<len(c):
          print(len(c))
          if clauseSize(c[i]) ==0:
              return 0
          if clauseSize(c[i]) == 1:
              y=int(literalCountCopy[clauseIndex[0]])
              z=clauseIndex[0]
              result=propagate(c,z,c[i][z]%2,literalAssignmentCopy,literalCountCopy)  
              if result==0 or result == 1:
                return result
              i=-1  
          i=i+1                      
    return 2

def propagate(c,literal,assignment,literalAssignmentCopy,literalCountCopy):
    literal=int(literal)
    literalAssignmentCopy[literal]=assignment
    literalCountCopy[literal]=-1      
    i=0
    while i<len(c):
      if c[i][literal] == assignment:
         del c[i]
         i=i-1   
         if len(c) ==0:
            return 1            
      elif (c[i][literal]==1 and assignment==0) or (c[i][literal]==0 and assignment==1):    
         c[i][literal]=-1
         if clauseSize(c[i]) ==0:
            return 0  
      
      i=i+1 
      
    return 2        

def DPLL_solve(c,literalAssignment,literalCount):
    ret=0
    clausesCopy=deepcopy(c)
    literalAssignmentCopy=deepcopy(literalAssignment)
    literalCountCopy=deepcopy(literalCount)
    p=unitResolution(clausesCopy,literalAssignmentCopy,literalCountCopy)
    if p ==0:
      return p
    clausesCopy2=deepcopy(clausesCopy)
    literalAssignment=deepcopy(literalAssignmentCopy)      
    if p==1:
      SATResult(literalAssignmentCopy)         
      return p
    y=np.max(literalCountCopy)
    x=int(np.argmax(literalCountCopy))
    if literalSignCount[x]>=0:    
      status= propagate(clausesCopy,x,1,literalAssignmentCopy,literalCountCopy)           
      if status==1:
         SATResult(literalAssignmentCopy)
         return 1
      if status==2:
          literalAssignment=deepcopy(literalAssignmentCopy)
          ret=DPLL_solve(clausesCopy,literalAssignmentCopy,literalCountCopy)
          if ret ==1:
           return ret 
      if status==0 or ret==0:
         clausesCopy=deepcopy(clausesCopy2)               
         status= propagate(clausesCopy,x,0,literalAssignmentCopy,literalCountCopy)
         if status==1:
            SATResult(literalAssignmentCopy)           
            return 1
         if status==2:
              literalAssignment=deepcopy(literalAssignmentCopy)                
              ret=DPLL_solve(clausesCopy,literalAssignmentCopy,literalCountCopy)
              if ret ==1:
                  return ret 
         if status==0 or ret==0:
            return 0   
    else:  
      status= propagate(clausesCopy,x,0,literalAssignmentCopy,literalCountCopy)
      if status==1:
         SATResult(literalAssignmentCopy)       
         return 1
      if status==2:     
         literalAssignment=deepcopy(literalAssignmentCopy)
         ret=DPLL_solve(clausesCopy,literalAssignmentCopy,literalCountCopy)
         if ret ==1:
           return ret   
      if status==0 or ret==0:
         clausesCopy=deepcopy(clausesCopy2) 
         status= propagate(clausesCopy,x,1,literalAssignmentCopy,literalCountCopy)
         if status==1:
            SATResult(literalAssignmentCopy)                      
            return 1
         if status==2:                      
           literalAssignment=deepcopy(literalAssignmentCopy)
           ret=DPLL_solve(clausesCopy,literalAssignmentCopy,literalCountCopy)
           if ret ==1:
             return ret            
         if status==0 or ret==0:
            return 0        


 
def SATResult(literalAssignment):
  print("SAT ")
  for i in range(len(literalAssignment)):
       if (literalAssignment[i]) ==-1 or (literalAssignment[i]) ==0:
          print(-1*(i+1),end=" ")
       else:
          print(i+1,end=" ")


if(DPLL_solve(clauses,literalAssignment,literalCount))==0:
  print("UNSAT")   
