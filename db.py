import mysql.connector

global cnx

cnx = mysql.connector.connect(
    host = 'chatbot-order-food-mysqldb-chatbot-food-order-db.l.aivencloud.com',
    user = 'avnadmin',
    port = '26271',    
    password = 'AVNS_2gglVMUeF4s7RtJnAqu',
    database = 'defaultdb'
)

print('Database Connected!!')

async def get_order_status(order_id: int):
    cursor = cnx.cursor()

    query = ('SELECT order_status FROM track_order where order_id = %s')

    cursor.execute(query, (order_id,))

    result = cursor.fetchone()

    cursor.close()

    if result is not None:
        return result[0]
    else:
        return None

async def upload_order(food_dict: dict):
    cursor = cnx.cursor()

    next_order_id = get_next_order_id()

    query = 'INSERT INTO order_details VALUES (%s, %s, %s, %s)'

    values = []
    total_amount_each_item = []
    
    for key,value in food_dict.items():
        query_for_index = ('SELECT id FROM food_items where item = %s')
        cursor.execute(query_for_index, (key,))
        index = cursor.fetchone()[0]
        print(f'Index = {index}')        
        
        quantity = int(value)
        
        query_for_price = ('SELECT price FROM food_items where item = %s')
        cursor.execute(query_for_price, (key,))
        price = cursor.fetchone()[0]
        print(f'Price = {price}')
        amount = price * quantity
        total_amount_each_item.append(amount)

        values.append((next_order_id, index, quantity, amount))
    
    print(f'Values = {values}')
    
    cursor.executemany(query, values)
    cnx.commit()

    print('Inserted!!')

    total_amount_query = 'SELECT SUM(amount) FROM order_details where order_id = %s'

    cursor.execute(total_amount_query,(next_order_id,))

    total_amount = cursor.fetchone()[0]

    cursor.close()

    insert_order_tracking(next_order_id)

    return {
        'order_id': next_order_id, 
        'total_amount': total_amount, 
        'total_amount_each_item': total_amount_each_item
    }

def get_next_order_id():
    cursor = cnx.cursor()
    query = ('SELECT MAX(order_id) FROM order_details')
    cursor.execute(query)
    max_order_id = cursor.fetchone()[0]
    print(f'Max order id = {max_order_id}')
    cursor.close()
    return max_order_id + 1    

def insert_order_tracking(order_id:int):
    cursor = cnx.cursor()
    query = ('INSERT INTO track_order VALUES (%s, %s)')
    value = (order_id, 'in-transit')
    cursor.execute(query,value)
    cnx.commit()
    cursor.close()    