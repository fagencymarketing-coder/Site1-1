# -*- coding: utf-8 -*-
"""Оценка каждой ссылки по двум критериям заказчика."""
import importlib.util, sys, os
def load(p):
    sp=importlib.util.spec_from_file_location('x',p); mod=importlib.util.module_from_spec(sp)
    o=sys.stdout; sys.stdout=open(os.devnull,'w'); sp.loader.exec_module(mod); sys.stdout=o
    return mod.A, mod.M
A, OLD = load('map.py')
_, NEW  = load('map_v2.py')

FINK={'upruchet','audit','optnalog','sudexp'}
def prio(c):
    if c=='abon': return 1
    if c in FINK: return 2
    if c=='yurobsl': return 3
    return 0
PNAME={1:'1 · абонентское бухобслуживание',2:'2 · финансовый и налоговый консалтинг',
       3:'3 · юридическое обслуживание',0:'вне приоритетов'}

# Релевантность: по умолчанию «высокая». Здесь — всё, что ниже, с причиной.
REL = {
 ('malyy','sred'):   ('средняя','ссылка на соседнюю категорию по размеру бизнеса, а не на услугу'),
 ('sred','krup'):    ('средняя','ссылка на соседнюю категорию по размеру бизнеса, а не на услугу'),
 ('glavbuh','sred'): ('средняя','родительская категория, а не соседняя услуга'),
 ('krup','ved'):     ('средняя','ВЭД нужен не каждому крупному клиенту'),
 ('ved','krup'):     ('средняя','ведёт в категорию, а не в услугу'),
 ('reg','malyy'):    ('средняя','ведёт в категорию, а не в услугу'),
 ('egrul','abon'):   ('средняя','смена данных в ЕГРЮЛ слабо связана с бухобслуживанием'),
 ('trud','abon'):    ('средняя','трудовой спор слабо связан с бухобслуживанием'),
 ('tz','abon'):      ('средняя','товарный знак слабо связан с бухобслуживанием'),
 ('onlayn','cons'):  ('средняя','физлицо с вычетом — не клиент бухобслуживания компаний'),
 ('ofis','cons'):    ('средняя','физлицо с вычетом — не клиент бухобслуживания компаний'),
 ('ndfl3','cons'):   ('средняя','физлицо с вычетом — не клиент бухобслуживания компаний'),
 ('onlayn','decl'):  ('средняя','декларации для бизнеса, а страница — для физлиц'),
 ('ofis','decl'):    ('средняя','декларации для бизнеса, а страница — для физлиц'),
 ('ndfl3','decl'):   ('средняя','декларации для бизнеса, а страница — для физлиц'),
 ('decl','ndfl3'):   ('средняя','уводит из B2B в B2C-воронку'),
 ('sudexp','yurobsl'):('средняя','экспертиза разовая, абонентская юрподдержка — не прямое продолжение'),
 ('intell','yurobsl'):('средняя','защита прав разовая, абонентка — не прямое продолжение'),
 ('voin','yurobsl'): ('средняя','воинский учёт ближе к кадрам, чем к юрподдержке'),
}
def rel(s,t): return REL.get((s,t), ('высокая',''))

def rows(M):
    out=[]
    for s,ts in M.items():
        for i,t in enumerate(ts,1):
            r,why = rel(s,t)
            out.append(dict(src=s,tgt=t,pos=i,rel=r,why=why,prio=prio(t)))
    return out

o,n = rows(OLD), rows(NEW)
def stat(rs,label):
    from collections import Counter
    c=Counter(x['prio'] for x in rs); rc=Counter(x['rel'] for x in rs)
    print(f'\n{label}')
    for p in (1,2,3,0): print(f'   {PNAME[p]:<40} {c[p]:>3}')
    print(f'   релевантность: высокая {rc["высокая"]}, средняя {rc["средняя"]}')
stat(o,'=== БЫЛО ==='); stat(n,'=== СТАЛО ===')

oldset={(x['src'],x['tgt']) for x in o}
newset={(x['src'],x['tgt']) for x in n}
print(f'\nУбрано ссылок: {len(oldset-newset)} | добавлено: {len(newset-oldset)} | без изменений: {len(oldset&newset)}')
changed=sorted({s for s,t in (oldset^newset)})
print(f'Затронуто страниц: {len(changed)} из 29')
