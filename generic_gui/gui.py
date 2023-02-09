import tkinter
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import customtkinter

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2) 

from InputHandler.input_handler import *

class GUI(customtkinter.CTk):
    # Params
    NAME = "[Telehealth] Prototype for Posture Analysis"
    WIDTH = 1600
    HEIGHT = 790

    def __init__(self):
        super().__init__()
        
        self.title(GUI.NAME)
        self.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}")
        self.minsize(GUI.WIDTH, GUI.HEIGHT)
        self.maxsize(GUI.WIDTH, GUI.HEIGHT)
        self.resizable(False, False)
        
        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def __create_camera_view(self):
        self.camera_view = customtkinter.CTkFrame(master=self,
                                                 width=1280,
                                                 corner_radius=0)
        # self.camera_view.set_scaling(1, 1, 1)
        self.camera_view.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

        self.camera_frame = customtkinter.CTkLabel(master=self.camera_view, text="Waiting for input")
        self.camera_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def __create_options_panel(self):
        ## Setup options panel at right
        self.options_panel = customtkinter.CTkFrame(master=self,
                                                 height=GUI.HEIGHT,
                                                 corner_radius=0)
        # self.options_panel.set_scaling(1, 1, 1)

        self.options_panel.grid(row=0, column=1, padx=5, pady=5, sticky="nswe")
        
        self.options_panel.rowconfigure((0,1,3,5,6,8), weight=0)
        self.options_panel.rowconfigure((2,4,7,9,11), minsize=10)

        self.options_panel.columnconfigure((0, 1), weight=1)
        
    def __create_camera_selection(self):
        # Create camera selection in options panel
        self.camera_id_text = customtkinter.CTkEntry(master=self.options_panel,
                                                    placeholder_text="ID / Path")
                                                    
        self.camera_id_text.grid(row=0, column=0, padx=5, pady=5, sticky="nwe")

        self.file_finder = customtkinter.CTkButton(master=self.options_panel, width=16, command=self.select_file, text="...",
                                                corner_radius=6)
        self.file_finder.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.camera_id_button = customtkinter.CTkButton(master=self.options_panel, width=30, command=self.setup_camera, text="Connect",
                                                corner_radius=6)
        self.camera_id_button.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="nwe")

        self.camera_record_button = customtkinter.CTkButton(master=self.options_panel, command=self.start_recording, text="Start Recording", corner_radius=6)
        self.camera_record_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nwe")

    def __create_mask_switch(self):
        self.mask_options = customtkinter.CTkLabel(master=self.options_panel, text="Mask Options", font=("Roboto Medium", -16))
        self.mask_options.grid(row=3, column=0, columnspan=2, padx=5, sticky="nwe")

        self.mask_enable = customtkinter.CTkLabel(master=self.options_panel, text="Enable Mask")
        self.mask_enable.grid(row=5, column=0, padx=5, sticky="nwe")

        self.mask_switch = customtkinter.CTkSwitch(master=self.options_panel, text='')
        self.mask_switch.grid(row=5, column=1, padx=5, pady=5, sticky="nwe")

        self.mask_opacity = customtkinter.CTkLabel(master=self.options_panel, text="Mask Opacity")
        self.mask_opacity.grid(row=6, column=0, padx=5, sticky="nwe")

        self.mask_slider = customtkinter.CTkSlider(master=self.options_panel)
        self.mask_slider.grid(row=6, column=1, padx=5, pady=5, sticky="nwe")

    # def __create_joints_menu(self):
    #     self.joints_menu = customtkinter.CTkLabel(master=self.options_panel, text="Joints Menu", font=("Roboto Medium", -16))
    #     self.joints_menu.grid(row=8, column=0, columnspan=2, padx=5, sticky="nwe")

    #     self.joint_var = tkinter.StringVar(value="left")

    #     self.joint_left = customtkinter.CTkRadioButton(master=self.options_panel, variable=self.joint_var, text="Left", value="left")
    #     self.joint_left.grid(row=10, column=0, columnspan=2, padx=30, sticky="w")
        
    #     self.joint_right = customtkinter.CTkRadioButton(master=self.options_panel, variable=self.joint_var, text="Right", value="right")
    #     self.joint_right.grid(row=10, column=1, padx=30, sticky="e")

    #     self.joint_left.select()
        
    #     self.joints = {}
    #     for j in AngleExtractor.joints_set_dict:
    #         self.joints[j.split('_', 1)[1]] = {'checkbox': None, 'angle_value': None}

    #     monitor_related_calls = ['Distance Head to Monitor', 'Height Eye to Monitor']
    #     for j in monitor_related_calls:
    #         self.joints[j] = {'checkbox': None, 'angle_value': None}

    #     at_row = 12
    #     for j in self.joints.keys():
    #         joint = customtkinter.CTkCheckBox(master=self.options_panel, text=j, width=16, height=16)
    #         joint.grid(row=at_row, column=0, columnspan=2, padx=5, pady=5, sticky="nwe")

    #         angle_label = customtkinter.CTkLabel(master=self.options_panel, text='0.00', width=60, height=16, corner_radius=6, fg_color=("white", "gray38"), justify=tkinter.CENTER) 
    #         angle_label.grid(row=at_row, column=1, padx=5, pady=5, sticky="ne")

    #         self.joints[j] = {'checkbox': joint, 'angle_value': angle_label}

    #         at_row += 1

    def __create_debug_menu(self):
        self.debug_menu = customtkinter.CTkLabel(master=self.options_panel, text="Debug Menu", font=("Roboto Medium", -16))
        self.debug_menu.grid(row=19, column=0, columnspan=2, padx=5, sticky="nwe")

        self.debugs = ["head_to_monitor"]
        self.debug_checks = {}

        at_row = 21
        for d in self.debugs:
            debug = customtkinter.CTkCheckBox(master=self.options_panel, text=d, width=16, height=16)
            debug.grid(row=at_row, column=0, columnspan=2, padx=5, pady=5, sticky="nwe")

            self.debug_checks[d] = debug
            at_row += 1

    def is_debug_enabled(self, debug_name):
        if not debug_name in self.debugs:
            raise Exception("Invalid debug name.")

        return self.debug_checks[debug_name].get()

    def get_mask_opacity(self):
        return self.mask_slider.get()

    def is_mask_enabled(self):
        return self.mask_switch.get()

    def start_recording(self):
        if(not self.input_handler.is_stopped):
            self.input_handler.start_recording()
            self.camera_record_button.configure(text="Stop Recording", fg_color="#d0003e", hover_color="#f06463", command=self.stop_recording) 
        else:
            showinfo("Error", "You can't start a recording without input running.")

    def stop_recording(self):
        self.input_handler.stop_recording()
        self.camera_record_button.configure(text="Start Recording", fg_color="#1f6aa4", hover_color="#1f69a5", command=self.start_recording)

    def set_input_handler(self, input_handler):
        self.input_handler = input_handler

    def get_checked_direction(self):
        return self.joint_var.get()

    def get_jointsets_status(self):
        jointsets_status = {}
        for j in self.joints.keys():
            jointsets_status[self.joint_var.get() + "_" + self.joints[j]['checkbox'].text] = self.joints[j]['checkbox'].get()
        
        return jointsets_status

    def get_jointset_value(self, jointset_name):
        if not jointset_name in self.joints.keys():
            raise Exception("Invalid jointset name.")

        return float(self.joints[jointset_name]['angle_value'].text)

    def set_jointset_value(self, jointset_name, value):
        if not jointset_name in self.joints.keys():
            raise Exception("Invalid jointset name.")

        self.joints[jointset_name]['angle_value'].configure(text=str(value))

    def setup_camera(self):
        started = self.input_handler.start(self.camera_id_text.get())
        if started: 
            self.camera_id_button.configure(text="Disconnect", fg_color="#d0003e", hover_color="#f06463", command=self.disconnect_camera) 
        else:
            showinfo("Error", "Failed to open the id/file '" + self.camera_id_text.get() + "'")

    def disconnect_camera(self):
        self.input_handler.stop()
        self.stop_recording()
        self.camera_id_button.configure(text="Connect", fg_color="#1f6aa4", hover_color="#1f69a5", command=self.setup_camera)

    def select_file(self):
        filetypes = (
            ('Video Files', ('*.mp4', '*.avi')),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        self.camera_id_text.delete(0, customtkinter.END)
        self.camera_id_text.insert(0, filename)

    def on_closing(self, event=0):
        self.input_handler.stop()
        self.destroy()

    def start(self):
        self.__create_camera_view()
        self.__create_options_panel()
        self.__create_camera_selection()
        self.__create_mask_switch()
        # self.__create_joints_menu()
        self.__create_debug_menu()

        self.mainloop()
