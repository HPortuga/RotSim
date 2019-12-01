import socket
import sys
import time

class roteador():
  def __init__(self, porta, tabRot):
    print("Instanciando roteador na porta %s\n" % porta)
    self.localIP = "127.0.0.1"
    self.bufferSize = 65335                           # Max packet size
    self.porta = porta
    self.tabRot = self.construirTabela(tabRot)                           # Pode ser uma lista de dicionarios construida na main a partir do txt. Os dicionarios possuem rede-destino/máscara/gateway/interface
    self.startServer()                                # usado para receber pacotes IP

  def construirTabela(self, tabRot):
    ret = []
    aux = tabRot.split()
    for e in aux:
      aux2 = e.split('/')
      for i in range(len(aux2)-1):
        aux2[i] = aux2[i].split(".")
        aux2[i] = [int (val) for val in aux2[i]]
        
      dic = {
        "destino": bytearray(aux2[0]),
        "mascara": bytearray(aux2[1]),
        "gateway": bytearray(aux2[2]),
        "porta": int(aux2[3])
      }
      
      ret.append(dic)

    return ret

  def startServer(self):

    while(True):
      updServerSocket = socket.socket(family=socket.AF_INET, type= socket.SOCK_DGRAM)
      updServerSocket.bind((self.localIP, self.porta))
      print("Servidor UDP escutando...")
      data = updServerSocket.recvfrom(self.bufferSize)
      print("conectado com {}".format(data[1]))
      self.processarPacote(bytearray(data[0]))
      updServerSocket.close()

  def processarPacote (self, data):
    pkg = list(data)
    ttl = pkg[8]

    if ttl == 0:
      return
      
    origem = pkg[12:16]
    destino = pkg[16:20]
    msg = pkg[24:]

    for i in range(len(msg)):
      msg[i] = chr(msg[i])

    msg = "".join(msg)

    maiorMask = 0
    index = -1
    index_def = -1
    flag = 0
    for e in range(len(self.tabRot)):

      if ((int.from_bytes(self.tabRot[e]["destino"], sys.byteorder ) & 
      int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder)) == 
      (int.from_bytes(bytes(pkg[16:20]), sys.byteorder) & 
      int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder))):

        if (int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder) != 0):
          if (self.tabRot[e]["gateway"] == bytearray([0, 0, 0, 0])):                      # I am the final destination
            print("destination reached. From %d.%d.%d.%d to %d.%d.%d.%d: %s" % (origem[0], origem[1]
            , origem[2], origem[3], destino[0], destino[1], destino[2], destino[3], msg))
            return
          
          if (maiorMask < int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder, signed=False)):      # I am the biggest current match
            maiorMask = int.from_bytes(self.tabRot[e]["mascara"], sys.byteorder, signed=False)
            index = e
        else:
          flag = 1
          index_def = e
    
    if ttl == 1:                         # Dropa pacote caso TTL tenha acabado
      print("Time to Live exceeded in Transit, dropping packet for ".join(destino))
      return
      
    data[8] = ttl - 1

    if (index == -1):                                                                   # Couldn't find compatible route

      if (flag == 1):
        print("SIJDAIOSJDSIODJASIODSJIO")
        # TODO: pegar rota default
        return

      print("destination %d.%d.%d.%d not found in routing table, dropping packet"
      % (destino[0], destino[1], destino[2], destino[3]))
      return 
    else:
      print("forwarding packet for %d.%d.%d.%d to next hop %d.%d.%d.%d over interface %d" 
      % (destino[0], destino[1], destino[2], destino[3],self.tabRot[index]["gateway"][0], 
      self.tabRot[index]["gateway"][1], self.tabRot[index]["gateway"][2],
      self.tabRot[index]["gateway"][3], self.tabRot[index]["porta"]))

      nextHopAddressPort = (self.localIP, self.tabRot[index]["porta"])
      udpClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
      udpClientSocket.sendto(data, nextHopAddressPort)

argumentos = sys.argv

argumento = ""
entradasDaTabela = argumentos[2:]

for entrada in entradasDaTabela:
  argumento += entrada + " "

argumento = argumento[:-1]
roteador = roteador(int(argumentos[1]), argumento)

# roteador = roteador(1111, "10.0.0.0/255.0.0.0/0.0.0.0/0 20.20.0.0/255.255.0.0/0.0.0.0/0 30.1.2.0/255.255.255.0/127.0.0.1/2222")

