from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db
import generic_helper

app = FastAPI()

inProgress_orders = {}

@app.get("/")
async def handleRequest():
    return JSONResponse(
        content = {'message': 'Backend is running!!'}
    )

@app.post("/")
async def handleRequest(request: Request):
    payload = await request.json()
    
    intent_name = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    outputContexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(outputContexts[0]['name'])

    print('Intent: '+str(intent_name))
    print('parameters: '+str(parameters))
    print('session_id: '+str(session_id))

    # if intent_name == 'order.add - context: ongoing-order':
    #     return JSONResponse(
    #         content={"fulfillmentText": "Message from backend: Order added successfully"}
    #     )
    
    # if intent_name == 'order.track-context:ongoing-tracking':
    #     return await track_order(parameters)

    intent_handler_dict = {
        'order.track-context:ongoing-tracking': track_order,
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_order,
        'order.complete - context: ongoing_order': complete_order
    }

    return await intent_handler_dict[intent_name](parameters,session_id)
        
async def add_to_order(parameters: dict, session_id:str):
    food_items = parameters['food-items']
    quantity = parameters['number']

    if len(food_items)!=len(quantity):
        return JSONResponse(
            content = {'fulfillmentText': 'Sorry, I did not understand. Please clearly specify the food items and quantity'}
        )
    else:
        food_dict = dict(zip(food_items,quantity))
        if session_id in inProgress_orders:
            inProgress_orders[session_id].update(food_dict)
        else:
            inProgress_orders[session_id] = food_dict
        
        order_str = generic_helper.get_order_list(inProgress_orders[session_id])

        return JSONResponse(
            content = {
                'fulfillmentText': f'Amazing! Added to the order. So far you have {order_str}. Do you need anything else?'
                }
        )
    
async def remove_order(parameters: dict, session_id:str):
    if session_id in inProgress_orders:        
        food_dict = inProgress_orders[session_id]
        food_items_to_remove = parameters['food-items']
        for key in food_items_to_remove:
            food_dict.pop(key)
        inProgress_orders[session_id].update(food_dict)
        print('Removed!')

        order_str = generic_helper.get_order_list(inProgress_orders[session_id])

        return JSONResponse(
            content = {
                'fulfillmentText': f'Yes ofcourse. Order updated!. Now you have {order_str}. Do you need anything else?'
                }
        )        
    else:
        return JSONResponse(
            content = {
                'fulfillmentText': f'Something went wrong from our side. Please start your order again. By saying new order'
                }
        )        
        
async def complete_order(parameters: dict, session_id:str):
    print(f'Food dict = {inProgress_orders[session_id]}')
    result = await db.upload_order(inProgress_orders[session_id])

    #remove the session ID bcz order is complete
    del inProgress_orders[session_id]

    if result == -1:
        return JSONResponse(
            content = {
                'fulfillmentText': 'Sorry, I was unable to place your order. Can you please place the order again?'
            }
        )
    else:
        return JSONResponse(
            content = {
                'fulfillmentText': f'Whoohoo!! Order placed successfully! Here are the details - Order ID: #{result['order_id']} and your total amount: ₹{result['total_amount']}'
            }
        )

async def track_order(parameters: dict, session_id:str):
    order_id = parameters['number']
    print(f'OrderID: {order_id}')
    order_id = int(order_id)
    order_status = await db.get_order_status(order_id)
    print(f'Order status: {order_status}')
    if order_status:            
        return JSONResponse(
            status_code = 200,
            content = {'fulfillmentText': f'Status of Order ID: {order_id} is {order_status}'}            )
    else:
        return JSONResponse(
            status_code = 200,
            content = {'fulfillmentText': f'Sorry, I could locate the Order ID: {order_id}?'}
        )