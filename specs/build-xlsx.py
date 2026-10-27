# -*- coding: utf-8 -*-
import importlib.util, sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.drawing.image import Image as XLImage
from PIL import Image as PILImage

spec = importlib.util.spec_from_file_location('m', 'map.py'); m = importlib.util.module_from_spec(spec)
_o = sys.stdout; sys.stdout = open(os.devnull, 'w'); spec.loader.exec_module(m); sys.stdout = _o
A, M = m.A, m.M

SITE = 'https://1-plus-1.ru'
GROUPS = [('Бухгалтерские услуги', ['abon','vosst','decl','cons','malyy','sred','krup','glavbuh']),
          ('Финансовый консалтинг', ['upruchet','audit','optnalog','sudexp']),
          ('Юридические услуги', ['yurobsl','dolgi','pravaudit','egrul','reg','dogovory','ved','trud','sudy','intell','otnalog','yurcons']),
          ('Декларации 3-НДФЛ', ['onlayn','ofis','ndfl3']),
          ('Отдельные услуги', ['tz','voin'])]
sec = lambda c: A[c][0].split('/')[1]

DARK, OLIVE, OLIVEBG, ROSE, ROSEBG, GREY, LINE = '1B1B1B','8E9142','EEF0DD','C32F55','FBE8EC','6C6D60','DCDCD2'
thin = Side(style='thin', color=LINE)
BOX  = Border(left=thin, right=thin, top=thin, bottom=thin)

def fit(path, w):
    im = PILImage.open(path); x = XLImage(path)
    x.width, x.height = w, int(im.height * w / im.width)
    return x, x.height

wb = Workbook()

# ═══════════ ЛИСТ 1 ═══════════
ws = wb.active; ws.title = 'Куда встаёт блок'
ws.sheet_view.showGridLines = False
ws.column_dimensions['A'].width = 3
ws.column_dimensions['B'].width = 120

def put(row, text, size=11, bold=False, color=DARK, h=None, wrap=True):
    c = ws.cell(row=row, column=2, value=text)
    c.font = Font(name='Calibri', size=size, bold=bold, color=color)
    c.alignment = Alignment(wrap_text=wrap, vertical='top')
    if h: ws.row_dimensions[row].height = h
    return c

put(2,  'Блок «Другие услуги» на страницах услуг', 20, True, DARK, 30)
put(3,  'Техническое задание · 1-plus-1.ru · 1С-Битрикс, шаблон /local/templates/main2025/ · версия 1 от 27.10.2026', 10, False, GREY, 18)

put(5,  'ЧТО ДЕЛАЕМ', 11, True, OLIVE, 20)
put(6,  'Добавляем на каждую страницу услуги секцию из четырёх карточек-ссылок на другие услуги. Заголовок секции — «Другие услуги». '
        'Карточка состоит из названия услуги и стрелки, кликабельна целиком. Всего 29 страниц и 116 новых ссылок.', 11, False, DARK, 34)
put(7,  'Верстать с нуля не нужно: на главной уже есть готовый блок с нужным видом — «Ещё услуги», класс .more-services. '
        'Берём его вёрстку и стили как есть, меняем заголовок и источник данных.', 11, False, DARK, 34)

put(9,  'КУДА ИМЕННО ВСТАЁТ', 11, True, OLIVE, 20)
put(10, 'Блок ставится непосредственно перед секцией manager-callback — это форма обратного звонка и подвал. '
        'Правило одно для всех 29 страниц, исключений нет.', 11, True, DARK, 34)
put(11, 'Важно: в шаблоне есть секция service-choose-callback («Не знаете какую услугу выбрать?»), но она закомментирована в HTML — '
        'в браузере её нет ни на одной странице услуги. Ориентироваться нужно на manager-callback. '
        'Если секцию service-choose-callback когда-нибудь раскомментируют, блок «Другие услуги» должен остаться выше неё.', 10, False, ROSE, 46)
put(12, 'Почему здесь: человек дочитал страницу, предложение он уже видел. Дальше у него два сценария — оставить заявку '
        'или посмотреть соседнюю услугу. Блок не перехватывает внимание до оффера и не отодвигает форму так далеко, чтобы её перестали замечать.', 11, False, DARK, 34)

r = 14
put(r, 'Порядок секций на странице услуги (пример: Бухгалтерское сопровождение)', 11, True, DARK, 20)
img, hpx = fit('shots/scheme.png', 560)
ws.add_image(img, f'B{r+1}')
r = r + 2 + hpx // 20

put(r, 'Как это выглядит на реальной странице (десктоп, 1440px)', 11, True, DARK, 20)
put(r+1, 'Блок встроен в живую страницу /bukhgalterskie-uslugi/abonentskoe-obsluzhivanie/ и снят скриншотом.', 10, False, GREY, 16)
img2, hpx2 = fit('shots/context.png', 940)
ws.add_image(img2, f'B{r+3}')
r = r + 4 + hpx2 // 20

put(r, 'Мобильная версия (390px)', 11, True, DARK, 20)
put(r+1, 'На ширине до 767px карточки встают в одну колонку, высота по содержимому — существующее поведение .more-service-card, менять не надо.', 10, False, GREY, 30)
img3, hpx3 = fit('shots/mobile.png', 300)
ws.add_image(img3, f'B{r+3}')
r = r + 4 + hpx3 // 20

put(r, 'ПАРАМЕТРЫ ОФОРМЛЕНИЯ', 11, True, OLIVE, 20); r += 1
ws.column_dimensions['C'].width = 46
specs = [('Карточек в блоке', '4'), ('Сетка', 'repeat(auto-fill, minmax(min(290px,100%), 1fr))'),
         ('Отступ между карточками', '20px'), ('Скругление', '20px'), ('Внутренний отступ', '30px'),
         ('Высота карточки', 'min-height 300px; на ≤767px — unset, отступы 30px 20px'),
         ('Заголовок услуги', '20px / 500 / 130%'), ('Стрелка', '24×24, справа сверху'),
         ('Фон 1-й и 3-й карточки', '#ffffff'), ('Фон 2-й и 4-й карточки', '#e6e7cf — правило nth-child(2n), уже есть'),
         ('Цвет текста', '#1b1b1b'), ('Ховер', '#d73a61, переход .3s'),
         ('Заголовок блока', '<h2>Другие услуги</h2> — тег h2, не div'),
         ('Кликабельная зона', 'вся карточка: .more-service-card__title:after { inset: 0 }'),
         ('Фокус с клавиатуры', 'видимая обводка — НАДО ДОБАВИТЬ, сейчас её нет')]
for k, v in specs:
    a = ws.cell(row=r, column=2, value=k); a.font = Font(size=10, bold=True); a.border = BOX
    a.alignment = Alignment(vertical='center')
    b = ws.cell(row=r, column=3, value=v); b.font = Font(size=10); b.border = BOX
    b.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[r].height = 17
    r += 1
print('лист 1 — строк:', r)

# ═══════════ ЛИСТ 2 ═══════════
t = wb.create_sheet('Перелинковка')
t.sheet_view.showGridLines = False
HEAD = ['№','Раздел','Страница','URL страницы','№','Анкор ссылки','URL ссылки','В другой раздел','Статус','Комментарий']
W    = [4.5, 22, 32, 52, 4.5, 32, 56, 15, 14, 48]
for i, w in enumerate(W, 1): t.column_dimensions[get_column_letter(i)].width = w

def cap(row, text, size=11, bold=False, color=DARK, h=16):
    c = t.cell(row=row, column=1, value=text)
    c.font = Font(size=size, bold=bold, color=color)
    c.alignment = Alignment(vertical='top')
    t.row_dimensions[row].height = h

cap(1, 'Карта внутренней перелинковки «Другие услуги»', 16, True, DARK, 24)
cap(2, 'Блок ставится непосредственно перед секцией manager-callback. Правило одно для всех страниц. '
       'Схема и скриншоты — на листе «Куда встаёт блок».', 10, False, GREY, 16)
cap(3, '29 страниц × 4 ссылки = 116 ссылок. Розовым выделены ссылки в другой раздел сайта — таких 52.', 10, False, GREY, 16)
cap(4, 'Подбор ручной: три ссылки на смежные по смыслу услуги плюс минимум одна в другой раздел. '
       'Автоподбор «случайные услуги из того же раздела» не подходит — он выдаёт родительские категории вместо соседних услуг.', 10, False, GREY, 16)

HR = 6
for i, h in enumerate(HEAD, 1):
    c = t.cell(row=HR, column=i, value=h)
    c.font = Font(size=10, bold=True, color='FFFFFF')
    c.fill = PatternFill('solid', fgColor=DARK)
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    c.border = BOX
t.row_dimensions[HR].height = 30

row = HR + 1
pg = 0
for gname, codes in GROUPS:
    for code in codes:
        pg += 1
        pu, pn = A[code]
        shade = (pg % 2 == 0)
        for j, tgt in enumerate(M[code], 1):
            tu, tn = A[tgt]
            cross = sec(tgt) != sec(code)
            vals = [pg, gname, pn, pu, j, tn, tu, 'да' if cross else '', '', '']
            for i, v in enumerate(vals, 1):
                c = t.cell(row=row, column=i, value=v)
                c.border = BOX
                c.font = Font(size=10)
                c.alignment = Alignment(vertical='center', wrap_text=(i in (3, 6, 10)))
                if shade: c.fill = PatternFill('solid', fgColor='F7F7F2')
                if i in (1, 5, 8): c.alignment = Alignment(horizontal='center', vertical='center')
                if i in (4, 7):
                    c.font = Font(size=9, color='7A7A70')
                    c.hyperlink = SITE + v
                if i == 6 and cross:
                    c.font = Font(size=10, bold=True, color=ROSE)
                if i == 8 and cross:
                    c.font = Font(size=10, bold=True, color=ROSE)
                if i == 3 and j == 1:
                    c.font = Font(size=10, bold=True)
            t.row_dimensions[row].height = 28
            row += 1

LAST = row - 1
t.freeze_panes = f'A{HR+1}'
t.auto_filter.ref = f'A{HR}:J{LAST}'
dv = DataValidation(type='list', formula1='"не начато,в работе,готово,вопрос"', allow_blank=True)
t.add_data_validation(dv); dv.add(f'I{HR+1}:I{LAST}')
print('лист 2 — строк данных:', LAST - HR)

# ═══════════ ЛИСТ 3 ═══════════
s = wb.create_sheet('Сводка')
s.sheet_view.showGridLines = False
for col, w in zip('ABCD', (40, 56, 16, 16)): s.column_dimensions[col].width = w
c = s.cell(row=1, column=1, value='Сколько ссылок приходит на каждую страницу')
c.font = Font(size=14, bold=True); s.row_dimensions[1].height = 22
c = s.cell(row=2, column=1, value='Проверка карты: страниц без входящих ссылок нет, страниц без кросс-раздельной ссылки нет.')
c.font = Font(size=10, color=GREY)
for i, h in enumerate(['Страница', 'URL', 'Входящих ссылок', 'Исходящих'], 1):
    c = s.cell(row=4, column=i, value=h)
    c.font = Font(size=10, bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor=DARK)
    c.alignment = Alignment(horizontal='center'); c.border = BOX
from collections import Counter
inb = Counter(x for v in M.values() for x in v)
r2 = 5
for code, _ in sorted(A.items(), key=lambda x: -inb[x[0]]):
    u, n = A[code]
    for i, v in enumerate([n, u, inb[code], len(M.get(code, []))], 1):
        c = s.cell(row=r2, column=i, value=v); c.border = BOX; c.font = Font(size=10)
        if i == 2: c.font = Font(size=9, color='7A7A70'); c.hyperlink = SITE + v
        if i in (3, 4): c.alignment = Alignment(horizontal='center')
    bar = s.cell(row=r2, column=3)
    bar.fill = PatternFill('solid', fgColor=OLIVEBG if inb[code] >= 4 else 'FFFFFF')
    r2 += 1

out = '/home/user/Site1-1/specs/perelinkovka-drugie-uslugi.xlsx'
wb.save(out)
print('сохранено:', out, os.path.getsize(out) // 1024, 'KB')
