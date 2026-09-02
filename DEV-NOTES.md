# glyphraid-site 工作筆記

> 給下一個 session 的 Claude（或未來的自己）。這裡只記「動這個 repo 需要知道的事」；
> 行銷計畫住 Claude 的 Artifact 頁、進度住 Vask repo 的 ROADMAP〈送審之後〉。

## 現狀（2026-09-02）

- `main` ＝ 舊佔位頁（**線上版**，GitHub Pages 正在服務它；兩個商店後台的
  隱私政策／支援頁網址都指著它，iOS 審核中，**不要動**）。
- `landing` ＝ 完整落地頁 v5.1，**Terry 2026-09-02 驗收通過**，等 iOS 核准後上線。
- `privacy.html` 兩個 branch 一字未動。

## 🔴 上線開關（iOS 核准後，四步）

1. merge `landing` 進 `main`（＝立刻上線）。
2. `index.html` 裡搜 `TODO(ios-live)`，三處：Smart App Banner 填 App Store ID、
   App Store badge 換掉「審核中」文字、（QR 改指 glyphraid.com，等第 3 步做完）。
3. Porkbun 把 `glyphraid.com` 指到 GitHub Pages ＋ repo 設 custom domain
   （github.io 會 301 過去，商店後台網址不用改）。⚠️ 審核期間不要綁網域。
4. Vask 的 ROADMAP〈送審之後〉與行銷計畫 Artifact 勾掉這格。

## 設計方向（v4 定案「紙上美術館」，五版回爐的結論）

- **單一暖紙底**；Fraunces 襯線大標＋Nunito Sans 內文；全頁唯一深色塊＝價格木牌。
- **像素資產當藝術品陳列**：海報＝墨線框＋硬偏移影＋微傾斜；怪物站在專用舞台圖上。
- Terry 判過退的（**不要走回去**）：色帶交替、統一圓角卡片網格、彩色警示框、
  綠底容器裝 sprites、暗色整頁（v1）、把直式圖 cover 撐寬螢幕（v3 的「一片土」）、
  文案長段落、空話（"no way to deal damage"）、emoji 混進標本系統。
- 怪物遊行五隻＝兔 thornhare／星座龜 glyphmite／符文羊 runeram／粉紅蝸牛 pearlsnail／
  蘑菇蛙 sporetoad——**矮胖土系、主題不重複**；魔王臉的（骨蛇、發條龍）不上首頁。
- **對外講遊戲機制的每一句話都要先過程式**（兩次被 Terry 抓錯的教訓）：
  五階＝New/Learning/Familiar/Mastered/**Proficient**（`Vask/logic/tiers.ts`）、
  五階顏色＝`Vask/config/theme.ts` 的 `TIER_COLORS`、
  商店＝常駐頁而非 run 內節點（金幣永久解鎖聖物）。
  文案的單一事實來源＝`Vask/store-assets/store-listing.md`；**零破折號**。

## 驗證管線（改完必跑，一個都不省）

```bash
# 桌機（headless Chrome 全頁；⚠️ 視窗最小寬 500px，390 的截圖是 500 版面的置中裁切，
#      不能當行動版證據）
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --hide-scrollbars --virtual-time-budget=9000 --screenshot=/tmp/site.png \
  --window-size=1440,4700 "file://$HOME/glyphraid-site/index.html"

# 行動版＝iOS 模擬器 Safari（唯一可信的行動版證據）
cd ~/Vask && bash scripts/ios-env.sh boot
python3 -m http.server 8791 --bind 127.0.0.1   # ⚠️ 要在非 sandbox shell 起,否則外部程序連不到
xcrun simctl openurl booted "http://127.0.0.1:8791/index.html?v=隨便換個數字"
#                                                    ^^^^ ⚠️ 模擬器 Safari 吃快取,
#                                                    複驗不帶 cache-buster 會看到舊版（吃過一次虧）
bash scripts/ios-env.sh shot 名字
```

- **橫向溢出**用頁內量測探針驗（把印 `vw/scrollW/超寬元素` 的 script 注入複本頁），
  不要用眼睛判。頁面已有三層防線：crew 尺寸總和 ≤336px、`.mural{overflow:hidden}`、
  `html,body{overflow-x:clip}`。
- 常見病根備忘：`img` reset 要含 `height:auto`；同一元素兩個 class 時
  `padding` shorthand 會把 `.wrap` 的左右 padding 蓋掉歸零；grid 子項要 `min-width:0`。

## 素材重出

- 生成走 Vask 的 Wavespeed 管線：`node ~/Vask/scripts/art/generate.mjs <jobs.json>`
  （kind=bg、`aspect_ratio:"16:9"`、quality=low ≈ $0.01/張）。
  `bg_valley_wide`（hero）與 `bg_stage`（怪物舞台）的 prompt 在
  Claude session 的 scratchpad 已散佚——要改就重寫 prompt，重點：
  舞台＝「中央整片開闊亮草地、樹線天空只留頂端、花只在角落、無人物無文字」。
- 海報＝`Vask/store-assets/screenshots/out/` 的商店圖直轉 webp（hero 用 **en-android/01**，
  iOS 版偏暗被判退）。怪物＝`Vask/assets/sprites/enemies/pool/` 裁邊轉 200px PNG。
- og.jpg ＝ main.png 天空＋logo＋吉祥物（亮版）。
