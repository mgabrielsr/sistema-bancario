import json
import tkinter as tk
from tkinter import messagebox
import getpass

# Funções auxiliares para carregar e salvar dados
def carregar_usuarios():
    try:
        with open("usuarios.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def salvar_usuarios(usuarios):
    with open("usuarios.json", "w") as file:
        json.dump(usuarios, file)

def carregar_dados_conta(usuario):
    try:
        with open(f"{usuario}_conta.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"saldo": 0, "extrato": "", "numero_saques": 0}

def salvar_dados_conta(usuario, dados):
    with open(f"{usuario}_conta.json", "w") as file:
        json.dump(dados, file)

# Funções para criação de conta e login
def criar_conta():
    def criar_conta_callback():
        nome = entry_nome.get()
        senha = entry_senha.get()
        senha_repetida = entry_senha_repetida.get()

        if nome in usuarios:
            messagebox.showerror("Erro", "Usuário já existe.")
            return

        if senha != senha_repetida:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        usuarios[nome] = senha
        salvar_usuarios(usuarios)
        messagebox.showinfo("Sucesso", "Conta criada com sucesso.")
        top_criar_conta.destroy()

    top_criar_conta = tk.Toplevel()
    top_criar_conta.title("Criar Conta")
    top_criar_conta.configure(bg='#303030')

    label_nome = tk.Label(top_criar_conta, text="Nome de usuário:", bg='#303030', fg='white')
    label_nome.pack()
    entry_nome = tk.Entry(top_criar_conta)
    entry_nome.pack()

    label_senha = tk.Label(top_criar_conta, text="Senha:", bg='#303030', fg='white')
    label_senha.pack()
    entry_senha = tk.Entry(top_criar_conta, show="*")
    entry_senha.pack()

    label_senha_repetida = tk.Label(top_criar_conta, text="Repita a senha:", bg='#303030', fg='white')
    label_senha_repetida.pack()
    entry_senha_repetida = tk.Entry(top_criar_conta, show="*")
    entry_senha_repetida.pack()

    btn_criar_conta = tk.Button(top_criar_conta, text="Criar Conta", command=criar_conta_callback, bg='blue', fg='white')
    btn_criar_conta.pack()

def login():
    def login_callback():
        nome = entry_nome.get()
        senha = entry_senha.get()

        if nome in usuarios and usuarios[nome] == senha:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso.")
            top_login.destroy()
            iniciar_sistema(nome)
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos.")

    top_login = tk.Toplevel()
    top_login.title("Login")
    top_login.configure(bg='#303030')

    label_nome = tk.Label(top_login, text="Nome de usuário:", bg='#303030', fg='white')
    label_nome.pack()
    entry_nome = tk.Entry(top_login)
    entry_nome.pack()

    label_senha = tk.Label(top_login, text="Senha:", bg='#303030', fg='white')
    label_senha.pack()
    entry_senha = tk.Entry(top_login, show="*")
    entry_senha.pack()

    btn_login = tk.Button(top_login, text="Login", command=login_callback, bg='blue', fg='white')
    btn_login.pack()

def iniciar_sistema(usuario):
    def depositar():
        valor = float(entry_valor_deposito.get())
        if valor > 0:
            dados["saldo"] += valor
            dados["extrato"] += f"Depósito: R$ {valor:.2f}\n"
            salvar_dados_conta(usuario, dados)
            messagebox.showinfo("Sucesso", "Depósito realizado com sucesso.")
            entry_valor_deposito.delete(0, tk.END)  # Limpa o campo após o depósito
        else:
            messagebox.showerror("Erro", "O valor informado é inválido.")

    def sacar():
        valor = float(entry_valor_saque.get())
        excedeu_saldo = valor > dados["saldo"]
        excedeu_limite = valor > LIMITE_SAQUE_VALOR
        excedeu_saques = dados["numero_saques"] >= LIMITE_SAQUES

        if excedeu_saldo:
            messagebox.showerror("Erro", "Você não tem saldo suficiente.")
        elif excedeu_limite:
            messagebox.showerror("Erro", "O valor do saque excede o limite.")
        elif excedeu_saques:
            messagebox.showerror("Erro", "Número máximo de saques excedido.")
        elif valor > 0:
            dados["saldo"] -= valor
            dados["extrato"] += f"Saque: R$ {valor:.2f}\n"
            dados["numero_saques"] += 1
            salvar_dados_conta(usuario, dados)
            messagebox.showinfo("Sucesso", "Saque realizado com sucesso.")
            entry_valor_saque.delete(0, tk.END)  # Limpa o campo após o saque
        else:
            messagebox.showerror("Erro", "O valor informado é inválido.")

    def extrato():
        top_extrato = tk.Toplevel()
        top_extrato.title("Extrato")
        top_extrato.configure(bg='#303030')

        label_extrato = tk.Label(top_extrato, text="Extrato Bancário", bg='#303030', fg='white')
        label_extrato.pack()

        text_extrato = tk.Text(top_extrato, bg='#303030', fg='white')
        text_extrato.insert(tk.END, dados["extrato"] if dados["extrato"] else "Não foram realizadas movimentações.")
        text_extrato.pack()

        label_saldo = tk.Label(top_extrato, text=f"Saldo: R$ {dados['saldo']:.2f}", bg='#303030', fg='white')
        label_saldo.pack()

    LIMITE_SAQUES = 3
    LIMITE_SAQUE_VALOR = 500

    dados = carregar_dados_conta(usuario)

    root = tk.Tk()
    root.title("Sistema Bancário")
    root.configure(bg='#303030')

    label_bem_vindo = tk.Label(root, text=f"Bem-vindo(a), {usuario}!", bg='#303030', fg='white')
    label_bem_vindo.pack()

    frame_opcoes = tk.Frame(root, bg='#303030')
    frame_opcoes.pack()

    label_valor_deposito = tk.Label(frame_opcoes, text="Valor do Depósito:", bg='#303030', fg='white')
    label_valor_deposito.grid(row=0, column=0)
    entry_valor_deposito = tk.Entry(frame_opcoes)
    entry_valor_deposito.grid(row=0, column=1)

    btn_depositar = tk.Button(frame_opcoes, text="Depositar", command=depositar, bg='blue', fg='white')
    btn_depositar.grid(row=0, column=2)

    label_valor_saque = tk.Label(frame_opcoes, text="Valor do Saque:", bg='#303030', fg='white')
    label_valor_saque.grid(row=1, column=0)
    entry_valor_saque = tk.Entry(frame_opcoes)
    entry_valor_saque.grid(row=1, column=1)

    btn_sacar = tk.Button(frame_opcoes, text="Sacar", command=sacar, bg='blue', fg='white')
    btn_sacar.grid(row=1, column=2)

    btn_extrato = tk.Button(frame_opcoes, text="Extrato", command=extrato, bg='blue', fg='white')
    btn_extrato.grid(row=2, column=1)

    btn_sair = tk.Button(root, text="Sair", command=root.destroy, bg='blue', fg='white')
    btn_sair.pack()

    root.mainloop()

# Início do programa
usuarios = carregar_usuarios()

root = tk.Tk()
root.title("Sistema Bancário")
root.configure(bg='#303030')

btn_login = tk.Button(root, text="Login", command=login, bg='blue', fg='white')
btn_login.pack()

btn_criar_conta = tk.Button(root, text="Criar Conta", command=criar_conta, bg='blue', fg='white')
btn_criar_conta.pack()

btn_sair = tk.Button(root, text="Sair", command=root.destroy, bg='blue', fg='white')
btn_sair.pack()

root.mainloop()
