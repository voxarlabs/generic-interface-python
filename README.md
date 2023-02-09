# Generic Interface Python

Esse projeto consiste no código para uma interface genérica que permite acessar câmeras IP ou USB, videos e imagens para compor demo das tecnologias do Voxar Labs construidas durante TGs, Mestrados e Doutorados.

A interface foi construida usando a biblioteca [Custom Tkinter](https://github.com/TomSchimansky/CustomTkinter), uma adaptação bonita do Tkinter. 

Importante que o usuário leia a seção de problemas conhecidos.

## Getting Started
1- Comece baixando este repositório no seu git manager favorito e coloque na pasta do seu projeto
```bash
git clone https://gitlab.cin.ufpe.br/Voxar-Labs/Tools/generic-interface-python.git
```

2- Instale as dependencias necessárias para o projeto funcionar bem usando o requirements.txt

```
pip install -r requirements.txt
```

3- Crie um arquivo main.py e siga o exemplo abaixo

```python
import sys
import os
import cv2
import argparse
import time



from generic_gui.gui import *
from InputHandler.input_handler import *


if __name__ == '__main__':
    

    # Create GUI instance
    gui = GUI()
    
    #Create a Model instance
    model = [] # crie aqui uma instancia para o seu modelo. Se tiver mais de um, crie cada um com uma variavel diferente e altere o construtor do InputHandler para recebê-los
    
    # Create CameraHandler instance
    input_handler = InputHandler(model,gui)

    # Set input handler into gui (start / stop / set new inputs)
    gui.set_input_handler(input_handler)

    # Start GUI
    gui.start()
```

4- Execute o arquivo main

## Sobre o módulo Generic GUI

## Sobre o módulo Input Handler

## Problemas Conhecidos
- A biblioteca Custom Tkinter funciona muito bem para aplicações no Windows e no Mac. Entretanto, em sistemas Linux based ela pode apresentar instabilidades devido ao motor gráfico que ela usa. Não espere bons resultados, não recomendamos o uso dela em sistemas Linux.

- A camera precisa ser desconectada antes do fechamento da aplicação. Caso contrario, é possivel que a camera fique em estado de ocupada.

- O frame da imagem deve sempre ser passado por referência. Cópias serão descartadas pelo Garbage Colector do Custom Tkinter.

## Authors and acknowledgment
- Zilde Neto Souto Maior [zsmn]
- Pedro Jorge Silva [pjls2]

