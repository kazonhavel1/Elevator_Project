import customtkinter as c
import time
import logging
from PIL import Image, ImageTk

logging.basicConfig(
    level=logging.INFO,
    filename="programa.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class JanelaProducao:
    img_references = Image.open("digital-removebg-preview.png")

    def __init__(self) -> None:
        self.jprod = c.CTk()
        self.jprod.title("Produção")
        self.jprod.geometry("800x650")
        self.jprod.resizable(width=False, height=False)
        c.set_appearance_mode("Dark")

        # Configuração de linhas e colunas para expandir conforme o tamanho da janela
        self.jprod.columnconfigure(0, weight=2)
        self.jprod.columnconfigure(2, weight=2)
        self.jprod.rowconfigure(0, weight=2)
        self.jprod.rowconfigure(1, weight=2)
        self.jprod.rowconfigure(2, weight=1)
        self.jprod.configure(padx=15, pady=15)

        status = c.CTkLabel(
            self.jprod,
            text="Desconectado",
            height=5,
            font=("Arial", 17),
            text_color=("red"),
            justify="center",
        )
        status.grid(column=1, sticky="n")

        self.criarGridPrincipal()
        self.criarGridAdicionais()
        

        self.jprod.mainloop()

        # Configurando a função fecharProducao para ser chamada ao fechar a janela de produção
        # self.jprod.protocol("WM_DELETE_WINDOW", self.fecharProducao)

    def criarGridPrincipal(self):
        main_grid = c.CTkFrame(
            self.jprod, width=60, height=60,fg_color="gray"
        )
        main_grid.grid(row=1, column=1)

        # Quadrado central com fundo cinza
        central_square = c.CTkLabel(
            main_grid,
            text="Último Acesso: Nathalia\n\nFunção: Logística",
            bg_color="transparent",
            padx=10,
            pady=10,
            justify="left",
            font=("Arial", 20)
            
        )
        central_square.grid(row=0, column=0)

        try:
            self.img = ImageTk.PhotoImage(self.img_references)
            image_label = c.CTkLabel(
                main_grid, image=self.img, corner_radius=7,text=""
            )
            image_label.grid(row=1, column=1,pady=5,padx=5)
        except Exception as e:
            logging.error(e)



    def criarGridAdicionais(self):
        # Grid superior esquerdo
        top_left_grid = c.CTkFrame(
            self.jprod, width=400, height=400, bg_color="transparent",fg_color="transparent", corner_radius=10
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
            top_left_grid,
            text="Peso Limite:",
            font=("Arial", 20),
            justify="left"
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
        top_left_text3.grid(row=3, column=0,sticky="nw")

        # Grid inferior esquerdo
        bottom_left_grid = c.CTkFrame(self.jprod, width=100, height=100, fg_color="transparent")
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
        bottom_right_grid = c.CTkLabel(
            self.jprod,
            text="Horário: 19:22 \n\nUsuário: João Pedro\nFunção: Produção",
            bg_color="gray",
            width=120,
            height=120,
            corner_radius=10,
            justify="left",
            font=("Arial", 18),
        )
        bottom_right_grid.grid(row=2, column=8, sticky="se")

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
            padx =10
            
        )
        top_right_grid.grid(row=0, column=8, sticky="ne")



        
        

        

pd = JanelaProducao()

pd.__init__()
