from basic_use import mostrar_video
from recomendation import main as music

def main():

    while True:
        emotion = mostrar_video()

        print("\t"+ emotion)

        music(f'estado de ánimo: {emotion}')


if __name__ == "__main__":
    main()