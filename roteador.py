import socket

class roteador():
  def __init__(self, porta, tabRot):
    self.localIP = "127.0.0.1"
    self.bufferSize = 65335                           # Max packet size
    self.porta = porta
    self.tabRot = tabRot                              # Pode ser uma lista de dicionarios construida na main a partir do txt. Os dicionarios possuem rede-destino/máscara/gateway/interface
    self.startServer()                                # usado para receber pacotes IP

  def startServer(self):
    updServerSocket = socket.socket(family=socket.AF_INET, type= socket.SOCK_DGRAM)
    updServerSocket.bind((self.localIP, self.porta))
    print("Servidor UDP escutando...")

    while(True):
      data = updServerSocket.recvfrom(self.bufferSize)
      pkg = list(data[0])
      address = data[1]
      ttl = pkg[8]
      origem = pkg[12:16]
      destino = pkg[16:20]
      msg = "".join(pkg[24:])

  def processarPacote (self, cabecalho):
    
    if cabecalho["TTL"] == 1:                         # Dropa pacote caso TTL tenha acabado
      print("Time to Live exceeded in Transit, dropping packet for" + cabecalho["destino"])
      return

    cabecalho["TTL"] -= 1

    # TODO: Check the correct Route. Send packet if there is a route, or inform if the destination is not reachable

roteador = roteador(8080, "")