a = int(input("numero: "))
for i in range(1, a+1):
    texto = ""
    if i%3==0:
        texto += "Fizz"
    if i%5==0:
        texto += "Buzz"
    if texto == "":
        print(i)
    else:
        print(texto)