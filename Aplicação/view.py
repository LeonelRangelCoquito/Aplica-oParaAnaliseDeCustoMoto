import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext



class VisaoAplicacao:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Aplicação de Análise de Ajuste de Valor Mínimo para Entregas")
        self.janela.geometry("1020x550")
        self.janela.resizable(False,False)

        # Definindo estilo
        self.estilo = ttk.Style()
        self.estilo.configure('Personalizado.TButton', font=('Helvetica', 10, 'bold'), padding=10)
        self.estilo.configure('Personalizado.TLabel', font=('Helvetica', 12))
        self.estilo.configure('Personalizado.TFrame', background='#f5f5f5')

        # Criando o menu lateral
        self.menu_lateral = tk.Frame(self.janela, width=200, bg='#dcdcdc')
        self.menu_lateral.grid(row=0, column=0, sticky='ns')
        
        # Botões do menu lateral
        ttk.Button(self.menu_lateral, text="Custos Fixos", command=self.mostrar_frame_custos, style='Personalizado.TButton').pack(fill='x', padx=5, pady=5)
        ttk.Button(self.menu_lateral, text="Cálculo de Gastos da Moto", command=self.mostrar_frame_custos_moto, style='Personalizado.TButton').pack(fill='x', padx=5, pady=5)
        ttk.Button(self.menu_lateral, text="Ajuda", command=self.mostrar_ajuda, style='Personalizado.TButton').pack(fill='x', padx=5, pady=5)

        # Frame principal de conteúdo
        self.frame_conteudo = tk.Frame(self.janela, bg='#f5f5f5')
        self.frame_conteudo.grid(row=0, column=1, sticky='nsew')
        
        # Atualiza as proporções das colunas
        self.janela.grid_columnconfigure(1, weight=1)
        
        # Criando os frames
        self.criar_frames()
        self.mostrar_frame_custos()

    def criar_frames(self):
        # FRAME DE CUSTOS FIXOS
        self.frame_custos = ttk.Frame(self.frame_conteudo, padding=20, style='Personalizado.TFrame')
        self.frame_custos.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.frame_custos.grid_forget() 

        # Título
        ttk.Label(self.frame_custos, text="Gerenciar Custos Fixos", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)

        # Descrição/Nome do Custo
        ttk.Label(self.frame_custos, text='Descrição/Nome do Custo').grid(row=1, column=0, padx=5, pady=10, sticky='w')
        self.descricao_custo = ttk.Entry(self.frame_custos)
        self.descricao_custo.grid(row=1, column=1, padx=5, pady=10, sticky='ew')

        # Valor do Custo
        ttk.Label(self.frame_custos, text='Valor do Custo').grid(row=2, column=0, padx=5, pady=10, sticky='w')
        self.valor_custo = ttk.Entry(self.frame_custos)
        self.valor_custo.grid(row=2, column=1, padx=5, pady=10, sticky='ew')

        # Botões para manipulação dos custos fixos
        self.botao_inserir_custo = ttk.Button(self.frame_custos, text='Inserir Custo', style='Personalizado.TButton')
        self.botao_inserir_custo.grid(row=3, column=0, padx=5, pady=5, sticky='e')

        self.botao_alterar_custo = ttk.Button(self.frame_custos, text='Alterar Custo Fixo', style='Personalizado.TButton')
        self.botao_alterar_custo.grid(row=3, column=1, padx=5, pady=5, sticky='e')

        self.botao_remover_custo = ttk.Button(self.frame_custos, text='Remover Custo', style='Personalizado.TButton')
        self.botao_remover_custo.grid(row=3, column=2, padx=5, pady=5, sticky='e')

        # Tabela de Custos Fixos
        self.colunas_tabela_custo_fixo = {
            'id': 'ID',
            'descricao': 'Descrição',
            'valor': 'Valor'
        }

        self.tabela_custo_fixo = ttk.Treeview(self.frame_custos, columns=list(self.colunas_tabela_custo_fixo.keys()), show='headings')
        self.tabela_custo_fixo.grid(row=4, column=0, columnspan=3, pady=10, sticky='nsew')

        for col, texto in self.colunas_tabela_custo_fixo.items():
            self.tabela_custo_fixo.heading(col, text=texto)
            self.tabela_custo_fixo.column(col, width=100)

        barra_rolete = ttk.Scrollbar(self.frame_custos, orient='vertical', command=self.tabela_custo_fixo.yview)
        barra_rolete.grid(row=4, column=3, sticky='ns')
        self.tabela_custo_fixo.configure(yscrollcommand=barra_rolete.set)

        # Atualiza o layout
        self.frame_custos.update_idletasks()
        self.tabela_custo_fixo.bind("<<TreeviewSelect>>", 
                                self.apresentarRegistrosSelecionados)

        # FRAME DE CÁLCULO DE GASTOS DA MOTO
        self.frame_custos_moto = ttk.Frame(self.frame_conteudo, padding=20, style='Personalizado.TFrame')
        self.frame_custos_moto.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.frame_custos_moto.grid_forget() 

        # Configuração de colunas e linhas para ajuste dinâmico
        self.frame_custos_moto.grid_columnconfigure(0, weight=1, minsize=150)
        self.frame_custos_moto.grid_columnconfigure(1, weight=2, minsize=200)
        self.frame_custos_moto.grid_columnconfigure(2, weight=0)  # Coluna da scrollbar
        self.frame_custos_moto.grid_rowconfigure(5, weight=0)
        self.frame_custos_moto.grid_rowconfigure(6, weight=1)  # Linha da tabela

        # Rendimento (km/l)
        ttk.Label(self.frame_custos_moto, text='Insira o rendimento (km/l)').grid(row=1, column=0, padx=5, pady=10, sticky='w')
        self.rendimento = tk.Entry(self.frame_custos_moto)
        self.rendimento.grid(row=1, column=1, padx=5, pady=10, sticky='ew')

        # Preço do combustível
        ttk.Label(self.frame_custos_moto, text='Insira o preço do combustível').grid(row=2, column=0, padx=5, pady=10, sticky='w')
        self.preco_combustivel = tk.Entry(self.frame_custos_moto)
        self.preco_combustivel.grid(row=2, column=1, padx=5, pady=10, sticky='ew')

        # Quantidade de dias de operação
        ttk.Label(self.frame_custos_moto, text='Insira a quantidade de dias de operação').grid(row=3, column=0, padx=5, pady=10, sticky='w')
        self.dias_operacao = tk.Entry(self.frame_custos_moto)
        self.dias_operacao.grid(row=3, column=1, padx=5, pady=10, sticky='ew')

        # Média de entregas por dia
        ttk.Label(self.frame_custos_moto, text='Digite a média de entregas por dia.').grid(row=4, column=0, padx=5, pady=10, sticky='w')
        self.media_entregas_dia = tk.Entry(self.frame_custos_moto)
        self.media_entregas_dia.grid(row=4, column=1, padx=5, pady=10, sticky='ew')

        # Botão de calcular
        self.botao_calcular = ttk.Button(self.frame_custos_moto, text='          Calcular', width=20, style='Personalizado.TButton')
        self.botao_calcular.grid(row=5, column=0, columnspan=2, pady=20, sticky='ew')

        # Tabela de Resultados
        self.colunas_tabela_rf1 = {
            'distancia': 'Distância percorrida (KM)',
            'custo_combustivel': 'Custo Combustível por KM',
            'custo_combustivel_atual': 'Custo Combustível Distância Atual (KM)',
            'custo_fixo': 'Custo Fixo ($)',
            'total_custo': 'Custo Total ($)'
        }
        self.tabela_rf1 = ttk.Treeview(self.frame_custos_moto, columns=list(self.colunas_tabela_rf1.keys()), show='headings')
        self.tabela_rf1.grid(row=6, column=0, columnspan=2, pady=10, sticky='nsew')

        for col, texto in self.colunas_tabela_rf1.items():
            self.tabela_rf1.heading(col, text=texto)
            self.tabela_rf1.column(col, width=150)

        barra_rolete_tabela_rf1 = ttk.Scrollbar(self.frame_custos_moto, orient='vertical', command=self.tabela_rf1.yview)
        barra_rolete_tabela_rf1.grid(row=6, column=2, sticky='ns')
        self.tabela_rf1.configure(yscrollcommand=barra_rolete_tabela_rf1.set)

       

    def mostrar_frame_custos(self):
        self.frame_custos.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.frame_custos_moto.grid_forget()
        

    def mostrar_frame_custos_moto(self):
        self.frame_custos.grid_forget()
        self.frame_custos_moto.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
    def mostrar_ajuda(self):
        # Cria a janela de ajuda
        janela_ajuda = tk.Toplevel()
        janela_ajuda.title("Ajuda - Como Utilizar")
        janela_ajuda.geometry("500x400")  # Define o tamanho da janela

        # Cria uma barra de rolagem para o texto de ajuda
        texto_ajuda = scrolledtext.ScrolledText(janela_ajuda, wrap=tk.WORD, width=60, height=20)
        texto_ajuda.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Insere o texto da ajuda
        texto = """
        Bem-vindo à Aplicação de Análise da Viabilidade de Diminuição de Valor Mínimo para Entregas!

        **1. Gerenciamento de Gastos Fixos**:

        Os gastos fixos são todos os custos recorrentes com a moto, exceto o combustível. 
        Estes custos incluem, por exemplo:
        - IPVA
        - Licenciamento
        - Manutenção
        - Troca de óleo
        - Pneus

        **Como Gerenciar os Gastos Fixos**:
        
        - **Inserir um Gasto Fixo**:
            1. Vá para a aba "Gastos Fixos".
            2. Clique no botão "Adicionar Gasto Fixo".
            3. Preencha as informações solicitadas, como o nome do gasto (ex.: Manutenção), o valor e a frequência (mensal ou anual).
            4. Clique em "Salvar" para adicionar o gasto fixo à lista.

        - **Editar um Gasto Fixo**:
            1. Na aba "Gastos Fixos", selecione o gasto que deseja editar.
            2. Clique no botão "Editar".
            3. Atualize as informações conforme necessário e clique em "Salvar".

        - **Visualizar Gastos Fixos**:
            1. Todos os gastos fixos cadastrados serão exibidos em uma lista na aba "Gastos Fixos".
            2. A lista inclui o nome do gasto, o valor e a frequência (mensal ou anual).

        - **Excluir um Gasto Fixo**:
            1. Selecione o gasto fixo que deseja remover.
            2. Clique no botão "Excluir" para removê-lo da lista.

        **2. Inserir Dados da Moto e do Combustível**:
            - Informe o rendimento da moto em km por litro de combustível (valor padrão: 28,71 km/l).
            - Insira o preço do combustível por litro.
            - Defina a quantidade de dias de operação da moto por mês e a quantidade média de entregas por dia.

        **3. Cálculo de Gastos por Distância**:
            - Após inserir os dados iniciais, clique no botão "Calcular Gastos".
            - O sistema irá gerar uma tabela que mostra os custos de combustível e custos fixos para distâncias entre 1 km e 15 km.
            - A tabela exibirá:
                - Km percorridos.
                - Custo de combustível por km.
                - Custo total do combustível para a distância.
                - Custos fixos por entrega (excluindo o combustível).

        **4. Análise dos Resultados**:
            - Após gerar a tabela de custos, analise se é viável diminuir o valor mínimo de entrega sem comprometer suas margens de lucro.
            - Compare os custos para cada distância com o valor atual cobrado pela entrega e veja se é possível ajustar o valor mínimo para ser mais competitivo no mercado.

        **Dicas**:
        - Mantenha os gastos fixos sempre atualizados para obter cálculos precisos.
        - Utilize a função de gerenciamento de gastos fixos regularmente para revisar ou ajustar os custos recorrentes.
        - Verifique se todos os dados necessários estão preenchidos corretamente antes de realizar os cálculos.

        **Sobre o Sistema**:
        - Linguagem: Python
        - Interface: Tkinter
        - Banco de Dados: SQLite3
        - Arquitetura: MVC (Model-View-Controller)

        Em caso de dúvidas, entre em contato com o suporte técnico.
        """

       
        texto_ajuda.insert(tk.END, texto)
        texto_ajuda.config(state=tk.DISABLED) 
        
    def apresentarRegistrosSelecionados(self,event):
        print("Função apresentarRegistrosSelecionados foi chamada!") 
        self.descricao_custo.delete(0, tk.END)
        self.valor_custo.delete(0, tk.END) 
        for selection in self.tabela_custo_fixo.selection():  
            item = self.tabela_custo_fixo.item(selection)
            print(selection) 
            descricao,valor = item["values"][1:3]
            print(descricao,' ',valor)
            self.descricao_custo.insert(0, descricao)  
            self.valor_custo.insert(0, valor)

    def iniciar(self):
        self.janela.mainloop()

