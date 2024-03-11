def if_same_color(x):
    """
    判断是否为同花

    参数：
        x：五张牌的列表

    返回值：
        如果五张牌的花色都相同，返回True，否则返回False
    """

    if [x[i][0] for i in range(0, 5)].count(x[0][0]) == 5:
        return True
    else:
        return False


def if_straight(x):
    """
    判断是否为顺子

    参数：
        x：五张牌的列表

    返回值：
        如果五张牌的点数连续，返回True，否则返回False
    """
    card_values = sorted([x[i][1] for i in range(0, 5)])
    straight_patterns = [['10', '7', '8', '9', 'J'],
                         ['10', '8', '9', 'J', 'Q'],
                         ['10', '9', 'J', 'K', 'Q'],
                         ['10', 'A', 'J', 'K', 'Q'],
                         ['10', '7', '8', '9', 'A']]
    if card_values in straight_patterns:
        return True
    else:
        return False


def if_four_one(x):
    """
    判断是否为四条

    参数：
        x：五张牌的列表

    返回值：
        如果有四张点数相同的牌，返回True，否则返回False
    """
    card_numbers = [x[i][1] for i in range(0, 5)]
    if card_numbers.count(x[0][1]) == 4 or card_numbers.count(x[1][1]) == 4:
        return True
    else:
        return False


def if_three_zero(x):
    """
    判断是否为三条（不包含四条）

    参数：
        x：五张牌的列表

    返回值：
        如果有三张点数相同的牌（不包含四条），返回True，否则返回False
    """
    card_numbers = [x[i][1] for i in range(0, 5)]
    if card_numbers.count(x[0][1]) == 3 or card_numbers.count(x[1][1]) == 3 or card_numbers.count(x[2][1]) == 3:
        return True
    else:
        return False


def if_two_two(x):
    """
    判断是否为两对（不包含葫芦）

    参数：
        x：五张牌的列表

    返回值：
        如果有两对点数相同的牌（不包含葫芦），返回True，否则返回False
    """
    if not if_four_one(x):
        card_values = sorted([x[i][1] for i in range(0, 5)])
        if (card_values[0] == card_values[1] and card_values[2] == card_values[3]) or \
                (card_values[0] == card_values[1] and card_values[3] == card_values[4]) or \
                (card_values[1] == card_values[2] and card_values[3] == card_values[4]):
            return True
        else:
            return False
    else:
        return False


def if_two_zero(x):
    """
    判断是否为一对（可能包含葫芦）

    参数：
        x：五张牌的列表

    返回值：
        如果有一对点数相同的牌（可能包含葫芦），返回True，否则返回False
    """
    if if_two_two(x):
        return False
    else:
        card_values = sorted([x[i][1] for i in range(0, 5)])
        if card_values.count(card_values[0]) == 2 or card_values.count(card_values[1]) == 2 or \
                card_values.count(card_values[2]) == 2 or card_values.count(card_values[3]) == 2:
            return True
        else:
            return False


# 各种牌型可能性统计的类别
class Count:
    same_color_straight = 0
    same_color = 0
    straight = 0
    four_one = 0
    three_zero = 0
    three_two = 0
    two_two = 0
    two_zero = 0

    def reset_counts(self):
        """重置各种牌型计数"""
        self.same_color_straight = 0
        self.same_color = 0
        self.straight = 0
        self.four_one = 0
        self.three_zero = 0
        self.three_two = 0
        self.two_two = 0
        self.two_zero = 0


# 阶乘
def factorial(a):
    """计算阶乘"""
    result = 1
    for i in range(1, a + 1):
        result *= i
    return result


# 组合
def combination(a, b):
    """计算组合"""
    return factorial(b) / factorial(b - a) / factorial(a)


def figure(a, b, c, d, participants):
    """
    统计牌型
    a: 已知的牌
    b: 未出现的牌
    c: 参与者索引
    d: 参与者手牌数量
    """

    def update_counts(puke_form):
        """更新牌型计数"""
        if if_same_color(puke_form):
            participants[c].same_color += 1
        if if_straight(puke_form):
            participants[c].straight += 1
        if if_same_color(puke_form) and if_straight(puke_form):
            participants[c].same_color_straight += 1
        if if_four_one(puke_form):
            participants[c].four_one += 1
        if if_two_two(puke_form):
            participants[c].two_two += 1
        if if_three_zero(puke_form):
            participants[c].three_zero += 1
        if if_two_zero(puke_form):
            participants[c].two_zero += 1
        if if_three_zero(puke_form) and if_two_zero(puke_form):
            participants[c].three_two += 1

    if d == 4:
        for card in b:
            behavior = [x for x in a if x != []]
            behavior.append(card)
            update_counts(behavior)

    if d == 3:
        for i in range(len(b) - 1):
            for j in range(i + 1, len(b)):
                behavior = [x for x in a if x != []]
                behavior.extend([b[i], b[j]])
                update_counts(behavior)

    if d == 2:
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    behavior = [x for x in a if x != []]
                    behavior.extend([b[i], b[j], b[k]])
                    update_counts(behavior)

    if d == 1:
        for i in range(len(b) - 3):
            for j in range(i + 1, len(b) - 2):
                for k in range(j + 1, len(b) - 1):
                    for l in range(k + 1, len(b)):
                        behavior = [a[0], b[i], b[j], b[k], b[l]]
                        update_counts(behavior)
