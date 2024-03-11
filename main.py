import tkinter as tk
from functools import partial

from judge import *

version = 1.0  # 版本号

participants = []
for i in range(5):
    participants.append(Count())  # 创建五个Count对象


class GUI:
    def __init__(self):
        self.puke_known = None  # 已知牌
        self.puke_all = None  # 所有牌
        self.number = None  # 人数
        self.color = None  # 花色
        self.p = None  # 标志位
        self.background_label = None  # 背景标签
        self.canvas = None  # 画布
        self.photo = None  # 图片
        self.probability = [0, 0, 0, 0, 0]  # 概率列表
        self.label_probability = None  # 概率标签
        self.label = None  # 标签
        self.buttons_number = None  # 数字按钮
        self.buttons_color = None  # 花色按钮
        self.labels = None  # 标签
        self.puke = []  # 牌
        self.stop = []  # 停止标志位
        self.n = 0  # 人数
        self.root = tk.Tk()  # 创建主窗口
        self.root.title('凡跃港式概率实时显示%.1f(designed by poke knight)' % version)  # 设置窗口标题
        self.root.geometry("500x500+0+0")  # 设置窗口大小和位置
        self.interface0()  # 调用界面

    # 第一个页面
    def interface0(self):
        """创建第一个页面界面"""
        self.clear_widgets()
        # 创建提示标签
        prompt_label = tk.Label(self.root, text="宝子，有几个人一起梭哈？", font=("黑体", 16), fg="black")
        prompt_label.place(relx=0.5, rely=0.3, anchor='center')

        # 创建按钮
        button_positions = [(0.1, 0.35), (0.35, 0.35), (0.6, 0.35), (0.85, 0.35)]
        for num, num_players in enumerate(range(2, 6)):
            button = tk.Button(self.root, font=("黑体", 20, "bold"), text=str(num_players), cursor='hand2',
                               command=lambda number=num_players: self.callback0(number))
            button.place(relx=button_positions[num][0], rely=button_positions[num][1], anchor='nw')

    # 第二个页面
    def interface1(self):
        """创建第二个页面界面"""

        # 初始化牌局信息
        self.p = [1, 1, 1, 1, 1]  # 第几张牌
        self.color = ['红桃', '方块', '梅花', '黑桃']  # 花色
        self.number = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.puke_all = [[x, y] for x in self.color for y in self.number]  # 所有牌
        self.puke_known = []  # 已知的牌

        # 创建玩家信息标签
        self.labels = []
        for player_index in range(self.n):
            label_text = "第%d个人的第%d张牌？" % (player_index + 1, self.p[player_index])
            label = tk.Label(self.root, text=label_text, font="黑体")
            label.place(relx=0, rely=(player_index * 4 + 0) / self.n / 4, anchor='nw')
            self.labels.append(label)

        # 创建牌型概率信息标签
        self.label_probability = []
        for player_index in range(self.n):
            label_text = "[同花顺，四条，葫芦，同花，顺子，三条，两对，一对]"
            label = tk.Label(self.root, text=label_text, font=("Helvetica", 10))
            label.place(relx=0, rely=(player_index * 4 + 3) / self.n / 4, anchor='nw')
            self.label_probability.append(label)

        # 创建花色按钮
        self.buttons_color = []
        for player_index in range(self.n):
            for j, color in enumerate(self.color):
                button = tk.Button(self.root, text=color, font="黑体", cursor='hand2')
                button.place(relx=j / len(self.color), rely=(player_index * 4 + 2) / self.n / 4, anchor='nw')
                self.buttons_color.append(button)
                self.buttons_color[player_index * 4 + j].config(command=partial(self.callback1, player_index, j))

        # 创建数字按钮
        self.buttons_number = []
        for player_index in range(self.n):
            for j, num in enumerate(self.number):
                button = tk.Button(self.root, text=num, font="黑体", cursor='hand2')
                button.place(relx=j / len(self.number), rely=(player_index * 4 + 1) / self.n / 4, anchor='nw')
                self.buttons_number.append(button)
                self.buttons_number[player_index * 8 + j].config(command=partial(self.callback2, player_index, j))

        # 绑定退格键事件到返回第一个页面的方法
        self.root.bind("<BackSpace>", lambda event: self.interface0())

    # 在第一个页面按下按钮后，给self.n赋值，清空并打开第二个页面
    def callback0(self, value):
        self.n = int(value)
        self.puke = [[[], [], [], [], []] for _ in range(self.n)]
        self.stop = [[0, 0] for _ in range(self.n)]
        self.clear_widgets()
        self.interface1()

    def callback1(self, x, y):
        if self.stop[x][0] == 0:
            # 添加所选花色到对应玩家的牌堆中
            self.puke[x][self.p[x] - 1].append(self.color[y])
            # 对玩家牌堆进行排序
            self.puke[x][self.p[x] - 1].sort(reverse=True)
            self.stop[x][0] = 1

        # 检查是否需要更新概率显示
        if self.stop[x][1] == 1 and self.stop[x][0] == 1:
            if x != 0 or self.p[x] != 1:
                card_text = self.puke[x][self.p[x] - 1][0] + self.puke[x][self.p[x] - 1][1]
            else:
                card_text = '***'

            # 显示选择的牌面
            self.label = tk.Label(self.root, text=card_text, font="黑体")
            self.label.place(relx=0.35 + (self.p[x] - 1) / 6, rely=x / self.n, anchor='nw')

            # 记录已知的牌  更新界面和概率显示
            self.puke_known.append(self.puke[x][self.p[x] - 1])
            for answer in range(self.n):
                if self.puke[answer] != [[], [], [], [], []]:
                    self.update(answer)
            self.p[x] += 1
            self.stop[x] = [0, 0]

    def callback2(self, x, y):
        if self.stop[x][1] == 0:
            # 添加所选数字到对应玩家的牌堆中
            self.puke[x][self.p[x] - 1].append(self.number[y])
            # 对玩家牌堆进行排序
            self.puke[x][self.p[x] - 1].sort(reverse=True)
            self.stop[x][1] = 1

        # 检查是否需要更新概率显示
        if self.stop[x][1] == 1 and self.stop[x][0] == 1:
            if x != 0 or self.p[x] != 1:
                card_text = self.puke[x][self.p[x] - 1][0] + self.puke[x][self.p[x] - 1][1]
            else:
                card_text = '***'
            # 显示选择的牌面
            self.label = tk.Label(self.root, text=card_text, font="黑体")
            self.label.place(relx=0.35 + (self.p[x] - 1) / 6, rely=x / self.n, anchor='nw')

            # 记录已知的牌 更新界面和概率显示
            self.puke_known.append(self.puke[x][self.p[x] - 1])
            answer: int
            for answer in range(self.n):
                if self.puke[answer] != [[], [], [], [], []]:
                    self.update(answer)
            self.p[x] += 1
            self.stop[x] = [0, 0]

    def update(self, index):
        # 更新标签文本
        self.labels[index].config(
            text="第%d个人的第%d张牌？" % (index + 1, len([puke for puke in self.puke[index] if puke != []]) + 1))

        # 计算
        unknown_pukes = [puke for puke in self.puke_all if puke not in self.puke_known]
        figure(self.puke[index], unknown_pukes, index, sum(1 for sub_lst in self.puke[index] if sub_lst), participants)
        # 计算组合数量
        num = combination(5 - sum(1 for sub_lst in self.puke[index] if sub_lst), len(unknown_pukes))

        # 更新概率标签
        self.label_probability[index].config(
            text='[同花顺，四条，葫芦，同花，顺子，三条，两对，一对]' + '\n' +
                 '[{:.2f}%, {:.2f}%, {:.2f}%, {:.2f}%, {:.2f}%, {:.2f}%, {:.2f}%, {:.2f}%]'.format(
                     100 * participants[index].same_color_straight / num,
                     100 * participants[index].four_one / num,
                     100 * participants[index].three_two / num,
                     100 * participants[index].same_color / num,
                     100 * participants[index].straight / num,
                     100 * participants[index].three_zero / num,
                     100 * participants[index].two_two / num,
                     100 * participants[index].two_zero / num
                 )
        )
        # 重置参与者的统计信息
        participants[index] = Count()

    # 清空所有组件
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == '__main__':
    a = GUI()
    a.root.mainloop()
