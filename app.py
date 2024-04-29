from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Словарь для хранения слов и переводов
word_dict = {}

@app.route('/')
def index():
    return send_from_directory('static', 'index.htm')


@app.route('/add_word', methods=['POST'])
def add_word():
    """
    Эндпойнт для добавления целого словаря слов и переводов.
    Ожидается JSON-объект, где ключи — это слова, а значения — списки переводов.
    """
    data = request.json  # Получаем JSON-данные из запроса

    if not data:
        return jsonify({'error': 'No data provided'}), 400  # Если нет данных, возвращаем ошибку

    for word, translations in data.items():
        if not isinstance(translations, list):
            return jsonify({'error': f'Translations for "{word}" should be a list'}), 400

        if word not in word_dict:
            word_dict[word] = []

        # Добавляем переводы к слову, избегая дубликатов
        for translation in translations:
            if translation not in word_dict[word]:
                word_dict[word].append(translation)

    return jsonify({'message': 'Words added successfully'}), 200  # Ответ при успешном добавлении


@app.route('/train', methods=['GET'])
def train():
    """
    Эндпойнт для тренировки. Возвращает набор из одного слова и 4 переводов,
    один из которых верный.
    """
    if not word_dict:
        return jsonify({'error': 'Dictionary is empty'}), 400

    word = random.choice(list(word_dict.keys()))
    correct_translation = random.choice(word_dict[word])

    # Составление списка из 4 вариантов перевода (с одним правильным)
    translations = set(word_dict[word])
    while len(translations) < 4:
        random_word = random.choice(list(word_dict.keys()))
        random_translation = random.choice(word_dict[random_word])
        translations.add(random_translation)

    # Преобразование в список для JSON-вывода
    translations = list(translations)
    random.shuffle(translations)

    return jsonify({
        'word': word,
        'options': translations,
        'correct': correct_translation
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)

