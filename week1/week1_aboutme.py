
# get information
name = input("What is your name? ")
age = input("How old are you? ")
origin = input("What country are you from? ")
future = input("What do you want to be when you grow up? ")

# both ways work
text = name + " is " + age + " years old.\n" + name + " is from " + origin + " and hopes to be a/an " + future + " in the future."
print(text)

text = f"{name} is {age} years old.\n{name} is from {origin} and hopes to be a/an {future} in the future."
print(text)