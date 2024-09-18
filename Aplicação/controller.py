import sqlite3
from tkinter import messagebox
from view import VisaoAplicacao

class ControladorAplicacao:
    def __init__(self, view):
        self.view = view
        self.conn = sqlite3.connect('custos_fixos.db')
        self.criar_tabela()
        self.vincular_eventos()
        self.atualizar_tabela_custos()

    def criar_tabela(self):
        """ Cria a tabela de custos fixos se não existir """
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS custos_fixos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL
            )
            """)

    def vincular_eventos(self):
        """ Vincula eventos da view aos métodos do controller """
        self.view.botao_inserir_custo.config(command=self.inserir_custo)
        self.view.botao_alterar_custo.config(command=self.atualizar_custo)
        self.view.botao_remover_custo.config(command=self.remover_custo)
        self.view.botao_calcular.config(command=self.calcular_custos_moto)
        

    def inserir_custo(self):
        """ Adiciona um novo custo fixo ao banco de dados """
        descricao = self.view.descricao_custo.get().upper()
        try:
            valor = float(self.view.valor_custo.get())
        except ValueError:
            messagebox.showerror("Erro", "O valor do custo deve ser um número válido.")
            return

        if descricao and valor >= 0:
            with self.conn:
                self.conn.execute("INSERT INTO custos_fixos (descricao, valor) VALUES (?, ?)", (descricao, valor))
            self.atualizar_tabela_custos()
            self.view.descricao_custo.delete(0, 'end')
            self.view.valor_custo.delete(0, 'end')
        else:
            messagebox.showerror("Erro", "Descrição não pode ser vazia e valor deve ser positivo.")

    def atualizar_custo(self):
        """ Altera um custo fixo existente """
        item_selecionado = self.view.tabela_custo_fixo.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um custo fixo para alterar.")
            return
        
        item_id = self.view.tabela_custo_fixo.item(item_selecionado)['values'][0]
        descricao = self.view.descricao_custo.get()
        try:
            valor = float(self.view.valor_custo.get())
        except ValueError:
            messagebox.showerror("Erro", "O valor do custo deve ser um número válido.")
            return

        if descricao and valor >= 0:
            with self.conn:
                self.conn.execute("UPDATE custos_fixos SET descricao = ?, valor = ? WHERE id = ?", (descricao, valor, item_id))
            self.atualizar_tabela_custos()
            self.view.descricao_custo.delete(0, 'end')
            self.view.valor_custo.delete(0, 'end')
        else:
            messagebox.showerror("Erro", "Descrição não pode ser vazia e valor deve ser positivo.")

    def remover_custo(self):
        """ Remove um custo fixo do banco de dados """
        item_selecionado = self.view.tabela_custo_fixo.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um custo fixo para remover.")
            return
        
        item_id = self.view.tabela_custo_fixo.item(item_selecionado)['values'][0]
        with self.conn:
            self.conn.execute("DELETE FROM custos_fixos WHERE id = ?", (item_id,))
        self.atualizar_tabela_custos()

    def atualizar_tabela_custos(self):
        """ Atualiza a tabela de custos fixos com os dados do banco de dados """
        for item in self.view.tabela_custo_fixo.get_children():
            self.view.tabela_custo_fixo.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM custos_fixos")
        for row in cursor:
            self.view.tabela_custo_fixo.insert('', 'end', values=row)
    
    
    def calcular_custos_moto(self):
        """ Calcula os gastos da moto com base nas entradas """
        try:
            rendimento = float(self.view.rendimento.get())
            preco_combustivel = float(self.view.preco_combustivel.get())
            dias_operacao = int(self.view.dias_operacao.get())
            media_entregas_dia = float(self.view.media_entregas_dia.get())
        except ValueError:
            messagebox.showerror("Erro", "Os valores inseridos devem ser válidos.")
            return

        # Recupera a soma dos custos fixos do banco de dados
        custo_fixo_total = self.obter_custo_fixo_total()
        self.view.tabela_rf1.delete(*self.view.tabela_rf1.get_children())
        for i in range(1, 16):
            
            distancia = i 
            custo_combustivel = preco_combustivel / rendimento
            custo_combustivel_total = distancia * custo_combustivel
            custo_fixo = custo_fixo_total /dias_operacao/ media_entregas_dia
            custo_total = custo_combustivel_total + custo_fixo

            # Insere os valores formatados na tabela
            
            self.view.tabela_rf1.insert('', 'end', values=(
                f"{distancia:.2f}",
                f"{custo_combustivel:.2f}",
                f"{custo_combustivel_total:.2f}",
                f"{custo_fixo:.2f}",
                f"{custo_total:.2f}"
            ))

    def obter_custo_fixo_total(self):
        """ Obtém a soma total dos custos fixos do banco de dados """
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT SUM(valor) FROM custos_fixos")
            resultado = cursor.fetchone()
            return resultado[0] if resultado[0] is not None else 0

    def fechar(self):
        """ Fecha a conexão com o banco de dados """
        self.conn.close()
      


if __name__ == "__main__":
    view = VisaoAplicacao()
    controlador = ControladorAplicacao(view)
    view.iniciar()
    controlador.fechar()
