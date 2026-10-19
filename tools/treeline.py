# 兩層像素樹林剪影（512 寬可水平無縫重複）。網頁上 4 倍放大＋pixelated。
import random
from PIL import Image
W, H = 512, 44
def mk(color):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); px = im.load()
    def put(x, y):
        if 0 <= y < H: px[x % W, y] = color
    return im, put
def pine(put, x, ground, tiers, tier_h):
    # 由上往下畫：每層一個小三角，下一層比上一層寬 2
    y = ground - 2 - tiers * (tier_h - 1) - 1
    for yy in (y - 2, y - 1): put(x, yy)            # 樹尖
    top_half = 1
    for t in range(tiers):
        for r in range(tier_h):
            half = top_half + r
            for dx in range(-half, half + 1): put(x + dx, y + r)
        y += tier_h - 1
        top_half += 2
    for yy in range(y, ground): put(x, yy); put(x + 1, yy)  # 樹幹
def bush(put, x, ground, r):
    for yy in range(ground - r, ground):
        d = ground - yy
        half = int(r * 1.6 - (d * d) / (r * 0.9))
        for dx in range(-half, half + 1): put(x + dx, yy)
def ground_fill(put, base):
    for x in range(W):
        for y in range(H - base, H): put(x, y)

random.seed(3)
back, putb = mk((9, 70, 73, 255))
gb = H - 6
ground_fill(putb, 6)
x = 6
while x < W - 8:
    # 成叢出現、叢之間留空：天際線才不會像鋸齒
    for _ in range(random.choice([1, 2, 3, 3, 4])):
        if x >= W - 8: break
        tiers = random.choice([2, 3, 3, 4, 4, 5]); th = random.choice([4, 5, 5, 6])
        pine(putb, x, gb, tiers, th)
        x += random.randint(7, 14)
    x += random.choice([6, 14, 22, 34])
random.seed(19)
front, putf = mk((6, 48, 47, 255))
gf = H - 11
ground_fill(putf, 11)
x = 3
while x < W - 6:
    r = random.choice([2, 2, 3, 3, 4, 5]); bush(putf, x, gf, r)
    x += random.choice([4, 6, 8, 10, 14, 20, 28])
import os; out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets') + '/'
back.save(out + 'trees_back.png', optimize=True); front.save(out + 'trees_front.png', optimize=True)



print('ok')
