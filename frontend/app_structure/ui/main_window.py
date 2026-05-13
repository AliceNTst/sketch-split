import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app_structure.styles_manager import StylesManager
from app_structure.ui.button import *
from app_structure.ui.sketch_canvas import *
from app_structure.ui.gallery_references import Gallery
# from app_structure.data import images_sorting
# from app_structure.data.images_sorting import Coefficients
# from app_structure.data.reference_images import ReferenceImages
from app_structure.ui.filter import Filter
from app_structure.api.api_requests import *

class MainWindow:
    styles_manager: StylesManager = None

    def __init__(self, app, styles_manager: StylesManager):
        self.styles_manager = styles_manager
        self.request = local_request
        self.create_layout(app)
        

    def create_layout(self, app):
        self.custom_buttons = []

        paned = ttk.Panedwindow(app, orient=HORIZONTAL)
        paned.pack(fill=BOTH, expand=True)

        left = ttk.Frame(paned)
        right = ttk.Frame(paned)

        paned.add(left, weight=1)
        paned.add(right, weight=1)

        left.grid_rowconfigure(0, weight=0)
        left.grid_rowconfigure(1, weight=1)
        left.grid_rowconfigure(2, weight=0)
        left.grid_columnconfigure(0, weight=1)

        right.grid_rowconfigure(0, weight=0)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)


        #Left side
        tool_bar_left = ttk.Frame(master=left, bootstyle=PRIMARY)
        tool_bar_left.grid(row=0, column=0, sticky="ew")


        main_content_left = ttk.Panedwindow(left, orient=HORIZONTAL)
        main_content_left.grid(row=1, column=0, sticky="nsew")

        sketch_canvas = SketchCanvas(main_content_left)
        sketch_canvas.add_to_paned(main_content_left, weight=5)

        # filter_frame = ttk.Frame(main_content_left)
        # filter_label = ttk.Label(filter_frame, text="FILTER", bootstyle=PRIMARY)
        # filter_label.pack(side="top")
        # main_content_left.add(filter_frame, weight=1)
        # main_content_left.remove(filter_frame)
        # main_content_left.add(filter_frame, weight=1)

        filter_frame = Filter(main_content_left)



        openimage_button = SideButtonL(tool_bar_left, width=150, height=50, r=40, font_size = 10, text="Open Image", styles_manager=self.styles_manager, command=sketch_canvas.open_image)
        openimage_button.pack("left")
        self.custom_buttons.append(openimage_button)

        ttk.Label(tool_bar_left, text="Point:", bootstyle=SECONDARY, background="#624996").pack(side="left", padx=(40, 0))
        ttk.Combobox(
            tool_bar_left,
            textvariable=sketch_canvas.point_var,
            values=POINT_NAMES,
            state="readonly",
            width=15
        ).pack(side="left", padx = (0, 40))

        # apply_button = SideButtonR(tool_bar_left, width=140, height=40, r=30, font_size = 8, text="Export JSON", styles_manager=self.styles_manager, command=sketch_canvas.export_json)
        # apply_button.pack("left", padx=10)
        clear_point_button = PrimaryButton(tool_bar_left, width=140, height=40, r=30, font_size = 8, text="Clear Selected", styles_manager=self.styles_manager, command=sketch_canvas.clear_selected)
        clear_point_button.pack("left")
        self.custom_buttons.append(clear_point_button)
        clear_all_points_button = PrimaryButton(tool_bar_left, width=140, height=40, r=30, font_size = 8, text="Clear All", styles_manager=self.styles_manager, command=sketch_canvas.clear_all)
        clear_all_points_button.pack("left")
        self.custom_buttons.append(clear_all_points_button)


        # action = lambda: self.styles_manager.apply_theme("green")
        tool_bar_bottom = ttk.Frame(master=left, bootstyle=LIGHT)
        tool_bar_bottom.grid(row=2, column=0, sticky="ew")
        style_switcher = CircleButton(tool_bar_bottom, r=30, styles_manager=self.styles_manager, command=self.change_theme)
        style_switcher.pack("left")
        self.custom_buttons.append(style_switcher)
        

        # sketch_canvas.grid(row=1, column=0, sticky="nsew")


        #Right side
        tool_bar_right = ttk.Frame(right,padding=5)
        tool_bar_right.grid(row=0, column=0, sticky="ew")
        style = ttk.Style()

        style.configure(
            "Custom.TButton",
            foreground="#C5E64F",   # text color
            font=("Segoe UI", 10, "bold")
        )

        ttk.Button(tool_bar_right, text="filter", style="Custom.TButton", command=filter_frame.toggle).pack(side="left")

        action = lambda: self.styles_manager.apply_theme("green")
        ttk.Button(tool_bar_right, text="filter", style="Custom.TButton", command=action).pack(side="right")

        reload = lambda: gallery.reload_images()
        ttk.Button(tool_bar_right, text="reload", style="Custom.TButton", command=reload).pack(side="right")

        # sbutton = StylisedButton(tool_bar_right, width=200, height=50, r=40, text="base", command = lambda: print("Hi!"))
        # sbutton.pack("left")

        # sbutton = PrimaryButton(tool_bar_right, width=200, height=50, r=40, text="primary", command = lambda: print("Hi!"))
        # sbutton.pack("left")

        # sbutton = SecondaryButton(tool_bar_right, width=200, height=50, r=40, text="secondary", command = lambda: print("Hi!"))
        # sbutton.pack("left")

        # sbutton = SideButton(tool_bar_right, width=200, height=50, r=40, text="side", command = lambda: print("Hi!"))
        # sbutton.pack("left")

        # referenceImages = ReferenceImages(r"C:\Users\Ramen\Downloads\test")

        
        gallery = Gallery(master = right, request = self.request)

        apply_s = lambda : self.apply(canvas = sketch_canvas, gallery=gallery, filter=filter_frame)
        apply_button = SideButtonR(tool_bar_left, width=140, height=40, r=30, font_size = 8, text="APPLY", styles_manager=self.styles_manager, command=apply_s)
        apply_button.pack("right", padx=10)
        self.custom_buttons.append(apply_button)

        # main_content_left.remove(filter_frame)
        # main_content_left.update_idletasks()
        # print("--------------------------------------------------------------")
        # print(f"Frame-mapped: {filter_frame.winfo_ismapped()}")



    def apply(self, canvas, gallery : Gallery, filter):
        landmarks = canvas.get_landmarks()

        if numpy.array_equal(landmarks, None):
            return
        
        # sketch_data = ImageData(landmarks = landmarks)

        options = filter.get_options()
        # coefficients = self.get_coefficients(options)
        # print(coefficients)

        self.request.sort(options = options, path = "", landmarks=landmarks)
        # sorted_images = images_sorting.sort_images(sketch= sketch_data, images=referenceImages.images, coefficients=coefficients)
        # sorted_images_
        # sorted_paths = [image.path for image in sorted_images]
        # referenceImages.set_images(sorted_images, sorted_paths)
        gallery.reload_images()

    # def apply(self, canvas, referenceImages, gallery):
    #     landmarks = canvas.get_landmarks()

    #     if numpy.array_equal(landmarks, None):
    #         return
        
    #     sketch_data = ImageData(landmarks = landmarks)

    #     print("-----------ANGLES--------------")
    #     print(f'POINTS: {sketch_data.parts_angles}')
    #     print(f'CONNECTIONS: {sketch_data.connection_angles}')

    # def get_coefficients(self, options):
    #     main_option = options["main_option"]
    #     match main_option:
    #             case "DEFAULT":
    #                 return Coefficients.DEFAULT
    #             case "HANDS":
    #                 return Coefficients.HANDS
    #             case "LEGS":
    #                 return Coefficients.LEGS
    #             case "HEAVY":
    #                 return Coefficients.HEAVY
    #             case "CUSTOM":
    #                 options_dict = options["custom_options"]
    #                 coefficients = images_sorting.calculate_coefficitents(options_dict)
    #                 return coefficients
    #             case _:
    #                 print(f"STRANGE OPTION VARIANT: {self.option.get()}")
    #                 return None
            

    def change_theme(self):
        #TODO create Next theme
        self.styles_manager.apply_theme("green")
        for button in self.custom_buttons:
            button.update_colors()
