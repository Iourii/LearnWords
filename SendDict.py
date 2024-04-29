import requests

url = 'http://127.0.0.1:5001/add_word'
data = {
    "apple": ["яблоко"],
    "car": ["машина"],
    "book": ["книга"],
    "teacher": ["учитель"],
    "cook": ["готовить"],
    "run": ["бежать"],
    "dig": ["копать"],
    "swim": ["плыть"],
    "peach": ["персик"],
    "sight": ["вид"],
    "false": ["ложь"],
    "fault": ["отказ"]
}
response = requests.post(url, json=data)
print(response.status_code)  # Вывод кода ответа
print(response.json())  # Вывод JSON-ответа, если он есть
