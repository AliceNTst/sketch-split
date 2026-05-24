import os
from PIL import Image, ImageTk, ImageDraw
from data.image_data import ImageData


class ReferenceImages:
    def __init__(self, database = None,  folder = None):
        """if there is folder path, images will be fetched from folder and their values will be calculated; 
           if there is database, images data will be fetched from database"""
        self.images = []
        self.images_paths = None
        self.images_loaded = 0
        self.images_number = 0
        self.database = database
        self.next_images_batch_number = 20
        
        if folder != None:
            self.__calculate_images_paths(folder)
            self.__initialize_images()
        else:
            self.images = self.database.fetch_images()
            self.images_paths = [image.path for image in self.images]
            print(f"Added images to RefImages: {self.images_paths}")
            self.images_number = len(self.images_paths)

    def __calculate_images_paths(self, folder):
        images = os.listdir(folder)
        self.images_paths = [os.path.join(folder, image) for image in images]
        self.images_number = len(self.images_paths)
        return self.images_paths
    
    def __initialize_images(self):

        for path in self.images_paths:
            try:
                image = ImageData(path)
            except:
                self.images_paths.remove(path)
                print(f"Not able to add image: {path}")
                return
            self.images.append(image)
            # self.images_number += 1

    def set_images(self, images, paths):
        self.images = images
        self.images_paths = paths
        self.images_number = len(paths)
    
    def append(self, path, landmarks):
        self.images_paths.append(path)
        self.images.append(ImageData(path, landmarks))
        self.images_number += 1

    def add_images(self, paths:list):

        for path in paths:
            try:
                image = ImageData(path)
                self.images.append(image)
            except:
                paths.remove(path)
                print(f"Not able to add image: {path}")

        if self.images_paths == None:
            self.images_paths = paths
            self.images_number = len(paths)
        else:
            self.images_paths.extend(paths)
            self.images_number = self.images_number + len(paths)

        return paths
    
    
    def next(self, count = 0):
        if self.images_paths == None:
            return None
        if self.images_loaded == self.images_number:
            return None
        if (self.images_number - self.images_loaded) < count:
            next_images_batch = self.images_paths[self.images_loaded : self.images_number]
            self.images_loaded = self.images_number
            return next_images_batch
        if count == 0:
            count = self.next_images_batch_number 
        else:
            self.next_images_batch_number = count
        
        new_loaded_count = self.images_loaded + count
        next_images_batch = self.images_paths[self.images_loaded : new_loaded_count]
        self.images_loaded = new_loaded_count
        print(f"images_number: {self.images_number} images_loaded: {self.images_loaded} images_next: {self.next_images_batch_number}")
        return next_images_batch 


    def get_loaded_images(self):
        if self.images_loaded == 0:
            return None
        
        return self.images_paths[0 : self.images_loaded]
    
    def reset_loaded_images(self):
        self.images_loaded = 0

    def remove_all_images(self):
        self.images = []
        self.images_paths = []
        self.images_loaded = 0
        self.images_number = 0
