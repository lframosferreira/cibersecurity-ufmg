import numpy as np  # vetores e matrizes
import pandas as pd  # processamento dos dados, arquivo CSV I/O (e.g. pd.read_csv)
import warnings

warnings.filterwarnings("ignore")

sms = pd.read_csv(
    "data/spam.csv",
    encoding="ISO-8859-1",
    usecols=[0, 1],
    skiprows=1,
    names=["label", "message"],
)

sms.label = sms.label.map({"ham": 0, "spam": 1})

from sklearn.model_selection import train_test_split
from sklearn import metrics

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text


# balanceamento do dataset
df_spam: pd.DataFrame = sms.query("label == 1")
df_ham: pd.DataFrame = sms.query("label == 0")
df_ham_downsampled: pd.DataFrame = df_ham.sample(df_spam.shape[0])
df_balanced: pd.DataFrame = pd.concat([df_ham_downsampled, df_spam])
df_balanced


X_train, X_test, y_train, y_test = train_test_split(
    df_balanced["message"], df_balanced["label"], stratify=df_balanced["label"]
)


bert_preprocess = hub.KerasLayer(
    "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
)
bert_encoder = hub.KerasLayer(
    "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4"
)

text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name="text")
preprocessed_text = bert_preprocess(text_input)
outputs = bert_encoder(preprocessed_text)


l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs["pooled_output"])
l = tf.keras.layers.Dense(1, activation="sigmoid", name="output")(l)


model = tf.keras.Model(inputs=[text_input], outputs=[l])
model.summary()


METRICS = [
    tf.keras.metrics.BinaryAccuracy(name="accuracy"),
    tf.keras.metrics.Precision(name="precision"),
    tf.keras.metrics.Recall(name="recall"),
]

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=METRICS)

model.fit(X_train, y_train, epochs=25)


y_predicted = model.predict(X_test)
y_predicted = y_predicted.flatten()


y_predicted = np.where(y_predicted > 0.5, 1, 0)
y_predicted


metrics.accuracy_score(y_test, y_predicted)
