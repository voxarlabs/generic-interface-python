import cv2

from threading import Thread
from datetime import datetime
from PIL import Image, ImageTk


# from miscs.utils import *
# from miscs.skeleton import *

class InputHandler():
    # def __init__(self, angle_extractor, pose_estimator, mask, gui):
    def __init__(self, model, gui):
        self.cap = None
        self.writer = None
        self.is_stopped = True
        self.is_recording = False
        self.input_is_camera = False
        self.last_frame_view = None

        # Setup modules
        self.model = model
        
        self.gui = gui

    def start_recording(self):
        # Get actual timestamp to set file name
        out = str(datetime.now()).replace(' ', '_').replace('.', '').replace(':', '_') + '.avi'

        # Instantiate writer
        codec = cv2.VideoWriter_fourcc(*'MJPG')
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = self.cap.get(cv2.CAP_PROP_FPS) if not self.input_is_camera else 5
        self.writer = cv2.VideoWriter(out, codec, fps, size)

        # Set as is recording
        self.is_recording = True

    def stop_recording(self):
        self.is_recording = False
        if self.writer is not None:
            self.writer.release()
            self.writer = None

    def start(self, inp):
        if(inp.isdigit()):
            self.input_is_camera = True
            self.cap = cv2.VideoCapture(int(inp))
        else:
            self.input_is_camera = False
            self.cap = cv2.VideoCapture(inp)

        if (not (self.cap is None or not self.cap.isOpened())):
            self.is_stopped = False
            Thread(target=self.get, args=()).start()
            return self
        else:
            return None

    def process_frame(self, frame):
        # sempre usar o ponteiro de frame para fazer modificações.
        # qualquer operação do tipo frame = op_modifica_frame(frame) dá erro na gestao de memoria do tkinter
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def convert_tkinter_view(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = ImageTk.PhotoImage(Image.fromarray(frame))
        
        self.last_frame_view = frame_pil

        return frame_pil

    def get(self):
        while not self.is_stopped:
            ret, frame = self.cap.read()

            if not ret:
                break

            self.process_frame(frame)

            # If is recording, write processed frame to output
            if(self.is_recording and self.writer.isOpened()):
                self.writer.write(frame)

            # Resize frame to fit view window
            view_size = (self.gui.camera_view.winfo_width(), self.gui.camera_view.winfo_height())
            frame = cv2.resize(frame, view_size)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = ImageTk.PhotoImage(Image.fromarray(frame))
            self.gui.camera_frame.configure(text='', image=frame_pil)
            self.last_frame_view = frame_pil
            
        self.gui.disconnect_camera()
        self.gui.camera_frame.configure(text='Waiting for input', image='')
        self.cap.release()
        self.cap = None

    def stop(self):
        self.is_stopped = True
