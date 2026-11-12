current_users=int(input("enter number of current users:"))
new_users=50
minutes=2
total_users= current_users +(new_users*minutes)
if total_users>1000:
    print("launch new server instance")
else:
   print("server stable")    
    
    
uptime=97.5
bill=50000
if uptime >= 99.9:
    refund=0
elif uptime>=98:
        refund=bill*0.10
else:
        refund=bill*0.25
        print("refund amount:",refund)        
        
        
        

weight = float(input("Enter weight in kg: "))
height = float(input("Enter height in meters: "))

bmi = weight / (height ** 2)

if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal"
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

print("BMI:", round(bmi, 2))
print("Category:", category)

      