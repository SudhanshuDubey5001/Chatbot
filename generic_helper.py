import re

def extract_session_id(session_string:str):
    match = re.search(r"sessions/(.*?)/contexts",session_string)
    if match:
        return match.group(1)
    return ''

def get_order_list(food_dict:dict):
    format = [f'{int(value)} {key}' for key, value in food_dict.items()]
    return '\n'.join(format)

# if __name__ == "__main__":
#     r = {'Cheeseburger': 5.0, 'Pepperoni pizza': 2.0, 'Mozzarella sticks': 5.0}
#     print(str(get_order_list(r)))