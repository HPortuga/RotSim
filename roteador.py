import socket

class roteador():
  def __init__(self, porta, tabRot):
    self.localIP = "127.0.0.1"
    self.bufferSize = 1024
    self.porta = porta
    self.tabRot = tabRot                              # Pode ser uma lista de dicionarios construida na main a partir do txt. Os dicionarios possuem rede-destino/máscara/gateway/interface
    self.cabecalho = {}       
    self.startServer()                        # usado para receber pacotes IP

  def startServer(self):
    msgFromServer = "Hello Client"
    bytesToSend = str.encode(msgFromServer)

    updServerSocket = socket.socket(family=socket.AF_INET, type= socket.SOCK_DGRAM)
    updServerSocket.bind((self.localIP, self.porta))
    print("Servidor UDP escutando...")

    while(True):
      data = updServerSocket.recvfrom(self.bufferSize)
      message = data[0]
      address = data[1]

      clientMsg = "Mensagem do cliente: {}".format(message)
      clientIP = "IP do cliente: {}".format(address)

      print(clientMsg)
      print(clientIP)

      updServerSocket.sendto(bytesToSend, address)

  def processarPacote (self, cabecalho):
    
    if cabecalho["TTL"] == 1:                         # Dropa pacote caso TTL tenha acabado
      print("Time to Live exceeded in Transit, dropping packet for" + cabecalho["destino"])
      return

    cabecalho["TTL"] -= 1

    # TODO: Check the correct Route. Send packet if there is a route, or inform if the destination is not reachable

roteador = roteador(8080, "")