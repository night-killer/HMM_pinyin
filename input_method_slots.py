from input_method import Ui_mainWindow
from hmm import HMM
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt


class myMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(myMainWindow, self).__init__(parent=parent)
        self.hmm=HMM()
        self.ui=Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start)
        self.pinyin=''
        self.ans=[]
        self.flag=True
        self.num_of_hanzi=0
        self.page_num=0
        self.click_num=0

    def start(self):
        if self.ui.lineEdit.text()!="":
            self.flag=False
            self.pinyin=self.ui.lineEdit.text()
            self.deal(self.pinyin)

    def deal(self,pinyin):
        temp = self.hmm.trans(pinyin)
        self.ans = [temp[i:i + 10] for i in range(0, len(temp), 10)]
        self.num_of_hanzi = len(temp[0])
        self.page_num = 0
        self.ui.textEdit.clear()
        self.show_candidate(self.page_num)

    def keyReleaseEvent(self, e) :
        self.click_num+=1
        print(self.click_num)
        if self.flag==True:
            return
        else:
            # 下一页
            if e.key()==Qt.Key_Equal:
                if self.page_num+1 < len(self.ans):
                    self.page_num+=1
                    self.ui.textEdit.clear()
                    self.show_candidate(self.page_num)
            # 上一页
            if e.key()==Qt.Key_Minus:
                if self.page_num-1 >= 0:
                    self.page_num-=1
                    self.ui.textEdit.clear()
                    self.show_candidate(self.page_num)
            # 选词
            if Qt.Key_0<=e.key()<=Qt.Key_9:
                choose=e.key()-Qt.Key_0
                if choose<len(self.ans[self.page_num]):
                    text=self.ui.textEdit_2.toPlainText()
                    self.ui.textEdit_2.setText(text+self.ans[self.page_num][choose])
                    self.num_of_hanzi-=len(self.ans[self.page_num][choose])
                    if self.num_of_hanzi == 0:
                        self.ui.textEdit.clear()
                        self.ui.lineEdit.clear()
                        self.flag=True
                    else:
                        temp=self.pinyin.split()
                        new=temp[-self.num_of_hanzi:]
                        self.pinyin=" ".join(i for i in new)
                        self.deal(self.pinyin)


    def show_candidate(self,page_num):
        for i in range(len(self.ans[page_num])):
            self.ui.textEdit.append(str(i) + ': ' + self.ans[page_num][i] + '\n')

