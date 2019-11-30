import socket
import binascii


class emissor():
  
  def __init__(self, ipRoteador, portaRoteador, ipOrigem, ipDestino, mensagem):
    self.ipRoteador = ipRoteador
    self.portaRoteador = portaRoteador
    self.ipOrigem = ipOrigem
    self.ipDestino = ipDestino
    self.mensagem = mensagem
    self.cabecalho = self.construirPacote()

  def encode (self, text):
    encoded = binascii.hexlify(bytes(text, "utf-8"))
    encoded = str(encoded).strip("b")
    encoded = encoded.strip("'")
    return encoded

  def construirPacote(self):
    cab = bytearray()
    msg_bytes = self.encode(self.mensagem)                        # Turn message into bytearray
    size = len(self.mensagem) + 24                                # Packet size 

    cab.append(0x00)                                        # Versao = 0, HL = 0, TOS = 00
    cab.append(0x00)

    if size < 256:
      cab.append(0x00)                                        # Get datagrama size
    cab.append(int(hex(size), 16))

    cab.append(0x00)                                 # ID = 0000, flags + offset = 0000
    cab.append(0x00)                                
    cab.append(0x00)                                 
    cab.append(0x00)                                 
    cab.append(0x05)                                      
    cab.append(0x00)                                         
    cab.append(0x00)                                         
    cab.append(0x00)                                         

    ip = self.ipOrigem.split('.')

    for i in ip:
      cab.append(int(i, 16))                                  # Get Ip de Origem

    ip = self.ipDestino.split('.')

    for i in ip:
      cab.append(int(i, 16))                                   # Get Ip de Origem

    cab.append(0x00)
    cab.append(0x00)
    cab.append(0x00)
    cab.append(0x00)

    for j in self.mensagem:
      char = ord(j)
      cab.append(int(hex(char), 16))                                     # Get message
    
    return cab

  def enviarMensagem(self):
    serverAddressPort = (self.ipRoteador, self.portaRoteador)
    bufferSize = 1024

    udpClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    udpClientSocket.sendto(self.cabecalho, serverAddressPort)
    msgFromServer = udpClientSocket.recvfrom(bufferSize)

    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)


emissor = emissor("127.0.0.1", 8080, "10.10.10.10", "5.5.5.5", "OLA")
emissor.enviarMensagem()
