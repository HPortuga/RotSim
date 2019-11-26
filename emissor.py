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