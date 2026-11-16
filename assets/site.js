/* 首頁：手機上依平台只留一顆商店按鈕（2026-11-16 改版；研究結論：主按鈕只有一顆比較清楚）。
   判斷不出來（電腦、其他裝置）就兩顆都留。判斷法跟 assets/get.js 一樣。
   沒有 JavaScript 時兩顆都在，不影響下載。 */
(function(){
  var ua = navigator.userAgent;
  // iPadOS 13 起 Safari 預設自稱 Mac，靠觸控點數分辨
  var ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  var os = ios ? 'ios' : /Android/.test(ua) ? 'android' : null;
  if (os) document.documentElement.classList.add('is-' + os);
  // 分享預覽圖的截圖版面（site.css 的 .og；只在產 og.jpg 時用）
  if (/[?&]og=1/.test(location.search)) document.documentElement.classList.add('og');
})();
