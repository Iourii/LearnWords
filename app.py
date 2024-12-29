from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import json
import csv
import pandas as pd

app = Flask(__name__)
CORS(app)

# Словарь для хранения слов и переводов
word_dict = {}
word_dict_reverse = {}
data = {}

greek = 0
rus = 1



def data_init():
	if len(data) == 0:
		dics = pd.read_csv('static/dicts.csv', sep='\t', dtype=str)
		
		# ~ print('dicts')
		print(dics)
		
		for index, row  in dics.iterrows():			
			df = pd.read_csv('static/'+row['file'], sep='\t', dtype=str)
			# Fill missing values in each row with the value from the first column
			df.fillna({'key': df['word']}, inplace=True)
			
			data[row['dictkey']] = {'full_name': row['name'], 'filename': row['file'],'nested': row['nested'], 'dframe': df}
	print(data)


@app.route('/')
def index():
    return send_from_directory('static', 'index.htm')


@app.route('/train2', methods=['GET'])
def train2():
	if len(data) == 0:
		data_init()

	direction = request.args.get('direction', 'forward')
	dictionary = request.args.get('dictionary', 'verbs')
	print(dictionary)
	print(direction)

	res = []

	# ~ print('HellO')
	# ~ print(data[dictionary]['dframe'])	
	print('HELLO2')
	# ~ res = data[dictionary]['dframe'][data[dictionary]['dframe']['word'] == 'Πίνω'].sample(n=1)
	
	if data[dictionary]['nested'] == '1':
		print('in nested == 1')
		res = data[dictionary]['dframe'].sample(n=4)
	else:
		print('333333')
		key = data[dictionary]['dframe'].sample(n=1).iloc[0].loc['key']
		# возможно это ошибка! Нвдо проверить неизменяемость даты
		# ~ key2 = to_list(key)
		
		print('12345')
		# ~ print(key2)	
		res = data[dictionary]['dframe'][data[dictionary]['dframe']['key'] == key].sample(n=4, replace=True)
		# ~ res = data[dictionary]['dframe'].sample(n=4)
	
	#print(rs)
	
	# return 'rs.to_json()'
    
	wrd = 'word'
	trsl = 'translation'
	if direction == 'reverse':
		wrd = 'translation'
		trsl = 'word'
    
    
    # ~ #word = random.choice(list(temp_dic.keys()))
	# ~ print(res.values)
	# ~ print('fff')
	# ~ print(res.values[2])
	# ~ print('gggg')
	# ~ print(res.iloc[2].iloc[1])
    
	word = res.iloc[0].loc[wrd]
	correct_translation = res.iloc[0].loc[trsl]
    

    # Составление списка из 4 вариантов перевода (с одним правильным)
	translations = set()
	translations.add(correct_translation)
	i = 1
	while i < 4:
		translations.add(res.iloc[i].loc[trsl])
		i=i+1
    
    # Преобразование в список для JSON-вывода
	translations = list(translations)
	random.shuffle(translations)

	print(  word)
	print( translations)
	print('correct')
	print( correct_translation)
    

	return jsonify({
        'word': word,
        'options': translations,
        'correct': correct_translation
    }), 200




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


@app.route('/test2', methods=['GET'])
def test2():
    # Открываем и читаем JSON файл
#    with open('static/dicts.csv', 'r', encoding='utf-8') as file:
#        data = json.load(file)

	data = []
	# Пример обработки данных
	with open('static/verbs.csv', newline='', encoding='utf-8') as csvfile:
		csvreader = csv.DictReader(csvfile)
		
			# Пример работы с данными в виде словаря
		for row in csvreader:
			print(row)  # Каждая строка представлена как словарь
		#	data.append(row)
		#print(data)
				
	return jsonify(data)



@app.route('/test3', methods=['GET'])
def test3():
	data = {}
	dics = []
	dics = pd.read_csv('static/dicts.csv', sep='\t', dtype=str)
	
	print(data)
	#df.insert(0, 'dict', 'dict0')	
	
	##result = pd.concat([df1, df2], axis=0)
	
	#rs = df[df['dict'] == 'dict0'].sample(n=4)
	
	#print(rs)
	
	return 'rs.to_json()'
	

if __name__ == '__main__':
    app.run(debug=True, port=5001)

