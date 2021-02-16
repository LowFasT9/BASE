# import statements
# i will be commenting only for the uncommon and/or important code
import speech_recognition as sr
import pyttsx3  # for text to speech conversion
import pywhatkit
import datetime
import wikipedia
import webbrowser
from googlesearch import search
from PyQt5 import QtCore, QtGui, QtWidgets  # for creating a gui
from PyQt5.QtGui import QMovie  # for playing animated gif on the window of the application
import sys

class Ui_MainWindow(object):
    listener = sr.Recognizer()  # to recognise voice commands
    engine = pyttsx3.init()     # initialize test to speech
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)   # setting voice 1 for female and 0 for male
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # create label
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(25, 25, 200, 200))
        self.label.setMinimumSize(QtCore.QSize(500, 500))
        self.label.setMaximumSize(QtCore.QSize(900, 900))  # changing the parameters will change the size of the window
        self.label.setObjectName("label")
        self.pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.pushbutton.setGeometry(QtCore.QRect(360, 230, 111, 61))    # width, height, x and y axis
        self.pushbutton.setObjectName("Hinata")
        self.pushbutton.setFont(font)
        self.pushbutton.setText("Konichiwa")

        # add label to main window
        MainWindow.setCentralWidget(self.centralwidget)

        # set movie as label
        self.movie = QMovie("hinata.gif")   # path to the gif or if the gif is in same folder then name of the gif
        self.label.setMovie(self.movie)
        self.movie.start()

        self.pushbutton.clicked.connect(lambda: run_alexa())    # IMPORTANT : if you are connecting a method to a button then make sure to use lambda as follows or it will throw error
        # main function to run the voice assistant
        def run_alexa():
            command = take_command()
            print(command)
            if 'play' in command:   # if user says play
                song = command.replace('play', '')
                talk('playing' + song)
                print(song)
                pywhatkit.playonyt(song)    # playonyt(youtube)
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%H:%M %p')
                print(time)
                talk('Current time is' + time)
            elif 'who is ' in command:
                person = command.replace('who is', '')
                info = wikipedia.summary(person, 2)
                print(info)
                talk(info)
            elif 'search' in command:
                talk(command)
                command = command.replace('search', '')
                query = command
                for url in search(query, tld="co.in", num=1, stop=1, pause=1):  # search for the command and return the url link
                    print(url)
                webbrowser.open_new(str(url))   # open the web browser search for the retrieved url link
            else:
                talk('please say the command again')

        def talk(text):
            self.engine.say(text)
            self.engine.runAndWait()

        def take_command():
            try:
                with sr.Microphone() as source:  # use the system microphone as source
                    self.listener.adjust_for_ambient_noise(source)
                    print("listening")
                    voice = self.listener.listen(source)   # take input from the microphone
                    command = self.listener.recognize_google(voice)    # using google to understand the command
                    command = command.lower()       # converting the command in lowercase
                    if 'alexa' in command:
                        command = command.replace('alexa', '')
                        print(command)
            except:
                print("pass")
                pass
            return command
        # gui code
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exit")