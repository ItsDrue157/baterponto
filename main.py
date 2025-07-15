import time
import datetime
import os
import sqlite3

def conectarBancoDeDados():
    global conexao, cursor
    conexao = sqlite3.connect(r'C:\Users\Carlos\Desktop\baterponto\baterponto\server\ponto.db')
    cursor = conexao.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        hora INTEGER
    )
    ''')



def registrarFuncionario():
        os.system('cls')
        hora_atual = datetime.datetime.today()
        hora_formatada = hora_atual.strftime("%d/%m/%Y %H:%M")


        fName = input("Digite o primeiro nome do funcionario: ")
        lName = input("Digite o sobrenome do funcionario: ")

        
        conectarBancoDeDados()
        cursor.execute("INSERT INTO usuarios (nome, hora) VALUES (?, ?)", (fName + lName, hora_formatada))
        conexao.commit()

def registrarSaida():
    os.system('cls')
    hora_atual = datetime.datetime.today()
    hora_formatada = hora_atual.strftime("%d/%m/%Y %H:%M")

    fName = input("Digite o primeiro nome do funcionario: ")
    lName = input("Digite o ultimo nome funcionario: ")
    
    conectarBancoDeDados()
    cursor.execute("INSERT INTO usuarios (nome, hora) VALUES (?, ?)", (fName + lName, hora_formatada))
    conexao.commit()
    print(f"Funcionario: {fName}  {lName} - Horario de saida registrado com sucesso!")

def exibirFuncionarios():
    os.system('cls')
    escolhaExibir = input('''
    Escolha uma opção:
    1. Exibir todos os funcionarios
    2. Escolher funcionario especifico
    3. Voltar ao menu principal
''')

    match escolhaExibir:
        case '1':  
            #mostrar todos os func 
            conectarBancoDeDados()
            cursor.execute("SELECT * FROM usuarios")
            resultados = cursor.fetchall()
            for linha in resultados:
                print(linha)
        
        
        case '2':
            conectarBancoDeDados()
            nome_funcionario = input("Digite o nome do funcionario que deseja pesquisar: ")
            cursor.execute("SELECT nome, hora FROM usuarios WHERE nome LIKE ?", ('%' + nome_funcionario + '%',))
            resultado = cursor.fetchall()
            if resultado:
                print(f"Horários registrados para '{nome_funcionario}':")
                for nome, hora in resultado:
                    print(f"Nome: {nome} | Horário: {hora}")
            else:
                print("Funcionário não encontrado.")
                
            


def sairPrograma():
    print("Saindo do programa...")
    time.sleep(2)
    exit()

def criarArquivo():
    if os.path.exists(r"C:\Users\Carlos\Desktop\baterponto\baterponto\server\funcionarios.txt"):
        print("Arquivo já existe")
        pass
    else:
        arquivo = open(r"C:\Users\Carlos\Desktop\baterponto\baterponto\server\funcionarios.txt", "x")
        arquivo.close()
        print("Arquivo criado com sucesso")








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