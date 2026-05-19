(install requirements for frontend and backend)

1. Install your database
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
 