import sqlite3

class ModeloCusto:
    def __init__(self, nome_db='custos.db'):
        self.nome_db = nome_db
        self.criar_tabela()

    def criar_conexao(self):
        """Cria uma conexão com o banco de dados SQLite."""
        return sqlite3.connect(self.nome_db)

    def criar_tabela(self):
        """Cria a tabela de custos fixos se não existir."""
        with self.criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS custos_fixos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT NOT NULL,
                    valor REAL NOT NULL
                )
            ''')
            conexao.commit()

    def inserir_custo(self, descricao, valor):
        """Insere um novo custo fixo no banco de dados."""
        with self.criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                INSERT INTO custos_fixos (descricao, valor)
                VALUES (?, ?)
            ''', (descricao, valor))
            conexao.commit()

    def atualizar_custo(self, id_custo, descricao, valor):
        """Atualiza um custo fixo existente no banco de dados."""
        with self.criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                UPDATE custos_fixos
                SET descricao = ?, valor = ?
                WHERE id = ?
            ''', (descricao, valor, id_custo))
            conexao.commit()

    def remover_custo(self, id_custo):
        """Remove um custo fixo do banco de dados."""
        with self.criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                DELETE FROM custos_fixos
                WHERE id = ?
            ''', (id_custo,))
            conexao.commit()

    def obter_todos_custos(self):
        """Recupera todos os custos fixos do banco de dados."""
        with self.criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                SELECT * FROM custos_fixos
            ''')
            return cursor.fetchall()

    def obter_custo_por_id(self, id_custo):
        """Recupera um custo fixo pelo seu ID."""
        with self.criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                SELECT * FROM custos_fixos
                WHERE id = ?
            ''', (id_custo,))
            return cursor.fetchone()
