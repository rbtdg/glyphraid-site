# 重算首頁（index.html、zh/index.html）內嵌腳本的 sha256，寫回 CSP 的 script-src。
# 改了內嵌 <script> 內容之後必跑：CSP 只准執行本站的檔案（'self'，assets/demo.js）和雜湊相符的內嵌腳本，不跑＝那段腳本被瀏覽器擋掉。
# 隱私、刪除資料頁沒有腳本（script-src 'none'），不用跑。
import base64, hashlib, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for name in ('index.html', os.path.join('zh', 'index.html')):
    p = os.path.join(ROOT, name)
    s = open(p, encoding='utf-8').read()
    # 先拿掉 HTML 註解：註解裡寫到「<script>」這個字會被誤認成腳本開頭（2026-10-19 踩過）
    scripts = re.findall(r'<script>(.*?)</script>', re.sub(r'<!--.*?-->', '', s, flags=re.S), re.S)
    hashes = ' '.join("'sha256-%s'" % base64.b64encode(hashlib.sha256(x.encode('utf-8')).digest()).decode() for x in scripts)
    s2 = re.sub(r"script-src [^;]+;", "script-src 'self' %s;" % hashes, s, count=1)
    open(p, 'w', encoding='utf-8').write(s2)
    print(name, '| inline scripts:', len(scripts), '| CSP updated' if s2 != s else '| already up to date')
