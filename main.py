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

