# -*- coding: utf-8 -*-
import importlib.util, sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

def load(p):
    sp=importlib.util.spec_from_file_location('x',p); m=importlib.util.module_from_spec(sp)
    o=sys.stdout; sys.stdout=open(os.devnull,'w'); sp.loader.exec_module(m); sys.stdout=o
    return m
mm=load('map_v2.py'); A,M=mm.A,mm.M
V=load('variants.py').V
T=load('texts.py')

ORDER=['abon','vosst','decl','cons','malyy','sred','krup','glavbuh',
       'upruchet','audit','optnalog','sudexp',
       'yurobsl','dolgi','pravaudit','egrul','reg','dogovory','ved','trud','sudy','intell','otnalog','yurcons',
       'onlayn','ofis','ndfl3','tz','voin']
DARK,LINE,OLIVE,OLIVEBG,ROSE,ROSEBG,GREY='1B1B1B','DCDCD2','8E9142','EEF0DD','C32F55','FBE8EC','6C6D60'
thin=Side(style='thin',color=LINE); BOX=Border(left=thin,right=thin,top=thin,bottom=thin)

def head(ws,row,names,widths):
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    for i,h in enumerate(names,1):
        c=ws.cell(row=row,column=i,value=h)
        c.font=Font(size=10,bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor=DARK)
        c.alignment=Alignment(horizontal='left',vertical='center'); c.border=BOX
    ws.row_dimensions[row].height=26

def cap(ws,row,txt,size=10,bold=False,color=GREY,h=16):
    c=ws.cell(row=row,column=1,value=txt); c.font=Font(size=size,bold=bold,color=color)
    c.alignment=Alignment(vertical='top'); ws.row_dimensions[row].height=h

wb=Workbook()

# ── Лист 1: варианты, строка на вариант ──
ws=wb.active; ws.title='Варианты'; ws.sheet_view.showGridLines=False
cap(ws,1,'Мелкий текст под названием услуги — варианты на выбор',16,True,DARK,24)
cap(ws,2,'По четыре варианта на услугу, разные углы: что делаем, от ситуации клиента, польза, коротко.')
cap(ws,3,'Отметьте выбранный в колонке «Выбор» или впишите свой в «Ваша формулировка».')
cap(ws,4,'Зелёным помечен мой вариант — он стоит первым в каждой четвёрке.',10,False,OLIVE)
HR=6
head(ws,HR,['Услуга','№','Вариант','Симв.','Угол','Мой выбор','Выбор','Ваша формулировка'],
     [34,4,44,7,15,11,9,40])
dv=DataValidation(type='list',formula1='"✓"',allow_blank=True); ws.add_data_validation(dv)
r=HR+1
for k,code in enumerate(ORDER):
    shade = k%2==1
    for i,(txt,angle) in enumerate(V[code],1):
        mine = 'мой' if i==1 else ''
        vals=[A[code][1] if i==1 else '', i, txt, len(txt), angle, mine, '', '']
        for j,v in enumerate(vals,1):
            c=ws.cell(row=r,column=j,value=v); c.border=BOX; c.font=Font(size=10)
            c.alignment=Alignment(vertical='center',wrap_text=(j in (1,3,8)))
            if shade: c.fill=PatternFill('solid',fgColor='F7F7F2')
            if j in (2,4,6,7): c.alignment=Alignment(horizontal='center',vertical='center')
            if j==1 and i==1: c.font=Font(size=10,bold=True)
            if j==4: c.font=Font(size=9,color='9A9B8E')
            if j==5: c.font=Font(size=9,color='9A9B8E')
            if j==6 and mine:
                c.font=Font(size=9,bold=True,color=OLIVE); c.fill=PatternFill('solid',fgColor=OLIVEBG)
        dv.add(ws.cell(row=r,column=7))
        ws.row_dimensions[r].height=22
        r+=1
ws.freeze_panes=f'A{HR+1}'
ws.auto_filter.ref=f'A{HR}:H{r-1}'

# ── Лист 2: где текст свой ──
e=wb.create_sheet('Где текст свой'); e.sheet_view.showGridLines=False
cap(e,1,'Страницы, где текст карточки отличается от базового',16,True,DARK,24)
cap(e,2,'Здесь ситуация клиента меняет смысл. Пример: на «Восстановлении учёта» карточка бухгалтерского')
cap(e,3,'сопровождения говорит не «возьмём учёт на себя», а «чтобы учёт больше не разваливался».')
cap(e,4,'Варианты сюда напишу после того, как выберете тон на первом листе.',10,False,ROSE)
head(e,6,['Страница, где стоит блок','Карточка','Текст на этой странице','Симв.','Ваша формулировка'],
     [32,30,44,7,40])
r=7
for src in ORDER:
    for tgt in M[src]:
        if (src,tgt) not in T.OVER: continue
        t=T.OVER[(src,tgt)]
        for j,v in enumerate([A[src][1], A[tgt][1], t, len(t), ''],1):
            c=e.cell(row=r,column=j,value=v); c.border=BOX; c.font=Font(size=10)
            c.alignment=Alignment(vertical='center',wrap_text=(j in (1,2,3,5)))
            if j==4: c.alignment=Alignment(horizontal='center',vertical='center'); c.font=Font(size=9,color='9A9B8E')
            if j==3: c.font=Font(size=10,color=ROSE); c.fill=PatternFill('solid',fgColor=ROSEBG)
        e.row_dimensions[r].height=28; r+=1
e.freeze_panes='A7'

out='/home/user/Site1-1/specs/teksty-kartochek.xlsx'
wb.save(out); print('сохранено:', out, os.path.getsize(out)//1024,'KB')
print('лист «Варианты»:', 29*4, 'строк | лист «Где текст свой»:', len(T.OVER), 'строк')
