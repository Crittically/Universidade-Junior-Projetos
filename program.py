from random import randint
print("""Choose:
1) Rock
2) Paper
3) Scissors""")

pao = int(input())
queijo = randint(1,3)
print("O computador escolheu: "+str(queijo))

if queijo == pao:
    print("Empate")
elif queijo == 1 and pao == 2:
    print("Ganhaste")
elif queijo == 2 and pao == 3:
    print ("Ganhaste")
elif queijo == 3 and pao == 1:
    print ("Ganhaste")
elif queijo == 3 and pao == 2:
    print ("Perdeste")
elif queijo == 2 and pao == 1:
    print ("Perdeste")
else:
    print ("Perdeste")