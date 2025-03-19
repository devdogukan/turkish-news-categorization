import tensorflow as tf

# Modeli yükle
model = tf.keras.models.load_model("models/turkish_news_catagory.h5")

# TensorFlow Lite Converter kullanarak modeli çevir
converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # Standart TFLite operasyonları
    tf.lite.OpsSet.SELECT_TF_OPS      # TF'nin tüm operasyonlarını dahil et
]

# TensorList işlemlerini dönüştürme
converter._experimental_lower_tensor_list_ops = False

tflite_model = converter.convert()

# TFLite modelini kaydet
with open("models/turkish_news_catagory.tflite", "wb") as f:
    f.write(tflite_model)
