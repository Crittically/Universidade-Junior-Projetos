from random import randint

frango = randint(1,100)
tentativas = 0
while True:
    tentativas += 1
    batata_frita = int(input())

    if frango == batata_frita:
        print("Acertaste")
        print("Tentativas:" + str(tentativas))
        break
    elif frango > batata_frita:
        print("A resposta certa é maior")
    elif frango < batata_frita:
        print("A resposta certa é menor")
