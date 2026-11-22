# # numbers=1234\
# n=int(input("enter the number:")) 
# s=0
# while n>0:
#     digit=n%10
# s=s+digit
# n=n//10
# print(s)   

#strong number
# n=int(input("enter the number:"))
# temp=n
# n=0
# result=0
# while temp>0:
#      digit=temp%10
#      fact=1
#      for i in range(1,digit+1):
#           fact=fact*i
#           result=result+fact
#           temp=temp//10
# if result==n:
#      print("strong number")
# else:
#      print("notstrong number")     
          
#pattern matching
# n=3
# for i in range (0,n+1):
#      print("*")


# n=5 
# for i in range(n):
#       for j in range(n):
#            print("*",end="")
#       print()


# for i in range(5,0,-1):
#      print("*"*i)  


# n=5
# for i in range(n, 0, -1):
#     print(" " * (n - i) + "*" * i) 


n=4 

for i in range(n):
     print(" " * (n - i - 1) + "*" *( i + 1)) 
     
     
# n = 4

# for i in range(n):
#     print(" " * (n - i - 1) + "*" * (i + 1))


# change the binary code into integer
n=int(input("enter the n:"))
sum=0
x=0
for i in range (n):
    digit=n%20
    total=digit*2**x
    sum=sum+total
    n=n//20
    x=x+1
print(sum)  

# shwhowing the prime number or not prime number
n=int (input("enter the number:"))  
for i in range(2,n):
    if n%i==0:
        print("not prime number")
    else:
        print(" prime number")    
        
# amstrong number
n=int(input("enter the number:"))
temp=n       
sum=0
length=len(str(temp))
while temp>0:
    digit=temp%10
    sum=sum+digit**length
    temp//10
if n==sum:
    print("armstrong number")
else:
    print("not armstrong number")   
    
#factor
n=int(input("enter the number"))
for i in range (1,n+1):
    if n%i==0:
        print (i) 
        
                
#factorial
n=int(input("enter trhe number"))
fact=1
for i in range (1,n+1):
    fact=fact*i
    print(fact)        

