const { chromium } = require('playwright');

const AR = `<svg width="22" height="22" viewBox="0 0 25 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5.62614 17.2929C5.23562 17.6834 5.23562 18.3166 5.62614 18.7071C6.01667 19.0976 6.64983 19.0976 7.04036 18.7071L5.62614 17.2929ZM18.3333 6H19.3333C19.3333 5.44772 18.8856 5 18.3333 5V6ZM9.33325 5C8.78097 5 8.33325 5.44772 8.33325 6C8.33325 6.55228 8.78097 7 9.33325 7V5ZM17.3333 15C17.3333 15.5523 17.781 16 18.3333 16C18.8856 16 19.3333 15.5523 19.3333 15H17.3333ZM18.3333 5H9.33325V7H18.3333V5ZM17.3333 6V15H19.3333V6H17.3333ZM12.5404 13.2071L19.0404 6.70711L17.6262 5.29289L11.1262 11.7929L12.5404 13.2071ZM7.04036 18.7071L12.5404 13.2071L11.1262 11.7929L5.62614 17.2929L7.04036 18.7071Z" fill="currentColor"/></svg>`;

const CARDS = [
  ['Бухгалтерское сопровождение','Чтобы учёт больше не разваливался','/bukhgalterskie-uslugi/abonentskoe-obsluzhivanie/'],
  ['Инициативный аудит бухгалтерии','Проверим, всё ли теперь в порядке','/finansoviy-konsalting/initsiativnyy-audit-bukhgalterii/'],
  ['Оптимизация налогообложения','Законно снизим налоговую нагрузку','/finansoviy-konsalting/optimizatsiya-nalogooblozheniya/'],
  ['Защита от налоговой','Если проверка уже на пороге','/yuristy-dlya-biznesa/zashchita-ot-nalogovoy/'],
];

const CSS = `
.ms2{background:#f2f3ed;padding:72px 0;margin:0}
.ms2 .ms2__in{width:min(1360px,100% - 40px);margin-inline:auto}
.ms2__t{font-family:Inter,sans-serif;font-size:40px;font-weight:600;line-height:1.1;letter-spacing:-.015em;
  color:#1b1b1b;margin:0 0 40px}
.ms2__list{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;list-style:none;margin:0;padding:0}
@media (max-width:1199px){.ms2__list{grid-template-columns:repeat(2,1fr)}}
.ms2__list>li{display:flex;min-width:0}
.ms2__card{background:#fff;border-radius:20px;padding:28px 26px;display:flex;flex-direction:column;
  color:#1b1b1b;text-decoration:none;position:relative;min-width:0;width:100%;height:100%;
  transition:transform .25s,box-shadow .25s}
.ms2__card:hover{transform:translateY(-4px);box-shadow:0 10px 28px rgba(27,27,27,.09)}
.ms2__ar{margin-left:auto;margin-bottom:38px;color:inherit;flex:none;line-height:0}
.ms2__nm{font-family:Inter,sans-serif;font-size:20px;font-weight:600;line-height:1.28;margin:auto 0 0}
.ms2__rs{font-family:Inter,sans-serif;font-size:15px;font-weight:400;line-height:1.4;color:#6b6a5f;margin:9px 0 0}
/* ВАРИАНТ А: все белые, одна акцентная */
.ms2--a .ms2__card--acc{background:#d73a61;color:#fff}
.ms2--a .ms2__card--acc .ms2__rs{color:rgba(255,255,255,.88)}
/* ВАРИАНТ Б: чередование, без акцента */
.ms2--b .ms2__list>li:nth-child(2n) .ms2__card{background:#e6e7cf}
@media (max-width:767px){
  .ms2{padding:44px 0}
  .ms2__t{font-size:26px;margin-bottom:26px}
  .ms2__list{grid-template-columns:1fr;gap:14px}
  .ms2__card{padding:24px 22px}
  .ms2__ar{margin-bottom:24px}
  .ms2__nm{font-size:18px}
}`;

const build = (variant) => `
<section class="ms2 ms2--${variant}" id="__v">
  <div class="ms2__in">
    <h2 class="ms2__t">Другие услуги</h2>
    <ul class="ms2__list">
      ${CARDS.map(([n, r, h], i) => `
      <li><a class="ms2__card${variant === 'a' && i === 0 ? ' ms2__card--acc' : ''}" href="${h}">
        <span class="ms2__ar">${AR}</span>
        <span class="ms2__nm">${n}</span>
        <span class="ms2__rs">${r}</span>
      </a></li>`).join('')}
    </ul>
  </div>
</section>`;

async function shoot(browser, variant, width, dsf, out) {
  const p = await browser.newPage({ viewport: { width, height: 1000 }, deviceScaleFactor: dsf,
                                    isMobile: width < 500, hasTouch: width < 500 });
  await p.goto('https://1-plus-1.ru/bukhgalterskie-uslugi/vosstanovlenie-ucheta/',
               { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(2500);
  await p.evaluate(() => {
    document.querySelectorAll('*').forEach(e => {
      const cs = getComputedStyle(e);
      if ((cs.position === 'fixed' || cs.position === 'sticky') && !['HTML','BODY'].includes(e.tagName)) {
        const c = (e.className || '').toString().toLowerCase();
        if (/cookie|popup|modal|up-button|scroll-top|header/.test(c)) e.style.display = 'none';
      }
    });
  });
  await p.evaluate(({ html, css }) => {
    const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    document.querySelector('.manager-callback').insertAdjacentHTML('beforebegin', html);
  }, { html: build(variant), css: CSS });
  await p.evaluate(async () => { await new Promise(r => { let y = 0;
    const t = setInterval(() => { window.scrollTo(0, y); y += 600;
      if (y > document.body.scrollHeight) { clearInterval(t); window.scrollTo(0,0); r(); } }, 60); }); });
  await p.waitForTimeout(1300);
  const el = await p.$('#__v');
  await el.scrollIntoViewIfNeeded();
  await p.waitForTimeout(500);
  await el.screenshot({ path: out });
  // контекст: секция выше + блок + начало формы
  const g = await p.evaluate(() => {
    const b = document.getElementById('__v'), prev = b.previousElementSibling;
    const abs = e => e.getBoundingClientRect().top + window.scrollY;
    return { top: Math.max(0, abs(prev) + prev.getBoundingClientRect().height - 260),
             h: 260 + b.getBoundingClientRect().height + 300,
             w: document.documentElement.clientWidth };
  });
  await p.screenshot({ path: out.replace('.png','-ctx.png'), fullPage: true, clip: { x:0, y:g.top, width:g.w, height:g.h } });
  const h = await p.evaluate(() => Math.round(document.querySelector('.ms2__card').getBoundingClientRect().height));
  console.log(out, '| высота карточки', h + 'px');
  await p.close();
}

(async () => {
  const b = await chromium.launch();
  await shoot(b, 'a', 1440, 2, 'shots/var-A-desktop.png');
  await shoot(b, 'b', 1440, 2, 'shots/var-B-desktop.png');
  await shoot(b, 'a', 1024, 2, 'shots/var-A-tablet.png');
  await shoot(b, 'a', 390, 2, 'shots/var-A-mobile.png');
  await shoot(b, 'b', 390, 2, 'shots/var-B-mobile.png');
  await b.close();
})();
