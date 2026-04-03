import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database as db
import file_utils as futils
import relatorio as rel

class AppAgendamento:
    def __init__(self, root):
        self.root = root
        self.root.title("📅 Sistema de Agendamento - RAD com Python")
        self.root.geometry("950x650")
        self.root.configure(bg='#f0f0f0')

        # Estilo personalizado
        self.configurar_estilos()

        # Criar banco e abas
        db.criar_tabelas()
        self.criar_widgets()

        # Carregar dados iniciais
        self.atualizar_lista_clientes()
        self.atualizar_lista_agendamentos()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')

        # Cores principais
        bg_color = "#f5f6fa"
        fg_color = "#2c3e50"
        accent = "#3498db"
        button_bg = "#ecf0f1"

        estilo.configure('TNotebook', background=bg_color, tabposition='nw')
        estilo.configure('TNotebook.Tab', background=button_bg, padding=[12, 4], font=('Segoe UI', 10, 'bold'))
        estilo.map('TNotebook.Tab', background=[('selected', accent), ('active', '#bdc3c7')])

        estilo.configure('TFrame', background=bg_color)
        estilo.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        estilo.configure('TButton', background=button_bg, foreground=fg_color, font=('Segoe UI', 9))
        estilo.map('TButton', background=[('active', '#d5dbdb')])

        estilo.configure('Treeview', background='white', foreground=fg_color, rowheight=25, fieldbackground='white', font=('Segoe UI', 9))
        estilo.map('Treeview', background=[('selected', accent)])

        # Estilo para Treeview com linhas alternadas (aplicaremos via tag no código)
        self.root.option_add('*TCombobox*Listbox.font', ('Segoe UI', 9))

    def criar_widgets(self):
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba Clientes
        self.frame_clientes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_clientes, text="👥 Clientes")
        self.criar_aba_clientes()

        # Aba Agendamentos
        self.frame_agendamentos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_agendamentos, text="📆 Agendamentos")
        self.criar_aba_agendamentos()

        # Menu
        self.criar_menu()

    def criar_aba_clientes(self):
        # Formulário
        frame_form = tk.Frame(self.frame_clientes, bg='#f5f6fa')
        frame_form.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(frame_form, text="Nome:", bg='#f5f6fa', font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30, font=('Segoe UI', 10))
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Telefone:", bg='#f5f6fa', font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_telefone = tk.Entry(frame_form, width=30, font=('Segoe UI', 10))
        self.entry_telefone.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Email:", bg='#f5f6fa', font=('Segoe UI', 10)).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_email = tk.Entry(frame_form, width=30, font=('Segoe UI', 10))
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(frame_form, bg='#f5f6fa')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="➕ Adicionar", command=self.adicionar_cliente, bg='#2ecc71', fg='white', font=('Segoe UI', 9, 'bold'), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Atualizar", command=self.atualizar_cliente, bg='#f39c12', fg='white', font=('Segoe UI', 9, 'bold'), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Excluir", command=self.excluir_cliente, bg='#e74c3c', fg='white', font=('Segoe UI', 9, 'bold'), padx=10).pack(side=tk.LEFT, padx=5)

        # Tabela
        frame_tabela = tk.Frame(self.frame_clientes, bg='#f5f6fa')
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_clientes = ttk.Treeview(frame_tabela, columns=("id", "nome", "telefone", "email"), show="headings", selectmode='browse')
        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("nome", text="Nome")
        self.tree_clientes.heading("telefone", text="Telefone")
        self.tree_clientes.heading("email", text="Email")
        self.tree_clientes.column("id", width=50, anchor='center')
        self.tree_clientes.column("nome", width=200)
        self.tree_clientes.column("telefone", width=120)
        self.tree_clientes.column("email", width=200)
        self.tree_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        self.tree_clientes.bind('<<TreeviewSelect>>', self.on_select_cliente)

        # Aplicar cores alternadas nas linhas (usando tag)
        self.tree_clientes.tag_configure('odd', background='#f9f9f9')
        self.tree_clientes.tag_configure('even', background='#ffffff')

    def criar_aba_agendamentos(self):
        # Seleção de cliente
        frame_cliente = tk.Frame(self.frame_agendamentos, bg='#f5f6fa')
        frame_cliente.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(frame_cliente, text="Cliente:", bg='#f5f6fa', font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.combo_clientes = ttk.Combobox(frame_cliente, width=40, font=('Segoe UI', 10))
        self.combo_clientes.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_cliente, text="🔍 Carregar agendamentos", command=self.carregar_agendamentos_por_cliente, bg='#3498db', fg='white', font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)

        # Formulário novo agendamento
        frame_form = tk.Frame(self.frame_agendamentos, bg='#f5f6fa')
        frame_form.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(frame_form, text="Data (AAAA-MM-DD):", bg='#f5f6fa', font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_data = tk.Entry(frame_form, width=15, font=('Segoe UI', 10))
        self.entry_data.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Hora (HH:MM):", bg='#f5f6fa', font=('Segoe UI', 10)).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_hora = tk.Entry(frame_form, width=10, font=('Segoe UI', 10))
        self.entry_hora.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Serviço:", bg='#f5f6fa', font=('Segoe UI', 10)).grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.entry_servico = tk.Entry(frame_form, width=20, font=('Segoe UI', 10))
        self.entry_servico.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(frame_form, text="➕ Adicionar Agendamento", command=self.adicionar_agendamento, bg='#2ecc71', fg='white', font=('Segoe UI', 9, 'bold')).grid(row=0, column=6, padx=10)

        # Tabela de agendamentos
        frame_tabela = tk.Frame(self.frame_agendamentos, bg='#f5f6fa')
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_agendamentos = ttk.Treeview(frame_tabela, columns=("id", "cliente", "data", "hora", "servico"), show="headings", selectmode='browse')
        self.tree_agendamentos.heading("id", text="ID")
        self.tree_agendamentos.heading("cliente", text="Cliente")
        self.tree_agendamentos.heading("data", text="Data")
        self.tree_agendamentos.heading("hora", text="Hora")
        self.tree_agendamentos.heading("servico", text="Serviço")
        self.tree_agendamentos.column("id", width=50, anchor='center')
        self.tree_agendamentos.column("cliente", width=200)
        self.tree_agendamentos.column("data", width=100, anchor='center')
        self.tree_agendamentos.column("hora", width=80, anchor='center')
        self.tree_agendamentos.column("servico", width=150)
        self.tree_agendamentos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree_agendamentos.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_agendamentos.configure(yscrollcommand=scrollbar.set)
        self.tree_agendamentos.bind('<<TreeviewSelect>>', self.on_select_agendamento)

        # Botão excluir
        tk.Button(self.frame_agendamentos, text="❌ Excluir Agendamento Selecionado", command=self.excluir_agendamento, bg='#e74c3c', fg='white', font=('Segoe UI', 9)).pack(pady=5)

        # Cores alternadas para tabela de agendamentos
        self.tree_agendamentos.tag_configure('odd', background='#f9f9f9')
        self.tree_agendamentos.tag_configure('even', background='#ffffff')

    def criar_menu(self):
        menubar = tk.Menu(self.root, bg='#ecf0f1', fg='#2c3e50')
        self.root.config(menu=menubar)

        arquivo_menu = tk.Menu(menubar, tearoff=0, bg='#ecf0f1', fg='#2c3e50')
        menubar.add_cascade(label="📁 Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="📂 Importar clientes (CSV)", command=self.importar_csv)
        arquivo_menu.add_command(label="💾 Exportar clientes (CSV)", command=self.exportar_csv)
        arquivo_menu.add_command(label="📄 Importar clientes (JSON)", command=self.importar_json)
        arquivo_menu.add_command(label="💿 Exportar clientes (JSON)", command=self.exportar_json)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="📑 Gerar relatório de agendamentos (TXT)", command=self.gerar_relatorio)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="🚪 Sair", command=self.root.quit)

    # ========== MÉTODOS DE EXIBIÇÃO COM CORES ALTERNADAS ==========
    def atualizar_lista_clientes(self):
        for i in self.tree_clientes.get_children():
            self.tree_clientes.delete(i)
        clientes = db.listar_clientes()
        for idx, cliente in enumerate(clientes):
            tag = 'even' if idx % 2 == 0 else 'odd'
            self.tree_clientes.insert("", tk.END, values=cliente, tags=(tag,))
        # Atualizar combobox
        self.combo_clientes['values'] = [f"{c[0]} - {c[1]}" for c in clientes]

    def atualizar_lista_agendamentos(self):
        for i in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(i)
        agendamentos = db.listar_agendamentos()
        for idx, ag in enumerate(agendamentos):
            tag = 'even' if idx % 2 == 0 else 'odd'
            self.tree_agendamentos.insert("", tk.END, values=ag, tags=(tag,))

    # ========== DEMAIS MÉTODOS (adicionar_cliente, etc.) PERMANECEM IGUAIS ==========
    # Eles são os mesmos do código anterior, apenas com as funções de atualização
    # de lista já modificadas acima. Vou repetir os métodos essenciais para completar.

    def on_select_cliente(self, event):
        selecionado = self.tree_clientes.selection()
        if selecionado:
            valores = self.tree_clientes.item(selecionado[0])['values']
            if valores:
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, valores[1])
                self.entry_telefone.delete(0, tk.END)
                self.entry_telefone.insert(0, valores[2] if valores[2] else "")
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, valores[3] if valores[3] else "")
                self.id_cliente_selecionado = valores[0]

    def adicionar_cliente(self):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome obrigatório.")
            return
        if email and not futils.validar_email(email):
            messagebox.showwarning("Aviso", "Email inválido.")
            return
        db.inserir_cliente(nome, telefone, email)
        self.limpar_campos_clientes()
        self.atualizar_lista_clientes()
        messagebox.showinfo("Sucesso", "Cliente adicionado.")

    def limpar_campos_clientes(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    def atualizar_cliente(self):
        if hasattr(self, 'id_cliente_selecionado'):
            nome = self.entry_nome.get().strip()
            telefone = self.entry_telefone.get().strip()
            email = self.entry_email.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "Nome obrigatório.")
                return
            db.atualizar_cliente(self.id_cliente_selecionado, nome, telefone, email)
            self.limpar_campos_clientes()
            self.atualizar_lista_clientes()
            messagebox.showinfo("Sucesso", "Cliente atualizado.")
            del self.id_cliente_selecionado
        else:
            messagebox.showwarning("Aviso", "Selecione um cliente.")

    def excluir_cliente(self):
        if hasattr(self, 'id_cliente_selecionado'):
            if messagebox.askyesno("Confirmar", "Excluir cliente e seus agendamentos?"):
                db.deletar_cliente(self.id_cliente_selecionado)
                self.limpar_campos_clientes()
                self.atualizar_lista_clientes()
                self.atualizar_lista_agendamentos()
                del self.id_cliente_selecionado
        else:
            messagebox.showwarning("Aviso", "Selecione um cliente.")

    def carregar_agendamentos_por_cliente(self):
        selecao = self.combo_clientes.get()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um cliente.")
            return
        try:
            cliente_id = int(selecao.split(" - ")[0])
        except:
            messagebox.showerror("Erro", "Cliente inválido.")
            return
        agendamentos = db.buscar_agendamentos_por_cliente(cliente_id)
        for i in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(i)
        for idx, ag in enumerate(agendamentos):
            tag = 'even' if idx % 2 == 0 else 'odd'
            self.tree_agendamentos.insert("", tk.END, values=ag, tags=(tag,))

    def adicionar_agendamento(self):
        selecao = self.combo_clientes.get()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um cliente.")
            return
        cliente_id = int(selecao.split(" - ")[0])
        data = self.entry_data.get().strip()
        hora = self.entry_hora.get().strip()
        servico = self.entry_servico.get().strip()
        if not data or not hora or not servico:
            messagebox.showwarning("Aviso", "Preencha data, hora e serviço.")
            return
        import re
        if not re.match(r'\d{4}-\d{2}-\d{2}', data):
            messagebox.showwarning("Aviso", "Data deve estar no formato AAAA-MM-DD")
            return
        if not re.match(r'\d{2}:\d{2}', hora):
            messagebox.showwarning("Aviso", "Hora deve estar no formato HH:MM")
            return
        db.inserir_agendamento(cliente_id, data, hora, servico)
        self.entry_data.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_servico.delete(0, tk.END)
        self.atualizar_lista_agendamentos()
        messagebox.showinfo("Sucesso", "Agendamento criado.")

    def on_select_agendamento(self, event):
        selecionado = self.tree_agendamentos.selection()
        if selecionado:
            valores = self.tree_agendamentos.item(selecionado[0])['values']
            if valores:
                self.id_agendamento_selecionado = valores[0]

    def excluir_agendamento(self):
        if hasattr(self, 'id_agendamento_selecionado'):
            if messagebox.askyesno("Confirmar", "Excluir este agendamento?"):
                db.deletar_agendamento(self.id_agendamento_selecionado)
                self.atualizar_lista_agendamentos()
                del self.id_agendamento_selecionado
        else:
            messagebox.showwarning("Aviso", "Selecione um agendamento.")

    def exportar_csv(self):
        clientes = db.listar_clientes()
        if not clientes:
            messagebox.showinfo("Info", "Nenhum cliente para exportar.")
            return
        ok, msg = futils.exportar_clientes_csv(clientes)
        messagebox.showinfo("Resultado", msg) if ok else messagebox.showerror("Erro", msg)

    def importar_csv(self):
        arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return
        ok, resultado = futils.importar_clientes_csv(arquivo)
        if ok:
            for nome, tel, email in resultado:
                db.inserir_cliente(nome, tel, email)
            self.atualizar_lista_clientes()
            messagebox.showinfo("Sucesso", f"Importados {len(resultado)} clientes.")
        else:
            messagebox.showerror("Erro", resultado)

    def exportar_json(self):
        clientes = db.listar_clientes()
        if not clientes:
            messagebox.showinfo("Info", "Nenhum cliente.")
            return
        dados = [{"id": c[0], "nome": c[1], "telefone": c[2], "email": c[3]} for c in clientes]
        ok, msg = futils.exportar_clientes_json(dados)
        messagebox.showinfo("Resultado", msg) if ok else messagebox.showerror("Erro", msg)

    def importar_json(self):
        arquivo = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not arquivo:
            return
        ok, resultado = futils.importar_clientes_json(arquivo)
        if ok:
            for nome, tel, email in resultado:
                db.inserir_cliente(nome, tel, email)
            self.atualizar_lista_clientes()
            messagebox.showinfo("Sucesso", f"Importados {len(resultado)} clientes.")
        else:
            messagebox.showerror("Erro", resultado)

    def gerar_relatorio(self):
        ok, msg = rel.gerar_relatorio_agendamentos()
        if ok:
            messagebox.showinfo("Relatório", f"Relatório gerado: {msg}")
        else:
            messagebox.showerror("Erro", msg)

def main():
    root = tk.Tk()
    app = AppAgendamento(root)
    root.mainloop()

if __name__ == "__main__":
    main()
