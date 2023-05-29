import numpy as np
import numpy.typing as npt
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import sklearn
import json

# constants

RANDOM_STATE: np.int_ = 42
TEST_SIZE: np.float_ = 0.2
EPOCHS: np.int_ = 25

sms: pd.DataFrame = pd.read_csv(
    "data/spam.csv",
    encoding="ISO-8859-1",
    usecols=[0, 1],
    skiprows=1,
    names=["label", "message"],
)

sms.label = sms.label.map({"ham": 0, "spam": 1})

# balanceamento do dataset
df_spam: pd.DataFrame = sms.query("label == 1")
df_ham: pd.DataFrame = sms.query("label == 0")
df_ham_downsampled: pd.DataFrame = df_ham.sample(df_spam.shape[0])
df_balanced: pd.DataFrame = pd.concat([df_ham_downsampled, df_spam])

X_train, X_test, y_train, y_test = train_test_split(
    df_balanced["message"],
    df_balanced["label"],
    stratify=df_balanced["label"],
    test_size=TEST_SIZE,
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

METRICS: list = [
    tf.keras.metrics.BinaryAccuracy(name="accuracy"),
    tf.keras.metrics.Precision(name="precision"),
    tf.keras.metrics.Recall(name="recall"),
]

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=METRICS)
model.fit(X_train, y_train, epochs=EPOCHS)

y_pred = model.predict(X_test)
y_pred = y_pred.flatten()
y_pred = np.where(y_pred > 0.5, 1, 0)

accuracy_score: np.float_ = sklearn.metrics.accuracy_score(y_test, y_pred)
precision_score: npt.NDArray[np.float_] = sklearn.metrics.precision_score(
    y_test, y_pred, average=None, zero_division=0
)
recall_score: npt.NDArray[np.float_] = sklearn.metrics.recall_score(
    y_test, y_pred, average=None, zero_division=0
)
f1_score: npt.NDArray[np.float_] = sklearn.metrics.f1_score(
    y_test, y_pred, average=None
)
confusion_matrix: npt.NDArray[np.int_] = sklearn.metrics.confusion_matrix(
    y_test, y_pred
)

run_info: dict = {
    "accuracy_score": accuracy_score,
    "precision_score": precision_score.tolist(),
    "recall_score": recall_score.tolist(),
    "f1_score": f1_score.tolist(),
    "confusion_matrix": confusion_matrix.tolist(),
    "random_state_seed": RANDOM_STATE,
    "test_size": TEST_SIZE,
    "epochs": EPOCHS,
}

with open("data/results.json", "a") as file:
    json.dump(run_info, file, indent=4)
