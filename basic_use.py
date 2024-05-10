import cv2
import tensorflow as tf
import numpy as np


def mostrar_video():
    cap = cv2.VideoCapture(0)

    model = tf.keras.models.load_model('./models/v4.h5')

    class_names = [
        'Happy',
        'Sad',
        'Neutral',
        'Angry',
        'Surprised'	
    ]

    if not cap.isOpened():
        print("Error al abrir la cámara")
        return
    
    # Se utiliza el clasificador de rostros haarcascade_frontalface_default
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    emotion = "Neutral"

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error al capturar el fotograma")
            break

        # Se detectan las caras dentro de la imagen
        faces = faceClassif.detectMultiScale(frame, 1.3, 5)

        # Tomamos los valores
        for (x, y, w, h) in faces:

            y -= 10
            h += 30

            # Se dibuja un rectangulo alrededor de la cara
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Se toma el rostro
            rostro = frame[y:y + h, x:x + w]


            mini_frame = cv2.resize(rostro, (64, 64))
            preprocessed_frame = np.expand_dims(mini_frame, axis=0)

            pred = model.predict(preprocessed_frame)

            emotion = class_names[np.argmax(pred)]

            print(f"Yo digo que es: {emotion}")

        cv2.imshow('live', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or emotion != 'Neutral':
            break

    cap.release()
    cv2.destroyAllWindows()

    return emotion


# mostrar_video()
