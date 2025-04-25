"""
Abigail Elena
April 24, conditional statement
"""
print("\n------ example 1 and 2: if statement ---------")
age = 20
agecode = 123

if age>= 21:
    print("You are an adult!")
    agecode = 200
else:
    print("You are under 21!")
    agecode = 100

print(f"After the 'if' statement, agecode = {agecode}")

print("\n------ example 3: multi statement --------------")
age = 50
if 0 <= age < 21:
    print("You are minor!")
elif 21<= age < 65:
     print("You are an adult!")
elif 65<= age <= 130:
    print("You are a senior citizen!")
else:
    print("unable to read age!")

print(f"\n------ example 4: and operator --------------")
temperature = 90
humidity = 60

if 70<= temperature <=90 and humidity <80:
    print("The weather is pleasant")
else:
    print("The weather is not ideal")

print("\n------ example 5: --------------")
day = "Sunday"
is_holiday = False

if day=="Saturday" or day=="Sunday" or is_holiday:
    print("You can relax today")
else:
    print("It is a workday")

print("\n------ example 6: nested conditional statement --------------")
number = int(input("Enter a number: "))
if (number>=0):
    if number==0:
        print("The number is zero")
    else:
        print(f"{number} is positive")
else:
    print(f"{number} is negative")

print("\n------ example 7: username validation--------------")
#username validation. username must have 3+ characters
username = input("Enter a username: ")
username = username.strip()
len_username = len(username)
if len_username>= 3:
    index_whitespace = username.find(" ")
    if index_whitespace == -1:
        print(f"{username} is valid")
    else:
        print(f"Username CANNOT have whitespace")
else:
    print(f"{username} is INVALID. Username must have 3+ character")

print("\n------ example 8: match-case statement--------------")
response_code = 404

match response_code:
    case 400:
        print(f"Code = {response_code}. Server CANNOT understand")
    case 401 | 403:
        print(f"Code = {response_code}. Server refused to send back")
    case 404:
         print(f"Code = {response_code}. Server can't find")
    case _:
        print("INVALID CODE")

print("\n------ LAB EXERCISE--------------")
# collect grades as integers 
grade1 = int(input("Enter first grade (0-100): "))
grade2 = int(input("Enter second grade (0-100): "))

# calculate average 
average = (grade1 + grade2) / 2
gpa = "UNDEFINED!"

if 90 <= average <= 100:
    gpa = "A"
elif 70 <= average < 90:
    gpa = "B"
elif 60 <= average < 70:
    gpa = "C"
elif 0 <= average < 60:
    gpa = "FAIL!"
else:
    gpa = "UNDEFINED!"

print(f"For the average of {average}, your GPA is {gpa}")

