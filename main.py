import os

if __name__ == "__main__":

	# Abre uma janela para cada processo
	os.system("gnome-terminal -x python3 roteador.py")
	os.system("gnome-terminal -x python3 emissor.py")