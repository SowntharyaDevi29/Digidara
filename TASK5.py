list=[9,2,4,1,8,6,7,9]
n=len(list)
for i in range(n):#0,1,2,3,4,5,6,7
    for j in range(0,n-i-1):#0,8-9-1 0,
        if list[j]>list[j+1]:
            list[j],list[j+1]=list[j+1],list[j]
print("ascending order",list)