const { chromium } = require('playwright');
const fs = require('fs');
const blocks = JSON.parse(fs.readFileSync('blocks.json','utf8'));
const only = process.argv[2] ? process.argv[2].split(',') : null;
const FORM = 260;            // сколько пикселей формы показываем
const outDir = 'ctx'; fs.mkdirSync(outDir, { recursive: true });

const AR = `<svg width="22" height="22" viewBox="0 0 25 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5.62614 17.2929C5.23562 17.6834 5.23562 18.3166 5.62614 18.7071C6.01667 19.0976 6.64983 19.0976 7.04036 18.7071L5.62614 17.2929ZM18.3333 6H19.3333C19.3333 5.44772 18.8856 5 18.3333 5V6ZM9.33325 5C8.78097 5 8.33325 5.44772 8.33325 6C8.33325 6.55228 8.78097 7 9.33325 7V5ZM17.3333 15C17.3333 15.5523 17.781 16 18.3333 16C18.8856 16 19.3333 15.5523 19.3333 15H17.3333ZM18.3333 5H9.33325V7H18.3333V5ZM17.3333 6V15H19.3333V6H17.3333ZM12.5404 13.2071L19.0404 6.70711L17.6262 5.29289L11.1262 11.7929L12.5404 13.2071ZM7.04036 18.7071L12.5404 13.2071L11.1262 11.7929L5.62614 17.2929L7.04036 18.7071Z" fill="currentColor"/></svg>`;

const CSS = `
.ms2{background:#f2f3ed;padding:56px 0 60px;margin:0}
.ms2 .ms2__in{width:min(1360px,100% - 40px);margin-inline:auto}
.ms2__t{font-family:Inter,sans-serif;font-size:40px;font-weight:600;line-height:1.1;letter-spacing:-.015em;color:#1b1b1b;margin:0 0 40px}
.ms2__list{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;list-style:none;margin:0;padding:0}
.ms2__list>li{display:flex;min-width:0}
.ms2__card{background:#fff;border-radius:20px;padding:28px 26px;display:flex;flex-direction:column;
  color:#1b1b1b;text-decoration:none;position:relative;min-width:0;width:100%;height:100%}
.ms2__ar{margin-left:auto;margin-bottom:38px;color:inherit;flex:none;line-height:0}
.ms2__nm{font-family:Inter,sans-serif;font-size:20px;font-weight:600;line-height:1.28;margin:auto 0 0}
.ms2__rs{font-family:Inter,sans-serif;font-size:15px;font-weight:400;line-height:1.4;color:#6b6a5f;margin:9px 0 0}
.ms2__card--acc{background:#d73a61;color:#fff}
.ms2__card--acc .ms2__rs{color:rgba(255,255,255,.88)}
#__fade{position:absolute;left:0;width:100%;pointer-events:none;
  background:linear-gradient(to bottom, rgba(249,249,249,0) 0%, rgba(249,249,249,.97) 82%, #f9f9f9 100%)}`;

const html = (b) => `<section class="ms2" id="__v"><div class="ms2__in">
<h2 class="ms2__t">Другие услуги</h2><ul class="ms2__list">
${b.cards.map(c => `<li><a class="ms2__card${c.accent?' ms2__card--acc':''}" href="#">
<span class="ms2__ar">${AR}</span><span class="ms2__nm">${c.name}</span><span class="ms2__rs">${c.text}</span></a></li>`).join('')}
</ul></div></section>`;

(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
  const list = only ? blocks.filter(b => only.includes(b.code)) : blocks;
  for (const b of list) {
    const url = b.url;
    try {
      await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await p.waitForTimeout(2200);
      await p.evaluate(() => {
        document.querySelectorAll('*').forEach(e => {
          const cs = getComputedStyle(e);
          if ((cs.position==='fixed'||cs.position==='sticky') && !['HTML','BODY'].includes(e.tagName)) {
            const c=(e.className||'').toString().toLowerCase();
            if (/cookie|popup|modal|up-button|scroll-top|header/.test(c)) e.style.display='none';
          }
        });
      });
      await p.evaluate(({h, css}) => {
        const s=document.createElement('style'); s.textContent=css; document.head.appendChild(s);
        document.querySelector('.manager-callback').insertAdjacentHTML('beforebegin', h);
      }, { h: html(b), css: CSS });
      await p.evaluate(async () => { await new Promise(r => { let y=0;
        const t=setInterval(()=>{window.scrollTo(0,y); y+=700;
          if(y>document.body.scrollHeight){clearInterval(t); window.scrollTo(0,0); r();}},55); }); });
      await p.waitForTimeout(1100);
      const g = await p.evaluate((FORM) => {
        const v=document.getElementById('__v');
        const abs=e=>e.getBoundingClientRect().top+window.scrollY;
        const top=Math.round(abs(v)), vh=Math.round(v.getBoundingClientRect().height);
        const f=document.createElement('div'); f.id='__fade';
        f.style.top=(top+vh+FORM-110)+'px'; f.style.height='110px';
        document.body.appendChild(f);
        return { top, h: vh + FORM, w: document.documentElement.clientWidth };
      }, FORM);
      await p.waitForTimeout(250);
      await p.screenshot({ path: `${outDir}/${b.code}.png`, fullPage: true,
                           clip: { x:0, y:g.top, width:g.w, height:g.h } });
      console.log(`${b.code.padEnd(11)} ${String(g.w)+'×'+g.h}  ${b.title.slice(0,32)}`);
    } catch (e) {
      console.log(`${b.code.padEnd(11)} ОШИБКА: ${e.message.split('\n')[0]}`);
    }
  }
  await browser.close();
})();
