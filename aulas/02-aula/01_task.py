with open('arquivo.txt', 'w') as file:
    while True:
        try:
            line = input("Digite algo: ");
            print(line, file=file);
        except EOFError:
            break