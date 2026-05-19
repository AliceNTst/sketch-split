(install requirements for frontend and backend)

1. Prepare database: 
-> Install your database Postgresql
-> open cmd
-> cd C:\Program Files\PostgreSQL\18\bin  #example for where it can be stored
-> create database: psql -U postgres -c "CREATE DATABASE my_new_database_name;" #change my_new_database_name 
-> add structure: psql -U postgres -d my_new_database_name -f path_to_received_sql\structure.sql
with this all the needed tables will be created in your database

2. Configure .env:
-> change .env.example in /backend to .env
-> fill .env with your databse credetials 

3. Add gallery images (references) to database
-> start terminal from /backend folder
-> start backend: uvicorn backend:app --reload
-> use API request to add gallery images from your folder: POST http://127.0.0.1:8000/images/add
body: {
  "folder_path": "your folder path"
}
-> restart backend

4. Start frontend:
-> start terminal form /frontend folder
-> start frontend: python start.py
 