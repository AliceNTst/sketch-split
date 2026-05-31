import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app_structure.ui.button import *
from app_structure.ui.sketch_canvas import *




class Filter:
    BASIC_OPTIONS = ['DEFAULT', 'HANDS', 'LEGS', 'HEAVY', 'CUSTOM']

    CUSTOM_OPTIONS = ['hand_right', 'hand_left', 'leg_right', 'leg_left', 'shoulders', 'hips', 'torso' ]

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        #value = 'DEFAULT': default option checked from the beginning
        self.option = tk.StringVar(value = 'DEFAULT')
        
        filter_label = ttk.Label(self.frame, text="FILTER", bootstyle=PRIMARY)
        filter_label.pack(side="top", pady = (0, 17))

        custom_options_frame = ttk.Frame(self.frame)
        
        # on_click = lambda: print(self.option.get())
        on_click = lambda: self.__close_custom_options(custom_options_frame)
        for option in self.BASIC_OPTIONS:

            _option = ttk.Radiobutton(self.frame, text=option, bootstyle = SECONDARY, variable=self.option, value = option, command=on_click)

            if option == "CUSTOM":
                # com = lambda: print(self.get_options())
                custom_click = lambda: self.__open_custom_options(custom_options_frame)
                _option.config(command=custom_click)

            _option.pack(side = 'top', anchor='w', padx = 10, pady = 3)

        

        # custom_options_frame = ttk.Frame(self.frame)
        # self.__toggle_custom_options(custom_options_frame)

        self.custom_options = []
        for c_option_name in self.CUSTOM_OPTIONS:
            custom_option = CustomOption(custom_options_frame, text = c_option_name)
            self.custom_options.append(custom_option)

        
        # test_frame = ttk.Frame(self.frame)
        # test_frame.pack(side = "top")
        # test_opt = tk.StringVar()
        # ttk.Radiobutton(test_frame, text="TEST", bootstyle = PRIMARY, variable=test_opt, value = "TEST", command=on_click).pack(side = 'left')
        


    def get_options(self):
        """ Returns dictionary with options: example {"main_option" : "DEFAULT"} 
        Compare with Coefficients in images_sorting """
        match self.option.get():
                case "DEFAULT":
                    return {"main_option" : "DEFAULT"}
                case "HANDS":
                    return {"main_option" : "HANDS"}
                case "LEGS":
                    return {"main_option" : "LEGS"}
                case "HEAVY":
                    return {"main_option" : "HEAVY"}
                case "CUSTOM":
                    custom_options_dict = self.__get_custom_options_dictionary()
                    return {"main_option" : "CUSTOM",
                            "custom_options" : custom_options_dict}
                case _:
                    print(f"STRANGE OPTION VARIANT: {self.option.get()}")
                    return None
            
    def __get_custom_options_dictionary(self):
        dict = {}
        for c_option in self.custom_options:
            dict[c_option.get_name()] = c_option.get_value()
        
        return dict


    def add_to_paned(self, paned, weight=0):
        paned.add(self.frame, weight=weight)

    def remove_from_paned(self, paned):
        paned.remove(self.frame)

    def toggle(self):
        if self.frame.winfo_ismapped():
            self.remove_from_paned(self.master)

        else:
            self.add_to_paned(self.master, weight=1)

    def __toggle_custom_options(self, custom_options):
        if custom_options.winfo_ismapped():
            custom_options.pack_forget()

        else:
            custom_options.pack(side="top", anchor="w", pady=30)

    def __open_custom_options(self, custom_options):
        if not custom_options.winfo_ismapped():
            custom_options.pack(side="top",fill="x", anchor="w", pady=30, padx = (10, 0))

    def __close_custom_options(self, custom_options):
        if custom_options.winfo_ismapped():
            custom_options.pack_forget()




class CustomOption:
    #primary - important, secondary - less important, free - can be any
    OPTIONS = [
    "primary",
    "secondary",
    "free"
]

    def __init__(self, master, text):
        self.value = tk.StringVar(value=self.OPTIONS[2])
        self.master = master
        self.name = text

        self.frame = ttk.Frame(master)
        self.frame.pack(side='top', fill="x", pady = 2)

        ttk.Label(self.frame, text=text).pack(side="left", anchor="w", padx=(0, 3))
        ttk.Combobox(
            self.frame,
            textvariable=self.value,
            values=self.OPTIONS,
            state="readonly",
            width = 15
        ).pack(side="right", anchor="e")

        #TO get current value
        #self.point_var.get()

    def get_value(self):
        return self.value.get()
    
    def get_name(self):
        return self.name

