# -*- coding: utf-8 -*-

'''
围棋视频分析程序

author: Sunny An

date: 2017年5月16日 星期二
'''


import os
import sys
import itertools
import math

import cv2
import numpy as np

import go_process as gp
from cross_point import get_cross_points




class GoVideoAnalyzer(object):
    '围棋视频分析类'

    def _is_black(self, hsv):
        '是否是黑色棋子'
        # return (abs(hsv - _black_hsv) <= self.qizi_color_threshold).all()
        return abs(float(hsv[2] - self._black_hsv[2])) <= self.qizi_color_threshold


    def _is_white(self, hsv):
        '是否是白色棋子'
        return (abs(hsv - self._white_hsv) <= self.qizi_color_threshold).all()

    
    def _get_qizi_area_fun(self, r):
        '传入棋子范围宽度，返回获取棋子范围函数'
        # np.s_[] 返回切片元组 tuple of slice
        return lambda x, y: np.s_[y+r:y+2*r,x-2*r:x-r,:]
    

    def _draw_board_coordinate(self, im):
        '画棋盘坐标'
        for x in range(self.points.shape[1]):
            qizi_x, qizi_y = self.points[0, x]
            cv2.putText(im, str(x), (qizi_x, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        for y in range(self.points.shape[0]):
            qizi_x, qizi_y = self.points[y, 0]
            cv2.putText(im, str(y), (10, qizi_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    

    def __init__(self):   
        self._black_hsv = np.array([0, 0, 20])  # 黑色棋子 hsv 颜色  
        self._white_hsv = np.array([19, 24, 230.5])  # 白色棋子 hsv 颜色
        self.qizi_color_threshold = 20  # 棋子 hsv 颜色允许阈值

        self.cap = None  # cv2 capture
        self.frame_count = 0  # 视频总帧数
        self.cur_frame_count = 0  # 当前帧数
        self.frame_step = 1  # 播放帧数步长
        self.go_board_im = None  # 围棋棋盘图像

        self.go_process = None  # 创建围棋进程记录对象
        self.points = None  # 交点坐标
        self.r = 0  # 棋子半径
        self.qizi_area = None  # 棋子范围函数

    

    def load_video(self, video_path, frame_step=None):
        '加载视频文件'
        self.cap = cv2.VideoCapture(video_path)

        if self.cap.isOpened() == False:
            return (False, None)

        self.frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频总帧数
        if frame_step is None:
             self.frame_step = int(self.cap.get(cv2.CAP_PROP_FPS)) // 3  # 播放帧数步长
        else:
            frame_step = int(frame_step)
            self.frame_step = frame_step if frame_step > 0 else 1
        
        # 读取第一帧图像
        ret, self.go_board_im = self.cap.read()
        return (True, self.go_board_im)
    

    def analyze_cross_point(self):
        '分析棋盘交叉点'
        # 转化为灰度图像
        im_gray = cv2.cvtColor(self.go_board_im, cv2.COLOR_BGR2GRAY)

        kw = {'canny_thresholds': (100, 255), 'close_times': 1, \
               'line_threshold': 500, 'r_error': 10, 't_error': 10*np.pi / 180}

        bin_img, self.points = get_cross_points(im_gray, **kw)
    
        # 是否成功找到交点
        if self.points is None:
            return (False, None)
        
        self.r = int(self.points[0, 1, 0] - self.points[0, 0, 0])  # 获取棋子半径
        self.qizi_area = self._get_qizi_area_fun(self.r // 6)  # 棋子范围函数
        self.go_process = gp.GoProcess(self.points.shape[:2])  # 创建围棋进程记录对象

        return (True, self.points)
    

    def mark_cross_point(self, radius=5, color=(0,0,255)):
        '标记交叉点'
        # 将二维点坐标用一维存储
        flat_points = self.points.reshape(self.points.shape[0] * self.points.shape[1], 2)

        im_mark = self.go_board_im.copy()  # 拷贝棋盘

        for x, y in flat_points:
            cv2.circle(im_mark, (x, y), radius, color)
        self._draw_board_coordinate(im_mark)
        
        return im_mark
    

    def next_round(self):
        '获取下一个围棋回合'

        # 直到有棋子落子，跳出
        while True:
            self.cur_frame_count += self.frame_step
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_count)
            ret, frame = self.cap.read()

            if ret == False:
                return (False, )

            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 棋局 hsv 颜色模式
            self.go_process.round_start()
            for y in range(self.points.shape[0]):
                for x in range(self.points.shape[1]):
                    # 确定棋子颜色
                    # 分别计算 h s v 的中值
                    qizi_x, qizi_y = self.points[y, x]
                    hsv = np.median(frame_hsv[self.qizi_area(qizi_x, qizi_y)], axis=(0, 1))
                    if self._is_black(hsv):
                        # 黑色棋子
                        self.go_process.found(x, y, gp.QI_BLACK)
                    elif self._is_white(hsv):
                        # 白色棋子
                        self.go_process.found(x, y, gp.QI_WHITE)
            rd0, rd = self.go_process.round_end()  # 回合结束，返回回合信息（可能有1回合或2回合）

            if rd0 is None and rd is None:
                # 无变化
                continue
            
            # 画棋子序号
            down_list = self.go_process.get_down_list()
            for x, y, no, qizi_type in down_list:
                color = (255, 255, 255) if qizi_type == gp.QI_BLACK else (0, 0, 0)
                qizi_x, qizi_y = self.points[y, x]
                # 计算绘制文字的尺寸
                text_size = cv2.getTextSize(str(no), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                # 将文字绘制在棋子中心
                pos = (qizi_x - text_size[0] // 2, qizi_y + text_size[1] // 2)
                cv2.putText(frame, str(no), pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            self._draw_board_coordinate(frame)

            return (True, frame, rd0, rd)
        
        return (False, )




if __name__ == '__main__':
    analyzer = GoVideoAnalyzer()
    analyzer.load_video(r'C:\Users\Jiaoyang\Videos\Captures\1.mp4')
    analyzer.analyze_cross_point()
    analyzer.mark_cross_point()
    print(analyzer.next_round())
        



        
    





