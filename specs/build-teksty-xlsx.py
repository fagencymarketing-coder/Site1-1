# -*- coding: utf-8 -*-
import importlib.util, sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def load(p):
    sp=importlib.util.spec_from_file_location('x',p); m=importlib.util.module_from_spec(sp)
    o=sys.stdout; sys.stdout=open(os.devnull,'w'); sp.loader.exec_module(m); sys.stdout=o
    return m
mm=load('map_v2.py'); A,M=mm.A,mm.M
T=load('texts.py')

ORDER=['abon','vosst','decl','cons','malyy','sred','krup','glavbuh',
       'upruchet','audit','optnalog','sudexp',
       'yurobsl','dolgi','pravaudit','egrul','reg','dogovory','ved','trud','sudy','intell','otnalog','yurcons',
       'onlayn','ofis','ndfl3','tz','voin']
DARK,LINE,ROSE,ROSEBG='1B1B1B','DCDCD2','C32F55','FBE8EC'
thin=Side(style='thin',color=LINE); BOX=Border(left=thin,right=thin,top=thin,bottom=thin)

def head(ws,row,names,widths):
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    for i,h in enumerate(names,1):
        c=ws.cell(row=row,column=i,value=h)
        c.font=Font(size=10,bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor=DARK)
        c.alignment=Alignment(horizontal='left',vertical='center'); c.border=BOX
    ws.row_dimensions[row].height=26

def cap(ws,row,txt,size=10,bold=False,color='6C6D60',h=16):
    c=ws.cell(row=row,column=1,value=txt); c.font=Font(size=size,bold=bold,color=color)
    c.alignment=Alignment(vertical='top'); ws.row_dimensions[row].height=h

wb=Workbook()

# ── 1. Базовые тексты ──
ws=wb.active; ws.title='Тексты услуг'; ws.sheet_view.showGridLines=False
cap(ws,1,'Мелкий текст под названием услуги в карточке',16,True,DARK,24)
cap(ws,2,'Одна фраза на услугу. Показывается везде, где эта услуга выводится карточкой.')
cap(ws,3,'Правьте в колонке «Ваша формулировка» — если пусто, берём мой вариант.')
head(ws,5,['Услуга','Мой вариант','Симв.','Ваша формулировка'],[36,46,8,46])
r=6
for code in ORDER:
    t=T.BASE[code]
    for j,v in enumerate([A[code][1], t, len(t), ''],1):
        c=ws.cell(row=r,column=j,value=v); c.border=BOX; c.font=Font(size=10)
        c.alignment=Alignment(vertical='center',wrap_text=(j in (1,2,4)))
        if j==3: c.alignment=Alignment(horizontal='center',vertical='center'); c.font=Font(size=9,color='9A9B8E')
        if r%2==1: c.fill=PatternFill('solid',fgColor='F7F7F2')
    ws.row_dimensions[r].height=22; r+=1
ws.freeze_panes='A6'

# ── 2. Исключения ──
e=wb.create_sheet('Где текст свой'); e.sheet_view.showGridLines=False
cap(e,1,'Страницы, где текст карточки отличается от базового',16,True,DARK,24)
cap(e,2,'Здесь ситуация клиента на странице меняет смысл. Пример: на «Восстановлении учёта» карточка')
cap(e,3,'бухгалтерского сопровождения говорит не «возьмём учёт на себя», а «чтобы учёт больше не разваливался».')
head(e,5,['Страница, где стоит блок','Карточка','Базовый текст','Текст на этой странице','Ваша формулировка'],[32,30,40,42,42])
r=6
for src in ORDER:
    for tgt in M[src]:
        if (src,tgt) not in T.OVER: continue
        for j,v in enumerate([A[src][1], A[tgt][1], T.BASE[tgt], T.OVER[(src,tgt)], ''],1):
            c=e.cell(row=r,column=j,value=v); c.border=BOX; c.font=Font(size=10)
            c.alignment=Alignment(vertical='center',wrap_text=True)
            if j==3: c.font=Font(size=9,color='9A9B8E')
            if j==4: c.font=Font(size=10,bold=True,color=ROSE); c.fill=PatternFill('solid',fgColor=ROSEBG)
        e.row_dimensions[r].height=30; r+=1
e.freeze_panes='A6'

# ── 3. Все 116 ──
f=wb.create_sheet('Все 116'); f.sheet_view.showGridLines=False
cap(f,1,'Что будет написано на каждой карточке',16,True,DARK,24)
cap(f,2,'Итоговая сборка для подрядчика. Собрана из двух листов выше.')
head(f,4,['Страница','Карточка','Текст под названием','Свой текст'],[34,34,46,12])
r=5
for k,src in enumerate(ORDER):
    for tgt in M[src]:
        own=(src,tgt) in T.OVER
        for j,v in enumerate([A[src][1], A[tgt][1], T.text(src,tgt), 'да' if own else ''],1):
            c=f.cell(row=r,column=j,value=v); c.border=BOX; c.font=Font(size=10)
            c.alignment=Alignment(vertical='center',wrap_text=(j in (1,2,3)))
            if j==4:
                c.alignment=Alignment(horizontal='center',vertical='center')
                if own: c.font=Font(size=10,bold=True,color=ROSE); c.fill=PatternFill('solid',fgColor=ROSEBG)
            elif k%2==1: c.fill=PatternFill('solid',fgColor='F7F7F2')
        f.row_dimensions[r].height=24; r+=1
f.freeze_panes='A5'; f.auto_filter.ref=f'A4:D{r-1}'

out='/home/user/Site1-1/specs/teksty-kartochek.xlsx'
wb.save(out); print('сохранено:', out, os.path.getsize(out)//1024,'KB')
print('листы: Тексты услуг (29), Где текст свой (%d), Все 116' % len(T.OVER))
