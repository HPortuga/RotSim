import socket
import binascii
import sys


class emissor():
  
  def __init__(self, ipRoteador, portaRoteador, ipOrigem, ipDestino):
    self.ipRoteador = ipRoteador
    self.portaRoteador = portaRoteador
    self.ipOrigem = ipOrigem
    self.ipDestino = ipDestino
    self.mensagem = "Bom dia"
    self.pacote = self.construirPacote()
    self.enviarMensagem()
    
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
      pkg.append(int(i, 10))                                # Get Ip de Origem

    ip = self.ipDestino.split('.')

    for i in ip:
      pkg.append(int(i, 10))                                # Get Ip de Origem

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
    return

argumentos = sys.argv
emissor = emissor(argumentos[1], int(argumentos[2]), argumentos[3], argumentos[4])

# emissor = emissor("127.0.0.1", 1111, "1.1.1.1", "10.0.0.5")
