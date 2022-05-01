import sys
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QGroupBox 
from PyQt5.QtGui import QFont
import tkinter as tk
import subprocess
import pathlib  


class ReadThisForMeWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None )
        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        #above line makes sure that the screen is always on top, and that there is no frame(i.e. no close, minimise...)
        #QtCore.Qt.FramelessWindowHint|
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.win_width = screen_width - 0.2*screen_width
        self.win_height = 0.15*screen_height
        x_co_ord = (screen_width - self.win_width)/2
        y_co_ord = 0.15*screen_height
        self.setGeometry(x_co_ord, y_co_ord, self.win_width, self.win_height)
        self.setWindowTitle("")
        self.setStyleSheet("background-color: white;") #bg colour of window
        #self.setWindowOpacity(0.78) # make translucent
        self.init_ui()
        self.language = "english"

    def init_ui(self):
        self.notificationText = QLabel(self)
        self.notificationText.setText("ReadThisForMe")
        self.notificationText.setFont(QFont('Arial', 24))
        self.notificationText.setStyleSheet("color: black;") #change text colour
        self.notificationText.adjustSize()
        self.notificationText.move(( self.win_width - self.notificationText.width() ) / 15, ( self.win_height - self.notificationText.height() ) / 2)
        
        self.changeLanguage = QLabel(self)
        self.changeLanguage.setText("Change Language:")
        self.changeLanguage.setFont(QFont('Arial', 14))
        self.changeLanguage.setStyleSheet("color: black;") #change text colour
        self.changeLanguage.adjustSize()
        self.changeLanguage.move(( (self.win_width - self.notificationText.width() ) / 15)*6, ( self.win_height - self.changeLanguage.height() ) / 2)

        self.cb = QComboBox(self)
        self.addItems()
        self.cb.setStyleSheet("background-color: white;")
        #width = self.cb.minimumSizeHint().width()
        self.cb.setMinimumWidth(200)
        self.cb.setFont(QFont('Arial', 12))
        self.cb.currentIndexChanged.connect(self.selectionchange)
        
        self.cb.move(( (self.win_width - self.notificationText.width() ) / 15)*9.3, ( self.win_height - self.cb.height() ) / 2)


        #add start button 
        self.startBtn = QPushButton(self)
        self.startBtn.setText("Start")
        self.startBtn.setStyleSheet("background-color : green")
        self.startBtn.move(( (self.win_width - self.notificationText.width() ) / 15)*13, ( self.win_height - self.startBtn.height() ) / 2)
        self.startBtn.setFixedSize(150,40)
        self.startBtn.clicked.connect(self.start_clicked)




    def selectionchange(self):
        self.language = self.cb.currentText()
        print(self.language)
    
    def start_clicked(self):
        self.startBtn.setStyleSheet("background-color : orange")
        self.startBtn.setText("Press q to stop")
        print(self.language)

        subprocess.call(['python', 'ReadThisForMe.py', self.language])
        
        #subprocess.call('.\ReadThisForMe\ReadThisForMe.exe ' +self.language, shell=False)
        
        self.startBtn.setText("Start")
        self.startBtn.setStyleSheet("background-color : green")
        

    def addItems(self):
        print("hmm")
        

        all_lang_models = list(pathlib.Path(r'..\Tesseract-OCR\tessdata').glob('*.traineddata'))
        i = 0
        eng_index = -1
        for x in all_lang_models:
            lang = (pathlib.Path(x).name.split('.')[0])
            print(lang)
            if lang == "english":
                eng_index = i 
            i += 1
            if lang != "osd":
                self.cb.addItem(lang)
        print(eng_index)
        self.cb.setCurrentIndex(eng_index)
        #print(something)


        

app = QApplication(sys.argv)
win = ReadThisForMeWidget()
win.show()
sys.exit(app.exec_())

dropdown = []

all_lang_models = list(pathlib.Path(r'..\Tesseract-OCR\tessdata').glob('*.traineddata'))
i = 0
eng_index = -1
for x in all_lang_models:
    lang = (pathlib.Path(x).name.split('.')[0])
    i += 1
    dropdown.addItem(lang)

subprocess.call('.\ReadThisForMe\ReadThisForMe.exe ' +lang, shell=False) 
#language is what was selected by the user in the drop down box


