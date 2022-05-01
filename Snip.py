"""
Created on Wed May 27 15:08:49 2020
A Snipping Tool for Programmers - Thsi program enables the user to snip portions of the screen, performas text recognition on the snipped image and then either performs an automatic google search in the chosen browser or copies the text to clip board. 
@author: Stephen Worsley

I have edited the function so that it will be used and called in a similar function to that of the original
windows snipping function
"""

from time import sleep
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QGroupBox
import tkinter as tk
from PIL import ImageGrab
import sys
import cv2
import numpy as np
# import imageToString
import pytesseract
from TextToSpeech import TextToSpeech 


from PIL import Image



class Communicate(QObject):
    
    snip_saved = pyqtSignal()

# class MyWindow(QMainWindow):
#     def __init__(self, lang, parent=None):
#         super(MyWindow, self).__init__()
#         self.lang = lang
#         print("lang in mywindow is",self.lang)
#         self.win_width = 350
#         self.win_height = 250
#         self.setGeometry(50, 50, self.win_width, self.win_height)
#         self.setWindowTitle("Snipping Tool for Programmers")
#         self.initUI()
        
#     def initUI(self):
#         #Define buttons
#         self.searchOpen = QPushButton(self)
#         self.searchOpen.setText("Start")
#         self.searchOpen.move(10,75)
#         self.searchOpen.setFixedSize(150,40)
#         self.searchOpen.clicked.connect(self.snip_search_clicked) 
        
#         self.copyPartNum = QPushButton(self)
#         self.copyPartNum.setText("Finish")
#         self.copyPartNum.move((self.win_width/2)+10, 75)
#         self.copyPartNum.setFixedSize(150,40)
#         self.copyPartNum.clicked.connect(self.snip_copy_clicked) 

#         self.notificationBox = QGroupBox("Notification Box", self)
#         self.notificationBox.move(10,135)
#         self.notificationBox.setFixedSize(self.win_width-20,55)
        
#         self.notificationText = QLabel(self)
#         self.notificationText.move(20, 145)
#         #self.reset_notif_text()
        
        
#     def snip_search_clicked(self):
#         self.snipWin = SnipWidget(self.lang)
#         #self.snipWin.notification_signal.connect(self.reset_notif_text)
#         self.snipWin.show()
#         if self.snipWin.msg == 'snip complete':
#             self.snipWin.close()
#         #self.notificationText.setText("Snipping... Press ESC to quit snipping")
#         #self.update_notif()
#         print("I'm only printing now that it's done")

#     def snip_copy_clicked(self):
#         self.close()
        
    
        
#     def keyPressEvent(self, event): 
#         if event.key() == QtCore.Qt.Key_S:
#             self.snipWin = SnipWidget( self.lang)
#         #self.snipWin.notification_signal.connect(self.reset_notif_text)
#             self.snipWin.show()
#         event.accept()
   
        

class SnipWidget(QMainWindow):
    
    notification_signal = pyqtSignal()
    
    def __init__(self,  language):
        super(SnipWidget, self).__init__()
        root = tk.Tk()# instantiates window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        self.is_snipping = False
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.c = Communicate()
        self.msg = ''
        self.show()
        self.lang = language
        print("lang in snip is",language)
            
            
    def paintEvent(self, event):
        if self.is_snipping:
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0
        else:
            brush_color = (128, 128, 255, 128)
            lw = 3
            opacity = 0.3

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print('Quit')
            QtWidgets.QApplication.restoreOverrideCursor();
            self.notification_signal.emit()
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        self.is_snipping = True        
        self.repaint()
        QtWidgets.QApplication.processEvents()
        print(x1,x2,y1,y2)
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.is_snipping = False
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        cv2.imwrite("small_screenshot.jpg", img)
        
        self.snipped_image = img
        QtWidgets.QApplication.restoreOverrideCursor();
        self.c.snip_saved.emit()
        self.close()
        self.msg = 'snip complete'
        self.notification_signal.emit()
        extractedText = pytesseract.image_to_string(Image.open('small_screenshot.jpg'), lang=self.lang)
        extractedText= extractedText.replace("\n", "")
        print(extractedText)
        tts = TextToSpeech(self.lang)
        tts.readOutLoud(extractedText)
        

        

    
    
            
import sys 
 
lang = sys.argv[1]
print(lang)
print("hello")
pytesseract.pytesseract.tesseract_cmd = r'..\Tesseract-OCR\tesseract.exe'
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# app = QApplication(sys.argv)
    
# win = MyWindow(lang)
# win.show()
# sys.exit(app.exec_())

app = QApplication(sys.argv)
win = SnipWidget(lang)
win.show()
sys.exit(app.exec_())

#window("eng")