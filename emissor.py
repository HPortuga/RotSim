import socket
import binascii


class emissor():
  
  def __init__(self, ipRoteador, portaRoteador, ipOrigem, ipDestino, mensagem):
    self.ipRoteador = ipRoteador
    self.portaRoteador = portaRoteador
    self.ipOrigem = ipOrigem
    self.ipDestino = ipDestino
    self.mensagem = mensagem
    self.pacote = self.construirPacote()

  def encode (self, text):
    encoded = binascii.hexlify(bytes(text, "utf-8"))
    encoded = str(encoded).strip("b")
    encoded = encoded.strip("'")
    return encoded

  def construirPacote(self):
    pkg = bytearray()
    size = len(self.mensagem) + 24                          # Packet size 

    pkg.append(0x00)                                        # Versao = 0, HL = 0, TOS = 00
    pkg.append(0x00)

    if size < 256:
      pkg.append(0x00)                                      # Get datagrama size
    pkg.append(int(hex(size), 16))

    pkg.append(0x00)                                 
    pkg.append(0x00)                                
    pkg.append(0x00)                                        # ID = 0000, flags + offset = 0000   
    pkg.append(0x00)                                 
    pkg.append(0x05)                                        # TTL = 5                                       
    pkg.append(0x00)                                         
    pkg.append(0x00)                                        # Protocolo = 00, checksum = 0000
    pkg.append(0x00)                                         

    ip = self.ipOrigem.split('.')

    for i in ip:
      pkg.append(int(i, 16))                                # Get Ip de Origem

    ip = self.ipDestino.split('.')

    for i in ip:
      pkg.append(int(i, 16))                                # Get Ip de Origem

    pkg.append(0x00)
    pkg.append(0x00)
    pkg.append(0x00)
    pkg.append(0x00)

    for j in self.mensagem:
      char = ord(j)
      pkg.append(int(hex(char), 16))                        # Get message
    
    return pkg

  def enviarMensagem(self):
    serverAddressPort = (self.ipRoteador, self.portaRoteador)
    bufferSize = 1024

    udpClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    udpClientSocket.sendto(self.pacote, serverAddressPort)


emissor = emissor("127.0.0.1", 8080, "10.10.10.10", "5.5.5.5", "OLA")
emissor.enviarMensagem()
