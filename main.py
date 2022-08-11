num = int(input("Enter your number: "))
result = bin(num)[2:]
hexnum = hex(num)[2:]
print("Your binary number: ", result)
print("Your Hexadecimal number: ", hexnum)

print("........................................")

intResult= int(result, 2)
hexResult= int(hexnum, 16)
print("Your integer number: ",intResult)
print("Your integer number: ",hexResult)
