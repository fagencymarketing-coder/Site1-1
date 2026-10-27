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

DARK, OLIVE, OLIVEBG, ROSE, GREY, LINE = '1B1B1B','8E9142','EEF0DD','C32F55','6C6D60','DCDCD2'
thin = Side(style='thin', color=LINE); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
ROWPX = 20  # высота строки по умолчанию

def place(ws, path, cell_row, col, w):
    im = PILImage.open(path); x = XLImage(path)
    x.width, x.height = w, int(im.height * w / im.width)
    ws.add_image(x, f'{col}{cell_row}')
    return cell_row + x.height // ROWPX + 2   # следующая свободная строка

wb = Workbook()

# ═══════════ ЛИСТ 1 — в урезанном виде, как оставила Ольга ═══════════
ws = wb.active; ws.title = 'Куда встаёт блок'
ws.sheet_view.showGridLines = False
ws.column_dimensions['A'].width = 3
ws.column_dimensions['B'].width = 120

def put(row, text, size=11, bold=False, color=DARK, h=None):
    c = ws.cell(row=row, column=2, value=text)
    c.font = Font(size=size, bold=bold, color=color)
    c.alignment = Alignment(wrap_text=True, vertical='top')
    if h: ws.row_dimensions[row].height = h

put(2, 'Блок «Другие услуги» на страницах услуг', 20, True, DARK, 30)
put(4, 'КУДА ИМЕННО ВСТАЁТ', 11, True, OLIVE, 20)
put(5, 'Блок ставится непосредственно перед секцией manager-callback — это форма обратного звонка и подвал. '
       'Правило одно для всех 29 страниц, исключений нет.', 11, True, DARK, 36)
put(6, 'Почему здесь: человек дочитал страницу, предложение он уже видел. Дальше у него два сценария — оставить заявку '
       'или посмотреть соседнюю услугу. Блок не перехватывает внимание до оффера и не отодвигает форму так далеко, '
       'чтобы её перестали замечать.', 11, False, DARK, 50)

r = place(ws, 'shots/scheme.png',  8, 'B', 560)
r = place(ws, 'shots/context.png', r, 'B', 940)
put(r, 'Мобильная версия (390px)', 11, True, DARK, 20)
r = place(ws, 'shots/mobile.png', r + 2, 'B', 300)
print('лист 1 готов, последняя строка:', r)

# ═══════════ ЛИСТ 2 ═══════════
t = wb.create_sheet('Перелинковка')
t.sheet_view.showGridLines = False
HEAD = ['№','Раздел','Страница','URL страницы','№','Анкор ссылки','URL ссылки','В другой раздел','Статус','Комментарий']
for i, w in enumerate([4.5, 22, 32, 52, 4.5, 32, 56, 15, 14, 48], 1):
    t.column_dimensions[get_column_letter(i)].width = w

def cap(row, text, size=11, bold=False, color=DARK, h=16):
    c = t.cell(row=row, column=1, value=text)
    c.font = Font(size=size, bold=bold, color=color); c.alignment = Alignment(vertical='top')
    t.row_dimensions[row].height = h

cap(1, 'Карта внутренней перелинковки «Другие услуги»', 16, True, DARK, 24)
cap(2, 'Блок ставится непосредственно перед секцией manager-callback. Правило одно для всех страниц. '
       'Схема и скриншоты — на листе «Куда встаёт блок».', 10, False, GREY)
cap(3, '29 страниц × 4 ссылки = 116 ссылок. Розовым выделены ссылки в другой раздел сайта — таких 48.', 10, False, GREY)
cap(4, 'Финансовый консалтинг выведен из бухгалтерских услуг: ни одна страница раздела «Бухгалтерские услуги» '
       'на него не ссылается. Обратные ссылки (с финконсалтинга на бухгалтерию) оставлены.', 10, False, ROSE)

HR = 6
for i, h in enumerate(HEAD, 1):
    c = t.cell(row=HR, column=i, value=h)
    c.font = Font(size=10, bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor=DARK)
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True); c.border = BOX
t.row_dimensions[HR].height = 30

row, pg = HR + 1, 0
for gname, codes in GROUPS:
    for code in codes:
        pg += 1
        pu, pn = A[code]; shade = pg % 2 == 0
        for j, tgt in enumerate(M[code], 1):
            tu, tn = A[tgt]; cross = sec(tgt) != sec(code)
            for i, v in enumerate([pg, gname, pn, pu, j, tn, tu, 'да' if cross else '', '', ''], 1):
                c = t.cell(row=row, column=i, value=v)
                c.border = BOX; c.font = Font(size=10)
                c.alignment = Alignment(vertical='center', wrap_text=(i in (3, 6, 10)))
                if shade: c.fill = PatternFill('solid', fgColor='F7F7F2')
                if i in (1, 5, 8): c.alignment = Alignment(horizontal='center', vertical='center')
                if i in (4, 7): c.font = Font(size=9, color='7A7A70'); c.hyperlink = SITE + v
                if i in (6, 8) and cross: c.font = Font(size=10, bold=True, color=ROSE)
                if i == 3 and j == 1: c.font = Font(size=10, bold=True)
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
c = s.cell(row=1, column=1, value='Сколько ссылок приходит на каждую страницу'); c.font = Font(size=14, bold=True)
s.row_dimensions[1].height = 22
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
    s.cell(row=r2, column=3).fill = PatternFill('solid', fgColor=OLIVEBG if inb[code] >= 4 else 'FFFFFF')
    r2 += 1

out = '/home/user/Site1-1/specs/perelinkovka-drugie-uslugi.xlsx'
wb.save(out)
print('сохранено:', out, os.path.getsize(out) // 1024, 'KB')
