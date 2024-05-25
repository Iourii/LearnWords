from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app)

# Словарь для хранения слов и переводов
word_dict = {}
word_dict_reverse = {}

greek = 0
rus = 1


@app.route('/')
def index():
    return send_from_directory('static', 'index.htm')


@app.route('/add_word', methods=['POST'])
def add_word():
    data = request.json  # Получаем JSON-данные из запроса
    if not data:
        return jsonify({'error': 'No data provided'}), 400  # Если нет данных, возвращаем ошибку

    for word, translation in data.items():
        if word not in word_dict:
            word_dict[word] = translation
        if translation not in word_dict_reverse:
            word_dict_reverse[translation] = word

    return jsonify({'message': 'Words added successfully'}), 200  # Ответ при успешном добавлении

@app.route('/train', methods=['GET'])
def train():
    """
    Эндпойнт для тренировки. Возвращает набор из одного слова и 4 переводов,
    один из которых верный.
    """
    #if not word_dict:
    #    return jsonify({'error': 'Dictionary is empty'}), 400

    direction = request.args.get('direction', 'forward')

    if direction == 'forward':
        temp_dic = word_dict
    else:
        temp_dic = word_dict_reverse

    word = random.choice(list(temp_dic.keys()))
    correct_translation = temp_dic[word]

    # Составление списка из 4 вариантов перевода (с одним правильным)
    translations = set()
    translations.add(correct_translation)
    while len(translations) < 4:
        random_word = random.choice(list(temp_dic.keys()))
        translations.add(temp_dic[random_word])

    # Преобразование в список для JSON-вывода
    translations = list(translations)
    random.shuffle(translations)

    return jsonify({
        'word': word,
        'options': translations,
        'correct': correct_translation
    }), 200

@app.route('/test', methods=['GET'])
def test():
    # Открываем и читаем JSON файл
    with open('static/dictionary_short.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Извлекаем многомерный массив
    #array = data['array']

    print(data[0]['name'])
    print(data[0]['goDeep'])
    print(data[0]['members'][0]['members'][0][greek])
    print(data[0]['members'][0]['members'][0][rus])
    #array[1]

    # Печатаем результат
    #print(array)

    return jsonify({
        'word': 'word',
        'options': 'translations',
        'correct': 'correct_translation'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)

