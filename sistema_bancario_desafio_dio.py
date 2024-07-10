import json
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

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

def carregar_contas():
    try:
        with open("contas.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def salvar_contas(contas):
    with open("contas.json", "w") as file:
        json.dump(contas, file)

# Funções para criação de conta e login
def criar_conta():
    def criar_conta_callback():
        nome = entry_nome.get()
        data_nascimento = entry_data_nascimento.get()
        cpf = entry_cpf.get()
        celular = entry_celular.get()
        email = entry_email.get()
        tipo_conta = tipo_conta_var.get()
        senha = entry_senha.get()
        senha_repetida = entry_senha_repetida.get()
        endereco = {
            "rua": entry_rua.get(),
            "numero": entry_numero.get(),
            "bairro": entry_bairro.get(),
            "cidade": entry_cidade.get(),
            "estado": entry_estado.get()
        }

        # Validações
        if cpf in contas:
            messagebox.showerror("Erro", "CPF já cadastrado.")
            return
        if senha != senha_repetida:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        if tipo_conta != "Corrente":
            messagebox.showerror("Erro", "Apenas contas do tipo Corrente são permitidas.")
            return
        try:
            data_nascimento_dt = datetime.strptime(data_nascimento, "%d/%m/%Y")
            idade = (datetime.now() - data_nascimento_dt).days // 365
            if idade < 18:
                messagebox.showerror("Erro", "Usuário deve ter pelo menos 18 anos.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Data de nascimento inválida.")
            return

        # Criação de conta
        usuarios[cpf] = senha
        numero_conta = len(contas) + 1
        contas[cpf] = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "celular": celular,
            "email": email,
            "endereco": endereco,
            "tipo_conta": tipo_conta,
            "numero_conta": numero_conta,
            "saldo": 0,
            "extrato": [],
            "numero_saques": 0
        }
        salvar_usuarios(usuarios)
        salvar_contas(contas)
        messagebox.showinfo("Sucesso", "Conta criada com sucesso.")
        top_criar_conta.destroy()

    top_criar_conta = tk.Toplevel()
    top_criar_conta.title("Criar Conta")
    top_criar_conta.configure(bg='#FFFFFF')

    label_nome = tk.Label(top_criar_conta, text="Nome completo:", bg='#FFFFFF', fg='#000080')
    label_nome.pack()
    entry_nome = tk.Entry(top_criar_conta)
    entry_nome.pack()

    label_data_nascimento = tk.Label(top_criar_conta, text="Data de nascimento (dd/mm/aaaa):", bg='#FFFFFF', fg='#000080')
    label_data_nascimento.pack()
    entry_data_nascimento = tk.Entry(top_criar_conta)
    entry_data_nascimento.pack()

    label_cpf = tk.Label(top_criar_conta, text="CPF:", bg='#FFFFFF', fg='#000080')
    label_cpf.pack()
    entry_cpf = tk.Entry(top_criar_conta)
    entry_cpf.pack()

    label_celular = tk.Label(top_criar_conta, text="Número de celular com DDD:", bg='#FFFFFF', fg='#000080')
    label_celular.pack()
    entry_celular = tk.Entry(top_criar_conta)
    entry_celular.pack()

    label_email = tk.Label(top_criar_conta, text="E-mail:", bg='#FFFFFF', fg='#000080')
    label_email.pack()
    entry_email = tk.Entry(top_criar_conta)
    entry_email.pack()

    label_endereco = tk.Label(top_criar_conta, text="Endereço:", bg='#FFFFFF', fg='#000080')
    label_endereco.pack()

    label_rua = tk.Label(top_criar_conta, text="Rua:", bg='#FFFFFF', fg='#000080')
    label_rua.pack()
    entry_rua = tk.Entry(top_criar_conta)
    entry_rua.pack()

    label_numero = tk.Label(top_criar_conta, text="Número:", bg='#FFFFFF', fg='#000080')
    label_numero.pack()
    entry_numero = tk.Entry(top_criar_conta)
    entry_numero.pack()

    label_bairro = tk.Label(top_criar_conta, text="Bairro:", bg='#FFFFFF', fg='#000080')
    label_bairro.pack()
    entry_bairro = tk.Entry(top_criar_conta)
    entry_bairro.pack()

    label_cidade = tk.Label(top_criar_conta, text="Cidade:", bg='#FFFFFF', fg='#000080')
    label_cidade.pack()
    entry_cidade = tk.Entry(top_criar_conta)
    entry_cidade.pack()

    label_estado = tk.Label(top_criar_conta, text="Estado:", bg='#FFFFFF', fg='#000080')
    label_estado.pack()
    entry_estado = tk.Entry(top_criar_conta)
    entry_estado.pack()

    label_tipo_conta = tk.Label(top_criar_conta, text="Tipo de conta:", bg='#FFFFFF', fg='#000080')
    label_tipo_conta.pack()
    tipo_conta_var = tk.StringVar(value="Corrente")  # Define o valor padrão como "Corrente"
    tipo_conta_options = ["Corrente", "Poupança", "Salário"]
    option_menu_tipo_conta = tk.OptionMenu(top_criar_conta, tipo_conta_var, *tipo_conta_options)
    option_menu_tipo_conta.pack()

    label_senha = tk.Label(top_criar_conta, text="Senha:", bg='#FFFFFF', fg='#000080')
    label_senha.pack()
    entry_senha = tk.Entry(top_criar_conta, show="*")
    entry_senha.pack()

    label_senha_repetida = tk.Label(top_criar_conta, text="Repita a senha:", bg='#FFFFFF', fg='#000080')
    label_senha_repetida.pack()
    entry_senha_repetida = tk.Entry(top_criar_conta, show="*")
    entry_senha_repetida.pack()

    btn_criar_conta = tk.Button(top_criar_conta, text="Criar Conta", command=criar_conta_callback, bg='#000080', fg='#FFFFFF')
    btn_criar_conta.pack()

def login():
    global cpf
    cpf = entry_cpf.get()
    senha = entry_senha.get()

    if cpf in usuarios and usuarios[cpf] == senha:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso.")
        root.destroy()
        iniciar_sistema()
    else:
        messagebox.showerror("Erro", "CPF ou senha incorretos.")

def extrato():
    top_extrato = tk.Toplevel()
    top_extrato.title("Extrato")
    top_extrato.configure(bg='#FFFFFF')

    label_extrato = tk.Label(top_extrato, text="Extrato da conta:", bg='#FFFFFF', fg='#000080')
    label_extrato.pack()

    txt_extrato = scrolledtext.ScrolledText(top_extrato, width=50, height=10, wrap=tk.WORD)
    txt_extrato.pack()

    txt_extrato.insert(tk.END, f"Nome: {contas[cpf]['nome']}\n")
    txt_extrato.insert(tk.END, f"CPF: {contas[cpf]['cpf']}\n")
    txt_extrato.insert(tk.END, f"Tipo de Conta: {contas[cpf]['tipo_conta']}\n")
    txt_extrato.insert(tk.END, f"Saldo atual: R$ {contas[cpf]['saldo']:.2f}\n")
    txt_extrato.insert(tk.END, "--------------------------------\n")
    txt_extrato.insert(tk.END, "Histórico de transações:\n")
    for transacao in contas[cpf]["extrato"]:
        txt_extrato.insert(tk.END, f"{transacao}\n")
    txt_extrato.configure(state=tk.DISABLED)

def iniciar_sistema():
    def depositar():
        def depositar_callback():
            valor = float(entry_valor_deposito.get())
            if valor > 0:
                contas[cpf]["saldo"] += valor
                contas[cpf]["extrato"].append(f"Depósito: R$ {valor:.2f}")
                salvar_contas(contas)
                messagebox.showinfo("Sucesso", "Depósito realizado com sucesso.")
                top_deposito.destroy()
                # entry_valor_deposito.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "O valor informado é inválido.")

        top_deposito = tk.Toplevel()
        top_deposito.title("Depósito")
        top_deposito.configure(bg='#FFFFFF')

        label_valor_deposito = tk.Label(top_deposito, text="Valor a depositar:", bg='#FFFFFF', fg='#000080')
        label_valor_deposito.pack()
        entry_valor_deposito = tk.Entry(top_deposito)
        entry_valor_deposito.pack()

        btn_depositar = tk.Button(top_deposito, text="Depositar", command=depositar_callback, bg='#000080', fg='#FFFFFF')
        btn_depositar.pack()

    def sacar():
        def sacar_callback():
            valor = float(entry_valor_saque.get())
            if valor > 0:
                if valor <= LIMITE_SAQUE_VALOR:
                    if contas[cpf]["numero_saques"] < LIMITE_SAQUES:
                        if contas[cpf]["saldo"] >= valor:
                            contas[cpf]["saldo"] -= valor
                            contas[cpf]["extrato"].append(f"Saque: R$ {valor:.2f}")
                            contas[cpf]["numero_saques"] += 1
                            salvar_contas(contas)
                            messagebox.showinfo("Sucesso", "Saque realizado com sucesso.")
                            entry_valor_saque.delete(0, tk.END)
                            top_sacar.destroy()
                        else:
                            messagebox.showerror("Erro", "Saldo insuficiente.")
                    else:
                        messagebox.showerror("Erro", f"Limite de saques diários ({LIMITE_SAQUES}) atingido.")
                else:
                    messagebox.showerror("Erro", f"Valor máximo de saque é de R$ {LIMITE_SAQUE_VALOR:.2f}.")
            else:
                messagebox.showerror("Erro", "O valor informado é inválido.")

        top_sacar = tk.Toplevel()
        top_sacar.title("Saque")
        top_sacar.configure(bg='#FFFFFF')

        label_valor_saque = tk.Label(top_sacar, text="Valor do saque:", bg='#FFFFFF', fg='#000080')
        label_valor_saque.pack()
        entry_valor_saque = tk.Entry(top_sacar)
        entry_valor_saque.pack()

        btn_sacar = tk.Button(top_sacar, text="Sacar", command=sacar_callback, bg='#000080', fg='#FFFFFF')
        btn_sacar.pack()

    root_sistema = tk.Tk()
    root_sistema.title("Sistema Bancário")
    root_sistema.configure(bg='#FFFFFF')

    label_bem_vindo = tk.Label(root_sistema, text=f"Bem-vindo, {contas[cpf]['nome']}!", bg='#FFFFFF', fg='#000080')
    label_bem_vindo.pack()

    label_tipo_conta = tk.Label(root_sistema, text=f"Tipo de Conta: Corrente", bg='#FFFFFF', fg='#000080')
    label_tipo_conta.pack()
    
    label_agencia = tk.Label(root_sistema, text=f"Agência: 0001", bg='#FFFFFF', fg='#000080')
    label_agencia.pack()

    label_numero_conta = tk.Label(root_sistema, text=f"Número da conta: {contas[cpf]['numero_conta']}", bg='#FFFFFF', fg='#000080')
    label_numero_conta.pack()

    label_cpf = tk.Label(root_sistema, text=f"CPF: {contas[cpf]['cpf']}", bg='#FFFFFF', fg='#000080')
    label_cpf.pack()

    label_saldo = tk.Label(root_sistema, text=f"Saldo atual: R$ {contas[cpf]['saldo']:.2f}", bg='#FFFFFF', fg='#000080')
    label_saldo.pack()

    btn_depositar = tk.Button(root_sistema, text="Depositar", command=depositar, bg='#000080', fg='#FFFFFF')
    btn_depositar.pack()

    btn_sacar = tk.Button(root_sistema, text="Sacar", command=sacar, bg='#000080', fg='#FFFFFF')
    btn_sacar.pack()

    btn_extrato = tk.Button(root_sistema, text="Extrato", command=extrato, bg='#000080', fg='#FFFFFF')
    btn_extrato.pack()

    btn_sair = tk.Button(root_sistema, text="Sair", command=root_sistema.destroy, bg='#FF0000', fg='#FFFFFF')
    btn_sair.pack()
    
    label_aviso = tk.Label(root_sistema, text=f"Saldo atualizado em 'Extrato' ou após sair e efetuar o login novamente", bg='#FFFFFF', fg='#000080')
    label_aviso.pack()

# Configurações gerais do sistema
LIMITE_SAQUE_VALOR = 500
LIMITE_SAQUES = 3

# Carregar dados iniciais
usuarios = carregar_usuarios()
contas = carregar_contas()

# Interface de login
root = tk.Tk()
root.title("Login")
root.configure(bg='#FFFFFF')

label_cpf = tk.Label(root, text="CPF:", bg='#FFFFFF', fg='#000080')
label_cpf.pack()
entry_cpf = tk.Entry(root)
entry_cpf.pack()

label_senha = tk.Label(root, text="Senha:", bg='#FFFFFF', fg='#000080')
label_senha.pack()
entry_senha = tk.Entry(root, show="*")
entry_senha.pack()

btn_login = tk.Button(root, text="Login", command=login, bg='#000080', fg='#FFFFFF')
btn_login.pack()

btn_criar_conta = tk.Button(root, text="Criar Conta", command=criar_conta, bg='#000080', fg='#FFFFFF')
btn_criar_conta.pack()

root.mainloop()