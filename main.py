import customtkinter as c

class JanelaProducao():
    def __init__(self, janela_principal) -> None:
        self.janela_principal = janela_principal
        self.jprod = c.CTk()
        self.jprod.title("Produção")
        self.jprod.geometry("800x600")
        self.jprod.resizable(width=False, height=False)
        c.set_appearance_mode("Dark")

        titulo = c.CTkLabel(self.jprod, text="Produção", height=10, font=("Arial", 50), justify="center")
        titulo.pack(padx=10, pady=150)

        # Configurando a função fecharProducao para ser chamada ao fechar a janela de produção
        self.jprod.protocol("WM_DELETE_WINDOW", self.fecharProducao)

    def exibir(self):
        self.janela_principal.fecharJanela()  # Fecha a janela principal antes de exibir a janela de produção
        self.jprod.mainloop()

    def fecharProducao(self):
        # Adicione aqui qualquer código necessário para fechar adequadamente a janela de produção
        self.jprod.destroy()
        self.janela_principal.reabrirPrincipal()

class JanelaLogistica():
    def __init__(self, janela_principal) -> None:
        self.janela_principal = janela_principal
        self.jlog = c.CTk()
        self.jlog.title("Logística")
        self.jlog.geometry("800x600")
        self.jlog.resizable(width=False, height=False)
        c.set_appearance_mode("Dark")

        titulo = c.CTkLabel(self.jlog, text="Logística", height=10, font=("Arial", 50), justify="center")
        titulo.pack(padx=10, pady=150)

        self.jlog.protocol("WM_DELETE_WINDOW", self.fecharLogistica)

    def exibir(self) -> None:
        self.janela_principal.fecharJanela() 
        self.jlog.mainloop()

    def fecharLogistica(self) -> None:
        self.jlog.destroy()
        self.janela_principal.reabrirPrincipal()

class JanelaPrincipal():
    def __init__(self) -> None:
        self.ativa = True

        self.janela = c.CTk()
        self.janela.title("Elevator")
        self.janela.geometry("800x600")
        self.janela.resizable(width=False, height=False)
        c.set_appearance_mode("Dark")

        titulo_inicial = c.CTkLabel(self.janela, text="Aguardando Leitor", height=10, font=("Arial", 50), justify="center")
        titulo_inicial.pack(padx=10, pady=150)

        progresso = c.CTkProgressBar(self.janela, orientation="horizontal", determinate_speed=1, mode="indeterminate", width=300, height=20)
        progresso.pack(pady=40)
        progresso.set(0)
        progresso.start()

        btn_teste = c.CTkButton(self.janela, text="Prod", command=lambda: self.abrirJanela(1))
        btn_teste.pack(pady=10)
        
        btn_log = c.CTkButton(self.janela, text="Log", command=lambda: self.abrirJanela(2))
        btn_log.pack(pady=5)

        self.janela.mainloop()

    def abrirJanela(self,tela) -> None:  
        
        if tela == 1:      
            janela_producao = JanelaProducao(self)
            janela_producao.exibir()
        elif tela == 2:
            janela_logistica = JanelaLogistica(self)
            janela_logistica.exibir()

    def fecharJanela(self) -> None:
        self.janela.destroy()

    def reabrirPrincipal(self):
        self.__init__()

# Instanciando a JanelaPrincipal para iniciar o programa
janela_principal = JanelaPrincipal()
