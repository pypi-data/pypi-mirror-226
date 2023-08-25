import requests, json



def is_library_exist (library_name:str):
    URL = f"https://pypi.org/pypi/{library_name}/json"
    content = requests.get(URL).text
    content = json.loads(content)

    if 'message' in content:
        if content['message'] == "Not Found":
            return False
    
    return True