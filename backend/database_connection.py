import psycopg2
import sys
import os
from data.image_data import ImageData
import json
import numpy
from pathlib import Path
import datetime
from dotenv import load_dotenv


class Database():
    def __init__(self):
        load_dotenv()

        host = os.getenv("host")
        dbname = os.getenv("dbname")
        user = os.getenv("user")
        password = os.getenv("password")
        port = os.getenv("port", "5432")
        connection_string = f"host='{host}' dbname='{dbname}' user='{user}' password='{password}' port='{port}'"

        self.connection = psycopg2.connect(connection_string)
        self.cursor = self.connection.cursor()
        print ("Connected to database!\n")

    
    def fetch_images(self):
        self.cursor.execute("SELECT path, landmarks, parts_angles, connection_angles FROM images;")
        rows = self.cursor.fetchall()

        images = []
        for row in rows:
            image = ImageData(path = row[0], landmarks=numpy.array(row[1]), parts_angles=numpy.array(row[2]), connection_angles=numpy.array(row[3]))
            images.append(image)
        # for row in rows:
        #     print(row)
        return images

    def __input_image(self, path):

        if not path.isascii():
            print(f"Image path {path} does not match ascii. Image name will be changed.")
            path = Path(path)
            time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_name = f"img_{time}_{hash(str(path))}.jpg"
            new_path = path.parent / new_name
            os.rename(path, new_path)
            path = str(new_path)

        try:
            image = ImageData(path = path)
        except:
            print(f"Not able to add image: {path} to database")
            return None
        columns = "path, landmarks, parts_angles, connection_angles"
        values = (image.path, json.dumps(image.landmarks.tolist()), json.dumps(image.parts_angles.tolist()), json.dumps(image.connection_angles.tolist()))

        self.cursor.execute(f"INSERT INTO images ({columns}) VALUES (%s, %s, %s, %s);", values)
        # self.connection.commit()
        print(f"Image: {path} was added to database")
        return path

    def input_images(self, folder_path):
        """Image infos will be added to database. If image path doesnt match ascii, file name will be changed. All checked and adjusted paths will be returned at the end"""
        checked_paths = []
        images = os.listdir(folder_path)
        images_paths = [os.path.join(folder_path, image) for image in images]
        for image_path in images_paths:
            print(f"Trying to add image: {image_path} to database")
            checked_path = self.__input_image(image_path)
            if checked_path != None:
                checked_paths.append(checked_path)

        self.connection.commit()
        print("Changes commited: adding images to database")
        return checked_paths
    
    def input_image(self, path, landmarks):
        try:
            image = ImageData(path = path, landmarks=landmarks)
        except:
            print(f"Not able to add image: {path} to database")
            return None
        columns = "path, landmarks, parts_angles, connection_angles"
        values = (image.path, json.dumps(image.landmarks), json.dumps(image.parts_angles.tolist()), json.dumps(image.connection_angles.tolist()))

        self.cursor.execute(f"INSERT INTO images ({columns}) VALUES (%s, %s, %s, %s);", values)
        self.connection.commit()
        print(f"Image: {path} was added to database")
        return path

    def remove_image(self, path):
        self.cursor.execute("DELETE FROM images WHERE path =  %s;", (path,))
        self.connection.commit()
        print(f"Image: {path} was removed from database")

    def remove_images(self, folder_path):
        images = os.listdir(folder_path)
        images_paths = [os.path.join(folder_path, image) for image in images]
        for image_path in images_paths:
            self.remove_image(image_path)

    def remove_all_images(self):
        self.cursor.execute("DELETE FROM images;")
        self.connection.commit()
        print(f"All images data was removed")

    def fetch_sketch(self):
        self.cursor.execute("SELECT path, landmarks FROM sketch WHERE id = 1;")
        rows = self.cursor.fetchall()

        sketch = ImageData(path = rows[0][0], landmarks=numpy.array(rows[0][1]))
        return sketch

    def input_sketch(self, path, landmarks):
        # columns = "id, path, landmarks"
        values = (1, path, json.dumps(landmarks))
        '''INSERT INTO settings (id, path, landmarks)
        VALUES (1, '{"key": "value"}')
        ON CONFLICT (id)
        DO UPDATE SET data = EXCLUDED.data;'''

        self.cursor.execute(f"INSERT INTO sketch (id, path, landmarks) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET landmarks = EXCLUDED.landmarks, path = EXCLUDED.path;", (values))
        self.connection.commit()
        # self.cursor.execute(f"INSERT INTO sketch (id, path, landmarks) VALUES (%s, %s, %s);", (values))


    def remove_sketch(self):
        self.cursor.execute("TRUNCATE TABLE sketch RESTART IDENTITY;")
        self.connection.commit()

    def update_data(self):
        pass



database = Database()
