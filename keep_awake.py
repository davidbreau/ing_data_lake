from pynput.keyboard import Key, Controller
import time

def keep_awake():
    keyboard = Controller()
    print("Programme de maintien d'activité démarré...")
    print("Appuie sur Shift toutes les 45 secondes.")
    print("Appuyez sur Ctrl+C pour arrêter.")
    
    try:
        while True:
            # Simule l'appui et le relâchement de la touche Shift
            keyboard.press(Key.shift)
            keyboard.release(Key.shift)
            print("Shift pressé !", flush=True)
            # Attend 45 secondes
            time.sleep(45)
            
    except KeyboardInterrupt:
        print("\nProgramme arrêté.")

if __name__ == "__main__":
    keep_awake()
