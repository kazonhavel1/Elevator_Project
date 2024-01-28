import customtkinter as c
from tkinter import messagebox
import time
import logging
from PIL import Image, ImageTk
import arduino as ard


logging.basicConfig(
    level=logging.INFO,
    filename="programa.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class JanelaProducao:
    
    usuario = ""
    funcao = ""
    
    def __init__(self, janela_principal) -> None:
        self.janela_principal = janela_principal
        self.jprod = c.CTk()
        self.jprod.title("Produção")
        self.jprod.geometry("800x600")
        self.jprod.resizable(width=False, height=False)

        # Configuração de linhas e colunas para expandir conforme o tamanho da janela
        self.jprod.columnconfigure(0, weight=1)
        self.jprod.columnconfigure(1, weight=1)
        self.jprod.rowconfigure(0, weight=1)
        self.jprod.rowconfigure(1, weight=1)
        self.jprod.rowconfigure(2, weight=1)
        self.jprod.configure(padx=15, pady=15)

        self.status = c.CTkLabel(
            self.jprod,
            text="Desconectado",
            height=5,
            font=("Arial", 17),
            text_color=("red"),
            justify="center",
        )
        self.status.grid(column=1, sticky="n")

        self.criarGridPrincipal()
        self.criarGridAdicionais()
        self.update_time()

        self.jprod.after(5000,lambda: self.verificaConexao())

        # Configurando a função fecharProducao para ser chamada ao fechar a janela de produção
        self.jprod.protocol("WM_DELETE_WINDOW", self.fecharProducao)

        self.jprod.mainloop()

    def imagem(self):
        imagem = ImageTk.PhotoImage(file="dedo.png", master=self.jprod)

        return imagem

    def criarGridPrincipal(self):
        main_grid = c.CTkFrame(self.jprod, width=60, height=60, fg_color="gray")
        main_grid.grid(row=1, column=1)

        # Quadrado central com fundo cinza
        central_square = c.CTkLabel(
            main_grid,
            text="Último Acesso: Nathalia\n\nFunção: Logística",
            bg_color="transparent",
            padx=10,
            pady=10,
            justify="left",
            font=("Arial", 20),
        )
        central_square.grid(row=0, column=0)

        try:
            self.img = self.imagem()
            image_label = c.CTkLabel(
                main_grid, image=self.img, corner_radius=7, text=""
            )
            image_label.grid(row=1, column=1, pady=5, padx=5)
        except Exception as e:
            logging.error(e)

    def criarGridAdicionais(self):
        # Grid superior esquerdo
        top_left_grid = c.CTkFrame(
            self.jprod,
            width=400,
            height=400,
            bg_color="transparent",
            fg_color="transparent",
            corner_radius=10,
        )
        top_left_grid.grid(row=0, column=0, sticky="nw")

        top_left_text = c.CTkLabel(
            top_left_grid, text="Peso atual:", font=("Arial", 20)
        )
        top_left_text.grid(row=0, column=0, sticky="nw")

        top_left_text1 = c.CTkLabel(
            top_left_grid,
            text="0 KG",
            font=("Arial", 35),
            bg_color="gray",
            corner_radius=10,
            width=200,
            height=50,
        )
        top_left_text1.grid(row=1, column=0)

        top_left_text2 = c.CTkLabel(
            top_left_grid, text="Peso Limite:", font=("Arial", 20), justify="left"
        )
        top_left_text2.grid(row=2, column=0, sticky="nw")

        top_left_text3 = c.CTkLabel(
            top_left_grid,
            text="1000 KG",
            font=("Arial", 25),
            bg_color="gray",
            corner_radius=10,
            width=200,
            height=30,
        )
        top_left_text3.grid(row=3, column=0, sticky="nw")

        # Grid inferior esquerdo
        bottom_left_grid = c.CTkFrame(
            self.jprod, width=100, height=100, fg_color="transparent"
        )
        bottom_left_grid.grid(row=2, column=0, sticky="sw")

        bottom_left_text = c.CTkLabel(
            bottom_left_grid, text="Andar: ", font=("Arial", 20)
        )
        bottom_left_text.grid(row=0, column=0, sticky="nesw", ipady=5, ipadx=5)

        bottom_left_text2 = c.CTkLabel(
            bottom_left_grid,
            text="1",
            bg_color="gray",
            height=25,
            width=100,
            font=("Arial", 20),
        )
        bottom_left_text2.grid(row=0, column=1, sticky="sw", ipady=5, ipadx=5)

        # Grid inferior direito
        self.bottom_right_grid = c.CTkLabel(
            self.jprod,
            text="Horário: 19:22 \n\nUsuário: João Pedro\nFunção: Produção",
            bg_color="gray",
            width=120,
            height=120,
            corner_radius=10,
            justify="left",
            font=("Arial", 18),
        )
        self.bottom_right_grid.grid(row=2, column=8, sticky="se")

        # Grid superior direito
        top_right_grid = c.CTkLabel(
            self.jprod,
            text="Porta Interna: Fechada\nPorta Externa: Fechada",
            bg_color="gray",
            corner_radius=5,
            width=50,
            height=50,
            justify="left",
            font=("Arial", 15),
            padx=10,
        )
        top_right_grid.grid(row=0, column=8, sticky="ne")

    def exibir(self,usuario,funcao):
        self.usuario = usuario
        self.funcao = funcao
        hora_atual = time.strftime("%H:%M")
        self.janela_principal.fecharJanela()
        self.bottom_right_grid.config(text=f"Horário: {hora_atual} \n\nUsuário: {usuario}\nFunção: {funcao}")
        self.jprod.deiconify()

    def fecharProducao(self):
        self.jprod.withdraw()
        self.janela_principal.reabrirPrincipal()

    def update_time(self):
      data_atual = time.strftime("%H:%M")
      self.bottom_right_grid(text=f"Horário: {data_atual} \n\nUsuário: {self.usuario}\nFunção: {self.funcao}")
      self.jprod.after(60000, lambda: self.update_time())

    def verificaConexao(self):
        conexao = ard.ConexaoArd()
        if conexao.validaConexao() == True:
            self.status.configure(text="Conectado",text_color="Green")
            return True
        else:
            self.status.configure(text="Desconectado",text_color="Red")
            return False
        
        
class JanelaPrincipal:
    def __init__(self) -> None:
        self.janela = c.CTk()
        self.janela.title("Elevator")
        self.janela.geometry("800x600")
        self.janela.resizable(width=False, height=False)
        c.set_appearance_mode("Dark")

        self.status = c.CTkLabel(
            self.janela,
            text="Desconectado",
            height=10,
            font=("Arial", 15),
            corner_radius=10,
            text_color=("red"),
            anchor="e",
        )
        self.status.pack(padx=10, pady=5, anchor="ne")

        titulo_inicial = c.CTkLabel(
            self.janela,
            text="Monta Cargas",
            height=10,
            font=("Arial", 50),
            justify="center",
        )
        titulo_inicial.pack(padx=10, pady=100)

        self.hora_atual = c.CTkLabel(
            self.janela, text="1", height=10, font=("Arial", 25), justify="center"
        )
        self.hora_atual.pack(padx=10, pady=10)

        self.progresso = c.CTkProgressBar(
            self.janela,
            orientation="horizontal",
            determinate_speed=1,
            mode="indeterminate",
            width=300,
            height=20,
        )
        self.progresso.pack(pady=40)
        self.progresso.set(0)
        self.progresso.start()


        self.btn_prod = c.CTkButton(
            self.janela, text="Conectar", command=lambda: self.conectarArd()
        )
        self.btn_prod.pack(pady=10)

        self.update_time()
        self.verificaConexao()

        self.janela.mainloop()
        logging.info("Janela Principal aberta")

    def update_time(self):
        data_atual = time.strftime("%H:%M:%S")
        self.hora_atual.configure(text=f"Horas: {data_atual}")
        self.janela.after(1000, lambda: self.update_time())

    def abrirJanela(self, tela,usuario,funcao) -> None:
        if tela == 1:
            janela_producao = JanelaProducao(self)
            logging.info("Abrindo Janela de Producao")
            janela_producao.exibir(usuario,funcao)

    def fecharJanela(self) -> None:
        self.janela.withdraw()

    def reabrirPrincipal(self):
        logging.info("Usuario Desconectado, Reabrindo Janela Principal")
        self.janela.deiconify()

    def conectarArd(self):
        self.btn_prod.configure(state="disabled", text="Conectando", fg_color="gray")
        conexao = ard.ConexaoArd()
        if conexao.conectarArduino() == True:
            self.btn_prod.configure(text="Aguardando Sensor")
            messagebox.showinfo("Monta Cargas", "Conexão Bem Sucedida!")
            self.status.configure(text="Conectado", text_color=("green"))
            self.login()
        else:
            messagebox.showerror(
                "Monta Cargas", "Erro ao se conectar com o Arduíno, verifique no log."
            )
            self.btn_prod.configure(text="Conectar", state="normal", fg_color="#1c6ca4")
    
    def login(self):
        ardu = ard.ConexaoArd()
        if ardu.validaConexao() == True:
           while True:
             retorno = ard.ser.readline().decode("utf-8")
             retorno_txt = retorno.strip()
             if "Vinicius" in retorno_txt:
               logging.info("Usuario Logado: Vinicius -- Gerente")
               self.abrirJanela(1,"Vinicius","Gerente")
               break
        else:
            pass   
    def verificaConexao(self):
        conexao = ard.ConexaoArd()
        if conexao.validaConexao() == True:
            self.status.configure(text="Conectado", text_color=("green"))
        else:
            self.btn_prod.configure(state="normal", text="Conectar", fg_color="#1c6ca4")
            self.status.configure(text="Desconectado", text_color=("red"))
        self.janela.after(10000,lambda: self.verificaConexao())
        

# Instanciando a JanelaPrincipal para iniciar o programa
janela_principal = JanelaPrincipal()
