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
    
    tela_ativa = False
    ardu = None

    conectado = False
    usuario = None
    funcao = None

    ultimo_login = None
    ultima_funcao = None

    def __init__(
        self, janela_principal, usuario, funcao, ardu, ultimo_login, ultima_funcao
    ) -> None:
        self.janela_principal = janela_principal
        self.jprod = c.CTk()
        self.jprod.title("Produção")
        self.jprod.geometry("1280x720")
        self.maximizar_janela()

        self.usuario = usuario
        self.funcao = funcao
        self.ardu = ardu
        
        self.ultimo_login = usuario
        self.ultima_funcao = funcao

        # Configuração de linhas e colunas para expandir conforme o tamanho da janela
        self.jprod.columnconfigure(0, weight=0)
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

        self.tela_ativa = True
        
        self.retorno_buffer = []
        
        self.criarGridPrincipal()
        self.criarGridAdicionais()
        self.update_time()


        self.atualiza()
        self.verificaConexao()
        
        
        # Configurando a função fecharProducao para ser chamada ao fechar a janela de produção
        self.jprod.protocol("WM_DELETE_WINDOW", self.fecharProducao)

        self.jprod.mainloop()
        logging.info("Janela Produção aberta")
        
        

    def maximizar_janela(self):
        largura = self.jprod.winfo_screenwidth()
        altura = self.jprod.winfo_screenheight() - 80  # Reduzindo 50 pixels da altura
        self.jprod.geometry("{0}x{1}+0+0".format(largura, altura))

    def imagem(self):
        imagem = ImageTk.PhotoImage(file="dedo.png", master=self.jprod)

        return imagem

    def criarGridPrincipal(self):
        main_grid = c.CTkFrame(self.jprod, width=60, height=60, fg_color="gray")
        main_grid.grid(row=1, column=1)

        # Quadrado central com fundo cinza
        central_square = c.CTkLabel(
            main_grid,
            text=f"Último Acesso: {self.ultimo_login}\n\nFunção: {self.ultima_funcao}",
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
            width=300,
            height=300,
            bg_color="transparent",
            fg_color="transparent",
            corner_radius=10,
        )
        top_left_grid.grid(row=0, column=0, sticky="nw")

        top_left_text = c.CTkLabel(
            top_left_grid, text="Peso atual:", font=("Arial", 20)
        )
        top_left_text.grid(row=0, column=0, sticky="nw")

        self.top_left_text1 = c.CTkLabel(
            top_left_grid,
            text="0 KG",
            font=("Arial", 35),
            bg_color="gray",
            corner_radius=10,
            width=200,
            height=50,
        )
        self.top_left_text1.grid(row=1, column=0)

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

        self.bottom_left_text2 = c.CTkLabel(
            bottom_left_grid,
            text="0",
            bg_color="gray",
            height=25,
            width=100,
            font=("Arial", 20),
        )
        self.bottom_left_text2.grid(row=0, column=1, sticky="sw", ipady=5, ipadx=5)

        # Grid inferior direito
        self.bottom_right_grid = c.CTkLabel(
            self.jprod,
            text="Horário: 19:22 \n\nUsuário: Nenhum\nFunção: Nenhum",
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
            #text="Porta Interna: Fechada\nPorta Externa: Fechada",
            bg_color="gray",
            fg_color="transparent",
            corner_radius=5,
            width=40,
            height=40,
            justify="left",
            font=("Arial", 15),
            padx=10,
        )
        top_right_grid.grid(row=0, column=8, sticky="ne")
        
        self.text_top_right_grid = c.CTkLabel(
            top_right_grid,
            text="Porta Interna: ",
            justify="left",
            font=("Arial", 15),
            bg_color="gray",
            fg_color="gray"
        )

        self.text_top_right_grid.grid(row=0,column=0)
        
        self.text_top_right_grid1 = c.CTkLabel(
            top_right_grid,
            text="Porta Externa: ",
            justify="left",
            font=("Arial", 15),
            bg_color="gray",
            fg_color="gray"
        )

        self.text_top_right_grid1.grid(row=1,column=0,padx=5)
    
    
    
    
     
    
    def fecharProducao(self):
        self.jprod.withdraw()
        self.janela_principal.last_function = self.ultima_funcao
        self.janela_principal.last_login = self.ultimo_login
        self.tela_ativa = False
        self.janela_principal.login()

    def update_time(self):
        data_atual = time.strftime("%H:%M")
        self.bottom_right_grid.configure(
            text=f"Horário: {data_atual} \n\nUsuário: {self.usuario}\nFunção: {self.funcao}"
        )
        self.jprod.after(60000, lambda: self.update_time())

    def verificaConexao(self):
        conexao = self.ardu
        if conexao.validaConexao() == True:
            self.status.configure(text="Conectado", text_color="Green")
            self.conectado = True
            return True
        else:
            self.status.configure(text="Desconectado", text_color="Red")
            self.conectado = False
            return False



    def atualiza(self):
        
        if self.tela_ativa == True:
            arduino = self.ardu
            while self.conectado == True:
                retorno = arduino.ser.readline().decode("utf-8")
                txt = retorno.strip()
                logging.info(f"Recebido do Arduino: {txt}")

                if "Peso:" in txt:
                            valor = retorno[6:].strip()
                            self.atualizaPeso(valor=valor)
                            break
                elif "andar" in txt:
                    valor = txt[6:]
                    self.atualizaAndar(valor=valor)
                    break
                
                elif "Porta Interna:" in txt:
                    valor = txt[15:]
                    self.atualizaPortaInterna(valor=valor)
                    break
                
                elif "Porta Externa:" in txt:
                    valor = txt[15:]
                    self.atualizaPortaExterna(valor=valor)
                    break
                
                else:
                    break

            self.jprod.after(500, lambda: self.atualiza())
    
    def atualizaPortaInterna(self,valor):
        self.text_top_right_grid.configure(text=f"Porta Interna: {valor}")
        
    def atualizaPeso(self,valor):
        self.top_left_text1.configure(text=f"{valor}")
        
    def atualizaAndar(self,valor):
        self.bottom_left_text2.configure(text=f"{valor}")
        
    def atualizaPortaExterna(self,valor):
        self.text_top_right_grid1.configure(text=f"Porta Externa: {valor}")
        
   
        
   
     

class JanelaPrincipal:
    ardu = ard.ConexaoArd()

    conectado = False
    
    last_login = ""
    last_function = ""

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
        self.janela.mainloop()
        logging.info("Janela Principal aberta")

    def update_time(self):
        data_atual = time.strftime("%H:%M:%S")
        self.hora_atual.configure(text=f"Horas: {data_atual}")
        self.janela.after(1000, lambda: self.update_time())

    def abrirJanela(self, tela, usuario, funcao) -> None:
        if tela == 1:
            janela_producao = JanelaProducao(self, usuario, funcao, ardu=self.ardu,ultimo_login=self.last_login,ultima_funcao=self.last_function)
            logging.info("Abrindo Janela de Producao")
            janela_producao.exibir(janela_principal=self)


    def conectarArd(self):
        self.btn_prod.configure(state="disabled", text="Conectando", fg_color="gray")
        conexao = self.ardu
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
        ardu = self.ardu
        if ardu.validaConexao() == True:
            while True:
                retorno = ardu.ser.readline().decode("utf-8")
                retorno_txt = retorno.strip()
                if "Vinicius" in retorno_txt:
                    logging.info("Usuario Logado: Vinicius -- Gerente")
                    self.abrirJanela(tela=1, usuario="Vinicius", funcao="Gerente")
                    break
                if "Nathalia" in retorno_txt:
                    logging.info("Usuario Logado: Nathalia -- Produção")
                    self.abrirJanela(tela=1, usuario="Nathalia", funcao="Produção")
                    break
                if "Bruna" in retorno_txt:
                    logging.info("Usuario Logado: Bruna  -- Logistica")
                    self.abrirJanela(tela=1, usuario="Bruna ", funcao="Logística")
                    break
                if "Rafael" in retorno_txt:
                    logging.info("Usuario Logado: Rafael  -- Tech Lead")
                    self.abrirJanela(tela=1, usuario="Rafael", funcao="Tech Lead")
                    break
        else:
            pass

    def verificaConexao(self):
        conexao = self.ardu
        if conexao.validaConexao() == True:
            self.status.configure(text="Conectado", text_color=("green"))
            self.conectado = True
        else:
            self.btn_prod.configure(state="normal", text="Conectar", fg_color="#1c6ca4")
            self.status.configure(text="Desconectado", text_color=("red"))
        self.janela.after(10000, lambda: self.verificaConexao())


# Instanciando a JanelaPrincipal para iniciar o programa
janela_principal = JanelaPrincipal()
