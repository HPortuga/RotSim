import os
from subprocess import call
from subprocess import Popen

RUNROT = "gnome-terminal -e python3 roteador.py "
RUNEMI = "gnome-terminal -x python3 emissor.py "

if __name__ == "__main__":
	roteadores = list()
	emissores = list()

	with open("testes.txt", "r") as file:
		lines = file.readlines()

	for line in lines:
		if (line[0] == "#" or line[0] == "\n" or line[0] == ' '):
			continue

		if (line[-1] == "\n"):
			line = line[:-1]

		dados = line.split(' ')

		if (dados[0] == "./roteador"):
			tabelaRoteamento = dados[2:]
			roteadores.append({
				"porta": dados[1],
				"tabela": tabelaRoteamento
			})

		elif (dados[0] == "./emissor"):
			emissores.append({
				"ip roteador": dados[1],
				"porta roteador": dados[2],
				"ip origem": dados[3],
				"ip destino": dados[4]
			})

	for roteador in roteadores:
		tabela = roteador["tabela"]
		argTabela = ""

		for line in tabela:
			argTabela = line + " "

		argTabela = argTabela[:-1]

		porta = roteador["porta"]
		call(['gnome-terminal', '-e', "python3 /home/Faculdade/Redes/T2/RotSim/roteador.py"])
		# Popen(["python3", "roteador.py"], shell=False)
		# Popen(["gnome-terminal", "python3", "roteador.py", roteador["porta"], argTabela])
	
	# Popen(["python3", "roteador.py"]) 
	# Popen(["python3", "emissor.py"]) 

	
	# call(['gnome-terminal', '-x', '-e', "python3 /home/Faculdade/Redes/T2/RotSim/roteador.py"])
	# Instanciar roteadores
	# for roteador in roteadores:
	# 	tabela = roteador["tabela"]
	# 	commandLineArgs = RUNROT + roteador["porta"]

	# 	for line in tabela:
	# 		commandLineArgs = commandLineArgs + " " + line

	# 	os.system(commandLineArgs)

	# Abre uma janela para cada processo
	# os.system("gnome-terminal -x python3 roteador.py")
	# os.system("gnome-terminal -x python3 emissor.py")