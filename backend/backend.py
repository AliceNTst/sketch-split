from fastapi import FastAPI
from database_connection import Database
from data.reference_images import ReferenceImages
from data import images_sorting
from data.image_data import ImageData

from pydantic import BaseModel


# class CustomOption:
#     #primary - important, secondary - less important, free - can be any
#     OPTIONS = [
#     "primary",
#     "secondary",
#     "free"
# ]
class Options(BaseModel):
    main_option: str
    custom_options: dict = {}

class Sketch(BaseModel):
    path: str = ""
    landmarks: list
    

app = FastAPI()
database = Database()
reference_images = ReferenceImages(database)

@app.get("/images")
def get_images():
    # images = database.fetch_images()
    return reference_images.images_paths

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/images/sort")
def sort_images(options: Options):
    """options examples: {"main_option" : "CUSTOM", "custom_options" : custom_options_dict}
    {"main_option" : "DEFAULT"}"""

    # images_sorting.calculate_coefficitents
    options_dir = {"main_option" : options.main_option, "custom_options" : options.custom_options}
    print(options_dir)

    sketch = database.fetch_sketch()
    images = reference_images.images
    coefficients = images_sorting.get_coefficients(options = options_dir)
    print(coefficients)

    sorted_images = images_sorting.sort_images(sketch= sketch, images=images, coefficients=coefficients)
    sorted_paths = [image.path for image in sorted_images]
    reference_images.set_images(sorted_images, sorted_paths)
    reference_images.reset_loaded_images()

    print(sorted_paths[0 : 10])



@app.get("/images/next")
def next_images(number: int):
    return reference_images.next(number)

@app.get("/images/reload")
def reload_images():
    if reference_images.images_loaded == 0:
        return reference_images.next()
    else:
        return reference_images.get_loaded_images()

@app.get("/images/loaded")
def get_loaded_images():
    return reference_images.get_loaded_images()

@app.get("/images/reset-loaded")
def reset_loaded_images():
    return reference_images.reset_loaded_images()

@app.post("/set-sketch")
def set_sketch(sketch: Sketch):
    print(f"Landmarks-sketch: {sketch.landmarks}")
    database.input_sketch(path = sketch.path, landmarks= sketch.landmarks)

@app.get("/get-sketch")
def get_sketch():
    sketch = database.fetch_sketch()
    return {"path": sketch.path, "landmarks" : sketch.landmarks}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}




# tasks = ["Learn FastAPI", "Build project"]

# @app.get("/tasks")
# def get_tasks():
#     return tasks

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}





# @app.get("/users")
# def get_users():
#     return {"Hello": "World"}


# @app.get("/sort_users/{smth}")  #@app.get("/users/sort_users/{smth}")
# def sort_users():
#     return {"Hello": "World"}


# @app.post("/add_users/{dir_path}")  #@app.get("/users/sort_users/{smth}")
# def sort_users():
#     return {"Hello": "World"}