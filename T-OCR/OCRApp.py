import pytesseract
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
tesseractPath = "C:/Program Files/Tesseract-OCR/tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = tesseractPath

from ImgDDLabel import ImgDDLabel

class OCRApp:
    def __init__(self):
        self.img = None
        self.main()
    def main(self):
        try:
            app = QtWidgets.QApplication(sys.argv)
            self.ui = uic.loadUi('ocr_ui.ui')
            self.imgddlabel = ImgDDLabel()
            self.ui.progressBar.hide()
            self.ui.progressBar.setValue(0)
            self.saveBtn = QtWidgets.QToolButton()
            self.saveBtn.setToolTip("Save Extracted text")
            self.saveBtn.setStyleSheet(u"border:none;\n"
"background-color:none;")
            icon = QtGui.QIcon()
            icon.addFile(u"./icons/save.png", QtCore.QSize(),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.saveBtn.setIcon(icon)
            self.saveBtn.setAutoRaise(1)
            self.ui.statusbar.addPermanentWidget(self.saveBtn)
            self.ui.imgLayout.addWidget(self.imgddlabel)
            self.ui.extractBtn.clicked.connect(self.extract)
            self.saveBtn.clicked.connect(self.saveExtractedText)
            self.ui.show()
            app.exec_()
        except Exception as e:
            print(e)

    def getImagePath(self):
        self.img = self.imgddlabel.image_path
        return self.img
    def setProgressbarValue(self,v):
        self.ui.progressBar.setValue(v)

    def extract(self):
        img = self.getImagePath()
        if img:
            try:
                self.ui.textEdit.clear()
                print('extracting text')
                self.ui.progressBar.show()
                self.ui.progressBar.setValue(0)
                self.ui.extractBtn.setText('Extracting... Please Wait.')
                image = cv2.imread(img)
                self.ui.progressBar.setValue(10)
                rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                self.ui.progressBar.setValue(20)
                text = pytesseract.image_to_string(rgb)
                self.ui.progressBar.setValue(90)
                if text=='':
                    print('No text found in image')
                    self.ui.textEdit.setHtml(f'<html><p><b>No Text Found in reading Image "{img}"<html/>')
                else:
                    self.ui.textEdit.setText(text)
                    self.ui.progressBar.setValue(100)
                self.ui.extractBtn.setText('Extract')
                self.ui.progressBar.setValue(0)
                self.ui.progressBar.hide()
            except Exception as e:
                print(e)
        else:
            print('Please select any Image')
    def saveExtractedText(self):
        fn = 'extracted_text.txt'
        if self.img:
            fn = self.img.rsplit('.')[0]
        try:
            fname = QtWidgets.QFileDialog.getSaveFileName(self.ui,
                                                          'Save File',
                                                          './Extracted texts/'+fn,
                                                          "Text Files (*.txt);;Word Files(*.docx);;Python Files(*.py);;All Files(*.*)"
                                                          )
            if fname:
                et = self.ui.textEdit.toPlainText()
                with open(fname[0],'w') as tfile:
                    tfile.write(et)
        except Exception as e:
            print(e)
            


if __name__ == "__main__":
    OCRApp()
        
