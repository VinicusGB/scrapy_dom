import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter.scrolledtext import ScrolledText
from datetime import date
import subprocess
import sys

from core.domsp.classe import DOMSP

#class StdoutRedirector:
#    def __init__(self, text_widget):
#        self.text_space = text_widget
#
#    def write(self, text):
#        self.text_space.insert(tk.END, text)
#        self.text_space.see(tk.END)
#
#    def flush(self):
#        pass

# Função para mostrar os campos selecionados e resultados em uma janela pop-up
def mostrar_dados_selecionados():
    dados_selecionados = []
    if opcao1_var.get():
        dados_selecionados.append("Extrair listagens")
    if opcao2_var.get():
        dados_selecionados.append("Baixar o diário")
    data_selecionada = data_var.get()
    #resultado_script = resultado_text.get(1.0, "end")

    janela_dados = tk.Toplevel()
    janela_dados.title("Dados Selecionados")

    ttk.Label(janela_dados, text="Campos Selecionados:").pack()
    ttk.Label(janela_dados, text=", ".join(dados_selecionados)).pack()
    ttk.Label(janela_dados, text="Data Selecionada:").pack()
    ttk.Label(janela_dados, text=data_selecionada).pack()
    ttk.Label(janela_dados, text="Resultado do Script:").pack()
    ScrolledText(janela_dados, wrap=tk.WORD, width=40, height=10).pack()
    ScrolledText(janela_dados, wrap=tk.WORD, width=40, height=10).insert(tk.END, resultado_script)

# Função para imprimir os dados
def imprimir_dados():
    dados = resultado_text.get(1.0, "end")
    print("Dados para impressão:")
    print(dados)
    # Você pode adicionar aqui a lógica para a impressão dos dados

# Função para executar a ação quando o botão "Executar" é pressionado
def executar_acao():
    data_selecionada = data_var.get().split('/')
    dia = data_selecionada[0]
    mes = data_selecionada[1]
    ano = data_selecionada[2]

    # Crie o widget de texto para a saída aqui
    output_text = ScrolledText(janela_principal, wrap=tk.WORD, width=40, height=10)
    output_text.grid(row=8, column=1, columnspan=2, padx=10, pady=10, sticky='w')
    
    # Redireciona a saída padrão (prints) para o widget output_text
#    sys.stdout = StdoutRedirector(output_text)
    DOMSP(published=date(int(ano), int(mes), int(dia)), varbaixar=opcao2_var.get(), vartratar=opcao1_var.get(), varacompanhar=opcao3_var.get())

# Criação da janela principal
janela_principal = tk.Tk()
janela_principal.title("Scrapy DOM-SP")

# Carregue a imagem (substitua 'imagem.png' pelo caminho da sua imagem)
imagem = Image.open("imagem.png")
imagem = imagem.resize((400, 400))
imagem = ImageTk.PhotoImage(imagem)

# Rótulo para a imagem
label_imagem = ttk.Label(janela_principal, image=imagem)
label_imagem.grid(row=0, column=0, rowspan=6, padx=10, pady=10, sticky='w')
label_imagem.image = imagem

# Criação de um frame para as opções com borda
frame_opcoes = ttk.Frame(janela_principal, borderwidth=2, relief="groove")
frame_opcoes.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='w')

# Rótulo para as opções
label_opcao = ttk.Label(frame_opcoes, text="Opções:")
label_opcao.grid(row=0, column=0, padx=10, pady=5, sticky='w')

# Variáveis para as opções (checkboxes)
opcao1_var = tk.BooleanVar(value=True)  # Defina como True para ativar por padrão
opcao2_var = tk.BooleanVar(value=True)
opcao3_var = tk.BooleanVar(value=False)

# Caixas de seleção (checkboxes) com as opções
opcao3 = ttk.Checkbutton(frame_opcoes, text="Acompanhar as etapas", variable=opcao3_var)
opcao2 = ttk.Checkbutton(frame_opcoes, text="Baixar o diário", variable=opcao2_var)
opcao1 = ttk.Checkbutton(frame_opcoes, text="Extrair listagens", variable=opcao1_var)

opcao3.grid(row=1, column=0, padx=10, pady=5, sticky='w')
opcao2.grid(row=2, column=0, padx=10, pady=5, sticky='w')
opcao1.grid(row=3, column=0, padx=10, pady=5, sticky='w')

# Rótulo para a data
label_data = ttk.Label(janela_principal, text="Data:")
label_data.grid(row=0, column=1, padx=10, pady=5, sticky='w')

# Campo de entrada para a data (usando tkcalendar)
data_var = tk.StringVar()
data_entry = DateEntry(janela_principal, textvariable=data_var, date_pattern="dd/mm/yyyy", background="darkblue", foreground="white")
data_entry.grid(row=0, column=2, padx=10, pady=5, sticky='w')

# Botão para executar a ação
botao_executar = ttk.Button(janela_principal, text="Executar", command=executar_acao)
botao_executar.grid(row=5, column=1, padx=10, pady=5, sticky='w')

# Botão para imprimir dados
#botao_imprimir = ttk.Button(janela_principal, text="Imprimir Dados", command=imprimir_dados)
#botao_imprimir.grid(row=6, column=1, padx=10, pady=5, sticky='w')

# Caixa de texto para o resultado do script
#resultado_text = ScrolledText(janela_principal, wrap=tk.WORD, width=40, height=10)
#resultado_text.grid(row=7, column=1, columnspan=2, padx=10, pady=10, sticky='w')

# Configuração da geometria para redimensionar corretamente
janela_principal.columnconfigure(1, weight=1)

# Iniciar a janela principal
janela_principal.mainloop()
