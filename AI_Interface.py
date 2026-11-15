import requests

def APIMessage(key, prompt, content, temp):
    url = 'http://sushi.it.ilstu.edu:8080/api/chat/completions'
    headers = {
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json'
    }
        
    data = {
    "model": "translategemma:latest",
    "messages": [
        {
            "role": "user",
            "content": f"{prompt}\n{content}"
        }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
        
    if response.status_code == 200:
                
            output = str(response.json()['choices'][0]['message']['content']).rstrip("\n")
            return output    
    else:
            return temp