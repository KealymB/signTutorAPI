import os
import tensorflow as tf
from tensorflow import keras
import numpy as np

print(np.__version__)

#params
img_height = 224
img_width = 224
class_names = ['E', 'G', 'I', 'N', 'R']

# load model
sign_model = tf.keras.models.load_model('ASL_MODEL_V1.h5')

img = tf.keras.utils.load_img(
    "C:\\Users\\kealy\\Desktop\\Projects\\signTutorAPI\\test_images\\testImage02.png", target_size=(img_height, img_width)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = sign_model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)