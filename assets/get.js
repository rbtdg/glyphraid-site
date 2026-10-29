/* /get/：首頁電腦版 QR code 指向這頁（tools/qr.py）。
   手機掃了就依平台直接轉去對的商店；判斷不出來（電腦、其他裝置）就留在這頁，兩個商店按鈕都給。
   商店網址只寫在 get/index.html 的兩個按鈕上，這裡讀按鈕的 href，不另寫一份。 */
(function(){
  var ua = navigator.userAgent;
  // iPadOS 13 起 Safari 預設自稱 Mac，靠觸控點數分辨
  var ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  var to = ios ? 'ios' : /Android/.test(ua) ? 'android' : null;
  if (to) location.replace(document.getElementById(to).href);
})();
