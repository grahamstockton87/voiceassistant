import speech_recognition as sr
import speedtest
import sys
import tkinter as tk
import threading

active = True

def listMics():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def speedTest():
    # Create a Speedtest object
    st = speedtest.Speedtest()

    # Perform the speed test
    download_speed = st.download() / 10**6  # Mbps
    upload_speed = st.upload() / 10**6  # Mbps
    ping = st.results.ping  # ms

    # Print the results
    print(f"Download speed: {download_speed:.2f} Mbps")
    print(f"Upload speed: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms")

def google(r, audio, text_label):
    try:
        heard = r.recognize_google(audio)
        text_label.config(text=heard)
        if heard == "done":
            print("done")
            sys.exit(0)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

def whisper(r, audio):
    try:
        print(r.recognize_whisper(audio, language="english"))
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")

def run(choice, text_label):
    active = True
    if choice == 0:
        speedtest()
    elif choice == 1:
        print ("Google Speaking:")
        while (active):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            google(r, audio, text_label)
    elif choice == 3:
        print ("Whisper Speaking:")
        while (active):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            whisper(r, audio)
    elif choice == 4:
        listMics()

# Create the main window
window = tk.Tk()
window.title("Speech Recognition")
window.geometry(f"{500}x{500}")

# Create a label to display the recognized text
text_label = tk.Label(window, text="Listening...")
text_label.config(font=("Arial", 40))
text_label.pack()

# Run the GUI event loop
choice = 1
thread = threading.Thread(target=run, args=(choice, text_label,))
thread.start()

window.mainloop()
