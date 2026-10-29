const { chromium } = require('playwright');
const fs = require('fs');

const data = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));  // [{code, title, cards:[{name,text,accent}]}]
const outDir = process.argv[3] || 'blocks';
fs.mkdirSync(outDir, { recursive: true });

const AR = `<svg width="22" height="22" viewBox="0 0 25 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5.62614 17.2929C5.23562 17.6834 5.23562 18.3166 5.62614 18.7071C6.01667 19.0976 6.64983 19.0976 7.04036 18.7071L5.62614 17.2929ZM18.3333 6H19.3333C19.3333 5.44772 18.8856 5 18.3333 5V6ZM9.33325 5C8.78097 5 8.33325 5.44772 8.33325 6C8.33325 6.55228 8.78097 7 9.33325 7V5ZM17.3333 15C17.3333 15.5523 17.781 16 18.3333 16C18.8856 16 19.3333 15.5523 19.3333 15H17.3333ZM18.3333 5H9.33325V7H18.3333V5ZM17.3333 6V15H19.3333V6H17.3333ZM12.5404 13.2071L19.0404 6.70711L17.6262 5.29289L11.1262 11.7929L12.5404 13.2071ZM7.04036 18.7071L12.5404 13.2071L11.1262 11.7929L5.62614 17.2929L7.04036 18.7071Z" fill="currentColor"/></svg>`;

const page = (b) => `<!doctype html><html lang="ru"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">
<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#f2f3ed;font-family:Inter,sans-serif}
.ms2{background:#f2f3ed;padding:56px 0 60px}
.ms2__in{width:1360px;margin-inline:auto}
.ms2__t{font-size:40px;font-weight:600;line-height:1.1;letter-spacing:-.015em;color:#1b1b1b;margin:0 0 40px}
.ms2__list{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;list-style:none;margin:0;padding:0}
.ms2__list>li{display:flex;min-width:0}
.ms2__card{background:#fff;border-radius:20px;padding:28px 26px;display:flex;flex-direction:column;
  color:#1b1b1b;text-decoration:none;position:relative;min-width:0;width:100%;height:100%}
.ms2__ar{margin-left:auto;margin-bottom:38px;color:inherit;flex:none;line-height:0}
.ms2__nm{font-size:20px;font-weight:600;line-height:1.28;margin:auto 0 0}
.ms2__rs{font-size:15px;font-weight:400;line-height:1.4;color:#6b6a5f;margin:9px 0 0}
.ms2__card--acc{background:#d73a61;color:#fff}
.ms2__card--acc .ms2__rs{color:rgba(255,255,255,.88)}
</style></head><body>
<section class="ms2"><div class="ms2__in">
<h2 class="ms2__t">Другие услуги</h2>
<ul class="ms2__list">
${b.cards.map(c => `<li><a class="ms2__card${c.accent ? ' ms2__card--acc' : ''}" href="#">
<span class="ms2__ar">${AR}</span><span class="ms2__nm">${c.name}</span><span class="ms2__rs">${c.text}</span></a></li>`).join('')}
</ul></div></section></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1440, height: 700 }, deviceScaleFactor: 2 });
  for (const b of data) {
    await p.setContent(page(b), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(250);
    const el = await p.$('.ms2');
    await el.screenshot({ path: `${outDir}/${b.code}.png` });
    const hs = await p.evaluate(() => [...document.querySelectorAll('.ms2__card')].map(c => Math.round(c.getBoundingClientRect().height)));
    const ok = new Set(hs).size === 1;
    console.log(`${b.code.padEnd(12)} ${b.title.slice(0,34).padEnd(36)} высоты ${hs.join('/')} ${ok ? '' : '← РАЗНЫЕ'}`);
  }
  await browser.close();
})();
