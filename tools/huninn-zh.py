# 中文頁的粉圓子集 assets/huninn-zh.woff2：只收 zh/index.html 畫面上的中文字與全形標點（2026-11-16 起網頁試玩拿掉，不再讀 demo.js）。
# 拉丁字母、數字由 assets/huninn-latin.woff2 負責（site.css 用 unicode-range 分開，英文頁不會下載中文子集）。
# 隱私、刪除資料頁的條文用系統字，不收。
# 改了中文頁的中文字之後重跑（中文頁由 tools/build-home.py 產生）：
#   python3 tools/huninn-zh.py <jf-openhuninn 的 .ttf>
# 需要 python3 的 fonttools 與 brotli。字型授權：SIL OFL 1.1（assets/huninn-LICENSE.txt）。
import os, re, sys
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
# 跟 site.css 裡中文子集的 unicode-range 一致
RANGES = [(0x3000, 0x303F), (0x4E00, 0x9FFF), (0xFF00, 0xFFEF)]


def page_chars():
    html = open(os.path.join(ROOT, 'zh', 'index.html'), encoding='utf-8').read()
    body = re.search(r'<body[^>]*>(.*)</body>', html, re.S).group(1)
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    text = re.sub(r'<[^>]+>', '', body)
    strings = ''
    return sorted({c for c in text + strings if any(a <= ord(c) <= b for a, b in RANGES)})


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python3 tools/huninn-zh.py <jf-openhuninn.ttf>')
    chars = page_chars()
    opts = subset.Options()
    opts.layout_features = ['*']
    opts.hinting = False
    font = TTFont(sys.argv[1])
    sub = subset.Subsetter(opts)
    sub.populate(text=''.join(chars))
    sub.subset(font)
    font.flavor = 'woff2'
    out = os.path.join(ROOT, 'assets', 'huninn-zh.woff2')
    font.save(out)
    cmap = font.getBestCmap()
    missing = [c for c in chars if ord(c) not in cmap]
    print('chars:', len(chars), '| size: %.1f KB' % (os.path.getsize(out) / 1024), '| missing:', ''.join(missing) or 'none')
    print(''.join(chars))


main()
