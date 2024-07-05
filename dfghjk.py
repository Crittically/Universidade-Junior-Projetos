from random import randint
from time import time

inicio = time()
corretos = 0
for i in range(10):
    oper_list = ["+", "-", "*", "//"]
    num1 = randint(0, 9)
    oper = randint(0, 3)
    if oper == 3:
        num2 = randint(1, 9)
    else:
        num2 = randint(0, 9)

    while True:
        try:
            ans = int(input("%d %s %d = " % (num1, oper_list[oper], num2)))
        except ValueError:
            print("Escreve um numero")
        else:
            break

    if ans == eval("%d %s %d" % (num1, oper_list[oper], num2)):
        print("Certo!")
        corretos += 1
    else:
        print("Errado")
fim = time()
print("\nAcabou! Acertaste %d/10 perguntas em %ss" % (corretos, round(fim-inicio, 1)))
