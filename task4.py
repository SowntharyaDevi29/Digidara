def armstrong():
    n=str(int(input("Enter the number")))
    print(type(n))
    sum=0
    for i in n:
      sum=sum+int(i)**len(n)
    if int(n)==sum:
      print(n,"armstrong")  
    else:
      print(n,"not armstrong") 
armstrong()         














