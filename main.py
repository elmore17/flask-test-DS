import tensorflow as tf
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, render_template, request

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)

# Загрузка обученной модели
if not os.path.exists("test_DS.h5"):
    print("Ошибка: Модель не найдена. Сначала обучите модель и сохраните ее.")
    exit(1)

model = tf.keras.models.load_model("test_DS.h5")
tokenizer = None
data_dir = "./aclImdb"

def load_data(subset):
    texts = []
    labels = []
    for label in ['pos', 'neg']:
        dir_name = os.path.join(data_dir, subset, label)
        for fname in os.listdir(dir_name):
            if fname.endswith('.txt'):
                with open(os.path.join(dir_name, fname), encoding='utf-8') as f:
                    texts.append(f.read())
                labels.append(1 if label == 'pos' else 0)
    return texts, labels

train_texts, train_labels = load_data("train")
test_texts, test_labels = load_data("test")

max_words = 10000
max_sequence_length = 300

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_texts)

train_sequences = tokenizer.texts_to_sequences(train_texts)
test_sequences = tokenizer.texts_to_sequences(test_texts)

train_data = pad_sequences(train_sequences, maxlen=max_sequence_length)
test_data = pad_sequences(test_sequences, maxlen=max_sequence_length)


# Предобработка данных пользователя
def preprocess_user_data(user_input, tokenizer, max_sequence_length):
    user_sequence = tokenizer.texts_to_sequences([user_input])
    user_data = pad_sequences(user_sequence, maxlen=max_sequence_length)
    return user_data

# Получение предсказания от модели
def get_prediction(model, user_data):
    prediction = model.predict(user_data)
    return prediction[0][0]

@app.route('/', methods=['post', 'get'])
def index():
    messageScore = ''
    messageSentiment = ''
    comment = ''
    if request.method == 'POST':
        username = request.form.get('comment')
        comment = username
        user_data = preprocess_user_data(comment, tokenizer, max_sequence_length)
        prediction = get_prediction(model, user_data)
        messageScore = str(prediction)[2]
        if prediction >= 0.5:
            sentiment = "Положительный комментарий."
        else:
            sentiment = "Отрицательный комментарий."
        messageSentiment = sentiment
    return render_template('index.html', messageScore=messageScore,messageSentiment = messageSentiment, comment = comment)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
