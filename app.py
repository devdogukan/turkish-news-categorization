from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import string
from TurkishStemmer import TurkishStemmer
import os

app = Flask(__name__)

# Model dizini
MODEL_DIR = 'models'

# Model ve diğer bileşenleri yükleme
def load_model_components():
    # Model mimarisini yükleme
    json_file = open(os.path.join(MODEL_DIR, 'turkish_news_catagory.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    
    # Model ağırlıklarını yükleme
    model.load_weights(os.path.join(MODEL_DIR, 'turkish_news_catagory.weights.h5'))
    
    # Model derleme
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    # Tokenizer'ı yükleme
    with open(os.path.join(MODEL_DIR, 'tokenizer.pickle'), 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    # LabelEncoder'ı yükleme
    with open(os.path.join(MODEL_DIR, 'label_encoder.pickle'), 'rb') as handle:
        label_encoder = pickle.load(handle)
    
    return model, tokenizer, label_encoder

# Metin ön işleme
def preprocess_text(text, stemmer):
    # Normalizasyon
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Lemmatizasyon
    words = text.split()
    lemmatized_words = [stemmer.stem(word) for word in words]
    return ' '.join(lemmatized_words)

# Global değişkenler
model, tokenizer, label_encoder = load_model_components()
stemmer = TurkishStemmer()
MAX_LENGTH = 200  # Eğitim sırasında kullanılan değer
print("Model hazır!")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # JSON verisini alma
        data = request.get_json(force=True)
        text = data['text']
        
        # Metin ön işleme
        processed_text = preprocess_text(text, stemmer)
        
        # Tokenizasyon ve padding
        sequence = tokenizer.texts_to_sequences([processed_text])
        padded_sequence = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post', truncating='post')
        
        # Tahmin
        prediction = model.predict(padded_sequence)
        predicted_class_index = np.argmax(prediction, axis=1)[0]
        predicted_class = label_encoder.classes_[predicted_class_index]
        confidence = float(prediction[0][predicted_class_index])
        
        # Sonuçları hazırlama
        result = {
            'category': predicted_class,
            'confidence': confidence,
            'all_probabilities': {
                category: float(prob) 
                for category, prob in zip(label_encoder.classes_, prediction[0])
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/demo')
def demo():
    # Örnek metinler
    sample_texts = {
        'siyaset': 'Cumhurbaşkanı bugün mecliste önemli açıklamalarda bulundu. Yeni reform paketi önümüzdeki hafta açıklanacak.',
        'ekonomi': 'Merkez Bankası faiz kararını açıkladı. Enflasyon rakamları beklentilerin üzerinde gerçekleşti.',
        'spor': 'Galatasaray, Şampiyonlar Ligi\'ndeki mücadelesinde deplasmanda rakibini 2-1 mağlup etti.',
        'teknoloji': 'Apple\'ın yeni iPhone modelleri tanıtıldı. Yapay zeka özellikleri dikkat çekiyor.',
        'saglik': 'Sağlık Bakanlığı yeni aşı kampanyasını duyurdu. Grip sezonu öncesi vatandaşlar aşı olmaya davet ediliyor.',
        'dunya': 'Birleşmiş Milletler\'de iklim değişikliği zirvesi başladı. Ülkeler yeni kararlar almak için bir araya geldi.',
        'kultur': 'İstanbul Film Festivali\'nde ödüller sahiplerini buldu. Bu yılki festivale katılım yoğun oldu.'
    }
    
    return render_template('demo.html', sample_texts=sample_texts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)