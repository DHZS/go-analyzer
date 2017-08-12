# -*- coding: utf-8 -*-

'''
获取灰度图像中水平直线、垂直直线的交点坐标

author: Sunny An

date: 2017年4月18日 星期二
'''

import cv2
import numpy as np
import math


# 形态学运算的模板
__kernel = np.ones((3,3), np.uint8)

def get_cross_points(gray_img, canny_thresholds=(100, 255), close_times=1, line_threshold=300, r_error=10, t_error=10*np.pi/180):
    '''
    获取灰度图像中水平直线、垂直直线的交点坐标

    gray_img: 灰度图像

    canny_thresholds: Canny 算法获取图像边界的两个阈值

    close_times: 形态学闭运算次数

    line_threshold: Hough 变换检测直线的投票阈值

    r_error: Hough 变换检测直线时，r 值之差小于 r_error 认为是相似直线

    t_error: Hough 变换检测直线时，theta 值之差小于 t_error 认为是相似直线

    返回 二值图像，numpy 三维数组，前两维表示交点的顺序，最后一维长度为 2 ，表示交点 x, y 坐标
    '''

    # Canny 算法求边界
    canny = cv2.Canny(gray_img, *canny_thresholds)

    # 形态学运算，闭运算(先膨胀，后腐蚀)，填充空隙
    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, __kernel, anchor=(1,1), iterations=close_times)

    # Hough 变换，检测直线
    lines = cv2.HoughLines(close, 1, np.pi / 180, line_threshold)
    if lines is None:
        return close, None
    
    # 只取 ± theta_range 误差内的的水平或垂直直线
    theta_range = 20 * np.pi / 180  # 20°

    # 最终筛选之后的直线
    horizontal_lines = []  # 水平线
    vertical_lines = [] # 垂直线

    for line in lines:
        rho, theta = int(line[0][0]), float(line[0][1])

        # 检测 ± theta_range 误差内的的水平或垂直直线
        line_type = 0  # 1水平线 2垂直线
        if rho >= 0 and theta >= np.pi / 2 - theta_range and theta <= np.pi / 2 + theta_range:
            line_type = 1
            line_list = horizontal_lines
        elif (rho >= 0 and theta >= 0 and theta <= theta_range) \
        or (rho <=0 and theta >= np.pi - theta_range and theta <np.pi):
            line_type = 2
            line_list = vertical_lines
        else:
            # 不在误差范围内，不是水平或垂直直线
            continue


        # 是否找到了相似直线
        found_similar = False
        insert_position = len(line_list)  # 插入直线信息的位置
        # 检查有无相似直线，并按 |rho| 升序排序
        for i, line in enumerate(line_list):
            r = line[0]
            t = line[1]
            
            symbol = rho * r >= 0
            if (symbol is True and abs(rho - r) <= r_error and abs(theta - t) <= t_error) \
            or (symbol is False and abs(rho + r) <= r_error and abs(np.pi - theta - t) <= t_error):
                # 是相似直线
                found_similar = True
                break
            elif abs(rho) < abs(r):
                # rho 长度 小于 r ，应插入 r 之前
                insert_position = i
                break
        
        if not found_similar:
            line_list.insert(insert_position, (rho, theta))

    
    len_h_lines, len_v_lines = len(horizontal_lines), len(vertical_lines)
    if len_h_lines < 3 or len_v_lines < 3:
        # 直线数量不足，认为没找到
        return close, None
    
    # 求得所有交点
    # 创建存放交点的数组
    points = np.empty((len_h_lines, len_v_lines, 2), dtype=int)
    for i in range(len_h_lines):
        c1, s1, r1 = math.cos(horizontal_lines[i][1]), math.sin(horizontal_lines[i][1]), horizontal_lines[i][0]
        for j in range(len_v_lines):
            c2, s2, r2 = math.cos(vertical_lines[j][1]), math.sin(vertical_lines[j][1]), vertical_lines[j][0]
            denominator = s1 * c2 - s2 * c1  # 分母
            x = int(round((r2 * s1 - r1 * s2) / denominator))
            y = int(round((r1 * c2 - r2 * c1) / denominator))
            points[i, j] = x, y

    # 过滤不在棋盘上的直线
    top, bottom, left , right = 0, 0, 0, 0
    #过滤上方水平直线
    for i in range(len_h_lines - 1):
        count = 0
        for j in range(len_v_lines):
            x = int(round(np.average(points[i: i + 2, j, 0])))
            y = int(round(np.average(points[i: i + 2, j, 1])))
            if 255 in close[y, x - 3: x + 3]:
                count += 1
        if count > len_v_lines // 2:
            # 超过一半的点在垂直直线上，认为该直线有效
            top = i
            break
    #过滤下方水平直线
    for i in range(len_h_lines - 2, -1, -1):
        count = 0
        for j in range(len_v_lines):
            x = int(round(np.average(points[i: i + 2, j, 0])))
            y = int(round(np.average(points[i: i + 2, j, 1])))
            if 255 in close[y, x - 3: x + 3]:
                count += 1
        if count > len_v_lines // 2:
            # 超过一半的点在垂直直线上，认为该直线有效
            bottom = i + 1
            break
    #过滤左侧垂直直线
    for i in range(len_v_lines - 1):
        count = 0
        for j in range(len_h_lines):
            x = int(round(np.average(points[j, i: i + 2, 0])))
            y = int(round(np.average(points[j, i: i + 2, 1])))
            if 255 in close[y - 3: y + 3, x]:
                count += 1
        if count > len_h_lines // 2:
            # 超过一半的点在垂直直线上，认为该直线有效
            left = i
            break
    #过滤右侧垂直直线
    for i in range(len_v_lines - 2, -1, -1):
        count = 0
        for j in range(len_h_lines):
            x = int(round(np.average(points[j, i: i + 2, 0])))
            y = int(round(np.average(points[j, i: i + 2, 1])))
            if 255 in close[y, x - 3: x + 3]:
                count += 1
        if count > len_h_lines // 2:
            # 超过一半的点在垂直直线上，认为该直线有效
            right = i + 1
            break
    
    # 精确地坐标
    # horizontal_lines = horizontal_lines[top: bottom + 1]
    # vertical_lines = vertical_lines[left: right + 1]
    points = points[top: bottom + 1, left: right + 1]
    
    return close, points
