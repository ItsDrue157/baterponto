import os 
import sqlite3
import datetime 

def criarBanco():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idFuncionario INTEGER,
            nome TEXT NOT NULL,
            trabalhouHoje TEXT DEFAULT 'N' 
        )
    ''')
    conn.commit()
    conn.close()
criarBanco()

def bancoDeHoras():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idFuncionario TEXT,
            nome TEXT,
            data TEXT,
            hora_entrada TEXT,
            hora_saida TEXT
        )
    ''')
    conn.commit()
    conn.close()
bancoDeHoras()







def cadastrarHorasEntrada(idFuncionario, nome):
    dataAtual = datetime.datetime.now().strftime("%Y-%m-%d")
    horarioEntrada = datetime.datetime.now().strftime("%H:%M:%S")
    with sqlite3.connect('banco.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO horas (idFuncionario, nome, data, hora_entrada) VALUES (?, ?, ?, ?)',
            (idFuncionario, nome, dataAtual, horarioEntrada)
        )
        print(f"Horário de ENTRADA registrado com sucesso para o funcionário {idFuncionario} ({nome}) às {horarioEntrada}")
        conn.commit()

def cadastrarHorasSaida(idFuncionario, nome):
    dataAtual = datetime.datetime.now().strftime("%Y-%m-%d")
    horarioSaida = datetime.datetime.now().strftime("%H:%M:%S")
    with sqlite3.connect('banco.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE horas SET hora_saida = ? 
               WHERE idFuncionario = ? AND data = ? AND hora_saida IS NULL''',
            (horarioSaida, idFuncionario, dataAtual)
        )
        if cursor.rowcount > 0:
            print(f"Horário de saida registrado com sucesso para o funcionário {idFuncionario} ({nome}) as {horarioSaida}")
        else:
            print("Nenhum registro de entrada encontrado para hoje.")
        conn.commit()
        


def menuLogin(idFuncionario, nome):
    while True:        
        escolhaMenu = input('''
        1. Registrar Horário de Entrada
        2. Registrar Horário de Saída
        3. Sair              
                            ''')
        match escolhaMenu:
            case '1':
                cadastrarHorasEntrada(idFuncionario, nome)
            case '2':
                cadastrarHorasSaida(idFuncionario, nome)
            case '3':
                print("Saindo do sistema...")
                break






def login():
    nome = input("Digite o nome do funcionário: ")
    idFuncionario = input("Digite o ID do funcionário: ")

    if nome and idFuncionario:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM funcionarios WHERE idFuncionario = ? AND nome = ?', (idFuncionario, nome))
        resultado = cursor.fetchone()

        if resultado:
            print(f"Login realizado com sucesso para {nome} (ID: {idFuncionario})!")
            menuLogin(idFuncionario, nome)
    else:
        print("Funcionário não encontrado ou dados incorretos.")
        pass
    

def listarHorasFucionario(ifuncionario):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM horas WHERE idFuncionario = ?', (ifuncionario,))
    horas = cursor.fetchall()
    conn.close()
    if horas:
        print(f"Listando horas do funcionário {ifuncionario}:")
        for hora in horas:
            print(f"Data: {hora[3]}, Entrada: {hora[4]}, Saída: {hora[5]}")








while True:
    escolhaMenu = input('''
    1. Cadastrar Funcionario
    2. Listar Funcionarios  
    3. Fazer Login
    4. Sair
    5. Listar horas de um Funcionario
                        
                        ''')

    match escolhaMenu:
        case '1':
            conn = sqlite3.connect('banco.db')
            idFuncionario = input("Digite o ID do funcionário: ")
            nomeFuncionario = input("Digite o nome do funcionário: ")
            
            cursor = conn.cursor()
            cursor.execute('INSERT INTO funcionarios (idFuncionario, nome) VALUES (?,?)', (idFuncionario, nomeFuncionario))
            conn.commit()
            conn.close()
           
            print(f"Funcionário '{nomeFuncionario}' cadastrado com sucesso com ID {idFuncionario}!")

        case '2':
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute('SELECT idFuncionario, nome FROM funcionarios')
            funcionarios = cursor.fetchall()
            
            conn.close()
            
            print("Listando Funcionários:")
            
            for idFuncionario, nome in funcionarios:
                 print(f"O Funcionário {nome} tem o id {idFuncionario}")
        
        case '3':
            login()
        case '4':
            print("Saindo do sistema...")
            break
        case '5':
            idFuncionario = input("Digite o ID do funcionário para listar as horas: ")
            listarHorasFucionario(idFuncionario)
