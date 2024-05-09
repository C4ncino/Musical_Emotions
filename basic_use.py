import cv2
import tensorflow as tf
import numpy as np


def mostrar_video():
    cap = cv2.VideoCapture(0)

    model = tf.keras.models.load_model('./models/cancino/v1.h5')

    class_names = [
        'controller',
        'nothing'
    ]

    if not cap.isOpened():
        print("Error al abrir la cámara")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error al capturar el fotograma")
            break

        mini_frame = cv2.resize(frame, (256, 256))
        preprocessed_frame = np.expand_dims(mini_frame, axis=0)

        pred = model.predict(preprocessed_frame)

        print(f"Yo digo que es: {class_names[np.argmax(pred)]}")

        cv2.imshow('live', mini_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


mostrar_video()
