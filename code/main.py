# -*- coding: utf-8 -*-

'''
主程序
'''

import os
import sys
import threading
import time

os.environ['QT_DRIVER'] = 'PyQt5'  # 设置当前 Qt 版本
import qimage2ndarray

from PyQt5 import QtWidgets, QtGui, QtCore

import go_process as gp
from go_video_analyzer import GoVideoAnalyzer
from gui import Ui_main_window



class Window(QtWidgets.QMainWindow):

    def cv2_to_pixmap(self, cv_img):
        'opncv 打开的图片转 QImage'
        return QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(cv_img[:,:,::-1]))


    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self._init_ui_and_data()

    
    def _init_ui_and_data(self):
        '初始化ui'
        self.ui.btn_cross.setEnabled(False)
        self.ui.btn_next.setEnabled(False)
        self.ui.btn_auto.setEnabled(False)
        self.ui.btn_sgf.setEnabled(False)

        self.ui.edit_round.setText('0')
        self.ui.edit_black.setText('0')
        self.ui.edit_white.setText('0')
        self.ui.edit_who.setText('无')
        self.ui.edit_where.setText('无')
        self.ui.edit_take_no.setText('0')
        self.ui.edit_take_where.setText('无')

        self.ui.label_info.setVisible(False)

        self.black_no = 0  # 黑白棋子数量
        self.white_no = 0
        self.is_end = False  # 是否分析完毕
        self.analyzer = GoVideoAnalyzer()  # 视频分析对象

    
    def add_log(self, message):
        '添加日志'
        item = QtWidgets.QListWidgetItem()
        item.setText(message)
        # 根据数据序号，设置背景颜色
        if self.ui.list_widget_log.count() % 2 == 1:
            brush = QtGui.QBrush(QtGui.QColor(240, 250, 255), QtCore.Qt.SolidPattern)
            item.setBackground(brush)
        self.ui.list_widget_log.addItem(item)
        self.ui.list_widget_log.setCurrentRow(self.ui.list_widget_log.count()-1)
    

    def get_color_text(self, text, color=(255,0,0)):
        '获得带颜色的文本'
        template = '<html><head/><body><p><span style=" color:rgb{};">{}</span></p></body></html>'
        return template.format(color, text)
    

    def on_action_open_click(self):
        '选择文件菜单'
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, '请选择围棋视频文件', '', 'Video Files (*.mp4 *.avi)')[0]
        if file_name:
            if self.analyzer.cap is not None:
                # 如重新选取文件，初始化数据
                self.ui.list_widget_log.clear()  # 清空
                self._init_ui_and_data()
            self.add_log('读取视频文件 {}'.format(file_name))  # 写日志
            self._init_video(file_name)
        

    
    def on_action_about_click(self):
        '关于菜单'
        QtWidgets.QMessageBox.information(self, 'About', '毕业设计作品\nSunny An 版权所有')
    
    def on_btn_cross_click(self):
        '获取交点按钮'
        rets = self.analyzer.analyze_cross_point()

        if rets[0] == False:
            self.add_log('分析棋盘交点失败')  # 写日志
            return
        else:
            self.add_log('分析棋盘交点成功')   # 写日志
        
        # 标记交点
        im = self.analyzer.mark_cross_point()
        self.ui.label_video.setPixmap(self.cv2_to_pixmap(im))
        
        self.add_log('棋盘大小 {}×{}'.format(rets[1].shape[0], rets[1].shape[1]))   # 写日志

        self.ui.btn_cross.setEnabled(False)  # 恢复按钮
        self.ui.btn_next.setEnabled(True)  # 恢复按钮
        self.ui.btn_auto.setEnabled(True)  # 恢复按钮
    

    def on_btn_next_click(self):
        '下一回合按钮'
        t = threading.Thread(target=self._next_round)
        t.start()
    

    def on_btn_auto_click(self):
        '自动模式按钮'
        if self.ui.btn_auto.isChecked():
            t = threading.Thread(target=self._auto_next)
            t.start()
        else:
            self.ui.btn_auto.setEnabled(False)
    

    def on_btn_sgf_click(self):
        '保存棋谱按钮'
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, '将棋谱保存到...', '', 'Smart Game Format (*.sgf)')[0]
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.analyzer.go_process.get_sgf_text())
            self.add_log('保存棋谱文件成功，路径 {}'.format(file_name))  # 写日志
        
    
    def _init_video(self, video_path):
        '初始化视频'
        rets = self.analyzer.load_video(video_path)

        if rets[0] == False:
            self.add_log('读取失败')  # 写日志
            return
        else:
            self.add_log('读取成功')   # 写日志

        frame_count = self.analyzer.frame_count  # 视频总帧数
        im = rets[1]  # 棋盘图像

        self.add_log('视频尺寸 {}×{}, 视频总帧数 {}'.format(im.shape[1], im.shape[0], frame_count))   # 写日志

        self.ui.label_video.setMinimumSize(im.shape[1], im.shape[0])
        self.ui.label_video.setPixmap(self.cv2_to_pixmap(im))

        self.ui.btn_cross.setEnabled(True)  # 恢复按钮
    

    def _next_round(self, is_auto=False):
        '分析下一回合'
        self.ui.label_info.setVisible(False)  # 不可见
        self.ui.btn_next.setEnabled(False)  # 不可用
        rets = self.analyzer.next_round()

        if rets[0] == False:
            self.is_end = True
            self.add_log('分析完成！')  # 写日志

            # 输出提示信息
            self.ui.btn_cross.setEnabled(False)  # 恢复按钮
            self.ui.btn_next.setEnabled(False)  # 恢复按钮
            self.ui.btn_auto.setEnabled(False)  # 恢复按钮
            self.ui.btn_sgf.setEnabled(True)  # 恢复按钮

            self.ui.label_info.setText(self.get_color_text('棋局结束！'))
            self.ui.label_info.setVisible(True)  # 可见

            return
        
        im, rd0, rd = rets[1:]  # 获取返回的 image 和棋局信息
        self.ui.label_video.setPixmap(self.cv2_to_pixmap(im))

        if rd0 != None:
            self.add_log(str(rd0))  # 写日志
        self.add_log(str(rd))  # 写日志
        
        # 输出提示信息
        if rd0 != None:
            self.ui.label_info.setText(str(rd0))
            self.ui.label_info.setVisible(True)  # 可见
        self.ui.edit_round.setText(str(rd.round_no))  # 回合数
        take_no = len(rd.take)  # 提子数目
        if rd.who == gp.QI_BLACK:
            who = '黑棋'
            self.black_no += 1
            self.white_no -= take_no
        else:
            who = '白棋'
            self.white_no += 1
            self.black_no -= take_no
        self.ui.edit_black.setText(str(self.black_no))  # 黑棋总数
        self.ui.edit_white.setText(str(self.white_no))  # 白棋总数
        self.ui.edit_who.setText(who)  # 下棋方
        self.ui.edit_where.setText('{}({},{})'.format(rd.down[2], rd.down[0], rd.down[1]))  # 落子位置
        self.ui.edit_take_no.setText(str(take_no))  # 提子数目
        if take_no == 0:
            self.ui.edit_take_where.setText('无')
        else:
            temp = []
            for x, y, no in rd.take:
                temp.append('{}({},{})'.format(no, x, y))
                self.ui.edit_take_where.setText(', '.join(temp))  # 提子坐标
        
        if is_auto == False:
            self.ui.btn_next.setEnabled(True)  # 可用
    

    def _auto_next(self):
        '自动下一回合'
        while self.ui.btn_auto.isChecked() and self.is_end == False:
            t = threading.Thread(target=self._next_round, args=(True,))
            t.start()
            t.join()
        
        if self.is_end == False:
            self.ui.btn_auto.setEnabled(True)
            self.ui.btn_next.setEnabled(True)
        else:
            self.ui.btn_auto.setChecked(False)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())

