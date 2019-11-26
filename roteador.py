class roteador():
  
  def __init__(self, porta, tabRot):
    self.porta = porta
    self.tabRot = tabRot                              # Pode ser uma lista de dicionarios construida na main a partir do txt. Os dicionarios possuem rede-destino/máscara/gateway/interface
    self.cabecalho = {}                               # usado para receber pacotes IP

  def processarPacote (self, cabecalho):
    
    if cabecalho["TTL"] == 1:                         # Dropa pacote caso TTL tenha acabado
      print("Time to Live exceeded in Transit, dropping packet for" + cabecalho["destino"])
      return

    cabecalho["TTL"] -= 1

    # TODO: Check the correct Route. Send packge if there is a route, or inform if the destination is not reachable