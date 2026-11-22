#calculation of electercity bill
units=int(input("enter number of units:"))
if units<=100:
    bill=units*1
elif units<=200:
    bill=100*2+(units-100)*2
else:
    bill=100*1+100*2+(units-200)*5
    print("electercity bill:",bill)    
 
 
 # calculation of type of triangles   
a=int(input("enter first angle:"))    
b=int(input("enter second angle:"))    
c=int(input("enter third angle:"))    
if a==b and b==c and c==a:
    print("equilateral triangle")
elif a==b and b==c and a==c:
    print("isoseleus triangle") 
else:
    print("scalene triangle")     
    
    
    #gamers are allowed or not allowed programme
    age=20
    has_id=False
    if age>=18:
        if has_id:
            print("entry allowed")
        else:
            print("show your id card")
    else:
        print("too young for entry")
        
        
        #for x in "123456":
   # print(x)
    
    
#for x in range(5,0,-1):
 #     print(x)    

  
      
      
# ATM machine problem      
current_password = "admin123"

for attempt in range(1, 4):
    password = input("Enter your password: ")

    if password == current_password:
        print("Login successfully")
        break

    else:
        print("Wrong password!")

        if attempt == 3:
            print("Account locked")  
 
 
# for loop concept            
total=0
for n in range (1,6):
   total +=n
print("sum:",total)