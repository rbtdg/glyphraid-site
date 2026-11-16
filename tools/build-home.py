# 產生兩個首頁：index.html（英文）與 zh/index.html（中文）。2026-11-16 改版（拿掉網頁試玩、講 2.0.0 的特點）。
# 版面只寫在這裡一次，兩頁只差文字；改首頁＝改這支再跑：
#   python3 tools/build-home.py && python3 tools/update-csp.py && python3 tools/huninn-zh.py <jf-openhuninn .ttf>
# 不要直接手改 index.html／zh/index.html（下次重跑會被蓋掉）。
#
# 忠於 app（官網不准畫 app 沒有的東西）：
#   ‧ 國旗＝照 app 的 components/language-flag.tsx 畫法（30×20 座標，同一組顏色）；問候語＝商店截圖用的那組
#     （Vask .claude/skills/store-screenshots/custom.py 的 LANGS／LANGS_ZH）。
#   ‧ 語言清單照 app 該介面語言的選語言頁：英文介面有簡中、沒有英文；中文介面有英文、沒有簡中（兩邊都是 11 種）。
#   ‧ 圖全部是 app 真實截圖或 app 素材（assets/v2/）。特點四格＝app 的美術素材組合（Terry 11/16：不用硬塞截圖，
#     放符合說明、整體好看的）：職業頭像、聖物圖示、魔王 briarhulk（Terry 11/16 指定）＋它在 app 裡的 grove 魔王背景（配對見 Vask config/art-sets.ts）、
#     主題圖示，背景是 app 的戰鬥背景上半部。
#     產生方式與素材路徑記在 Vask docs/rounds/2026-11-16-site-v2.md。
import html, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LANG_SNIPPET = open(os.path.join(ROOT, 'tools', 'lang-snippet.js'), encoding='utf-8').read()

APP_ID = '6785621868'
# App Store：活動連結（pt＝Terry 帳號的 provider 編號，ct＝來源）；Google Play：referrer 帶 utm_medium
def appstore(ct): return f'https://apps.apple.com/app/apple-store/id{APP_ID}?pt=129099104&ct={ct}&mt=8'
def play(medium): return ('https://play.google.com/store/apps/details?id=com.terryouyang.glyphraid'
                          f'&referrer=utm_source%3Dglyphraid_site%26utm_medium%3D{medium}')

# ── 國旗（照 app components/language-flag.tsx） ──
def star(cx, cy, r, rot=0.0):
    import math
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.382
        a = rot + math.pi * i / 5 - math.pi / 2
        pts.append(f'{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}')
    return ' '.join(pts)

def stripes_h(colors):
    n = len(colors); return ''.join(f'<rect x="0" y="{20 / n * i:.3f}" width="30" height="{20 / n + 0.01:.3f}" fill="{c}"/>' for i, c in enumerate(colors))

def stripes_v(colors):
    n = len(colors); return ''.join(f'<rect x="{30 / n * i:.3f}" y="0" width="{30 / n + 0.01:.3f}" height="20" fill="{c}"/>' for i, c in enumerate(colors))

def korean():
    import math
    s = '<rect width="30" height="20" fill="#FFFFFF"/>'
    s += '<path d="M10 10 A5 5 0 0 1 20 10 A2.5 2.5 0 0 1 15 10 A2.5 2.5 0 0 0 10 10 Z" fill="#CD2E3A"/>'
    s += '<path d="M10 10 A5 5 0 0 0 20 10 A2.5 2.5 0 0 1 15 10 A2.5 2.5 0 0 0 10 10 Z" fill="#0047A0"/>'
    for x, y, a in ((6.5, 5.3, -61), (23.5, 5.3, 61), (6.5, 14.7, 61), (23.5, 14.7, -61)):
        s += (f'<path d="M{x - 2} {y - 1.1:.1f} h4 v0.8 h-4 Z M{x - 2} {y + 0.3:.1f} h4 v0.8 h-4 Z" fill="#000000" '
              f'transform="rotate({a} {x} {y})"/>')
    return s

FLAGS = {
    'thai': stripes_h(['#A51931', '#F4F5F8', '#2D2A4A', '#2D2A4A', '#F4F5F8', '#A51931']),  # app：紅白藍(兩倍)白紅
    'japanese': '<rect width="30" height="20" fill="#FFFFFF"/><circle cx="15" cy="10" r="6" fill="#BC002D"/>',  # 紅圓直徑＝旗高 3/5
    'english': ''.join(f'<rect x="0" y="{20 / 13 * i:.3f}" width="30" height="{20 / 13 + 0.01:.3f}" fill="{"#FFFFFF" if i % 2 else "#B22234"}"/>' for i in range(13))
               + f'<rect x="0" y="0" width="12" height="{20 / 13 * 7:.3f}" fill="#3C3B6E"/>'
               + ''.join(f'<circle cx="{1.8 + c * 2.8:.1f}" cy="{1.9 + r * 3.3:.1f}" r="0.55" fill="#FFFFFF"/>' for r in range(3) for c in range(4)),
    'spanish': '<rect width="30" height="20" fill="#AA151B"/><rect x="0" y="5" width="30" height="10" fill="#F1BF00"/>',
    'korean': korean(),
    'french': stripes_v(['#0055A4', '#FFFFFF', '#EF4135']),
    'german': stripes_h(['#000000', '#DD0000', '#FFCE00']),
    'portuguese': ('<rect width="30" height="20" fill="#009C3B"/><polygon points="15,2.2 27.5,10 15,17.8 2.5,10" fill="#FFDF00"/>'
                   '<circle cx="15" cy="10" r="4.6" fill="#002776"/><path d="M10.6 9.2 Q15 7.6 19.5 10.6 L19.3 11.4 Q15 8.6 10.5 10 Z" fill="#FFFFFF"/>'),
    'chinese': ('<rect width="30" height="20" fill="#EE1C25"/>' + f'<polygon points="{star(5, 5, 3)}" fill="#FFFF00"/>'
                + ''.join(f'<polygon points="{star(x, y, 1, r)}" fill="#FFFF00"/>' for x, y, r in ((10, 2, 0.6), (12, 4, 1.1), (12, 7, 0), (10, 9, 0.5)))),
    'italian': stripes_v(['#009246', '#FFFFFF', '#CE2B37']),
    'indonesian': stripes_h(['#CE1126', '#FFFFFF']),
    'turkish': ('<rect width="30" height="20" fill="#E30A17"/><circle cx="11.2" cy="10" r="5" fill="#FFFFFF"/>'
                '<circle cx="12.45" cy="10" r="4" fill="#E30A17"/>' + f'<polygon points="{star(17.6, 10, 2.1, -1.5707963)}" fill="#FFFFFF"/>'),
}
HELLO = {'thai': ('สวัสดี', 'th'), 'japanese': ('こんにちは', 'ja'), 'english': ('Hello', 'en'), 'spanish': ('¡Hola!', 'es'),
         'korean': ('안녕하세요', 'ko'), 'french': ('Bonjour', 'fr'), 'german': ('Hallo', 'de'), 'portuguese': ('Olá', 'pt-BR'),
         'chinese': ('你好', 'zh-Hans'), 'italian': ('Ciao', 'it'), 'indonesian': ('Halo', 'id'), 'turkish': ('Merhaba', 'tr')}

PAGES = {
    'en': dict(
        out='index.html', up='', html_lang='en', canonical='https://glyphraid.com/',
        title='Glyphraid · Learn a language by fighting monsters',
        desc=('A language learning game for iPhone and Android. Thai, Japanese, Korean, Spanish, French, German, Portuguese, '
              'Chinese, Italian, Indonesian and Turkish. Every monster holds a word card: answer it to strike, miss and it hits you. '
              'Free to start, one payment unlocks everything. No ads, no subscription.'),
        og_desc='Every monster holds a word card. Answer it and you strike. Miss and it hits you.',
        og_locale='en_US',
        switch=('zh/?hl=zh', 'zh-Hant', 'zh', '中文'),
        home_label='Glyphraid home',
        h1='Learn a language by fighting monsters.',
        lede='Every monster holds a word card. Answer it and you strike. Miss and it hits you.',
        langs_label='11 languages',
        langs=[('thai', 'Thai'), ('japanese', 'Japanese'), ('spanish', 'Spanish'), ('korean', 'Korean'), ('french', 'French'),
               ('german', 'German'), ('portuguese', 'Portuguese'), ('chinese', 'Chinese'), ('italian', 'Italian'),
               ('indonesian', 'Indonesian'), ('turkish', 'Turkish')],
        price='<b>Free to start.</b> One payment of US$9.99 unlocks all 11 languages. No ads, no subscription.',
        badge_as='Download on the App Store', badge_gp='Get it on Google Play',
        qr_alt='QR code that opens glyphraid.com/get on your phone', qr_text='Scan with your phone to download.',
        phone_alt='The battle screen in the app: a monster takes a hit after a right answer.',
        feats_label='What is in the game',
        feats=[('classes', 'feat-classes-3.webp', 'Pick a class', 'Archer, Swordsman or Mage'),
               ('relics', 'feat-relics.webp', 'Collect relics', '50+ to find'),
               ('boss', 'feat-boss-5.webp', 'Beat the boss', "Can you beat the dungeon's guardian?"),
               ('words', 'feat-words.webp', '17,000+ word cards', 'Audio and notes on nearly every card')],
        feat_alts={'classes': 'The three classes: Archer, Swordsman and Mage.',
                   'relics': 'Three relics from the game.', 'boss': 'The Briar Hulk, a forest boss.',
                   'words': 'Theme icons: food, animals, travel, chat, home, festivals.'},
        foot='© 2026 Glyphraid. Made by one person learning Thai.',
        privacy='Privacy', delete='Delete my data',
    ),
    'zh': dict(
        out='zh/index.html', up='../', html_lang='zh-Hant', canonical='https://glyphraid.com/zh/',
        title='Glyphraid｜打怪學語言',
        desc=('語言學習遊戲，iPhone、Android 都有。泰文、日文、英文、韓文、西班牙文、法文、德文、葡萄牙文、義大利文、印尼文、土耳其文。'
              '每隻怪都帶著一張字卡：答對你打牠，答錯牠打你。免費開始，一次付費解鎖全部，沒有廣告、沒有訂閱。'),
        og_desc='每隻怪都帶著一張字卡。答對你打牠，答錯牠打你。',
        og_locale='zh_TW',
        switch=('../?hl=en', 'en', 'en', 'English'),
        home_label='Glyphraid 首頁',
        h1='打怪學語言',
        lede='每隻怪都帶著一張字卡。答對你打牠，答錯牠打你。',
        langs_label='11 種語言',
        langs=[('thai', '泰文'), ('japanese', '日文'), ('english', '英文'), ('spanish', '西班牙文'), ('korean', '韓文'),
               ('french', '法文'), ('german', '德文'), ('portuguese', '葡萄牙文'), ('italian', '義大利文'),
               ('indonesian', '印尼文'), ('turkish', '土耳其文')],
        price='<b>免費開始。</b>一次付費 US$9.99，11 種語言全部解鎖。沒有廣告、沒有訂閱。',
        price_zh_html=('<b>免費開始。</b><span class="nb">一次付費 US$9.99，</span><span class="nb">11 種語言全部解鎖。</span>'
                       '<span class="nb">沒有廣告、</span><span class="nb">沒有訂閱。</span>'),
        badge_as='在 App Store 下載', badge_gp='在 Google Play 下載',
        qr_alt='用手機掃描，打開 glyphraid.com/get', qr_text='用手機掃描下載。',
        phone_alt='app 的戰鬥畫面：答對之後怪物被打中。',
        feats_label='遊戲裡有什麼',
        feats=[('classes', 'feat-classes-3.webp', '選職業', '弓手、劍士、法師'),
               ('relics', 'feat-relics.webp', '收集聖物', '超過 50 種可以收集'),
               ('boss', 'feat-boss-5.webp', '打倒魔王', '你能打敗|地城的守門人嗎？'),
               ('words', 'feat-words.webp', '超過|17,000 張字卡', '每張都有發音，幾乎每張都有說明')],
        feat_alts={'classes': '三種職業：弓手、劍士、法師。', 'relics': '遊戲裡的三顆聖物。',
                   'boss': '森林的魔王：荊棘巨人。', 'words': '主題圖示：食物、動物、旅行、聊天、家、節慶。'},
        foot='© 2026 Glyphraid。一個正在學泰文的人做的。',
        privacy='隱私權政策', delete='刪除我的資料',
    ),
}


def esc(s): return html.escape(s, quote=True)


def nb_parts(s, sep=' '):
    # 標題裡用 | 標出唯一准換行的位置（中文長標題，盲審 r2：「…張字／卡」孤字）；沒有 | 就原樣
    if '|' not in s: return esc(s)
    return sep.join(f'<span class="nb">{esc(x)}</span>' for x in s.split('|'))


def clauses(s):
    # 中文：每個子句（到 。，、 為止）包成不換行的 span，只准在標點後換行（盲審 r1）。英文原樣。
    import re
    parts = re.findall(r'[^。，、]+[。，、]?', s)
    return ''.join(f'<span class="nb">{p}</span>' for p in parts)


def flag_list(p):
    items = []
    for key, name in p['langs']:
        hello, hl = HELLO[key]
        items.append(
            f'<li><svg viewBox="0 0 30 20" preserveAspectRatio="none" aria-hidden="true">{FLAGS[key]}</svg>'
            f'<b>{esc(name)}</b><span lang="{hl}">{esc(hello)}</span></li>')
    return '\n        '.join(items)


def feats(p):
    up = p['up']; out = []
    for key, img, label, sub in p['feats']:
        out.append(
            f'<li><img src="{up}assets/v2/{img}" alt="{esc(p["feat_alts"][key])}" width="392" height="294" loading="lazy">'
            f'<b>{nb_parts(label)}</b><span>{(nb_parts(sub, "") if "|" in sub else clauses(esc(sub))) if p["html_lang"] != "en" else esc(sub)}</span></li>')
    return '\n      '.join(out)


def badges(p, where):
    up = p['up']
    return (f'<a class="b-as" href="{esc(appstore(where))}"><img src="{up}assets/badge-appstore.svg" alt="{esc(p["badge_as"])}" width="144" height="48"></a>\n'
            f'          <a class="b-gp" href="{esc(play(where))}"><img src="{up}assets/badge-play-tight.png" alt="{esc(p["badge_gp"])}" width="161" height="48"></a>')


def page(p):
    up = p['up']; sw = p['switch']; zh = p['html_lang'] != 'en'
    return f'''<!doctype html>
<html lang="{p['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<!-- ⚠️ 這頁由 tools/build-home.py 產生，不要手改。 -->
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['desc'])}">
<meta name="theme-color" content="#1D2A12">
<!-- 內容安全政策：腳本只准本站的檔案（assets/site.js）和雜湊相符的那一段內嵌腳本（語言）。⚠️ 改了內嵌腳本一定要跑 python3 tools/update-csp.py -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self'; font-src 'self'; media-src 'none'; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<link rel="canonical" href="{p['canonical']}">
<link rel="alternate" hreflang="en" href="https://glyphraid.com/">
<link rel="alternate" hreflang="zh-Hant" href="https://glyphraid.com/zh/">
<link rel="alternate" hreflang="x-default" href="https://glyphraid.com/">
<!-- 語言：第一次來、瀏覽器第一語言是中文、沒選過 → 轉到 /zh/；右上角的切換連結帶 ?hl=，到了這頁才記住選擇；只有首頁會轉 -->
<script>{LANG_SNIPPET}</script>

<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['og_desc'])}">
<meta property="og:locale" content="{p['og_locale']}">
<meta property="og:image" content="https://glyphraid.com/assets/{'og-zh.jpg' if zh else 'og.jpg'}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" type="image/png" href="{up}assets/favicon.png">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" href="{up}assets/fonts/dela-gothic-one-400-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{up}assets/fonts/nunito-latin.woff2" crossorigin>
<link rel="preload" as="image" href="{up}assets/v2/bg.webp">
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body{' class="zh"' if zh else ''}>
<div class="page">
  <header class="top">
    <a class="brand" href="./" aria-label="{esc(p['home_label'])}">
      <img src="{up}assets/favicon.png" alt="" width="36" height="36">
      <b>Glyphraid</b>
    </a>
    <nav class="toplinks"><a href="{sw[0]}" hreflang="{sw[1]}" lang="{sw[1]}" data-lang="{sw[2]}">{sw[3]}</a></nav>
  </header>

  <main class="main">
    <div class="copy">
      <h1>{esc(p['h1'])}</h1>
      <p class="lede">{clauses(esc(p['lede'])) if zh else esc(p['lede'])}</p>

      <ul class="langs" aria-label="{esc(p['langs_label'])}">
        {flag_list(p)}
      </ul>

      <div class="getbox" id="get">
        <div class="get">
          {badges(p, 'web')}
        </div>
        <!-- 只給電腦版看：手機掃了到 /get/，依平台轉去商店（tools/qr.py） -->
        <div class="qr"><img src="{up}assets/qr-get.svg" alt="{esc(p['qr_alt'])}" width="87" height="87"><p>{esc(p['qr_text'])}</p></div>
      </div>
      <p class="price">{p['price_zh_html'] if zh else p['price']}</p>
    </div>

    <div class="stage">
      <div class="phone"><img src="{up}assets/v2/battle-{'zh' if zh else 'en'}.webp" alt="{esc(p['phone_alt'])}" width="640" height="1391"></div>
    </div>

    <ul class="feats" aria-label="{esc(p['feats_label'])}">
      {feats(p)}
    </ul>
    <!-- 只在手機版顯示：特點看完不用捲回頂端（site.css 的 .get-end） -->
    <div class="get get-end">
          {badges(p, 'finish')}
    </div>
  </main>

  <footer class="foot">
    <span>{esc(p['foot'])}</span>
    <span class="sp"></span>
    <a href="mailto:terry@glyphraid.com">terry@glyphraid.com</a>
    <a href="privacy.html">{esc(p['privacy'])}</a>
    <a href="delete-data.html">{esc(p['delete'])}</a>
  </footer>
</div>
<script src="{up}assets/site.js"></script>
</body>
</html>
'''


for p in PAGES.values():
    with open(os.path.join(ROOT, p['out']), 'w', encoding='utf-8') as f:
        f.write(page(p))
    print('wrote', p['out'])
