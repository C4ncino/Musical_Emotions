import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt


datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0/255.0,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    './data/images',
    target_size=(256, 256),
    batch_size=32,
    class_mode='categorical',
    shuffle=True,
)

valid_generator = datagen.flow_from_directory(
    './data/images',
    target_size=(256, 256),
    batch_size=32,
    class_mode='categorical',
    shuffle=True,
)

class_names = train_generator.class_indices
print(class_names)


model = tf.keras.Sequential([
    layers.Conv2D(128, (3, 3), activation='relu', input_shape=(256, 256, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax'),
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model_history = model.fit(
    train_generator,
    steps_per_epoch=10,
    epochs=10,
    validation_data=valid_generator,
    validation_steps=10,
)

plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()

model.save('./models/v1.h5')

print("model saved!")
