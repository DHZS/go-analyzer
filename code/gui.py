# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui1.ui'
#
# Created: Fri May 19 17:11:07 2017
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1025, 987)
        self.central_widget = QtWidgets.QWidget(main_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.central_widget.setObjectName("central_widget")
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName("vertical_layout")
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.label_video = QtWidgets.QLabel(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_video.sizePolicy().hasHeightForWidth())
        self.label_video.setSizePolicy(sizePolicy)
        self.label_video.setMinimumSize(QtCore.QSize(600, 600))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_video.setFont(font)
        self.label_video.setMouseTracking(False)
        self.label_video.setAlignment(QtCore.Qt.AlignCenter)
        self.label_video.setObjectName("label_video")
        self.horizontal_layout.addWidget(self.label_video)
        self.vertical_layout_2 = QtWidgets.QVBoxLayout()
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.btn_cross = QtWidgets.QPushButton(self.central_widget)
        self.btn_cross.setAutoDefault(False)
        self.btn_cross.setDefault(False)
        self.btn_cross.setFlat(False)
        self.btn_cross.setObjectName("btn_cross")
        self.vertical_layout_2.addWidget(self.btn_cross)
        self.btn_next = QtWidgets.QPushButton(self.central_widget)
        self.btn_next.setObjectName("btn_next")
        self.vertical_layout_2.addWidget(self.btn_next)
        self.btn_auto = QtWidgets.QPushButton(self.central_widget)
        self.btn_auto.setCheckable(True)
        self.btn_auto.setChecked(False)
        self.btn_auto.setAutoRepeat(False)
        self.btn_auto.setObjectName("btn_auto")
        self.vertical_layout_2.addWidget(self.btn_auto)
        self.btn_sgf = QtWidgets.QPushButton(self.central_widget)
        self.btn_sgf.setObjectName("btn_sgf")
        self.vertical_layout_2.addWidget(self.btn_sgf)
        self.group_box = QtWidgets.QGroupBox(self.central_widget)
        self.group_box.setMinimumSize(QtCore.QSize(200, 0))
        self.group_box.setObjectName("group_box")
        self.label = QtWidgets.QLabel(self.group_box)
        self.label.setGeometry(QtCore.QRect(10, 30, 81, 18))
        self.label.setObjectName("label")
        self.edit_round = QtWidgets.QLineEdit(self.group_box)
        self.edit_round.setGeometry(QtCore.QRect(90, 25, 100, 25))
        self.edit_round.setFrame(False)
        self.edit_round.setReadOnly(True)
        self.edit_round.setObjectName("edit_round")
        self.edit_black = QtWidgets.QLineEdit(self.group_box)
        self.edit_black.setGeometry(QtCore.QRect(90, 75, 100, 25))
        self.edit_black.setFrame(False)
        self.edit_black.setReadOnly(True)
        self.edit_black.setObjectName("edit_black")
        self.label_2 = QtWidgets.QLabel(self.group_box)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 81, 18))
        self.label_2.setObjectName("label_2")
        self.edit_white = QtWidgets.QLineEdit(self.group_box)
        self.edit_white.setGeometry(QtCore.QRect(90, 125, 100, 25))
        self.edit_white.setFrame(False)
        self.edit_white.setReadOnly(True)
        self.edit_white.setObjectName("edit_white")
        self.label_3 = QtWidgets.QLabel(self.group_box)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 81, 18))
        self.label_3.setObjectName("label_3")
        self.edit_who = QtWidgets.QLineEdit(self.group_box)
        self.edit_who.setGeometry(QtCore.QRect(90, 175, 100, 25))
        self.edit_who.setFrame(False)
        self.edit_who.setReadOnly(True)
        self.edit_who.setObjectName("edit_who")
        self.label_4 = QtWidgets.QLabel(self.group_box)
        self.label_4.setGeometry(QtCore.QRect(10, 180, 81, 18))
        self.label_4.setObjectName("label_4")
        self.edit_where = QtWidgets.QLineEdit(self.group_box)
        self.edit_where.setGeometry(QtCore.QRect(90, 225, 100, 25))
        self.edit_where.setFrame(False)
        self.edit_where.setReadOnly(True)
        self.edit_where.setObjectName("edit_where")
        self.label_5 = QtWidgets.QLabel(self.group_box)
        self.label_5.setGeometry(QtCore.QRect(10, 230, 81, 18))
        self.label_5.setObjectName("label_5")
        self.edit_take_no = QtWidgets.QLineEdit(self.group_box)
        self.edit_take_no.setGeometry(QtCore.QRect(90, 275, 100, 25))
        self.edit_take_no.setMaxLength(32766)
        self.edit_take_no.setFrame(False)
        self.edit_take_no.setReadOnly(True)
        self.edit_take_no.setObjectName("edit_take_no")
        self.label_6 = QtWidgets.QLabel(self.group_box)
        self.label_6.setGeometry(QtCore.QRect(10, 280, 81, 18))
        self.label_6.setObjectName("label_6")
        self.edit_take_where = QtWidgets.QLineEdit(self.group_box)
        self.edit_take_where.setGeometry(QtCore.QRect(90, 325, 100, 25))
        self.edit_take_where.setFrame(False)
        self.edit_take_where.setReadOnly(True)
        self.edit_take_where.setObjectName("edit_take_where")
        self.label_7 = QtWidgets.QLabel(self.group_box)
        self.label_7.setGeometry(QtCore.QRect(10, 330, 81, 18))
        self.label_7.setObjectName("label_7")
        self.label_info = QtWidgets.QLabel(self.group_box)
        self.label_info.setEnabled(True)
        self.label_info.setGeometry(QtCore.QRect(10, 380, 181, 81))
        self.label_info.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_info.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_info.setTextFormat(QtCore.Qt.AutoText)
        self.label_info.setScaledContents(False)
        self.label_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_info.setWordWrap(True)
        self.label_info.setObjectName("label_info")
        self.vertical_layout_2.addWidget(self.group_box)
        self.horizontal_layout.addLayout(self.vertical_layout_2)
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.list_widget_log = QtWidgets.QListWidget(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_widget_log.sizePolicy().hasHeightForWidth())
        self.list_widget_log.setSizePolicy(sizePolicy)
        self.list_widget_log.setMinimumSize(QtCore.QSize(0, 200))
        self.list_widget_log.setObjectName("list_widget_log")
        self.vertical_layout.addWidget(self.list_widget_log)
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1025, 30))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        main_window.setMenuBar(self.menubar)
        self.action_open = QtWidgets.QAction(main_window)
        self.action_open.setEnabled(True)
        self.action_open.setObjectName("action_open")
        self.action_exit = QtWidgets.QAction(main_window)
        self.action_exit.setObjectName("action_exit")
        self.action_about = QtWidgets.QAction(main_window)
        self.action_about.setObjectName("action_about")
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_exit)
        self.menu_help.addAction(self.action_about)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(main_window)
        self.action_exit.triggered.connect(main_window.close)
        self.btn_cross.clicked.connect(main_window.on_btn_cross_click)
        self.action_open.triggered.connect(main_window.on_action_open_click)
        self.action_about.triggered.connect(main_window.on_action_about_click)
        self.btn_next.clicked.connect(main_window.on_btn_next_click)
        self.btn_auto.clicked.connect(main_window.on_btn_auto_click)
        self.btn_sgf.clicked.connect(main_window.on_btn_sgf_click)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "围棋进程分析程序"))
        self.label_video.setText(_translate("main_window", "请选择视频"))
        self.btn_cross.setText(_translate("main_window", "获取棋盘交点"))
        self.btn_next.setText(_translate("main_window", "下一回合"))
        self.btn_auto.setText(_translate("main_window", "自动模式"))
        self.btn_sgf.setText(_translate("main_window", "保存棋谱"))
        self.group_box.setTitle(_translate("main_window", "棋局信息"))
        self.label.setText(_translate("main_window", "当前回合"))
        self.edit_round.setText(_translate("main_window", "9999"))
        self.edit_black.setText(_translate("main_window", "9999"))
        self.label_2.setText(_translate("main_window", "黑棋总数"))
        self.edit_white.setText(_translate("main_window", "9999"))
        self.label_3.setText(_translate("main_window", "白棋总数"))
        self.edit_who.setText(_translate("main_window", "黑子"))
        self.label_4.setText(_translate("main_window", "执棋方"))
        self.edit_where.setText(_translate("main_window", "(10,10)"))
        self.label_5.setText(_translate("main_window", "落子坐标"))
        self.edit_take_no.setText(_translate("main_window", "0"))
        self.label_6.setText(_translate("main_window", "提子数目"))
        self.edit_take_where.setText(_translate("main_window", "无"))
        self.label_7.setText(_translate("main_window", "提子坐标"))
        self.label_info.setText(_translate("main_window", "<html><head/><body><p><span style=\" color:#ff0000;\">注：上一回合，黑棋方放弃</span></p></body></html>"))
        self.menu_file.setTitle(_translate("main_window", "文件"))
        self.menu_help.setTitle(_translate("main_window", "帮助"))
        self.action_open.setText(_translate("main_window", "打开"))
        self.action_exit.setText(_translate("main_window", "退出"))
        self.action_about.setText(_translate("main_window", "关于"))

