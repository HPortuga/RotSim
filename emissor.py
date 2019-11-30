class emissor():
  
  def __init__(self, ipRoteador, portaRoteador, ipOrigem, ipDestino, mensagem):
    self.ipRoteador = ipRoteador
    self.portaRoteador = portaRoteador
    self.ipOrigem = ipOrigem
    self.ipDestino = ipDestino
    self.mensagem = mensagem
    self.cabecalho = self.construirCabecalho()

  def construirCabecalho(self):
    cab = bytearray()
    msg_bytes = self.mensagem.encode()                        # Turn message into bytearray
    size = len(msg_bytes) + 24                                # Packet size 

    cab.append(0x0000)                                        # Versao = 0, HL = 0, TOS = 00

    if size < 16:
      cab.append(0x000)
    elif size < 256:
      cab.append(0x00)                                        # Get datagrama size
    elif size < 4096:
      cab.append(0x0)
    cab.append(hex(size))

    cab.append(0x00000000)                                    # ID = 00, flags + offset = 00
    cab.append(0x5)                                           # TTL = 5
    cab.append(0x000)                                         # Protocolo = 0, checksum = 00

    ip = self.ipOrigem.split('.')

    for i in ip:
      if i < 16:
        cab.append(0x0)
      cab.append(hex(i))                                    # Get Ip de Origem

    ip = self.ipDestino.split('.')

    for i in ip:
      if i < 16:
        cab.append(0x0)
      cab.append(hex(i))                                    # Get Ip de Destino

    cab.append(0x00000000)                                  # Options = 00000000

    cab.append(msg_bytes)                                   # Get message
    
    return cab

    