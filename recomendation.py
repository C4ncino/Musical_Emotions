from openai import OpenAI

import os
import time
import re

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

import webbrowser
import pyautogui

client_id = "21a86f17a0304be2ab1ddd07c22639a9"
client_secret = "33b9c06cf9d74f1ca40bcc0510a9f458"


def main(text: str):

    systemRole = "Eres un sistema recomendador de música de acuerdo al estado de ánimo. Recomiendas 5 canciones. En caso de tener un ánimo Tristeza, Enojo, Nuetral, recomiendas música que levante el ánimo de la persona para sentirse mejor. En caso de tener un ánimo de Alegría, Asombro, Sorprendido, recomiendas música que mantenga ese estado de ánimo. Solo dame la lista de canciones que se dividan por , cada sugerencia y que se separe el autor de la cancion con un - ."

    client = OpenAI(
        api_key=os.getenv("OPENAI_TOKEN"),
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemRole},
            {"role": "user", "content": text}
        ]
    )

    respuesta = completion.choices[0].message.content

    print(respuesta)

    songs = re.split(r'[1-5]', respuesta)

    lista_canciones = []

    caracteres_eliminar = ['.', '"']

    for s in songs:
        query = "".join(caracter for caracter in s if caracter not in caracteres_eliminar)

        lista_canciones.append(query)

        print(query)

    play_music(lista_canciones)


def play_music(songs: list):

    time_to_wait = 0

    for song in songs:

        # Reiniciar el tiempo
        time_to_wait = 0

        # Cancion - Artista
        info_song = song.split("-")

        # Eliminar el ultimo espacio de la cancion
        if info_song[0][len(info_song[0]) - 1] == " ":
            song = ""
            for i in range(len(info_song[0])-1):
                song += info_song[0][i]
            info_song[0] = song

        # Conectarse a la API de spotipy con las credenciales de desarrollador
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id, client_secret)
        )

        # Buscar al autor
        result = sp.search(info_song[1])

        # Buscar la canción
        for i in range(0, len(result["tracks"]["items"])):
            
            name_song = result["tracks"]["items"][i]["name"]

            if name_song == info_song[0]:

                # Actualizar el tiempo de espera de acuerdo a la canción actual
                time_to_wait = result["tracks"]["items"][i]["duration_ms"] / 1000
                # time_to_wait = 10

                # Abrrir la aplicación de spotify con la canción especificada
                webbrowser.open(result['tracks']['items'][i]['uri'])
                
                break

        print("Reproduciendo cancion: " + info_song[0] + " - " + info_song[1])
        
        # Esperar a que la última cancion se termine
        time.sleep(time_to_wait)

        pyautogui.press("enter")


if __name__ == "__main__":
    main("estado de ánimo: Triste")
    # play_music(["Beat It - Michael Jackson", "Locked out of Heaven - Bruno Mars"])