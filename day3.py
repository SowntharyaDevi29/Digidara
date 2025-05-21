a=int(input("enter a number"))
b=int(input("enter a number"))
s=input("enter the operator")
if s=="+":
    print(a+b)
elif s=="-":
    print(a-b)
elif s=="*":
    print(a*b)
elif s=="/":
    print(a/b)
elif s=="%":
    print(a%b)
else:
    print("Invalid operator")
