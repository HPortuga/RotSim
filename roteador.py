import socket

class roteador():
  def __init__(self, porta, tabRot, meuIp):
    self.localIP = meuIp.strip(".")
    self.bufferSize = 65335                           # Max packet size
    self.porta = porta
    self.tabRot = tabRot                              # Pode ser uma lista de dicionarios construida na main a partir do txt. Os dicionarios possuem rede-destino/máscara/gateway/interface
    self.startServer()                                # usado para receber pacotes IP

  def startServer(self):
    updServerSocket = socket.socket(family=socket.AF_INET, type= socket.SOCK_DGRAM)
    updServerSocket.bind(("127.0.0.1", self.porta))
    print("Servidor UDP escutando...")

    while(True):
      data = updServerSocket.recvfrom(self.bufferSize)
      self.processarPacote(bytearray(data[0]))

  def processarPacote (self, data):
    pkg = list(data)
    ttl = pkg[8]
    origem = pkg[12:16]
    destino = pkg[16:20]
    msg = pkg[24:]

    for i in range(len(msg)):
      msg[i] = chr(msg[i])

    msg = "".join(msg)
           
    if ttl == 1:                         # Dropa pacote caso TTL tenha acabado
      print("Time to Live exceeded in Transit, dropping packet for ".join(destino))
      return

    data[8] = ttl - 1

    for e in self.tabRot:
      e


    # TODO: Check the correct Route. Send packet if there is a route, or inform if the destination is not reachable

roteador = roteador(8080, "", "65.65.65.65")