import requests


BASE = "http://127.0.0.1:5000"

data = [{"name": "Learn python", "likes": 98, "views": 450},
        {"name": "Learn flask", "likes": 1028, "views": 1200},
        {"name": "Learn rest api", "likes": 228, "views": 120}]

for i in range(len(data)):
    response = requests.put(BASE + "/video/" + str(i),
                            json = data[i])
    print(response.json())

response = requests.delete(BASE + "/video/0")

print(response)

input()

response = requests.get(BASE + "/video/2")

print(response.json())
