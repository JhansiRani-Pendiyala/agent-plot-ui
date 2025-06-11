***Backend 

    pip install -r requirements.txt
    
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

    Create Postgres connection and update the config.json
    create open API key and add into config.json file
    
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

DashBoard

<img width="1440" alt="image" src="https://github.com/user-attachments/assets/cd10482d-a95a-463b-bbc2-3bb3d4da25e7" />






    

