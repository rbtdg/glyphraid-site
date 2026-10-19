# 重算 index.html 內嵌腳本的 sha256，寫回 CSP 的 script-src。
# 改了 <script> 內容之後必跑：CSP 只准執行雜湊相符的腳本，不跑＝試玩整個被瀏覽器擋掉。
import base64, hashlib, os, re
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
s = open(p, encoding='utf-8').read()
# 先拿掉 HTML 註解：註解裡寫到「<script>」這個字會被誤認成腳本開頭（2026-10-19 踩過）
scripts = re.findall(r'<script>(.*?)</script>', re.sub(r'<!--.*?-->', '', s, flags=re.S), re.S)
hashes = ' '.join("'sha256-%s'" % base64.b64encode(hashlib.sha256(x.encode('utf-8')).digest()).decode() for x in scripts)
s2 = re.sub(r"script-src [^;]+;", 'script-src %s;' % hashes, s, count=1)
open(p, 'w', encoding='utf-8').write(s2)
print('scripts:', len(scripts), '| CSP updated' if s2 != s else '| already up to date')
