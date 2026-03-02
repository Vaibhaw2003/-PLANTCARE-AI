import tensorflow as tf
import os

os.makedirs("model", exist_ok=True)

# Minimal lightweight model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(10,)),
    tf.keras.layers.Dense(4, activation="softmax")
])

model.save("model/plant_model.h5")

print("✅ Model created successfully!")