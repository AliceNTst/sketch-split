import numpy
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app_structure.styles_manager import StylesManager
from app_structure.ui.button import *
from app_structure.ui.sketch_canvas import *
from app_structure.ui.gallery_references import Gallery
from app_structure.ui.filter import Filter
from app_structure.api.api_requests import *
from tkinter import font

class MainWindow:
    styles_manager: StylesManager = None

    def __init__(self, app, styles_manager: StylesManager):
        self.styles_manager = styles_manager
        self.request = local_request
        self.create_layout(app)

        #TODO adjust font
        # Get Tk's default font object
        # default_font = font.nametofont("TkDefaultFont")

        # # Modify it in place  "Segoe UI"
        # default_font.configure(family="Nunito")
        

    def create_layout(self, app):
        self.custom_buttons = []
        self.tool_bar_left_labels = []
        self.widgets_to_update = []

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


        main_content_left = ttk.Panedwindow(left, orient=HORIZONTAL, bootstyle=LIGHT)
        main_content_left.grid(row=1, column=0, sticky="nsew")

        sketch_canvas = SketchCanvas(main_content_left, styles_manager=self.styles_manager)
        sketch_canvas.add_to_paned(main_content_left, weight=5)
        self.widgets_to_update.append(sketch_canvas)

        filter_frame = Filter(main_content_left)



        openimage_button = SideButtonL(tool_bar_left, width=165, height=50, r=40, font_size = 10, text="Open Image", styles_manager=self.styles_manager, command=sketch_canvas.open_image)
        openimage_button.pack("left")
        self.custom_buttons.append(openimage_button)

        point_label = ttk.Label(tool_bar_left, text="Point:", bootstyle=SECONDARY, background=self.styles_manager.get_primary())
        point_label.pack(side="left", padx=(60, 0))
        self.tool_bar_left_labels.append(point_label)
        ttk.Combobox(
            tool_bar_left,
            textvariable=sketch_canvas.point_var,
            values=POINT_NAMES,
            state="readonly",
            width=15
        ).pack(side="left", padx = (0, 20))

       
        clear_point_button = PrimaryButton(tool_bar_left, width=120, height=40, r=30, font_size = 8, text="Clear Selected", styles_manager=self.styles_manager, command=sketch_canvas.clear_selected)
        clear_point_button.pack(side="left", padx=(0, 5), anchor="n")
        self.custom_buttons.append(clear_point_button)
        clear_all_points_button = PrimaryButton(tool_bar_left, width=120, height=40, r=30, font_size = 8, text="Clear All", styles_manager=self.styles_manager, command=sketch_canvas.clear_all)
        clear_all_points_button.pack(side="left", padx=(5, 0), anchor="n")
        self.custom_buttons.append(clear_all_points_button)


        #Right side
        tool_bar_right = ttk.Frame(right)
        tool_bar_right.grid(row=0, column=0, sticky="ew")

        # style = ttk.Style()
        # style.configure(
        #     "Custom.TButton",
        #     foreground="#C5E64F",   # text color
        #     font=("Segoe UI", 10, "bold")
        # )

        # ttk.Button(tool_bar_right, text="filter", style="Custom.TButton", command=filter_frame.toggle).pack(side="left")

        filter_button = SecondarySideButtonL(tool_bar_right, width=100, height=50, r=40, font_size = 10, text="filter", styles_manager=self.styles_manager, command=filter_frame.toggle)
        filter_button.pack("left")
        self.custom_buttons.append(filter_button)

        # action = lambda: self.styles_manager.apply_theme("green")
        # ttk.Button(tool_bar_right, text="filter", style="Custom.TButton", command=action).pack(side="right")


        # reload = lambda: gallery.reload_images()
        # ttk.Button(tool_bar_right, text="reload", style="Custom.TButton", command=reload).pack(side="right")

        reload = lambda: gallery.reload_images()
        reload_gallery_button = SecondaryButton(tool_bar_right, width=70, height=30, r=30, font_size = 8, text="reload", styles_manager=self.styles_manager, command=reload)
        reload_gallery_button.pack("right")
        self.custom_buttons.append(reload_gallery_button)

       

        
        gallery = Gallery(master = right, request = self.request)

        apply_s = lambda : self.apply(canvas = sketch_canvas, gallery=gallery, filter=filter_frame)
        apply_button = SideButtonR(tool_bar_left, width=140, height=50, r=30, font_size = 8, text="APPLY", styles_manager=self.styles_manager, command=apply_s)
        apply_button.pack("right")
        self.custom_buttons.append(apply_button)

        _add_to_gallery = lambda: self._add_sketch_to_gallery(sketch_canvas)
        add_sketch_to_gallery = SecondaryButton(tool_bar_left, width=120, height=30, r=30, font_size = 8, text="add to Gallery", bg_style="primary", styles_manager=self.styles_manager, command=_add_to_gallery)
        add_sketch_to_gallery.pack(side="right", padx = (0, 10))
        self.custom_buttons.append(add_sketch_to_gallery)



        tool_bar_bottom = ttk.Frame(master=left, bootstyle=LIGHT)
        tool_bar_bottom.grid(row=2, column=0, sticky="ew")
        style_switcher = CircleButton(tool_bar_bottom, r=30, styles_manager=self.styles_manager, command=self.change_theme)
        style_switcher.pack("left", padx = (5, 5), pady = (5, 5))
        self.custom_buttons.append(style_switcher)
        
        _switch_point_color = lambda: self.switch_point_color(canvas=sketch_canvas, label=points_color_switcher_label)
        points_color_switcher = CircleButton(tool_bar_bottom, r=30, styles_manager=self.styles_manager, command=_switch_point_color)
        points_color_switcher.pack("left", padx = (5, 5), pady = (5, 5))
        self.custom_buttons.append(points_color_switcher)
        points_color_switcher_label = ttk.Label(tool_bar_bottom, text="point", bootstyle=SECONDARY, background=self.styles_manager.get_light())
        points_color_switcher_label.pack(side="left")

        _switch_text_color = lambda: self.switch_text_color(canvas=sketch_canvas, label=text_color_switcher_label)
        text_color_switcher = CircleButton(tool_bar_bottom, r=30, styles_manager=self.styles_manager, command=_switch_text_color)
        text_color_switcher.pack("left", padx = (5, 5), pady = (5, 5))
        self.custom_buttons.append(text_color_switcher)
        text_color_switcher_label = ttk.Label(tool_bar_bottom, text="point name", bootstyle=SECONDARY, background=self.styles_manager.get_light())
        text_color_switcher_label.pack(side="left")



        action_toggle_blur = lambda: self.toggle_blur(sketch_canvas=sketch_canvas, style_switcher_button=style_switcher)
        blur_button = PrimaryButton(tool_bar_bottom, width=140, height=50, r=30, font_size = 8, text="BLUR", bg_style="light", styles_manager=self.styles_manager, command=action_toggle_blur)
        blur_button.pack("right", padx = (5, 5), pady = (5, 5))
        self.custom_buttons.append(blur_button)


       
    def toggle_blur(self, sketch_canvas, style_switcher_button):
        if sketch_canvas.image:
            sketch_canvas.toggle_blur()
            if style_switcher_button.get_text() == "UNBLUR":
                style_switcher_button.change_text_to(text="BLUR")
            elif style_switcher_button.get_text() == "BLUR":
                style_switcher_button.change_text_to(text="UNBLUR")


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

    

    def change_theme(self):
        #TODO create Next theme
        # self.styles_manager.apply_theme("green")
        self.styles_manager.next_theme()
        for button in self.custom_buttons:
            button.update_colors()

        for label in self.tool_bar_left_labels:
            print("Changing Label")
            label.configure(background=self.styles_manager.get_primary())

        for widget in self.widgets_to_update:
            widget.update_colors()


    def switch_point_color(self, canvas, label):
        current_index = canvas.point_color_index
        if current_index == len(self.styles_manager.get_points_color()) - 1:
            new_index = 0
        else:
            new_index = current_index + 1

        canvas.set_point_color_index(new_index)
        label.config(bootstyle=self.styles_manager.get_text_bootstyles()[new_index])
        canvas.on_resize()


    def switch_text_color(self, canvas, label):

        current_index = canvas.text_color_index
        if current_index == len(self.styles_manager.get_points_color()) - 1:
            new_index = 0
        else:
            new_index = current_index + 1

        canvas.set_text_color_index(new_index)
        label.config(bootstyle=self.styles_manager.get_text_bootstyles()[new_index])
        canvas.on_resize()

    def _add_sketch_to_gallery(self, canvas):
        landmarks = canvas.get_landmarks()

        if numpy.array_equal(landmarks, None):
            return
        
        path = canvas.image_path

        print(f"Send request to add sketch: {path} {landmarks} to database")
        self.request.add_sketch_to_gallery(path = path, landmarks=landmarks)
        
