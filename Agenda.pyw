from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import sqlite3


root = Tk()
    
class Funcs():

    def limpar_tela(self):
        self.codigo_entry.delete(0,END)
        self.nome_entry.delete(0, END)
        self.morada_entry.delete(0, END)
        self.contacto_entry.delete(0, END)
        self.email_entry.delete(0, END)

    def conecta_db(self):
        self.conex = sqlite3.connect("agenda.db")
        self.cursor = self.conex.cursor()

    def desconectar_db(self):
        self.conex.close()


            

    def monta_tabelas(self):
        self.conecta_db()

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS pessoas(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NOME VARCHAR(50),
                        MORADA VARCHAR(30),
                        CONTACTO INTEGER(15),
                        EMAIL VARCHAR(50))
                        """)
        self.conex.commit()
        self.desconectar_db()


    def add_cliente(self):
        self.nome = self.nome_entry.get()
        self.morada = self.morada_entry.get()
        self.contacto = self.contacto_entry.get()
        self.email = self.email_entry.get()
        self.conecta_db()

        self.cursor.execute("""INSERT INTO pessoas ( ID,NOME, MORADA,CONTACTO, EMAIL)
                                        VALUES(NULL,?,?,?,? )""",(self.nome, self.morada, self.contacto, self.email))

        self.conex.commit()
        self.desconectar_db()
        self.select_lista()
        self.limpar_tela()
        messagebox.showinfo("Salvo!", "Cadastro adicionado com sucesso." )


    def select_lista(self):

        self.listaCli.delete(*self.listaCli.get_children())  #função para limpar a lista
        self.conecta_db()
        lista = self.cursor.execute(""" SELECT ID,NOME, MORADA,CONTACTO, EMAIL
                                FROM pessoas ORDER BY NOME ASC;""")

        for i in lista:
            self.listaCli.insert("", END, values = i)

        self.desconectar_db()

    def duplo_click(self, event):
        self.limpar_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4,col5 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2 )
            self.morada_entry.insert(END, col3)
            self.contacto_entry.insert(END,col4)
            self.email_entry.insert(END, col5)
            
                

    def deletar_cliente(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.morada = self.morada_entry.get()
        self.contacto = self.contacto_entry.get()
        self.email = self.email_entry.get()

        self.conecta_db()

        self.cursor.execute("""DELETE FROM pessoas WHERE ID= ?""", (self.codigo,))
        self.conex.commit()

        messagebox.showinfo("", "Cadastro eliminado com sucesso." )

        self.desconectar_db()
        self.limpar_tela()
        self.select_lista()

    def alterar_cliente(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.morada = self.morada_entry.get()
        self.contacto = self.contacto_entry.get()
        self.email = self.email_entry.get()

        self.conecta_db()

        self.cursor.execute(""" UPDATE pessoas SET NOME =?, MORADA = ?, CONTACTO = ?, EMAIL =?
                                            WHERE ID = ? """,(self.nome, self.morada, self.contacto, self.email, self.codigo))

        messagebox.showinfo("", "Cadastro alterado com sucesso." )

        self.conex.commit()
        

        self.desconectar_db()
        self.limpar_tela()
        self.select_lista()


    def buscar_clientes(self):

        self.conecta_db()

        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
                """ SELECT ID, NOME, MORADA, CONTACTO, EMAIL FROM pessoas
                WHERE NOME LIKE '%s' ORDER BY NOME ASC""" %  nome)
        buscanomeCli = self.cursor.fetchall()

        for i in buscanomeCli:
                
            self.listaCli.insert("", END, values = i)
                
        self.limpar_tela()
        self.desconectar_db()
                
            


        self.desconectar_db()


            

                
class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.criando_butoes()
        self.lista_frame2()
        self.monta_tabelas()
        self.select_lista()
        #self.add_cliente()
        root.mainloop()

    def tela(self):
        self.root.title("\t\tAgenda")
        self.root.configure(background ='#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width = 900, height = 700)
        self.root.minsize(width = 400, height = 300)

    def frames_da_tela(self):
        self.frame1 = Frame(self.root, bd = 4, bg = '#dfe3ee',
                            highlightbackground = '#759fe6', highlightthickness = 3)
        self.frame1.place(relx = 0.02, rely =0.02, relwidth = 0.96, relheight = 0.46)
        #relx e rely usa-se para definir a percentagem da distância da tela que queremos o
        #nosso frame ou widget  ele acompanha a tela se ela aumenta ou diminue
        #o relwidth é a largura e o relheight é a altura
        #bd é borda o highlightbackground é a cor da borda e o highlightthickness é a largura da borda

        self.frame2 = Frame(self.root, bd = 4, bg = '#dfe3ee',
                            highlightbackground = '#759fe6', highlightthickness = 3)
        self.frame2.place(relx = 0.02, rely =0.5, relwidth = 0.96, relheight = 0.46)

    def criando_butoes(self):
        self.bt_limpar = Button(self.frame1, text = "Limpar",bd = 2, bg = "#107db2", fg = "white",
                                font = ("Verdana", 6, 'bold'),command = self.limpar_tela)
        self.bt_limpar.place(relx = 0.15 , rely = 0.1, relwidth = 0.1, relheight = 0.15)

        self.bt_buscar = Button(self.frame1, text = "Buscar",bd = 2, bg = "#107db2", fg = "white",
                                font = ("Verdana", 6, 'bold'), command = self.buscar_clientes)
        self.bt_buscar.place(relx = 0.3, rely = 0.1, relwidth = 0.1, relheight = 0.15)

        self.bt_novo = Button(self.frame1, text = "Novo",bd = 2, bg = "#107db2", fg = "white",
                                font = ("Verdana", 6, 'bold'),command = self.add_cliente)
        self.bt_novo.place(relx = 0.55, rely = 0.1, relwidth = 0.1, relheight = 0.15)

        self.bt_alterar = Button(self.frame1, text = "Alterar",bd = 2, bg = "#107db2", fg = "white",
                                font = ("Verdana", 6, 'bold'), command = self.alterar_cliente )
        self.bt_alterar.place(relx = 0.7, rely = 0.1, relwidth = 0.1, relheight = 0.15)

        self.bt_apagar = Button(self.frame1, text = "Apagar",bd = 2, bg = "#107db2", fg = "white",
                                font = ("Verdana", 6, 'bold'), command = self.deletar_cliente)
        self.bt_apagar.place(relx = 0.85, rely = 0.1, relwidth = 0.1, relheight = 0.15)

            #Criação das labels


        self.lb_nome = Label(self.frame1, text ="Nome", bg = '#dfe3ee',fg = "#107db2")
        self.lb_nome.place(relx = 0.05, rely = 0.35)
            
        self.nome_entry = Entry(self.frame1)
        self.nome_entry.place(relx = 0.05, rely = 0.45, relwidth = 0.4)

        self.lb_email = Label(self.frame1, text ="Email", bg = '#dfe3ee',fg = "#107db2")
        self.lb_email.place(relx = 0.05, rely = 0.65)
            
        self.email_entry = Entry(self.frame1)
        self.email_entry.place(relx = 0.05, rely = 0.75, relwidth = 0.4)

        self.lb_morada = Label(self.frame1, text ="Morada", bg = '#dfe3ee',fg = "#107db2")
        self.lb_morada.place(relx = 0.55, rely = 0.35)
            
        self.morada_entry = Entry(self.frame1)
        self.morada_entry.place(relx = 0.55, rely = 0.45, relwidth = 0.4)

        self.lb_contacto= Label(self.frame1, text ="Contacto", bg = '#dfe3ee',fg = "#107db2")
        self.lb_contacto.place(relx = 0.55, rely = 0.65)
            
        self.contacto_entry = Entry(self.frame1)
        self.contacto_entry.place(relx = 0.55, rely = 0.75, relwidth = 0.4)

        self.lb_codigo = Label(self.frame1, text ="Código",bg = '#dfe3ee',fg = "#107db2")
        self.lb_codigo.place(relx = 0.05, rely = 0.05)

        self.codigo_entry = Entry(self.frame1)
        self.codigo_entry.place(relx = 0.05, rely = 0.15, relwidth = 0.08 )

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame2,height = 3, column =("col1", "col2", "col3", "col4", "col5"))
        self.listaCli.heading("#0", text ="")
        self.listaCli.heading("#1", text ="Código")
        self.listaCli.heading("#2", text ="Nome")
        self.listaCli.heading("#3", text ="Morada")
        self.listaCli.heading("#4", text ="Contacto")
        self.listaCli.heading("#5", text ="Email")

        self.listaCli.column("#0", width = 0)
        self.listaCli.column("#1", width = 25)
        self.listaCli.column("#2", width = 150)
        self.listaCli.column("#3", width = 120)
        self.listaCli.column("#4", width = 50)
        self.listaCli.column("#5", width = 140)

        self.listaCli.place(relx = 0.01, rely = 0.1, relwidth = 0.95, relheight = 0.85)

        self.scrol_lista = Scrollbar(self.frame2, orient = "vertical", command = self.listaCli.yview)
        self.listaCli.configure(yscroll = self.scrol_lista.set)
        self.scrol_lista.place(relx = 0.96, rely = 0.1, relwidth = 0.03, relheight = 0.85)

        self.listaCli.bind("<Double-1>", self.duplo_click)
            


Application()
