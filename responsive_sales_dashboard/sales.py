import random
from datetime import datetime, timedelta

# Expanded list of products
item_names = [
    "Laptop", "Monitor", "Keyboard", "Mouse", "Webcam", "Desk", "Chair", "Tablet",
    "Printer", "Docking Station", "Smartphone", "Router", "Projector", "Scanner",
    "Microphone", "Speaker", "External Hard Drive", "Flash Drive", "Graphics Card",
    "RAM", "SSD", "Power Supply", "Motherboard", "Cooling Fan", "Surge Protector"
]

# Date range
start_date = datetime.strptime("2025-05-15", "%Y-%m-%d")
end_date = datetime.strptime("2025-06-01", "%Y-%m-%d")

# Function to generate a random timestamp
def random_timestamp(start, end):
    delta = end - start
    rand_seconds = random.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=rand_seconds)).strftime("%Y-%m-%d %H:%M:%S")

# Generate insert statements with id column
insert_statements = []
id_counter = 1
for emp_id in range(100, 1099):  # 994 employees approx
    items = random.sample(item_names, 5)
    for item in items:
        qty = random.randint(1, 10)
        amt = round(random.uniform(20.00, 1000.00), 2)
        sale_date = random_timestamp(start_date, end_date)
        stmt = f"INSERT INTO sales (id, item_name, quantity, amount, sale_date, employee_id) VALUES ({id_counter}, '{item}', {qty}, {amt}, '{sale_date}', {emp_id});"
        insert_statements.append(stmt)
        id_counter += 1

# Save to file
with open("employee_sales.sql", "w") as f:
    f.write("\n".join(insert_statements))

print(f"File 'employee_sales.sql' has been created with {len(insert_statements)} records.")