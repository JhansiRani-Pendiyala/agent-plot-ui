***Backend 

    pip install -r requirements.txt
    
    uvicorn main:app --reload --host 0.0.0.0 --port 8080
    
FrontEnd

    cd frontend
    
    pip install -r requirements.txt
    
    python app.py
    
 Request Payload to test from postman 
 
       curl --location 'http://0.0.0.0:8080/api/query' \
    --header 'Content-Type: application/json' \
    --data '{
        "query" :"all employee details along with the total products sold by each emaploye "
    
    }'


prompts to load the dahsboard - 

     provide total sales by each employee
     all employee details along with the total products sold by each emaploye 

<img width="1440" alt="image" src="https://github.com/user-attachments/assets/5ce3eb0d-a2f9-4cd1-b0a9-3c3df48c88ae" />






    

