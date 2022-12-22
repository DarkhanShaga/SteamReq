import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': 'Apple',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())
