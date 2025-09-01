from faker import Faker
import os

fake= Faker()

#ensure folder exists
os.makedirs("File",exist_ok=True) 
# generate fake data
name =fake.name()
email=fake.email()
address=fake.address()
phone=fake.phone_number()


# write fake data into file 
with open("File/data.txt","a") as file:
    file.write(f"name:{name},email :{email},address:{address}")

#read a file 
with open("File/data.txt","r") as file:
    content=file.read()
    print(content)