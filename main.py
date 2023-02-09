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
    
    # Create CameraHandler instance
    input_handler = InputHandler(gui)

    # Set input handler into gui (start / stop / set new inputs)
    gui.set_input_handler(input_handler)

    # Start GUI
    gui.start()

