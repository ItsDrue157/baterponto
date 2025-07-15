import datetime
import sqlite3
from pathlib import Path

class FuncionarioDB:
    def __init__(self, caminho_db):
        base_dir = Path(__file__).resolve().parent  # diretório do arquivo atual
        if caminho_db is None:
            caminho_db = base_dir / "server" / "funcionarios.db"
        self.conn = sqlite3.connect(caminho_db)
        self.criar_tabela()

    def criar_tabela(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    horario_entrada TEXT,
                    horario_saida TEXT
                )
            ''')

    def cadastrar_funcionario(self, nome):
        with self.conn:
            self.conn.execute('INSERT INTO funcionarios (nome) VALUES (?)', (nome,))
        print(f"Funcionário '{nome}' cadastrado com sucesso!")

    def listar_funcionarios(self):
        cursor = self.conn.execute('SELECT id, nome FROM funcionarios')
        funcionarios = cursor.fetchall()
        if funcionarios:
            print("\nLista de Funcionários:")
            for id_, nome in funcionarios:
                print(f"{id_} - {nome}")
        else:
            print("Nenhum funcionário cadastrado.")
    
    def fazerLogin(self):
        id_funcionario = input("Digite o ID do funcionário: ")
        nome = input("Digite o nome do funcionário: ")
        cursor = self.conn.execute(
            'SELECT id, nome FROM funcionarios WHERE id = ? AND nome = ?', 
            (id_funcionario, nome)
        )
        resultado = cursor.fetchone()
        if resultado:
            print(f"Login realizado com sucesso para {nome} (ID: {id_funcionario})!")
        else:
            print("Funcionário não encontrado ou dados incorretos.")

    def __del__(self):
        self.conn.close()

    def entradaDeHoras(self, id_funcionario):
        hora_entrada = datetime.datetime.now().strftime("%H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE funcionarios SET horario_entrada = ? WHERE id = ?', 
            (hora_entrada, id_funcionario)
        )
        self.conn.commit()
        print(f"Horário de entrada registrado para o ID {id_funcionario}: {hora_entrada}")
        return hora_entrada
    
    def saidaDeHoras(self, id_funcionario):
        hora_saida = datetime.datetime.now().strftime("%H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE funcionarios SET horario_saida = ? WHERE id = ?', 
            (hora_saida, id_funcionario)
        )
        self.conn.commit()
        print(f"Horário de saída registrado para o ID {id_funcionario}: {hora_saida}")
        return hora_saida


    def cadastrarHoras(self):
        escolha = input('''Escolha uma opção:
        1. Registrar Horário de Entrada
        2. Registrar Horário de Saída
        3. Voltar ao Menu Principal
        ''')
        match escolha:
            case '1':
                id_funcionario = input("Digite o ID do funcionario para registrar o horário de entrada: ")
                self.entradaDeHoras(id_funcionario)
                print("Horário de entrada registrado com sucesso!")
            case '2':
                id_funcionario = input("Digite o ID do funcionario para registrar o horário de saída: ")
                self.saidaDeHoras(id_funcionario)
                print("Horário de saída registrado com sucesso!")
            case '3':
                print("Voltando ao menu principal...")


def menu():
    db = FuncionarioDB(r"C:\Users\Carlos\Desktop\baterponto\baterponto\server\funcionarios.db")
    while True:
        escolha = input('''
        Bem vindo ao Menu Principal!
        1. Cadastrar Funcionário
        2. Listar Funcionários
        3. Sair
        4. Fazer Login
                        
        Escolha uma opção: ''')
        match escolha:
            case '1':
                nome = input("Digite o nome do funcionario: ")
                db.cadastrar_funcionario(nome)
            case '2':
                db.listar_funcionarios()
            case '3':
                print("Saindo do programa...")
                break
            case '4':
                db.fazerLogin()
                db.cadastrarHoras()

            

















if __name__ == "__main__":
    menu()