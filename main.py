from pathlib import Path
import sqlite3
import datetime 


db_path = Path(__file__).resolve().parent / "server" / "banco.db"
db_path.parent.mkdir(exist_ok=True)  

def criarBanco():
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO horas (idFuncionario, nome, data, hora_entrada) VALUES (?, ?, ?, ?)',
            (idFuncionario, nome, dataAtual, horarioEntrada)
        )
        print(f"Horário de ENTRADA registrado com sucesso para o funcionario {idFuncionario} ({nome}) às {horarioEntrada}")
        conn.commit()

def cadastrarHorasSaida(idFuncionario, nome):
    dataAtual = datetime.datetime.now().strftime("%Y-%m-%d")
    horarioSaida = datetime.datetime.now().strftime("%H:%M:%S")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE horas SET hora_saida = ? 
               WHERE idFuncionario = ? AND data = ? AND hora_saida IS NULL''',
            (horarioSaida, idFuncionario, dataAtual)
        )
        if cursor.rowcount > 0:
            print(f"Horário de saida registrado com sucesso para o funcionario {idFuncionario} ({nome}) as {horarioSaida}")
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
    nome = input("Digite o nome do funcionario: ")
    idFuncionario = input("Digite o ID do funcionario: ")

    if nome and idFuncionario:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM funcionarios WHERE idFuncionario = ? AND nome = ?', (idFuncionario, nome))
        resultado = cursor.fetchone()

        if resultado:
            print(f"Login realizado com sucesso para {nome} (ID: {idFuncionario})!")
            menuLogin(idFuncionario, nome)
    else:
        print("funcionario não encontrado ou dados incorretos.")
        pass
    

def listarHorasFucionario(idfuncionario):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM horas WHERE idFuncionario = ?', (idfuncionario,))
    horas = cursor.fetchall()
    conn.close()
    if horas:
        print(f"Listando horas do funcionario {idfuncionario}:")
        for hora in horas:
            print(f"Data: {hora[3]}, Entrada: {hora[4]}, Saída: {hora[5]}")
    else:
        print(f"Nenhum registro de horas encontrado para o funcionario {idfuncionario}.")


def calcularHorasTrabalhadas(idFuncionario):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT hora_entrada, hora_saida FROM horas where idFuncionario = ?', (idFuncionario,))
    registros = cursor.fetchall()
    conn.close()
    total_horas = datetime.timedelta()
    for entrada, saida in registros:
        if entrada and saida:
            entrada = datetime.datetime.strptime(entrada, "%H:%M:%S")
            saida = datetime.datetime.strptime(saida, "%H:%M:%S")
            total_horas += (saida - entrada)
        else: 
            print(f"Registro incompleto para o funcionario {idFuncionario}.")
            return
    print(f"Total de horas trabalhadas: {total_horas} para o funcionario {idFuncionario}")





while True:
    escolhaMenu = input('''
    1. Cadastrar Funcionario
    2. Listar Funcionarios  
    3. Fazer Login
    4. Sair
    5. Listar horas de um Funcionario
    6. Calcular horas trabalhadas
    ''')

    match escolhaMenu:
        case '1':
            conn = sqlite3.connect(db_path)
            idFuncionario = input("Digite o ID do funcionario: ")
            nomeFuncionario = input("Digite o nome do funcionario: ")
            
            cursor = conn.cursor()
            cursor.execute('INSERT INTO funcionarios (idFuncionario, nome) VALUES (?,?)', (idFuncionario, nomeFuncionario))
            conn.commit()
            conn.close()
           
            print(f"funcionario '{nomeFuncionario}' cadastrado com sucesso com ID {idFuncionario}!")

        case '2':
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT idFuncionario, nome FROM funcionarios')
            funcionarios = cursor.fetchall()
            
            conn.close()
            
            print("Listando funcionarios:")
            
            for idFuncionario, nome in funcionarios:
                 print(f"O funcionario {nome} tem o id {idFuncionario}")
        
        case '3':
            login()
        case '4':
            print("Saindo do sistema...")
            break
        case '5':
            idFuncionario = input("Digite o ID do funcionario para listar as horas: ")
            listarHorasFucionario(idFuncionario)
        case '6':
            idFuncionario = input("Digite o ID do funcionario para calcular as horas trabalhadas: ")
            calcularHorasTrabalhadas(idFuncionario)
