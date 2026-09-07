import sys

conversion = input("Convert C to F or F to C? ")

if conversion.lower() == "c":
    C = float(input("Enter temperature in Celsius: "))
    F = round((C * 9/5) + 32, 1)
elif conversion.lower() == "f":
    F = float(input("Enter temperature in Fahrenheit: "))
    C = round(((F - 32) * 5/9),1)
else:
    print("Input either C or F")
    sys.exit()

description = ""
if C > 35:
    description = "Very Hot"
elif C >= 26 and C <= 35:
    description = "Warm"
elif C >= 16 and C <= 25:
    description = "Mild"
elif C >= 6 and C <= 15:
    description = "Cold"
elif C <= 5:
    description = "Very Cold"

print(f"{C}°C = {F}°F \n{description}")