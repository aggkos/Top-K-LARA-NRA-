import sys
stats=[]
filenames = ["2017_TRB.csv","2017_AST.csv","2017_STL.csv","2017_BLK.csv","2017_PTS.csv"]
string=input("give stats 1-5 separated by comma ")
s=string.split(",")
for i in s:
    stats.append(int(i))
K=int(input("give K "))
print (stats)

if K<1 or K>595:
    print ("wrong input")
    sys.exit(0)
f = [None] * len(stats)
for i,j in enumerate(stats):
    f[i]=open(filenames[j-1],"r")
    
    
#GROWING phase (LARA)
import heapq
max_values=[]
current_max=[]
heap=[]
heapq.heapify(heap)
for i in f:
    v=int(i.readline().split(",")[1])
    max_values.append(v)
    current_max.append(v)
    i.seek(0)
candidates={}
count=0
while (1):
    T=0
    count+=1
    for i,j in enumerate(f):
        line=j.readline()
        value=int(line.split(",")[1])/max_values[i]
        id_=line.split(",")[0]
        current_max[i]=value
        #update candidates
        if (id_ in candidates):
            candidates[id_][0]+=value
            candidates[id_][1][i]=1
        else:
            seen=[0] * len(stats)
            seen[i]=1
            lb=value
            in_heap=0
            candidates[id_] = [lb,seen,in_heap]
        #update heap
        if len(heap)==K:
            if heap[0][0]<candidates[id_][0]:
                if candidates[id_][2]==0: 
                    ret=heapq.heappushpop(heap,(candidates[id_][0],[id_,candidates[id_]]))
                    candidates[id_][2]=1
                    candidates[ret[1][0]][2]=0
                else:#in heap
                    for i in heap:
                        if id_==i[1][0]:
                            heap.remove(i)
                            ret=heapq.heappush(heap,(candidates[id_][0],[id_,candidates[id_]]))
                            candidates[id_][2]=1
                            break
        else:
            if candidates[id_][2]==0:
                heapq.heappush(heap,(candidates[id_][0],[id_,candidates[id_]]))
                candidates[id_][2]=1
            else : #in heap
                for i in heap:
                    if id_==i[1][0]:
                        heap.remove(i)
                        heapq.heappush(heap,(candidates[id_][0],[id_,candidates[id_]]))
                        break
        T+=value
    t=heap[0][0]
    if(t>=T and len(heap)==K):
        break
print ("end of growing phase in ",count," lines")
print (len(candidates),"candidates") #candidates[id]=[lb,[seen],in_heap,ub]
#initialize ub for candidates
max_ub=0
for k,v in candidates.items():
    temp=0
    for i in range(len(v[1])):
        if v[1][i]==0:
            temp+=current_max[i]
    ub=v[0]+temp
    if v[2]==0:
        if ub>max_ub:
            max_ub=ub
    candidates[k].append(ub)
#SHRINKING phase (NRA)
while (heap[0][0]<max_ub):
    count+=1
    for i,j in enumerate(f):
        line=j.readline()
        value=int(line.split(",")[1])/max_values[i]
        id_=line.split(",")[0]
        current_max[i]=value
        if id_ in candidates:
            #update lb in candidates[id_]
            candidates[id_][0]+=value
            candidates[id_][1][i]=1
            #update heap
            if heap[0][0]<candidates[id_][0]:
                if candidates[id_][2]==0:
                    ret=heapq.heappushpop(heap,(candidates[id_][0],[id_,candidates[id_]]))
                    candidates[id_][2]=1
                    candidates[ret[1][0]][2]=0
                else:#in heap
                    for i in heap:
                        if id_==i[1][0]:
                            heap.remove(i)
                            ret=heapq.heappush(heap,(candidates[id_][0],[id_,candidates[id_]]))
                            candidates[id_][2]=1
                            break
        #update ub for all candidates and compute max_ub
        max_ub=0
        for k,v in candidates.items():
            temp=0
            for i in range(len(v[1])):
                if v[1][i]==0:
                    temp+=current_max[i]
            ub=v[0]+temp
            if v[2]==0:#compute max_ub of those who are not in heap
                if ub>max_ub:
                    max_ub=ub
            candidates[k][3]=ub
print ("end of shrinking and growing phase in",count,"lines in total")
#computing final scores 
final=[]
not_final={}
for i in heap:
    if i[1][1][1]==[1]*len(stats):
        final.append((i[0],i[1][0]))
    else :
        not_final[i[1][0]]=[i[0],i[1][1][1]]
print ("i have to compute final scores for", len(not_final),"players")
while(len(not_final)!=0):
    count+=1
    for i,j in enumerate(f):
        line=j.readline()
        value=int(line.split(",")[1])/max_values[i]
        id_=line.split(",")[0]
        if id_ in not_final:
            not_final[id_][0]+=value
            not_final[id_][1][i]=1
            if not_final[id_][1]==[1]*len(stats):
                final.append((not_final[id_][0],id_))
                not_final.pop(id_)
print ("end of shrinking phase , growing phase and computing final scores in",count,"lines")
final.sort(reverse=True)

#compute top K with naive approach and check the final results
for i in f:
    i.seek(0)
naive={}
s=0
while (1):
    for i,j in enumerate(f):
        try:
            line=j.readline()
        except:
            s=1
            break
        try:
            value=int(line.split(",")[1])/max_values[i]
        except:
            s=1
            break
        id_=line.split(",")[0]
        if id_ in naive:
            naive[id_]+=value
        else:
            naive[id_]=value
    if s==1:
        break
h=[]
heapq.heapify(h)
for k,v in naive.items():
        if len(h)==K:
            if h[0][0]<=v:
                heapq.heappushpop(h,(v,k))
        else:
            heapq.heappush(h,(v,k))
h.sort(reverse=True)
for i in range(K):
    print ("naive:",h[i],"LARA+NRA:",final[i])
ff=open("2017_ALL.csv","r")
for i in final:
    while(1):
        line=ff.readline()
        if i[1]==line.split(",")[0]:
            print (line.split(",")[1])
            ff.seek(0)
            break
ff.close()
for i,j in enumerate(f):
    f[i].close()
