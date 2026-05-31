from fastapi import FastAPI
from database_connection import Database
from data.reference_images import ReferenceImages
from data import images_sorting
from data.image_data import ImageData
import os

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

class Images(BaseModel):
    folder_path: str 
    

app = FastAPI()
database = Database()
reference_images = ReferenceImages(database)

@app.get("/images")
def get_images():
    # images = database.fetch_images()
    # return reference_images.images_paths
    images = database.fetch_images()
    images_paths = [image.path for image in images]
    return images_paths

@app.get("/")
def read_root():
    return {"Hello": "Wanderer"}


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
    print(f"Sorted images: {sorted_paths[0:10]}...")
    reference_images.set_images(images = sorted_images, paths = sorted_paths)
    reference_images.reset_loaded_images()
    # print(f"Check 1: {sorted_images[0].landmarks}")

    #TODO for testing
    print(f"Sketch: parts_angles: {sketch.parts_angles}  connection_angles: {sketch.connection_angles}")
    for ref in sorted_images[0:10]:
        print(f"Ref{ref.path}: parts_angles: {ref.parts_angles}  connection_angles: {ref.connection_angles}")
    images_sorting.__compare_images_test(image1= sketch, image2=sorted_images[3], coefficients=coefficients)
    images_sorting.__compare_images_test(image1= sketch, image2=sorted_images[4], coefficients=coefficients)




@app.get("/images/next")
def next_images(number: int):
    next_images_batch = reference_images.next(number)
    print(f"Next images batch: {next_images_batch}")
    return next_images_batch

@app.get("/images/reload")
def reload_images():
    # reference_images.images = reference_images.database.fetch_images()
    # reference_images.images_paths = [image.path for image in reference_images.images]
    # reference_images.images_number = len(reference_images.images_paths)
    
    if reference_images.images_loaded == 0:
        next_images_batch = reference_images.next()
        print(f"Next: {next_images_batch}")
        return next_images_batch
    else:
        images = reference_images.get_loaded_images()
        print(f"Get loaded images: {images}")
        return images

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

@app.delete("/remove-all-images")
def remove_all_images():
    print("Removing all images data from database")
    database.remove_all_images()
    reference_images.remove_all_images()
    print("Images data removed from database successfully")

@app.post("/sketch/add-to-gallery")
def set_sketch(sketch: Sketch):
    print(f"Landmarks-sketch: {sketch.landmarks}")
    database.input_image(path = sketch.path, landmarks= sketch.landmarks)
    reference_images.append(path = sketch.path, landmarks= sketch.landmarks)


@app.post("/images/add")
def add_images(images: Images):
    checked_paths = database.input_images(images.folder_path)
    added_images = reference_images.add_images(checked_paths)
    print(f"Successfully added {len(added_images)} images")



