import socket
import sys
import time

class roteador():
  def __init__(self, porta, tabRot):
    print("Instanciando roteador na porta %s\n" % porta)
    self.localIP = "127.0.0.1"
    self.bufferSize = 65335                           # Max packet size
    self.porta = porta
    self.tabRot = list()                              # Pode ser uma lista de dicionarios construida na main a partir do txt. Os dicionarios possuem rede-destino/máscara/gateway/interface
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
    destino = bytes(pkg[16:20])
    msg = pkg[24:]

    for i in range(len(msg)):
      msg[i] = chr(msg[i])

    msg = "".join(msg)
           
    if ttl == 1:                         # Dropa pacote caso TTL tenha acabado
      print("Time to Live exceeded in Transit, dropping packet for ".join(destino))
      return

    data[8] = ttl - 1

    line = [("destino", bytearray([65,65,65,65])), ("mascara", bytearray([255, 255, 255, 0])), ("gateway", bytearray([0,7,0,0]))]
    line = dict(line)
    self.tabRot.append(line)

    maiorMask = 0
    index = -1
    for e in range(len(self.tabRot)):

      if ((int.from_bytes(self.tabRot[e]["destino"], sys.byteorder ) & 
      int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder)) == 
      (int.from_bytes(destino, sys.byteorder) & 
      int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder))):

        if (self.tabRot[e]["gateway"] == bytearray([0, 0, 0, 0])):                      # I am the final destination
          # print("destination reached. From %s to  %s: %s", "".join(origem), "".join(pkg[16:20]), msg )
          print("DESTINO ALCANÇADO")
          return
        
        if (maiorMask < int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder)):      # I am the biggest current match
          maiorMask = int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder)
          index = e

    if (index == -1):                                                                   # Couldn't find compatible route
      print("destination not found")
    else:
      # TODO: Forward message
      print("MSG ENVIADA")

argumentos = sys.argv
roteador = roteador(int(argumentos[1]), argumentos[2])

