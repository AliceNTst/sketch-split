import psycopg2
import sys
import os
from data.image_data import ImageData
import json
import numpy


class Database():
    #TODO relocate login data
    def __init__(self, connection_string = "host='localhost' dbname='sketch' user='postgres' password='datarinebase_2026'"):
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

    def input_image(self, path):
        image = ImageData(path = path)
        columns = "path, landmarks, parts_angles, connection_angles"
        values = (image.path, json.dumps(image.landmarks.tolist()), json.dumps(image.parts_angles.tolist()), json.dumps(image.connection_angles.tolist()))

        self.cursor.execute(f"INSERT INTO images ({columns}) VALUES (%s, %s, %s, %s);", values)
        self.connection.commit()
        print(f"Image: {path} was added to database")

    def input_images(self, folder_path):
        images = os.listdir(folder_path)
        images_paths = [os.path.join(folder_path, image) for image in images]
        for image_path in images_paths:
            self.input_image(image_path)

    def remove_image(self, path):
        self.cursor.execute("DELETE FROM images WHERE path =  %s;", (path,))
        self.connection.commit()
        print(f"Image: {path} was removed from database")

    def remove_images(self, folder_path):
        images = os.listdir(folder_path)
        images_paths = [os.path.join(folder_path, image) for image in images]
        for image_path in images_paths:
            self.remove_image(image_path)


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
# database.input_images(r"C:\Users\Ramen\Downloads\test_images_sort")
# images = database.fetch_images()
# for image in images:
#     print(image)
# print(images[0])
test_image = ImageData(r"C:\Users\Ramen\Downloads\test_images_sort\6.JPG")
print(test_image.landmarks)
database.input_sketch(path = r"C:\Users\Ramen\Downloads\test_images_sort\6.JPG", landmarks = test_image.landmarks.tolist())

# database.remove_image(r"C:\Users\Ramen\Downloads\test_images_sort\6.JPG")
# database.remove_images(r"C:\Users\Ramen\Downloads\test_images_sort")
# database.input_sketch(r"C:\Users\Ramen\Downloads\test_images_sort\3.JPG", {"type": "CUSTOM"})
# database.remove_sketch()



# cursor = None
# connection = None

# def test_database():
#     conn_string = "host='localhost' dbname='secondbase' user='postgres' password='datarinebase_2026'"

# 	# print the connection string we will use to connect
#     # print "Connecting to database\n	->%s" % (conn_string)

# 	# get a connection, if a connect cannot be made an exception will be raised here
#     conn = psycopg2.connect(conn_string)

# 	# conn.cursor will return a cursor object, you can use this cursor to perform queries
#     cursor = conn.cursor()
#     print ("Connected!\n")

#     cursor.execute("SELECT * FROM cats")

#     data = cursor.fetchall()


#     print(data)


# def create_connection():
#     global connection
#     connection = psycopg2.connect(
#     dbname="your_database",    # Database name
#     user="your_username",      # PostgreSQL username
#     password="your_password",  # Password for the user
#     host="localhost",          # Database host
#     port="5432"                # Database port
# )

#     # Open a cursor to perform database operations
#     global cursor
#     cursor = connection.cursor()

#     # Print a success message
#     print("Connected to PostgreSQL")


# def create_table():
#     # Define the SQL query for creating a table
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS employees (
#         id SERIAL PRIMARY KEY,
#         name VARCHAR(100),
#         position VARCHAR(100),
#         hire_date DATE
#     );
#     '''

#     # Execute the create table query
#     cursor.execute(create_table_query)
#     connection.commit()  # Commit the transaction
#     print("Table created successfully")

# def fetch_data():
#     cursor.execute("SELECT * FROM employees;")
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)


# def insert_data(name, position, hire_date):
#     insert_query = '''
#     INSERT INTO employees (name, position, hire_date)
#     VALUES (%s, %s, %s) RETURNING id;
#     '''
#     cursor.execute(insert_query, (name, position, hire_date))
#     connection.commit()
#     print("Employee inserted with ID:", cursor.fetchone()[0])

# def update_data(new_position, emp_id):
#     update_query = '''
#     UPDATE employees
#     SET position = %s
#     WHERE id = %s;
#     '''
#     cursor.execute(update_query, (new_position, emp_id))
#     connection.commit()
#     print("Employee position updated")

# def delete_data(emp_id):
#     delete_query = '''
#     DELETE FROM employees WHERE id = %s;
#     '''
#     cursor.execute(delete_query, (emp_id,))
#     connection.commit()
#     print("Employee deleted")