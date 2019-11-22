class emissor():
  def __init__(self, ipRoteador, portaRoteador, ipOrigem, ipDestino, mensagem):
    self.ipRoteador = ipRoteador
    self.portaRoteador = portaRoteador
    self.ipOrigem = ipOrigem
    self.ipDestino = ipDestino
    self.mensagem = mensagem

    self.cabecalho = self.construirCabecalho()

  def constrirCabecalho(self):
    return dict()