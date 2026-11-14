import requests

def APIMessage(key, prompt, content):
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
                
            output = response.json()['choices'][0]['message']['content']
            return output    
    else:
            return f"Error: {response.status_code} - {response.text}"