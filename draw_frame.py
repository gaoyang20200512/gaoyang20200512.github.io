import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon
import numpy as np

# 中文字体
plt.rcParams['font.family'] = 'Noto Sans CJK SC'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(16, 11), dpi=140)
fig.patch.set_facecolor('#0e1013')
ax.set_facecolor('#13161c')

# 层: (名称, 颜色, 宽, 高, 厚, y偏移, x偏移, 备注)
layers = [
    ('01 木框 300×218×26',     '#8b5a2b', 300, 218, 26,   0,   0, None),
    ('02 哑光玻璃 249.5×167.5', '#b8d4e3', 250, 168, 1.5,  0,   0, 'glass'),
    ('03 深色内衬 边宽15mm',    '#1a1c20', 250, 168, 1.2,  0,   0, 'mat'),
    ('04 屏幕模组 232×146×3',  '#2a2f38', 232, 146, 3,    0,   0, None),
    ('05 发光面 216.9×135.6',  '#1e4258', 217, 136, 0.4,  0,   0, None),
    ('06 屏驱动板 62×40',      '#1c5c42',  62,  40, 3,  -30,  80, None),
    ('07 主板 110×70',         '#1b3a5c', 110,  70, 1.6, -10,   0, 'pcb'),
    ('08 传感器板 22×16',      '#1c5c42',  22,  16, 1.2,  30, -90, None),
    ('09 扬声器 ×2 ⌀20',       '#23272e',  20,  20, 5,   -60, 100, 'spk'),
    ('10 背板 296×214×2.5',    '#3a4048', 296, 214, 2.5,  0,   0, None),
    ('11 折叠支架',            '#8a9099',  60,  78, 3,   -90,  0, 'leg'),
]

# 爆炸展开 y 位置（从前到后）
ORDER = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 前→后
layers_drawn = [layers[i] for i in ORDER]

y_cur = 0
positions = []
for layer in layers_drawn:
    h = layer[3]
    yc = y_cur + h / 2
    positions.append(yc)
    y_cur += h + 40

# 顶部再留 100，底部留 80
y_max = y_cur + 100
y_min = -80

for i, (name, color, w, h, t, dy, dx, tag) in enumerate(layers_drawn):
    y = positions[i] + dy
    cx = dx

    if tag == 'glass':
        rect = FancyBboxPatch((-w/2+cx, -h/2+y), w, h,
            boxstyle="round,pad=2", facecolor=color,
            edgecolor='#6ea8fe', linewidth=1.5, alpha=0.65, zorder=3)
        ax.add_patch(rect)
    elif tag == 'mat':
        rect = FancyBboxPatch((-w/2+cx, -h/2+y), w, h,
            boxstyle="round,pad=2", facecolor=color,
            edgecolor='#6ea8fe', linewidth=1.5, zorder=3)
        ax.add_patch(rect)
        # 中间挖洞
        hole = patches.Rectangle((-109+cx, -68.4+y), 218, 136.8,
            facecolor='#0e1013', edgecolor='none', zorder=4)
        ax.add_patch(hole)
    elif name.startswith('01'):
        rect = FancyBboxPatch((-w/2+cx, -h/2+y), w, h,
            boxstyle="round,pad=3", facecolor=color,
            edgecolor='#6ea8fe', linewidth=2, zorder=3)
        ax.add_patch(rect)
        hole = patches.Rectangle((-125+cx, -84+y), 250, 168,
            facecolor='#0e1013', edgecolor='none', zorder=4)
        ax.add_patch(hole)
    elif tag == 'pcb':
        rect = FancyBboxPatch((-w/2+cx, -h/2+y), w, h,
            boxstyle="round,pad=1", facecolor=color,
            edgecolor='#6ea8fe', linewidth=1.2, zorder=3)
        ax.add_patch(rect)
        # 芯片
        chip = patches.Rectangle((-8+cx, -4+y), 16, 16,
            facecolor='#2b2f36', edgecolor='#cfe1ff', lw=0.8, zorder=5)
        ax.add_patch(chip)
        ram = patches.Rectangle((4+cx, -6+y), 24, 12,
            facecolor='#2b2f36', edgecolor='#cfe1ff', lw=0.8, zorder=5)
        ax.add_patch(ram)
        usb = patches.Rectangle((-4+cx, -35+y), 8, 4,
            facecolor='#8a9099', edgecolor='#cfe1ff', lw=0.8, zorder=5)
        ax.add_patch(usb)
    elif tag == 'spk':
        for sx in (-50, 50):
            c = plt.Circle((sx+cx, y), 10, facecolor='#23272e',
                ec='#6ea8fe', lw=1.5, zorder=4)
            ax.add_patch(c)
            c2 = plt.Circle((sx+cx, y), 5, facecolor='#14161a',
                ec='#6ea8fe', lw=0.8, zorder=5)
            ax.add_patch(c2)
    elif tag == 'leg':
        leg = Polygon([
            (-15+cx, -39+y), (15+cx, -39+y),
            (25+cx, 39+y), (-25+cx, 39+y),
        ], facecolor='#8a9099', edgecolor='#6ea8fe', lw=1.5, zorder=4)
        ax.add_patch(leg)
        foot = patches.Rectangle((-18+cx, -44+y), 36, 6,
            facecolor='#6a7079', edgecolor='#6ea8fe', lw=1.2, zorder=4)
        ax.add_patch(foot)
    else:
        rect = FancyBboxPatch((-w/2+cx, -h/2+y), w, h,
            boxstyle="round,pad=1.5", facecolor=color,
            edgecolor='#6ea8fe', linewidth=1.5, zorder=3)
        ax.add_patch(rect)

# 左侧层名标注
for i, layer in enumerate(layers_drawn):
    y = positions[i] + layer[5]
    ax.text(-195, y, layer[0], ha='right', va='center',
        color='#e8eaed', fontsize=10, fontweight='medium',
        fontfamily='Noto Sans CJK SC', zorder=10)

# 右侧厚度标注
for i, layer in enumerate(layers_drawn):
    y = positions[i] + layer[5]
    t = layer[4]
    w = layer[2]
    rgt = max(w/2 + 25, 180)
    if layer[7] == 'spk':
        rgt = 80
    elif layer[7] == 'leg':
        rgt = 50
    ax.annotate(f't={t}mm', xy=(rgt, y), xytext=(rgt+6, y),
        ha='left', va='center', color='#98a2ad', fontsize=9,
        fontfamily='Noto Sans CJK SC', zorder=10)

# 层间虚线
for i in range(len(positions)-1):
    yt = positions[i]
    yb = positions[i+1]
    ax.plot([-160, -160], [yt+20, yb-20],
        color='#6ea8fe', alpha=0.25, ls='--', lw=1, zorder=2)

# 标题
ax.text(0, y_max - 30, '10.1" 相框 · 爆炸结构图',
    ha='center', va='center', color='#e8eaed', fontsize=20, fontweight='bold')
ax.text(0, y_max - 58, '外框 300 × 218 × 26 mm   |   可视区 216.9 × 135.6 mm   |   IPS 1280×800',
    ha='center', va='center', color='#98a2ad', fontsize=10.5, fontfamily='Noto Sans CJK SC')

# 方向箭头
for (tx, ty, txt) in [(180, positions[0]+15, '← 前'), (180, positions[-1]-15, '后 →')]:
    ax.annotate(txt, xy=(165, ty), xytext=(tx, ty),
        arrowprops=dict(arrowstyle='->', color='#6ea8fe', lw=1.8),
        color='#6ea8fe', fontsize=13, fontweight='bold', zorder=10)

# 底部规格
spec_lines = [
    '屏幕: 10.1" IPS 1280×800 · 300nit · 178° 可视角',
    '主板上限: 110 × 70 × 10 mm · SoC + 1GB DDR + 8GB eMMC',
    '传感器: BH1750 光感 + LD2410C 毫米波 + GT911 触摸',
    '供电: 5V/2A USB-C · 5W 常亮功耗 · 背板散热孔阵列',
    '结构: 木框 + 哑光玻璃 + 黑卡纸内衬 + 金属背板',
]
for j, line in enumerate(spec_lines):
    ax.text(-195, y_min + 18 + j*16, line, color='#98a2ad',
        fontsize=8.5, fontfamily='Noto Sans CJK SC', zorder=10)

ax.set_xlim(-240, 260)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout(pad=0.5)
plt.savefig('/workspace/frame-exploded-view.png', dpi=140, bbox_inches='tight',
    facecolor='#0e1013', edgecolor='none')
print('OK size =', plt.gcf().get_size_inches())
