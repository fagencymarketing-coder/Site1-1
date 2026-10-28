# -*- coding: utf-8 -*-
import importlib.util, sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from PIL import Image as PILImage

sp=importlib.util.spec_from_file_location('m','map_v2.py'); mm=importlib.util.module_from_spec(sp)
_o=sys.stdout; sys.stdout=open(os.devnull,'w'); sp.loader.exec_module(mm); sys.stdout=_o
A, M = mm.A, mm.M

SITE='https://1-plus-1.ru'
ORDER=['abon','vosst','decl','cons','malyy','sred','krup','glavbuh',
       'upruchet','audit','optnalog','sudexp',
       'yurobsl','dolgi','pravaudit','egrul','reg','dogovory','ved','trud','sudy','intell','otnalog','yurcons',
       'onlayn','ofis','ndfl3','tz','voin']
DARK,LINE,GREY='1B1B1B','DCDCD2','6C6D60'
thin=Side(style='thin',color=LINE); BOX=Border(left=thin,right=thin,top=thin,bottom=thin)

wb=Workbook()

# ── Лист 1: куда встаёт блок ──
ws=wb.active; ws.title='Куда встаёт блок'; ws.sheet_view.showGridLines=False
ws.column_dimensions['A'].width=3; ws.column_dimensions['B'].width=110
c=ws.cell(row=2,column=2,value='Блок «Другие услуги» на страницах услуг')
c.font=Font(size=18,bold=True); ws.row_dimensions[2].height=28
c=ws.cell(row=4,column=2,value='Блок ставится непосредственно перед секцией manager-callback — это форма обратного звонка и подвал. '
                               'Правило одно для всех 29 страниц, исключений нет.')
c.font=Font(size=11,bold=True); c.alignment=Alignment(wrap_text=True,vertical='top'); ws.row_dimensions[4].height=36
im=PILImage.open('shots/context.png'); x=XLImage('shots/context.png'); x.width=940; x.height=int(im.height*940/im.width)
ws.add_image(x,'B6')

# ── Лист 2: перелинковка ──
t=wb.create_sheet('Перелинковка'); t.sheet_view.showGridLines=False
HEAD=['Услуга','Ссылка на страницу','Услуга к допродаже','Ссылка на её страницу','Комментарий']
for i,w in enumerate([34,58,34,58,40],1): t.column_dimensions[get_column_letter(i)].width=w
for i,h in enumerate(HEAD,1):
    c=t.cell(row=1,column=i,value=h)
    c.font=Font(size=10,bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor=DARK)
    c.alignment=Alignment(horizontal='left',vertical='center'); c.border=BOX
t.row_dimensions[1].height=26

row=2
for k,code in enumerate(ORDER):
    pu,pn=A[code]; shade = k%2==1
    for tgt in M[code]:
        tu,tn=A[tgt]
        for j,v in enumerate([pn, SITE+pu, tn, SITE+tu, ''],1):
            c=t.cell(row=row,column=j,value=v); c.border=BOX
            c.alignment=Alignment(vertical='center',wrap_text=(j in (1,3,5)))
            if j in (2,4):
                c.font=Font(size=9,color='7A7A70'); c.hyperlink=v
            else:
                c.font=Font(size=10)
            if shade: c.fill=PatternFill('solid',fgColor='F7F7F2')
        t.row_dimensions[row].height=24
        row+=1
t.freeze_panes='A2'
t.auto_filter.ref=f'A1:E{row-1}'

out='/home/user/Site1-1/specs/perelinkovka-drugie-uslugi.xlsx'
wb.save(out)
print('сохранено:', out, os.path.getsize(out)//1024, 'KB')
print('листы: Куда встаёт блок, Перелинковка |', row-2, 'строк данных')
