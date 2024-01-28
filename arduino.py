import serial
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    filename="programa.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ConexaoArd:
    
    def __init__(self) -> None:
        self.porta_serial = "COM5"  # Substitua pela porta serial do seu Arduino (pode ser 'COMx' no Windows)
        self.baud_rate = 9600
        self.ser = None

    serial = None

    conectado = False

    def conectarArduino(self):
        try:
            # Inicialize a comunicação serial
            self.ser = serial.Serial(self.porta_serial, self.baud_rate, timeout=2)
            logging.info(f"Conexao com o Arduino bem sucedida!")
            self.conectado = True
            return self.conectado
        except Exception as e:
            self.conectado = False
            logging.error(f"Erro ao se conectar no Arduino: {e}")
            return e

    def validaConexao(self):
        status_atual = False
        try:
            if self.ser is not None and self.ser.is_open == True:
                status_atual = True
                return status_atual
            else:
                logging.info("Arduino desconectado, tentando reconexao...")
                status_atual = self.conectarArduino()
                return status_atual
        except Exception as e:
            status_atual = False
            logging.error(f"Erro ao validar conexao: {e}")
            return status_atual

    def recebeInfos(self):
        if self.conectado == True:
            while True:
                # Envie dados para o Arduino  # Leia dados do Arduino
                resposta = self.ser.readline().decode("utf-8")
                retorno = (
                    f"Recebido do Arduino: {resposta.strip()}"  # Aguarde um segundo
                )
                #time.sleep()
                print(retorno)
                #return retorno
        else:
            return "Arduino não Conectado"


#c = ConexaoArd()
#
#c.conectarArduino()
#
#ce = c.recebeInfos()
#while True:
#    print(time.strftime("%H:%M:%S ") + ce)
#st = c.ser.is_open
#
#print(st)