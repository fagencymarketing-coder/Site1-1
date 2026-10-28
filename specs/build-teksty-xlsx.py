# -*- coding: utf-8 -*-
import importlib.util, sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def load(p):
    sp=importlib.util.spec_from_file_location('x',p); m=importlib.util.module_from_spec(sp)
    o=sys.stdout; sys.stdout=open(os.devnull,'w'); sp.loader.exec_module(m); sys.stdout=o
    return m
A = load('map_v2.py').A
V = load('variants.py').V
SITE='https://1-plus-1.ru'

# второй вариант подобран так, чтобы отличался углом от первого
SECOND = {
 'abon':'Если бухгалтерия отнимает время',      'vosst':'Если в учёте накопился беспорядок',
 'decl':'Заполним декларации без ошибок',        'cons':'Если есть конкретный вопрос',
 'malyy':'Если штатный бухгалтер пока не нужен', 'sred':'Когда оборот вырос, а учёт нет',
 'krup':'Когда нужна команда, а не бухгалтер',   'glavbuh':'Если ищете главбуха в штат',
 'upruchet':'Если непонятно, где прибыль',       'audit':'Если не уверены в своём бухгалтере',
 'optnalog':'Законные способы платить меньше',   'sudexp':'Дадим заключение для суда',
 'yurobsl':'Договоры, споры и риски — на нас',   'dolgi':'От претензии до исполнительного листа',
 'pravaudit':'Если давно не проверяли документы','egrul':'Если меняется директор или адрес',
 'reg':'Регистрация ООО и ИП под ключ',          'dogovory':'Если шаблон из интернета не подходит',
 'ved':'Валютный контроль и НДС 0%',             'trud':'Если работник пошёл в суд или ГИТ',
 'sudy':'Если дело дошло до суда',               'intell':'Если ваш знак или контент копируют',
 'otnalog':'Если пришло требование или проверка','yurcons':'Если нужен совет до решения',
 'onlayn':'Если некогда ехать в офис',           'ofis':'Если хотите разобраться лично',
 'ndfl3':'3-НДФЛ без ошибок и штрафов',          'tz':'Если боитесь, что название займут',
 'voin':'Если нет кадровика для этой задачи',
}
ORDER=['abon','vosst','decl','cons','malyy','sred','krup','glavbuh',
       'upruchet','audit','optnalog','sudexp',
       'yurobsl','dolgi','pravaudit','egrul','reg','dogovory','ved','trud','sudy','intell','otnalog','yurcons',
       'onlayn','ofis','ndfl3','tz','voin']
for c in ORDER:
    assert SECOND[c] in [t for t,_ in V[c]], c
    assert SECOND[c] != V[c][0][0], c

DARK,LINE='1B1B1B','DCDCD2'
thin=Side(style='thin',color=LINE); BOX=Border(left=thin,right=thin,top=thin,bottom=thin)

wb=Workbook(); ws=wb.active; ws.title='Тексты карточек'
ws.sheet_view.showGridLines=False
HEAD=['Услуга','Страница услуги','Вариант 1','Вариант 2']
for i,w in enumerate([34,56,42,42],1): ws.column_dimensions[get_column_letter(i)].width=w
for i,h in enumerate(HEAD,1):
    c=ws.cell(row=1,column=i,value=h)
    c.font=Font(size=10,bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor=DARK)
    c.alignment=Alignment(horizontal='left',vertical='center'); c.border=BOX
ws.row_dimensions[1].height=26

r=2
for k,code in enumerate(ORDER):
    u,n = A[code]
    for j,v in enumerate([n, SITE+u, V[code][0][0], SECOND[code]],1):
        c=ws.cell(row=r,column=j,value=v); c.border=BOX
        c.alignment=Alignment(vertical='center',wrap_text=(j in (1,3,4)))
        if j==2:
            c.font=Font(size=9,color='7A7A70'); c.hyperlink=v
        else:
            c.font=Font(size=10)
        if k%2==1: c.fill=PatternFill('solid',fgColor='F7F7F2')
    ws.row_dimensions[r].height=24; r+=1
ws.freeze_panes='A2'
ws.auto_filter.ref=f'A1:D{r-1}'

out='/home/user/Site1-1/specs/teksty-kartochek.xlsx'
wb.save(out); print('сохранено:', out, os.path.getsize(out)//1024,'KB |', r-2,'строк')
