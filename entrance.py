# coding:utf-8
from PyQt5 import QtCore,QtGui,QtWidgets
import PyQt5
import sys
import qtawesome
import json
import dig
import time

filename='filelocation.json'

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ifBig=False
        self.init_ui()


    def init_ui(self):
        self.setFixedSize(1280, 720)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.generatLeft()#生成左侧部分
        self.generateRight()#生成右侧部分
        self.beauty()#大美为美

    #顾名思义
    def beauty(self):
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.left_widget.setStyleSheet('''
        QPushButton{border:none;color:white;}
        QPushButton#left_label{
            border:none;
            border-bottom:1px solid white;
            font-size:18px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QPushButton#left_button:hover{border-left:4px solid white;font-weight:700;}
        QWidget#left_widget{
            background:gray;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
        }
        ''')
        self.right_supportRateTxt.setStyleSheet(
            '''
            QLabel{
            font-size:18px;
            font-weight::600
            }
            '''
        )
        self.right_confidenceRateTxt.setStyleSheet(
            '''
            QLabel{
            font-size:18px;
            font-weight::600
            }
            '''
        )
        self.right_filebrowser.setStyleSheet('''
        QPushButton{
            color:solid gray;
            border-top:1px solid gray;
            border-bottom:1px solid gray;
            border-left:1px solid gray;
            border-right:1px solid gray;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
            border-top-right-radius:10px;
            border-bottom-right-radius:10px;
            font-size:18px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QPushButton:hover{border:2px solid gray;font-weight:900;}
''')
        self.right_supportRateInput.setStyleSheet('''
                        QSpinBox{
                            color:solid gray;
                            border-top:1px solid gray;
                            border-bottom:1px solid gray;
                            border-left:1px solid gray;
                            border-right:1px solid gray;
                            border-top-left-radius:5px;
                            border-bottom-left-radius:5px;
                            border-top-right-radius:5px;
                            border-bottom-right-radius:5px;
                            font-size:18px;
                            font-weight:500;
                        }
                ''')
        self.right_confidenceRateInput.setStyleSheet('''
                QSpinBox{
                    color:solid gray;
                    border-top:1px solid gray;
                    border-bottom:1px solid gray;
                    border-left:1px solid gray;
                    border-right:1px solid gray;
                    border-top-left-radius:5px;
                    border-bottom-left-radius:5px;
                    border-top-right-radius:5px;
                    border-bottom-right-radius:5px;
                    font-size:18px;
                    font-weight:500;
                }
        ''')
        self.right_fileProcessTrigger.setStyleSheet('''
                QPushButton{
                    color:solid gray;
                    border-top:1px solid gray;
                    border-bottom:1px solid gray;
                    border-left:1px solid gray;
                    border-right:1px solid gray;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
                    font-size:18px;
                    font-weight:700;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton:hover{border-left:4px solid gray;border-right:4px solid gray;font-weight:700;}
        ''')
        self.right_fileinput.setStyleSheet('''
        QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                font-size:18px;
                font-weight:500;
                padding:2px 4px;
        }''')
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:12px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.right_labelShowResult.setStyleSheet('''QTextEdit{
            border-top:1px solid gray;
            border-bottom:1px solid gray;
            border-left:1px solid gray;
            border-right:1px solid gray;
            font-size:18px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }''')

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)
        
    def generatLeft(self):
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_close.clicked.connect(self.close)
        self.left_visit.clicked.connect(self.changeWindow)
        self.left_mini.clicked.connect(self.showMinimized)

        self.left_label_1 = QtWidgets.QPushButton("我的看板")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("个性化")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy', color='white'), "分布统计")
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.clicked.connect(self.layoutShow)
        self.left_button_1.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.magnet', color='white'), "聚类分析")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(self.PCAshow)
        self.left_button_2.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.gears', color='white'), "关联规则")
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.clicked.connect(self.associateRulesShow)
        self.left_button_3.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='white'), "更换主题")
        self.left_button_4.setObjectName('left_button')
        self.left_button_4.clicked.connect(self.remainTobedone)
        self.left_button_4.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.music', color='white'), "背景音乐")
        self.left_button_5.setObjectName('left_button')
        self.left_button_5.clicked.connect(self.remainTobedone)
        self.left_button_5.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), "我的数据")
        self.left_button_6.setObjectName('left_button')
        self.left_button_6.clicked.connect(self.remainTobedone)
        self.left_button_6.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_7.clicked.connect(self.contactUs)
        self.left_button_7.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_8.clicked.connect(self.contactUs)
        self.left_button_8.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_9.setObjectName('left_button')
        self.left_button_9.clicked.connect(self.forhelp)
        self.left_button_9.setCursor(QtCore.Qt.PointingHandCursor)
        self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_mini, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
    def generateRight(self):
##########下面创建右上侧文件导入部分
        #创建文件输入入口部件
        self.right_fileProcessTrigger=QtWidgets.QPushButton()
        self.right_fileProcessTrigger.setText("处理")
        self.right_fileinput = QtWidgets.QLineEdit()
        self.right_fileinput.setObjectName("Empty")
        self.right_fileinput.setPlaceholderText("输入文件路径")
        self.right_filebrowser = QtWidgets.QPushButton()
        self.right_filebrowser.setText("浏览")
        self.right_filebrowser.clicked.connect(self.fileInput_button_click)
        self.right_filebrowser.setCursor(QtCore.Qt.PointingHandCursor)
        self.right_fileProcessTrigger.clicked.connect(self.triggerReflect)
        self.right_fileProcessTrigger.setCursor(QtCore.Qt.PointingHandCursor)
        self.right_supportRateInput=QtWidgets.QSpinBox()
        self.right_supportRateInput.setValue(15)###
        self.right_supportRateInput.setSingleStep(1)###
        self.right_supportRateInput.setMaximum(99)###
        self.right_supportRateInput.setMinimum(1)###
        self.right_confidenceRateInput=QtWidgets.QSpinBox()
        self.right_confidenceRateInput.setValue(15)
        self.right_confidenceRateInput.setSingleStep(1)
        self.right_confidenceRateInput.setMaximum(99)
        self.right_confidenceRateInput.setMinimum(1)
        self.right_supportRateTxt=QtWidgets.QLabel()
        self.right_supportRateTxt.setText("支持度阈值(%)")
        self.right_confidenceRateTxt=QtWidgets.QLabel()
        self.right_confidenceRateTxt.setText("置信度阈值(%)")
        #规划文件输入入口布局
        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部文件导入部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)

        self.right_bar_layout.addWidget(self.right_filebrowser,0,8,1,1)
        self.right_bar_layout.addWidget(self.right_fileinput,0,1,1,7)
        self.right_bar_layout.addWidget(self.right_fileProcessTrigger,0,0,1,1)
        self.right_bar_layout.addWidget(self.right_supportRateInput,0,9,1,1)###
        self.right_bar_layout.addWidget(self.right_confidenceRateInput,0,11,1,1)
        self.right_bar_layout.addWidget(self.right_confidenceRateTxt,0,12,1,1)
        self.right_bar_layout.addWidget(self.right_supportRateTxt,0,10,1,1)
        self.right_layout.addWidget(self.right_bar_widget,0,0,1,9)

        # self.right_labelShowResult=QtWidgets.QLabel("")
        self.right_labelShowResult=QtWidgets.QTextEdit()
        self.right_layout.addWidget(self.right_labelShowResult,1,0,8,10)
        self.right_labelShowResult.setText("在上方选择文件并设置支持度阈值和置信度阈值")
    def remainTobedone(self):
        self.right_labelShowResult.setText("正在努力开发中(☄⊙ω⊙)☄")
    def forhelp(self):
        self.right_labelShowResult.setText("在右侧上方选择并上传文件\n点击处理按钮开始数据分析\n在左侧选择展示内容\n关联规则的详细内容将储存于一个xlsx文件中\n该文件位于本程序同级文件夹下")
    def contactUs(self):
        self.right_labelShowResult.setText("开发团队：蓝翔数据挖掘技校\n负责人：SocraLee 邮箱：ledge@pku.edu.cn\n            依泠           邮箱：2664425329@qq.com")
    def layoutShow(self):
        dig.statistics()
        try:
            with open('InteractiveText.json') as obj:
                resultOutput = json.load(obj)
        except:
            self.right_labelShowResult.setText("Result open process failed")
            return

        self.right_labelShowResult.setText(resultOutput)
        dig.plt.show()

    def PCAshow(self):
        dig.PCA_graph()
        self.right_labelShowResult.setText("PCA process finished")
        dig.plt.show()
    def triggerReflect(self):
        support=self.right_supportRateInput.value()
        confidence=self.right_confidenceRateInput.value()
        information=str(confidence)+' '+str(support)
        try:
            with open('Information.json', 'w') as inf:
                json.dump(information,inf)
        except:
            self.right_labelShowResult.setText("Information transportation process failed")
        dig.associateRules()

        with open("InformationBack.json") as ib:
            back = json.load(ib)
        self.right_labelShowResult.setText("Process Finished\n"+back)
    def associateRulesShow(self):
        try:
            with open("arInteractiveText.json") as ij:
                arOut=json.load(ij)
        except:
            self.right_labelShowResult.setText("Result open process failed")
            return
        arOut+="\n关联规则详细结果已生成，请查看工程文件夹下生成的xlsx文件"
        self.right_labelShowResult.setText(arOut)

    def fileInput_button_click(self):
        absolute_path=QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
        if absolute_path:
            cur_path=QtCore.QDir('.')
            relative_path=cur_path.relativeFilePath(str(absolute_path[0]))
            self.right_fileinput.setText(absolute_path[0])
            with open(filename,'w') as f_obj:
                json.dump(absolute_path[0],f_obj)
    def changeWindow(self):
        if self.ifBig:
            self.showNormal()
            self.ifBig=False
        else:
            self.showMaximized()
            self.ifBig=True

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = True
            self._startPos = QtCore.QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

class MyWindow(QtWidgets.QPushButton):

    def __init__(self):
        QtWidgets.QPushButton.__init__(self)

        self.setText("关闭窗口")

        self.clicked.connect(QtWidgets.qApp.quit)

    def load_data(self, sp):
        list = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 75, 90, 100]
        for i in range(1, 101):  # 模拟主程序加载过程
            if i in list:
                a = QtGui.QPixmap("start" + str(i) + ".jpg")
                sp.setPixmap(a)
                sp.showMessage("加载... {0}%".format(i), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
            QtWidgets.qApp.processEvents()  # 允许主进程处理事件
            time.sleep(0.05)  # 加载数据
        time.sleep(0.3)

def main():
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("begin.png"))
    splash.showMessage("加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()  # 显示启动界面
    QtWidgets.qApp.processEvents()  # 处理主进程事件
    window = MyWindow()
    window.setWindowTitle("QSplashScreen类使用")
    window.resize(300, 30)
    window.load_data(splash)  # 加载数据
    window.show()
    splash.finish(window)  # 隐藏启动界面
    window.close()
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
