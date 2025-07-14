import time
import datetime
import os


def criarArquivo():
    if os.path.exists(r"C:\Users\Carlos\Desktop\baterponto\baterponto\server\funcionarios.txt"):
        print("Arquivo já existe")
        pass
    else:
        arquivo = open(r"C:\Users\Carlos\Desktop\baterponto\baterponto\server\funcionarios.txt", "x")
        arquivo.close()
        print("Arquivo criado com sucesso")

def registrarFuncionario():
        os.system('cls')
        hora_atual = datetime.datetime.today()
        hora_formatada = hora_atual.strftime("%d/%m/%Y %H:%M")


        fName = input("Digite o primeiro nome do funcionario: ")
        lName = input("Digite o sobrenome do funcionario: ")

        funcionario = fName + lName +" "+ str(hora_formatada) 
        
        arquivo = open(r"C:\Users\Carlos\Desktop\baterponto\baterponto\server\funcionarios.txt", "a")
        arquivo.write(funcionario + " " + "\n")
        print(f"Funcionario: {fName} {lName} - Horario registrado com sucesso!")

def registrarSaida():
    os.system('cls')
    hora_atual = datetime.datetime.today()
    hora_formatada = hora_atual.strftime("%d/%m/%Y %H:%M")

    fName = input("Digite o primeiro nome do funcionario: ")
    lName = input("Digite o ultimo nome funcionario: ")

    funcionario = fName + lName +" "+ str(hora_formatada) 
    
    arquivo = open(r"C:\Users\Carlos\Desktop\baterponto\baterponto\server\funcionarios.txt", "a")
    arquivo.write(funcionario + " " + "\n")
    print(f"Funcionario: {fName}  {lName} - Horario de saida registrado com sucesso!")


def exibirFuncionarios():
      os.system('cls')
      with open(r"C:\Users\Carlos\Desktop\baterponto\baterponto\server\funcionarios.txt", ) as arquivo:
            print("Lista de Funcionários:")
            for nomes in arquivo:
                print(nomes.strip())



def sairPrograma():
    print("Saindo do programa...")
    time.sleep(2)
    exit()




def menu():
    global escolha
    escolha = input('''
    Bem vindo ao Menu Principal!
    1. Registrar Horario
    2. Registrar Saida
    3. Exibir lista de funcionários
    4. Sair
    5. Criar arquivo (admin)
''')


    match escolha:
        case '1':
                print("Registrar Entrada")
                registrarFuncionario()
        case '2':
                print("Registrar Saida")
                registrarSaida()
        case '3':
                print("Exibindo lista de funcionários...")
                exibirFuncionarios()
        case '4':
                print("Saindo do programa...")
                sairPrograma()
        case '5':
                print("criar arquivo (admin)")
                criarArquivo()
                menu()




menu()