/* 手機裡的「新手第一場」（index.html 與 zh/index.html 共用；頁面的 <html lang> 決定用哪一套字）。
   規則照 app：答對打怪 1、答錯被打 1；傷害只來自答對字卡。打贏就收尾（不無限出怪），打輸＝重試畫面。
   app 1.3.2 起戰鬥卡沒有 NEW 標籤，新卡只靠燈泡 💡。
   中文字串照 app 的 zh-TW 介面（Vask config/i18n.ts、data/cards.ts）。改了中文字，要重跑 tools/huninn-zh.py（粉圓子集）。 */
(() => {
  const ZH = /^zh/i.test(document.documentElement.lang);
  const BASE = document.currentScript.src;   // 音檔路徑跟著這支檔案走（/ 和 /zh/ 都對）
  // config/onboarding.ts 的 ONBOARDING_CARD_IDS；資料照 data/letter-cards.ts
  const CARDS = [
    ['letter-ko-kai', 'ก', 'g / k', 'gor', 'gài', 'ไก่', 'chicken', '雞'],
    ['letter-mo-ma', 'ม', 'm', 'mor', 'máa', 'ม้า', 'horse', '馬'],
    ['letter-no-nu', 'น', 'n', 'nor', 'nǔu', 'หนู', 'mouse', '鼠'],
    ['letter-do-dek', 'ด', 'd', 'dor', 'dèk', 'เด็ก', 'child', '小孩'],
    ['letter-so-suea', 'ส', 's', 'sǒr', 'sǔea', 'เสือ', 'tiger', '虎'],
    ['letter-ro-ruea', 'ร', 'r', 'ror', 'ruea', 'เรือ', 'boat', '船'],
  ].map(([id, th, rom, sound, ex, exTh, exEn, exZh]) => ({ id, th, rom, sound, ex, exTh, exMean: ZH ? exZh : exEn, name: `${sound} ${ex}` }));

  // 動態的字（頁面上固定的字寫在 HTML 裡）。教學提示＝app 的 coach.answer、battle.introNewCard1/2 原文
  const T = ZH ? {
    coach: [['這是一張字卡。選對它的讀音，就是你這一回合的攻擊。'], ['角落有燈泡 💡 的字，是你第一次遇到。', '想先看看它是什麼，就點燈泡。看完這題還是要自己答。']],
    letters: n => `${n} 個字母`,
    liveRight: c => `答對了。${c.th} 是 ${c.name}。`,
    liveWrong: c => `答錯了。${c.th} 是 ${c.name}。怪打了你一下。`,
    liveWon: '打倒怪了，第一場贏了。',
    wordsH: '打打看第一場。',
    wonH: '第一場贏了。',
    tallyWon: w => `<b>你學會了 ${w}。</b>`,
    tally: w => `目前 <b>${w}</b>。`,
    underWon: '<b>這場贏了。</b>在 app 裡，下一步是商店。',
    dock: w => `<b>${w}。</b>app 會教完全部 44 個子音。`,
    dockWon: w => `<b>第一場贏了。</b>學會 ${w}。app 會教完全部 44 個子音。`,
    notes: c => [
      `${c.sound} 是這個字母單獨的唸法。`,
      `${c.ex} 是它的例字 <span lang="th">${c.exTh}</span>（${c.exMean}）。泰文字母都用「唸法＋例字」當名字，方便區分同音字母。`,
      `在單字裡，這個字母發 ${c.rom} 的音。`,
    ],
  } : {
    coach: [['This is a flashcard. Getting it right is your attack for the turn.'], ['A card with a bulb 💡 in the corner is one you are seeing for the first time.', 'Tap the bulb to look it up. You still have to answer it yourself.']],
    letters: n => `${n} ${n === 1 ? 'letter' : 'letters'}`,
    liveRight: c => `Correct. ${c.th} is ${c.name}.`,
    liveWrong: c => `Wrong. ${c.th} is ${c.name}. The monster hits you.`,
    liveWon: 'Monster defeated. You won your first fight.',
    wordsH: 'Play the first fight.',
    wonH: 'You won your first fight.',
    tallyWon: w => `<b>You learned ${w}.</b>`,
    tally: w => `<b>${w}</b> so far.`,
    underWon: '<b>Fight won.</b> In the app, the shop is next.',
    dock: w => `<b>${w}.</b> The app teaches all 44 consonants.`,
    dockWon: w => `<b>You won your first fight.</b> ${w} learned. The app teaches all 44 consonants.`,
    notes: c => [
      `${c.sound} is how this letter is pronounced on its own.`,
      `${c.ex} is its example word <span lang="th">${c.exTh}</span> (${c.exMean}). Every Thai letter is named “sound + example word”, to tell same-sounding letters apart.`,
      `In words, this letter makes the sound ${c.rom}.`,
    ],
  };

  const MON_HP = 3, YOU_HP = 10;             // ONBOARDING_MONSTER_HP / PLAYER_MAX_HP
  const NEW_PER_FIGHT = 5;                   // NEW_CARDS_PER_BATTLE
  const NEXT_AFTER_RIGHT = 900, NEXT_AFTER_WRONG = 1500;
  const COACH = [
    { target: 'card', lines: T.coach[0] },
    { target: 'bulb', lines: T.coach[1] },
  ];

  const $ = id => document.getElementById(id);
  const screen = $('screen'), card = $('card'), opts = $('opts'), mon = $('mon'), monimg = $('monimg');
  const UNDER = $('under').textContent;
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const narrow = matchMedia('(max-width:860px)');
  const audio = {};

  let monHp, youHp, cur, queue, last, busy, over, coachStep = 0;
  let answeredEarly = false;
  const answered = new Set();                // 答過一次就不再是新卡（對錯都算）
  const learned = [];                        // 答對過的字（輸了也不會被拿走）

  // ── 小工具 ──
  const at = el => { const s = screen.getBoundingClientRect(), b = el.getBoundingClientRect(); return { x: b.left - s.left + b.width / 2, y: b.top - s.top + b.height / 2, b, s }; };
  function add(cls, x, y, text){ const e = document.createElement('div'); e.className = cls; e.style.left = x + 'px'; e.style.top = y + 'px'; if (text) e.textContent = text; screen.appendChild(e); return e; }
  function replay(el, cls){ el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }
  function fly(from, to, foe){
    const a = at(from), b = at(to);
    const ball = add('ball' + (foe ? ' foe' : ''), a.x, a.y);
    return ball.animate([{ transform: 'translate(0,0)' }, { transform: `translate(${b.x - a.x}px,${b.y - a.y}px)` }],
      { duration: still ? 1 : 260, easing: 'cubic-bezier(.5,0,.9,.6)' }).finished.then(() => { ball.remove(); return b; });
  }
  function burst(x, y){
    const e = add('burst', x, y);
    for (let i = 0; i < 6; i++) { const s = document.createElement('s'), t = i / 6 * Math.PI * 2; s.style.setProperty('--x', Math.cos(t) * 34 + 'px'); s.style.setProperty('--y', Math.sin(t) * 34 + 'px'); e.appendChild(s); }
    setTimeout(() => e.remove(), 340);
  }
  function dmg(x, y, text = '-1'){ const e = add('dmg', x, y, text); setTimeout(() => e.remove(), 1800); return e; }
  function bars(){
    $('monfill').style.transform = `scaleX(${monHp / MON_HP})`; $('monnum').textContent = `${monHp} / ${MON_HP}`;
    $('youfill').style.transform = `scaleX(${youHp / YOU_HP})`; $('younum').textContent = `${youHp} / ${YOU_HP}`;
  }
  function say(c){ const a = audio[c.id] || (audio[c.id] = new Audio(new URL(`audio/${c.id}.mp3`, BASE).href)); a.currentTime = 0; a.play().catch(() => {}); }

  // ── 一場戰鬥 ──
  function startFight(){
    monHp = MON_HP; youHp = YOU_HP; over = false; last = null;
    // 這一場會出現的 5 張（6 張裡隨機挑），先出還沒答過的
    const pick = shuffle(CARDS.slice()).slice(0, NEW_PER_FIGHT);
    queue = [...pick.filter(c => !answered.has(c.id)), ...pick.filter(c => answered.has(c.id))];
    screen.classList.remove('gone'); mon.classList.remove('down', 'hit');
    screen.querySelectorAll('.coin').forEach(c => c.remove());
    bars(); deal();
  }
  function deal(){
    if (!queue.length) queue = shuffle(CARDS.filter(c => c !== last)).slice(0, 3);
    cur = queue.shift(); last = cur;
    const choices = shuffle([cur, ...shuffle(CARDS.filter(c => c !== cur)).slice(0, 3)]);
    $('th').textContent = cur.th; $('mean').textContent = '';
    card.classList.remove('bad'); card.classList.toggle('seen', answered.has(cur.id)); replay(card, 'enter');
    opts.innerHTML = '';
    choices.forEach(c => {
      const b = document.createElement('button');
      b.className = 'opt'; b.type = 'button'; b.dataset.id = c.id; b.textContent = c.name;
      b.addEventListener('click', () => answer(b));
      opts.appendChild(b);
    });
    opts.removeAttribute('aria-busy'); busy = false;
  }

  async function answer(btn){
    if (busy || over) return; busy = true; opts.setAttribute('aria-busy', 'true');
    answeredEarly = true;
    $('under').textContent = UNDER;
    const right = btn.dataset.id === cur.id;
    answered.add(cur.id);
    if (right){
      btn.classList.add('right'); card.classList.add('seen');
      $('live').textContent = T.liveRight(cur);
      const p = await fly($('you').querySelector('.hp'), monimg, false);
      burst(p.x, p.y); replay(mon, 'hit');
      monHp -= 1; bars();
      const c = at(card);
      dmg(c.x + c.b.width * .42, c.b.bottom - c.s.top + 2);
      replay(document.querySelector('.phone'), 'jolt');
      collect(cur);
      if (monHp === 0) return win();
      await wait(NEXT_AFTER_RIGHT);
    } else {
      btn.classList.add('wrong');
      [...opts.children].find(b => b.dataset.id === cur.id).classList.add('reveal');
      card.classList.add('bad'); $('mean').textContent = cur.name;
      $('live').textContent = T.liveWrong(cur);
      queue.splice(Math.min(3, queue.length), 0, cur);   // 答錯的卡隔幾張再回來（REVIEW_MIN_GAP_CARDS）
      replay(mon, 'lunge');
      const p = await fly(monimg, $('you').querySelector('.hp'), true);
      burst(p.x, p.y); replay($('you'), 'hurt');
      youHp -= 1; bars();
      dmg(p.b.left - p.s.left + p.b.width * .78, p.b.top - p.s.top - 30);
      await wait(NEXT_AFTER_WRONG);
      if (youHp === 0) return lose();
    }
    deal();
  }

  // 打贏：怪連同字卡、血條淡出，掉 6 枚金幣＋「+35」，然後收尾
  async function win(){
    over = true;
    screen.classList.add('gone');
    $('live').textContent = T.liveWon;
    const m = at(monimg);
    for (let i = 0; i < 6; i++) { const e = add('coin', m.x, m.b.bottom - m.s.top - 6); e.style.setProperty('--x', (i - 2.5) * 14 + 'px'); e.style.animationDelay = i * 50 + 'ms'; }
    const plus = dmg(m.x, m.b.top - m.s.top + m.b.height * .3, '+35'); plus.style.color = '#F1CE8A';
    firefly();
    await wait(1100);
    finish();
  }
  function finish(){
    const w = T.letters(learned.length);
    $('words-h').textContent = T.wonH;
    $('tally').innerHTML = T.tallyWon(w);
    $('words').classList.add('won');
    $('under').innerHTML = T.underWon;
    if (narrow.matches){
      const d = $('dock');
      $('docktext').innerHTML = T.dockWon(w);
      $('dockwords').innerHTML = learned.map(c => `<li lang="th">${c.th}</li>`).join('');
      d.classList.add('show', 'won'); d.removeAttribute('aria-hidden');
      document.body.classList.add('won-page');
      d.querySelectorAll('[tabindex]').forEach(x => x.removeAttribute('tabindex'));
      document.body.classList.add('docked');
    }
  }
  function lose(){
    over = true;
    $('retry').classList.add('show'); $('retrybtn').focus({ preventScroll: true });
    $('under').textContent = '';
  }
  $('retrybtn').addEventListener('click', () => { $('retry').classList.remove('show'); $('under').textContent = UNDER; startFight(); });
  document.querySelectorAll('[data-again]').forEach(b => b.addEventListener('click', () => {
    $('words').classList.remove('won'); $('words-h').textContent = T.wordsH;
    $('dock').classList.remove('won'); document.body.classList.remove('won-page');
    $('dockwords').innerHTML = learned.slice(0, 2).map(c => `<li lang="th">${c.th}</li>`).join('');
    tally(); startFight();
    if (narrow.matches) scrollToPhone();
  }));

  // ── 教學提示（照 coach-mark：壓暗、金框圈住目標、吉祥物在下方，點任何地方繼續） ──
  function showCoach(){
    const step = COACH[coachStep];
    if (!step) { $('coach').classList.remove('show'); return; }
    const t = step.target === 'card' ? card : $('bulb');
    const s = screen.getBoundingClientRect(), b = t.getBoundingClientRect(), pad = 8;
    Object.assign($('hole').style, { left: b.left - s.left - pad + 'px', top: b.top - s.top - pad + 'px', width: b.width + pad * 2 + 'px', height: b.height + pad * 2 + 'px' });
    $('coachtext').innerHTML = step.lines.map(l => `<p>${l}</p>`).join('');
    $('coach').classList.add('show');
  }
  function nextCoach(){ coachStep++; showCoach(); }
  $('coach').addEventListener('click', nextCoach);

  // ── 燈泡詳解（照 card-detail-dialog；文字照 data/cards.ts 的字母模板） ──
  function openDetail(){
    if (busy || over) return;
    $('dglyph').textContent = cur.th; $('drom').textContent = cur.rom; $('dname').textContent = cur.name;
    $('dnotes').innerHTML = T.notes(cur).map((t, i) => `<li><b>${i + 1}</b><span>${t}</span></li>`).join('');
    $('detail').classList.add('show'); $('dclose').focus({ preventScroll: true });
  }
  function closeDetail(){ $('detail').classList.remove('show'); $('bulb').focus({ preventScroll: true }); }
  $('bulb').addEventListener('click', openDetail);
  $('dclose').addEventListener('click', closeDetail);
  $('dspeak').addEventListener('click', () => say(cur));

  // ── 答對的字飛出手機，落進「你的字」（手機版落進底部條） ──
  const ua = navigator.userAgent;
  if (/iPhone|iPad|iPod/.test(ua)) $('dockcta').href = 'https://apps.apple.com/app/id6785621868';
  else if (/Android/.test(ua)) $('dockcta').href = 'https://play.google.com/store/apps/details?id=com.terryouyang.glyphraid&referrer=utm_source%3Dglyphraid_site%26utm_medium%3Ddock';
  function scrollToPhone(){
    setTimeout(() => {
      const ph = document.querySelector('.phone').getBoundingClientRect(), dk = $('dock').getBoundingClientRect();
      const d = ph.bottom - (dk.top - 12);
      if (d > 0) scrollBy({ top: d, behavior: still ? 'auto' : 'smooth' });
    }, 350);
  }
  function tile(c){
    if (narrow.matches){
      const ol = $('dockwords'), li = document.createElement('li');
      li.lang = 'th'; li.textContent = c.th; ol.prepend(li);
      while (ol.children.length > 2) ol.lastElementChild.remove();
      const first = !$('dock').classList.contains('show');
      document.body.classList.add('docked'); $('dock').classList.add('show');
      $('dock').removeAttribute('aria-hidden'); $('dockcta').removeAttribute('tabindex');
      if (first) scrollToPhone();
      return li;
    }
    const slots = $('slots'), li = document.createElement('li');
    li.className = 'got'; li.innerHTML = `<span class="th" lang="th">${c.th}</span><span class="en">${c.name}</span>`;
    slots.prepend(li);
    const empty = [...slots.children].filter(x => !x.classList.contains('got'));
    if (empty.length) empty[empty.length - 1].remove(); else slots.lastElementChild.remove();
    slots.querySelectorAll('li:not(.got)').forEach((x, i) => { x.className = i === 0 ? 'next' : ''; x.textContent = ''; });
    return li;
  }
  function collect(c){
    if (learned.some(w => w.id === c.id)) return;
    learned.unshift(c);
    const li = tile(c);
    tally();
    li.style.visibility = 'hidden';
    const show = () => { li.style.visibility = ''; replay(li, 'land'); };
    const go = () => {
      const from = $('th').getBoundingClientRect(), to = li.getBoundingClientRect();
      if (still || !to.width || to.top > innerHeight || to.bottom < 0) return show();
      const f = document.createElement('div'); f.className = 'flyword'; f.lang = 'th'; f.textContent = c.th;
      f.style.fontSize = getComputedStyle($('th')).fontSize;
      const x0 = from.left + from.width / 2, y0 = from.top + from.height / 2;
      const x1 = to.left + Math.min(40, to.width / 2), y1 = to.top + to.height / 2;
      f.style.left = x0 + 'px'; f.style.top = y0 + 'px'; document.body.appendChild(f);
      const lift = Math.min(y0, y1) - 80;
      f.animate([
        { transform: 'translate(-50%,-50%) scale(1)' },
        { transform: `translate(calc(-50% + ${(x1 - x0) * .5}px), calc(-50% + ${lift - y0}px)) scale(.9)`, offset: .45 },
        { transform: `translate(calc(-50% + ${x1 - x0}px), calc(-50% + ${y1 - y0}px)) scale(.62)` },
      ], { duration: 620, easing: 'cubic-bezier(.4,0,.6,1)' }).finished.then(() => { f.remove(); show(); });
    };
    narrow.matches ? setTimeout(go, 320) : go();
  }
  function tally(){
    const n = learned.length, w = T.letters(n);
    $('tally').innerHTML = n ? T.tally(w) : '';
    $('docktext').innerHTML = T.dock(w);
  }
  function firefly(){
    if (still) return;
    const g = document.querySelector('.ground').getBoundingClientRect();
    const e = document.createElement('div'); e.className = 'firefly';
    e.style.left = Math.round((.15 + Math.random() * .7) * innerWidth / 4) * 4 + 'px';
    e.style.top = (g.top + scrollY + 60) + 'px';
    document.body.appendChild(e); setTimeout(() => e.remove(), 2700);
  }

  // ── 鍵盤：1~4 作答；提示開著時任何鍵繼續；Esc 關詳解 ──
  document.addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if ($('coach').classList.contains('show')) { if (e.key !== 'Tab') { e.preventDefault(); nextCoach(); } return; }
    if ($('detail').classList.contains('show')) { if (e.key === 'Escape') closeDetail(); return; }
    const i = '1234'.indexOf(e.key);
    if (i >= 0 && opts.children[i] && !busy && !over) opts.children[i].click();
  });

  document.fonts && document.fonts.load('16px Silkscreen', '-1');
  startFight();
  // 提示要等手機大半進到畫面裡才出現（手機版一開頁時手機在折線下，提示框會在畫面外）；
  // 字型到位後才量框的位置。訪客若在提示出現前就先作答，提示就不再出現。
  const coachWhenVisible = () => {
    if (!('IntersectionObserver' in window)) return setTimeout(showCoach, 250);
    const io = new IntersectionObserver(es => {
      if (!es.some(e => e.intersectionRatio >= .6)) return;
      io.disconnect();
      if (answeredEarly) return;
      // 整支手機捲到畫面中間（被圈住的字卡在手機上半部，只露出一部分時會看不到）
      // 放得下＝置中；放不下（小手機）＝手機底對齊畫面底，字卡在上方 17% 處仍看得到，提示框也在畫面內
      const r = document.querySelector('.phone').getBoundingClientRect();
      const dy = r.height <= innerHeight ? (r.top + r.bottom - innerHeight) / 2 : r.bottom - (innerHeight - 8);
      const move = Math.abs(dy) > 4 && (r.top < 0 || r.bottom > innerHeight);
      if (move) scrollBy({ top: dy, behavior: still ? 'auto' : 'smooth' });
      setTimeout(showCoach, move ? 600 : 250);
    }, { threshold: [.6] });
    io.observe(document.querySelector('.phone'));
  };
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(coachWhenVisible);
  addEventListener('resize', () => { if ($('coach').classList.contains('show')) showCoach(); });
})();
