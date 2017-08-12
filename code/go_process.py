# -*- coding: utf-8 -*-

'''
围棋进程记录
'''

import numpy as np

'空白'
QI_BLANK = 0
'黑棋'
QI_BLACK = 1
'白棋'
QI_WHITE = 2

'动作-落子'
ACT_DOWN = 1
'动作-落子提子'
ACT_DOWN_TAKE = 2
'动作-停一手'
ACT_GIVE_UP = 3


class Round(object):
    '回合动作'
    
    def __init__(self):
        '回合'
        self.round_no = None
        '当前哪一方：黑、白'
        self.who = None
        '动作：落子，落子提子，放弃'
        self.action = None
        '落子坐标：(x，y, 序号)'
        self.down = None
        '提子坐标：[(x, y, 序号), (x, y, 序号)...]'
        self.take = []
    
    
    def __str__(self):
        if self.action == ACT_GIVE_UP:
            t = '第 %d 回合\n%s方停一手' % (self.round_no, '黑' if self.who == QI_BLACK else '白')
        else:
            t = '第 %d 回合\n%s方落子坐标 (%d, %d)' % (self.round_no, '黑' if self.who == QI_BLACK else '白', self.down[0], self.down[1])
        if self.action == ACT_DOWN_TAKE:
            t1 = []
            for x, y, i in self.take:
                t1.append('(%d, %d)' % (x, y))
            t = t + '\n提 %d 子: %s' % (len(self.take), ', '.join(t1))
        return t
    

    __repr__ = __str__



class GoProcess(object):
    '围棋进程记录类'

    # 回合开始标志
    __round_start = 1
    # 回合结束表示
    __round_end = 2


    def __init__(self, shape):
        '棋盘大小'
        self.shape = shape
        '棋局记录'
        self.process = []
        '史棋盘棋子布局'
        self.__qiju1 = np.zeros(shape, dtype=int)
        '新棋盘棋子布局'
        self.__qiju2 = None
        '回合状态'
        self.__round_status = self.__round_end
        '落子计数'
        self.__down_count = 0
        '落子棋子坐标'
        self.__down_list = []
    

    def round_start(self):
        '回合开始'
        self.__qiju2 = np.zeros(self.shape, dtype=int)
        self.__round_status = self.__round_start
    

    def found(self, x, y, qizi_type):
        '发现棋子\n\nx, y: 坐标\n\nqizi_type: 棋子类型'
        self.__qiju2[y, x] = qizi_type
    

    def round_end(self):
        '回合结束'
        status = self.__qiju2 - self.__qiju1

        blacks = []  # 记录黑棋坐标
        whites = []  # 记录白棋坐标
        take_blacks = []  # 记录被提黑棋坐标
        take_whites = []  # 记录被提白棋坐标
        rd0 = None  # 如有停一手回合，记录之
        rd = Round()  # 记录当前回合

        for y in range(status.shape[0]):
            for x in range(status.shape[1]):
                s = status[y, x]
                if s == QI_BLACK:
                    blacks.append((x, y))
                elif s == QI_WHITE:
                    whites.append((x, y))
                elif s == -QI_BLACK:
                    take_blacks.append((x, y))
                elif s == -QI_WHITE:
                    take_whites.append((x, y))
        
        len_b = len(blacks)
        len_w = len(whites)
        len_tb = len(take_blacks)
        len_tw = len(take_whites)

        if len_b == 1 and len_tw == 0 and len_w == 0 and len_tb == 0:
            # 黑棋落子

            # 判断上一回合是否是黑棋，如果是，说明白棋停一手
            if len(self.process) != 0 and self.process[-1].who == QI_BLACK:
                rd0 = Round()
                rd0.round_no = len(self.process) + 1
                rd0.who = QI_WHITE
                rd0.action = ACT_GIVE_UP
                self.process.append(rd0)

            self.__down_count += 1

            rd.round_no = len(self.process) + 1
            rd.who = QI_BLACK
            rd.action = ACT_DOWN
            x, y = blacks[0]
            rd.down = (x, y, self.__down_count)

            self.process.append(rd)
            self.__down_list.append((x, y, self.__down_count, QI_BLACK))
        elif len_b == 1 and len_tw > 0 and len_w == 0 and len_tb == 0:
            # 黑棋落子，白棋被提子

            # 判断上一回合是否是黑棋，如果是，说明白棋停一手
            if len(self.process) != 0 and self.process[-1].who == QI_BLACK:
                rd0 = Round()
                rd0.round_no = len(self.process) + 1
                rd0.who = QI_WHITE
                rd0.action = ACT_GIVE_UP
                self.process.append(rd0)
            
            self.__down_count += 1

            rd.round_no = len(self.process) + 1
            rd.who = QI_BLACK
            rd.action = ACT_DOWN_TAKE
            x, y = blacks[0]
            rd.down = (x, y, self.__down_count)
            for x, y in take_whites:
                no = self.__take_in_down_list(x, y)
                rd.take.append((x, y, no))
            
            self.process.append(rd)
            self.__down_list.append((x, y, self.__down_count, QI_BLACK))
        elif len_w == 1 and len_tb == 0 and len_b == 0 and len_tw == 0:
            # 白棋落子

            # 判断上一回合是否是白棋，如果是，说明黑棋停一手
            if len(self.process) != 0 and self.process[-1].who == QI_WHITE:
                rd0 = Round()
                rd0.round_no = len(self.process) + 1
                rd0.who = QI_BLACK
                rd0.action = ACT_GIVE_UP
                self.process.append(rd0)
            
            self.__down_count += 1

            rd.round_no = len(self.process) + 1
            rd.who = QI_WHITE
            rd.action = ACT_DOWN
            x, y = whites[0]
            rd.down = (x, y, self.__down_count)

            self.process.append(rd)
            self.__down_list.append((x, y, self.__down_count, QI_WHITE))
        elif len_w == 1 and len_tb > 0 and len_b == 0 and len_tw == 0:
            # 白棋落子，黑棋被提子

            # 判断上一回合是否是白棋，如果是，说明黑棋停一手
            if len(self.process) != 0 and self.process[-1].who == QI_WHITE:
                rd0 = Round()
                rd0.round_no = len(self.process) + 1
                rd0.who = QI_BLACK
                rd0.action = ACT_GIVE_UP
                self.process.append(rd0)

            self.__down_count += 1

            rd.round_no = len(self.process) + 1
            rd.who = QI_WHITE
            rd.action = ACT_DOWN_TAKE
            x, y = whites[0]
            rd.down = (x, y, self.__down_count)
            for x, y in take_blacks:
                no = self.__take_in_down_list(x, y)
                rd.take.append((x, y, no))
            
            self.process.append(rd)
            self.__down_list.append((x, y, self.__down_count, QI_WHITE))
        
        self.__round_status = self.__round_end

        if rd.who == None:
            # 其他落子情况
            return None, None
        # 更新棋盘
        self.__qiju1 = self.__qiju2
        return rd0, rd
    

    def __take_in_down_list(self, _x, _y, _down_list=None):
        '在 down_list 中提子，返回该棋子 down_count'
        if _down_list == None:
            _down_list = self.__down_list
        
        for i, (x, y, no, qi_type) in enumerate(_down_list):
            if x == _x and y == _y:
                _down_list.pop(i)
                return no
        return None
    

    def get_down_list(self, round_no=None):
        '''获得指定回合落子状态

        round_no: 指定的回合，None 表示到最后一回合
        '''
        if round_no == None:
            round_no = len(self.process)
        
        down_list = []
        for i in range(round_no):
            rd = self.process[i]
            if rd.action == ACT_GIVE_UP:
                # 如果停一手，down 为 None
                continue
            x, y, no = rd.down
            down_list.append((x, y, no, rd.who))
            for x, y, no in rd.take:
                self.__take_in_down_list(x, y, down_list)
        
        return down_list
    

    def get_sgf_text(self, round_no=None):
        '''获取sgf棋谱文本

        round_no: 指定的回合，None 表示到最后一回合
        '''
        co = 'abcdefghijklmnopqrstuvwxyz'  # 棋谱坐标
        text = ''  # 描述信息

        if round_no == None:
            round_no = len(self.process)
        
        for i in range(round_no):
            rd = self.process[i]
            who = ';B[{}{}]' if rd.who == QI_BLACK else ';W[{}{}]'
            if rd.down == None:
                text += who.format('', '')
            else:
                text += who.format(co[rd.down[0]], co[rd.down[1]])
        
        return '(;SZ[{}]\n{})'.format(self.shape[0], text)
            
        

        


        



if __name__ == '__main__':
    # 测试
    go_process = GoProcess((9, 9))

    go_process.round_start()
    go_process.found(0, 0, QI_WHITE)
    go_process.round_end()

    go_process.round_start()
    go_process.found(0, 0, QI_WHITE)
    go_process.found(0, 1, QI_BLACK)
    go_process.round_end()

    go_process.round_start()
    go_process.found(0, 0, QI_WHITE)
    go_process.found(0, 1, QI_BLACK)
    go_process.found(1, 1, QI_WHITE)
    go_process.round_end()

    go_process.round_start()
    go_process.found(0, 1, QI_BLACK)
    go_process.found(1, 1, QI_WHITE)
    go_process.found(1, 0, QI_BLACK)
    go_process.round_end()

    for rd in go_process.process:
        print(rd)
        print('\r\n')
    
    print(go_process.get_down_list())
    print(go_process.get_sgf_text())

