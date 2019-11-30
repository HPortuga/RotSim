import socket

class emissor():
  
  def __init__(self, ipRoteador, portaRoteador, ipOrigem, ipDestino, mensagem):
    self.ipRoteador = ipRoteador
    self.portaRoteador = portaRoteador
    self.ipOrigem = ipOrigem
    self.ipDestino = ipDestino
    self.mensagem = mensagem
    self.cabecalho = self.construirCabecalho()

  def construirCabecalho(self):
    cab = {}
    cab["versao"] = ""
    cab["IHL"] = ""
    cab["TOS"] = ""
    cab["tamTotal"] = ""
    cab["ID"] = ""
    cab["flag"] = ""
    cab["offset"] = ""
    cab["TTL"] = 5
    cab["protocolo"] = "Ipv4"
    cab["checkSum"] = ""
    cab["origem"] = self.ipOrigem
    cab["destino"] = self.ipDestino
    cab["opcoes"] = ""
    cab["dados"] = self.mensagem
    return cab

  def enviarMensagem(self):
    msgFromClient = "Hello UDP server"
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = (self.ipRoteador, self.portaRoteador)
    bufferSize = 1024

    udpClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    udpClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = udpClientSocket.recvfrom(bufferSize)

    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)


emissor = emissor("127.0.0.1", 8080, "", "", "")
emissor.enviarMensagem()