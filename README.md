Backend 
   cd backend
    export OPENAI_API_KEY="your_openai_api_key"
    export DB_HOST=localhost
    export DB_PORT=5432
    export DB_NAME=yourdb
    export DB_USER=youruser
    export DB_PASSWORD=yourpassword
    pip install -r requirements.txt
    uvicorn main:app --reload --host 0.0.0.0 --port 8080
FrontEnd
    cd frontend
    pip install -r requirements.txt
    python app.py

