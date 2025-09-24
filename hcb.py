import re

from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import sys
import os
import ctypes
from PIL import ImageGrab, Image
from collections import deque, Counter
from heapq import heappush, heappop
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWinExtras import QtWin
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from time import sleep
import pyautogui




# 使用BeautifulSoup解析HTML
# soup = BeautifulSoup(html_text, 'html.parser')

# 存储合成配方和名称映射
recipes = {'aer': [], 'terra': [], 'ignis': [], 'aqua': [], 'ordo': [], 'perditio': [], 'alienis': ['vacuos', 'tenebrae'], 'arbor': ['aer', 'herba'], 'auram': ['praecantatio', 'aer'], 'bestia': ['motus', 'victus'], 'cognitio': ['ignis', 'spiritus'], 'corpus': ['mortuus', 'bestia'], 'exanimis': ['motus', 'mortuus'], 'fabrico': ['humanus', 'instrumentum'], 'fames': ['victus', 'vacuos'], 'gelum': ['ignis', 'perditio'], 'herba': ['victus', 'terra'], 'humanus': ['bestia', 'cognitio'], 'instrumentum': ['humanus', 'ordo'], 'iter': ['motus', 'terra'], 'limus': ['victus', 'aqua'], 'lucrum': ['humanus', 'fames'], 'lux': ['aer', 'ignis'], 'machina': ['motus', 'instrumentum'], 'messis': ['herba', 'humanus'], 'metallum': ['terra', 'vitreus'], 'meto': ['messis', 'instrumentum'], 'mortuus': ['victus', 'perditio'], 'motus': ['aer', 'ordo'], 'pannus': ['instrumentum', 'bestia'], 'perfodio': ['humanus', 'terra'], 'permutatio': ['perditio', 'ordo'], 'potentia': ['ordo', 'ignis'], 'praecantatio': ['vacuos', 'potentia'], 'sano': ['ordo', 'victus'], 'sensus': ['aer', 'spiritus'], 'spiritus': ['victus', 'mortuus'], 'telum': ['instrumentum', 'ignis'], 'tempestas': ['aer', 'aqua'], 'tenebrae': ['vacuos', 'lux'], 'tutamen': ['instrumentum', 'terra'], 'vacuos': ['aer', 'perditio'], 'venenum': ['aqua', 'perditio'], 'victus': ['aqua', 'terra'], 'vinculum': ['motus', 'perditio'], 'vitium': ['praecantatio', 'perditio'], 'vitreus': ['terra', 'ordo'], 'volatus': ['aer', 'motus'], 'ira': ['telum', 'ignis'], 'infernus': ['ignis', 'praecantatio'], 'gula': ['fames', 'vacuos'], 'invidia': ['sensus', 'fames'], 'desidia': ['vinculum', 'spiritus'], 'superbia': ['volatus', 'vacuos'], 'luxuria': ['corpus', 'fames'], 'tempus': ['vacuos', 'ordo'], 'electrum': ['potentia', 'machina'], 'magneto': ['metallum', 'iter'], 'nebrisum': ['perfodio', 'lucrum'], 'radio': ['lux', 'potentia'], 'strontio': ['perditio', 'cognitio'], 'exubitor': ['alienis', 'mortuus'], 'citrus': ['herba', 'sensus'], 'magnes': ['metallum', 'potentia'], 'fluctuatio': ['magnes', 'machina'], 'revelatio': ['alienis', 'cognitio'], 'MRU': ['praecantatio', 'potentia'], 'matrix': ['MRU', 'humanus'], 'radiation': ['MRU', 'motus'], 'terminus': ['lucrum', 'alienis'], 'signum': ['potentia', 'auram'], 'perplexus': ['cognitio', 'vinculum'], 'darkness': ['tenebrae', 'telum'], 'odachi': ['telum', 'vacuos'], 'proud': ['spiritus', 'odachi'], 'taurethrim': ['abonnen', 'arbor'], 'morwaith': ['abonnen', 'venenum'], 'dunlan': ['abonnen', 'perditio'], 'mordor': ['orchoth', 'telum'], 'torog': ['orchoth', 'tenebrae'], 'perian': ['humanus', 'sensus'], 'dale': ['abonnen', 'permutatio'], 'angdol': ['nauglin', 'perfodio'], 'nazgul': ['angmar', 'spiritus'], 'harad': ['abonnen', 'ignis'], 'ithryn': ['alfirin', 'praecantatio'], 'eredluin': ['nauglin', 'gelum'], 'fangorn': ['onodrim', 'arbor'], 'isengard': ['mornogol', 'praecantatio'], 'lothlorien': ['edhel', 'auram'], 'edhel': ['humanus', 'alfirin'], 'nauglin': ['humanus', 'perfodio'], 'valaraukar': ['alfirin', 'alienis'], 'dunedain': ['abonnen', 'iter'], 'rohan': ['abonnen', 'bestia'], 'druardh': ['edhel', 'arbor'], 'onodrim': ['arbor', 'motus'], 'lindon': ['edhel', 'aqua'], 'uhorm': ['arbor', 'bestia'], 'draugol': ['bestia', 'telum'], 'angmar': ['orchoth', 'vitium'], 'orchoth': ['edhel', 'exanimis'], 'dorwinion': ['abonnen', 'edhel'], 'dolguldur': ['orchoth', 'spiritus'], 'shire': ['perian', 'meto'], 'pertorog': ['abonnen', 'torog'], 'gundabad': ['orchoth', 'venenum'], 'gondor': ['abonnen', 'ordo'], 'mornogol': ['orchoth', 'abonnen'], 'utumno': ['valaraukar', 'alienis'], 'abonnen': ['humanus', 'lucrum'], 'rhudel': ['abonnen', 'fames'], 'alfirin': ['praecantatio', 'permutatio'], 'dragon': ['praecantatio', 'bestia'], 'substance': ['aqua', 'ordo'], 'space': ['substance', 'vacuos'], 'universe': ['substance', 'ordo'], 'destroy': ['aqua', 'ignis'], 'mana': ['auram', 'potentia'], 'dream': ['cognitio', 'ordo'], 'relic': ['cognitio', 'herba'], 'evil': ['vitium', 'lucrum'], 'treasure': ['lucrum', 'telum'], 'dackmagic': ['praecantatio', 'vitium'], 'manaherba': ['praecantatio', 'herba'], 'darkenergy': ['perditio', 'potentia'], 'magnetic': ['metallum', 'potentia'], 'electricity': ['aqua', 'potentia'], 'cave': ['terra', 'vacuos'], 'antimatter': ['perditio', 'substance'], 'enchant': ['undefined', 'telum'], 'alloy': ['ignis', 'metallum'], 'lava': ['terra', 'ignis'], 'time': ['ordo', 'vacuos'], 'rock': ['terra', 'perditio'], 'vegetation': ['aer', 'terra'], 'paper': ['herba', 'fabrico'], 'gravity': ['potentia', 'substance'], 'anteanus': ['humanus', 'chronos'], 'chronos': ['permutatio', 'motus'], 'priscus': ['bestia', 'chronos'], 'luacdiaoz': ['herba', 'bestia'], 'rattus': ['perditio', 'bestia'],
           'caelum': ['vitreus', 'metallum'], 'tabernus': ['iter', 'tutamen']}
name_mapping = {'aer': '风', 'terra': '地', 'ignis': '火', 'aqua': '水', 'ordo': '秩序', 'perditio': '混沌', 'alienis': '异域', 'arbor': '木头', 'auram': '灵气', 'bestia': '野兽', 'cognitio': '思维', 'corpus': '肉体', 'exanimis': '亡灵', 'fabrico': '合成', 'fames': '饥饿', 'gelum': '寒冰', 'herba': '植物', 'humanus': '人类', 'instrumentum': '工具', 'iter': '旅行', 'limus': '粘液', 'lucrum': '贪婪', 'lux': '光明', 'machina': '机械', 'messis': '作物', 'metallum': '金属', 'meto': '收获', 'mortuus': '死亡', 'motus': '运动', 'pannus': '布匹', 'perfodio': '采掘', 'permutatio': '交换', 'potentia': '能量', 'praecantatio': '魔法', 'sano': '治愈', 'sensus': '感知', 'spiritus': '灵魂', 'telum': '武器', 'tempestas': '气候', 'tenebrae': '黑暗', 'tutamen': '装备', 'vacuos': '虚空', 'venenum': '剧毒', 'victus': '生命', 'vinculum': '陷阱', 'vitium': '腐化', 'vitreus': '水晶', 'volatus': '飞行', 'ira': '暴怒', 'infernus': '下界', 'gula': '饕餮', 'invidia': '妒忌', 'desidia': '怠倦', 'superbia': '傲慢', 'luxuria': '欲望', 'tempus': 'MB时间', 'electrum': 'GT电力', 'magneto': '磁性', 'nebrisum': '欺诈', 'radio': '辐射', 'strontio': '愚锶', 'exubitor': '守护', 'citrus': '柑橘', 'magnes': 'TR磁力', 'fluctuatio': '波动', 'revelatio': '启示', 'MRU': '魔力辐射单元', 'matrix': '矩阵', 'radiation': '放射', 'terminus': '终结', 'signum': '信号', 'perplexus': '谜题', 'darkness': '幽暗', 'odachi': '野太刀', 'proud': '荣耀', 'taurethrim': '陶瑞斯', 'morwaith': '墨怀斯', 'dunlan': '黑蛮地', 'mordor': '魔多', 'torog': '食人妖', 'perian': '霍比特', 'dale': '长湖', 'angdol': '铁丘陵', 'nazgul': '那兹古尔', 'harad': '近哈拉德', 'ithryn': '迈雅', 'eredluin': '蓝色山脉', 'fangorn': '范贡森林', 'isengard': '艾森加德', 'lothlorien': '罗斯洛瑞恩', 'edhel': '精灵', 'nauglin': '矮人', 'valaraukar': '炎魔', 'dunedain': '游民', 'rohan': '洛汗', 'druardh': '森林王国', 'onodrim': '树人', 'lindon': '林顿', 'uhorm': '暗胡奥恩', 'draugol': '座狼', 'angmar': '安格玛', 'orchoth': '奥克', 'dorwinion': '多温尼安', 'dolguldur': '多古尔都', 'shire': '夏尔', 'pertorog': '半食人妖', 'gundabad': '北方奥克', 'gondor': '刚铎', 'mornogol': '乌鲁克', 'utumno': '乌图姆诺', 'abonnen': '中土人类', 'rhudel': '东夷', 'alfirin': '不朽', 'dragon': '龙', 'substance': '物质', 'space': '空间', 'universe': '宇宙', 'destroy': '毁灭', 'mana': 'M3魔法', 'dream': '梦想', 'relic': '文物', 'evil': '邪恶', 'treasure': '财富', 'dackmagic': '黑魔法', 'manaherba': '魔法植物', 'darkenergy': '暗能量', 'magnetic': 'M3磁力', 'electricity': 'M3电力', 'cave': '洞窟', 'antimatter': '反物质', 'enchant': '附魔', 'alloy': '合金', 'lava': '熔岩', 'time': 'M3时间', 'rock': '岩石', 'vegetation': '植被', 'paper': '纸张', 'gravity': '重力', 'anteanus': '历史', 'chronos': 'FA时间', 'priscus': '遗蜕', 'luacdiaoz': '辣条', 'rattus': '老鼠',
                'caelum': '宙空', 'tabernus': '靴子'}

# 查找所有要素行
# aspect_rows = soup.find_all('li', class_='tctool-aspect-row')
#
# for row in aspect_rows:
#     chinese_name = row.find('div').text.strip()
#     english_name = row.find('div', class_='desc').text.strip()
#     name_mapping[english_name] = chinese_name
#
#     recipe_content = row.get('data-content', '')
#     recipe_soup = BeautifulSoup(recipe_content, 'html.parser')
#
#     recipe_p = recipe_soup.find('p', string=re.compile('合成方式:'))
#
#     if recipe_p:
#         next_p = recipe_p.find_next('p')
#         if next_p:
#             if "是一阶要素，无需合成" in next_p.text:
#                 recipes[english_name] = []
#             else:
#                 # 使用正则表达式提取 (英文名) 部分
#                 components = re.findall(r'\((\w+)\)', next_p.text)
#                 if components:
#                     recipes[english_name] = components


# # 输出结果
# print("合成配方:")
# for eng, recipe in recipes.items():
#     print(f"{eng}: {recipe}")
# #
# print("\n中英文名称映射:")
# for eng, chn in name_mapping.items():
#     print(f"{eng}: {chn}")

ys = {}
with open("ys.txt", "r", encoding="utf-8") as f:
    inp = f.readlines()
    for i in inp:
        ycl = i.replace("\n","").replace(" ","").split(":")
        try:
            ys[tuple(map(int,ycl[1].split(",")))] = ycl[0]
        except Exception as e:
            pass
            # print(i)
# print(ys)
# 元素系统
memo = {}
PRIMAL = {'aer', 'terra', 'ignis', 'aqua', 'ordo', 'perditio'}

# 配置
CONFIG_PATH = os.path.join(os.getcwd(), 'gc.txt')
CLASS_NAMES_PATH = os.path.join(os.getcwd(), 'class.txt')
MODEL_PATH = os.path.join(os.getcwd(), 'icon_classifier.pth')
RELOAD_INTERVAL = 100  # ms
DETECT_INTERVAL = 4000  # ms
IMAGE_SIZE = 24  # 与训练时一致
# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")



# 加载类别名
ids = {}
getids = {}
cont = {}
lins = open(CLASS_NAMES_PATH, 'r').readlines()
for i in range(len(lins)):
    ids[i] = lins[i].strip().lower()
    cont[i] = set()
    getids[lins[i].strip().lower()] = i

for k, v in recipes.items():
    if k in PRIMAL:
        continue
    if k in getids:
        if v[0] in getids:
            cont[getids[k]].add(getids[v[0]])
            cont[getids[v[0]]].add(getids[k])
        if v[1] in getids:
            cont[getids[k]].add(getids[v[1]])
            cont[getids[v[1]]].add(getids[k])

# for i, j in cont.items():
#     if i!=0 and i!=1:
#         print(name_mapping[ids[i]], end=" :  ")
#         for ii in j:
#             print(name_mapping[ids[ii]], end=" ")
#         print()

print(ids)

# print(cont)
def is_con(id1, id2):
    return (id2 in cont[id1]) or (id1 in cont[id2])


def compute_cost(elem):
    if elem not in getids:
        return float('inf')
    if elem in PRIMAL:
        elem = getids[elem]
        memo[elem] = 1
        return memo[elem]
    elem = getids[elem]
    if elem in memo:
        return memo[elem]
    else:
        parts = recipes.get(ids[elem], [])
        # 如果没有配方，算无限大
        if not parts:
            return float('inf')
        else:
            if sum(compute_cost(p) for p in parts) == float('inf'):
                return float('inf')
            memo[elem] = sum(compute_cost(p) for p in parts)
    return memo[elem]
for eng, chn in name_mapping.items():
    compute_cost(eng)


# model = models.resnet18(pretrained=False)
# model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
# model.maxpool = nn.Identity()
# model.fc = nn.Linear(model.fc.in_features, len(ids))
# model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
# model.to(DEVICE).eval()
# transform = T.Compose([
#             T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
#             T.ToTensor(),
# ])


class Box:
    def __init__(self, x, y, size, row=None, col=None):
        self.rect = QtCore.QRect(x, y, size, size)
        self.x = x
        self.y = y
        self.size = size
        self.row = row
        self.col = col
        self.center = QtCore.QPoint(x + size // 2, y + size // 2)

        self.label = None  # 分类结果ID
        #self.color = QtGui.QColor(0, 0, 0)
        self.highlight = False

    def draw(self, painter):
        #pen = QtGui.QPen(self.color if not self.highlight else QtGui.QColor(0, 255, 0))
        if self.label is not None and self.label != 0:
            pen = QtGui.QPen(QtGui.QColor(0, 240, 0))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(self.rect)
            if self.label != 1:
                pen.setColor(QtGui.QColor(255, 255, 255))
                pen.setWidth(4)
                painter.setPen(pen)
                text = str(name_mapping[ids[self.label]])
                text_pos = self.rect.topLeft() + QtCore.QPoint(4, self.rect.height() // 2 + 4)
                painter.drawText(text_pos, text)





def see(crop):
    crop = crop.resize((24, 24), Image.LANCZOS)
    aaaa = crop
    # 预处理图像 - 转为黑白
    pixels = crop.load()

    color_counter = Counter()
    su255 = 0
    for y 在 range(crop.height):
        for x 在 range(crop.width):
            r_, g_, b_ = pixels[x, y]
            if (r_, g_, b_) != (255, 255, 255):
                su255+=1
            if (r_, g_, b_) != (255, 255, 255) and (r_, g_, b_) != (0, 0, 0) and (r_, g_, b_) != (1, 0, 0):
                color_counter[(r_, g_, b_)] += 1
    if su255 < 4:
        return getids[ys[(255,255,255)]]

    if color_counter:
        most_common_color, count = color_counter.most_common(1)[0]
        #print(f"最常见的颜色是: {most_common_color}，出现次数: {count}")
        if most_common_color 在 ys:
            return getids[ys[most_common_color]]
        else:
            print(f"无法识别：最常见的颜色是: {most_common_color}，出现次数: {count}")
            # aaaa.show()
            # print(color_counter)
            # aa = input()

            return 0
    else:
        return 0




    # >>> 添加：将底部两行像素强制设为纯黑 <<<
    # for y in range(crop.height - 2, crop.height):
    #     for x in range(crop.width):
    #         pixels[x, y] = (0, 0, 0)

    # 识别元素
    # img = transform(crop).unsqueeze(0).to(DEVICE)
    # with torch.no_grad():
    #     outputs = model(img)
    #     pred = torch.argmax(outputs, dim=1).item()

    # if pred!=1 and pred!=0:
    #     crop.show()
    #     sleep(1)



def get_hex_neighbors(row, col):
    # 偶-奇配合的六边形偏移
    offsets = [(-1, -1), (2, 0), (1, -1), (-2, 0), (1, 1), (-1, 1)]
    return [(row + dr, col + dc) for dr, dc in offsets]



