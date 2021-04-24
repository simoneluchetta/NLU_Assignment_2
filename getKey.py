# Function to verify if a key is present in a dictionary

def get_key(matching, my_dict):
    for key, value in my_dict.items():
         if key == matching:
             return True
 
    return False