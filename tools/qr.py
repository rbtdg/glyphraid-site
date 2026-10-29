# 產生首頁電腦版那張 QR code：assets/qr-get.svg，內容＝https://glyphraid.com/get/
# /get/ 那頁會依手機平台轉去 App Store 或 Google Play（判斷寫在 assets/get.js）。
# QR code 只放自己網域的網址：之後要換跳去哪，改 get/ 就好，QR code 不用重做。
# 改網址才需要重跑：python3 tools/qr.py（需要 python3 的 qrcode 套件）
import os
import qrcode

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
URL = 'https://glyphraid.com/get/'
INK, PAPER = '#06302F', '#FAF3E2'   # site.css 的 --teal-ink、--cream-hi
QUIET = 2                             # 留白（格數）：2 格＋外面的米色就夠手機相機讀；總寬 29 格，畫成 87px＝每格剛好 3px（不整數倍的話一般螢幕上格子會糊，2026-10-30 量過 80px 解不出來）

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
qr.add_data(URL)
qr.make(fit=True)
m = qr.get_matrix()
n = len(m) + QUIET * 2
d = ''.join('M%d %dh1v1h-1z' % (x + QUIET, y + QUIET) for y, row in enumerate(m) for x, on in enumerate(row) if on)
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" shape-rendering="crispEdges">'
       '<rect width="%d" height="%d" fill="%s"/><path fill="%s" d="%s"/></svg>\n') % (n, n, n, n, PAPER, INK, d)
open(os.path.join(ROOT, 'assets', 'qr-get.svg'), 'w').write(svg)
print('assets/qr-get.svg | %d×%d modules | %s' % (len(m), len(m), URL))
