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


promts to load the dahsboard - 

     provide total sales by each employee
     all employee details along with the total products sold by each emaploye 


 


    

