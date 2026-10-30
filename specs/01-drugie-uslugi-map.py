# -*- coding: utf-8 -*-
A = {  # короткий код -> (URL, анкор)
 'abon':('/bukhgalterskie-uslugi/abonentskoe-obsluzhivanie/','Бухгалтерское сопровождение'),
 'vosst':('/bukhgalterskie-uslugi/vosstanovlenie-ucheta/','Восстановление учёта'),
 'decl':('/bukhgalterskie-uslugi/zapolnenie-deklaratsiy/','Заполнение деклараций'),
 'cons':('/bukhgalterskie-uslugi/konsultatsii/','Консультация бухгалтера'),
 'malyy':('/bukhgalterskie-uslugi/dlya-malogo-biznesa-/','Бухгалтерия для малого бизнеса'),
 'sred':('/bukhgalterskie-uslugi/dlya-srednego-biznesa-/','Бухгалтерия для среднего бизнеса'),
 'krup':('/bukhgalterskie-uslugi/dlya-krupnogo-biznesa-/','Бухгалтерия для крупного бизнеса'),
 'glavbuh':('/bukhgalterskie-uslugi/dlya-srednego-biznesa-/podbor-glavbukhov/','Подбор главбухов'),
 'upruchet':('/finansoviy-konsalting/upravlencheskiy-finansovyy-uchyet/','Управленческий финансовый учёт'),
 'audit':('/finansoviy-konsalting/initsiativnyy-audit-bukhgalterii/','Инициативный аудит бухгалтерии'),
 'optnalog':('/finansoviy-konsalting/optimizatsiya-nalogooblozheniya/','Оптимизация налогообложения'),
 'sudexp':('/finansoviy-konsalting/sudebnaya-bukhgalterskaya-i-finansovo-ekonomicheskaya-ekspertiza/','Судебная бухгалтерская экспертиза'),
 'yurobsl':('/yuristy-dlya-biznesa/yuridicheskoe-obsluzhivanie/','Юридическое обслуживание'),
 'dolgi':('/yuristy-dlya-biznesa/vzyskanie-dolgov/','Взыскание долгов'),
 'pravaudit':('/yuristy-dlya-biznesa/pravovoy-audit/','Правовой аудит'),
 'egrul':('/yuristy-dlya-biznesa/-vnesenie-izmeneniy-v-dokumenty-egryul-egrip/','Внесение изменений в ЕГРЮЛ и ЕГРИП'),
 'reg':('/yuristy-dlya-biznesa/registratsiya-i-likvidatsiya/','Регистрация и ликвидация бизнеса'),
 'dogovory':('/yuristy-dlya-biznesa/sostavlenie-dogovorov/','Составление договоров'),
 'ved':('/yuristy-dlya-biznesa/soprovozhdenie-vneshneekonomicheskoy-deyatelnosti/','Сопровождение ВЭД'),
 'trud':('/yuristy-dlya-biznesa/spory-v-trudovykh-otnosheniyakh/','Споры в трудовых отношениях'),
 'sudy':('/yuristy-dlya-biznesa/predstavitelstvo-v-sudakh/','Представительство в судах'),
 'intell':('/yuristy-dlya-biznesa/zashchita-intellektualnykh-prav/','Защита интеллектуальных прав'),
 'otnalog':('/yuristy-dlya-biznesa/zashchita-ot-nalogovoy/','Защита от налоговой'),
 'yurcons':('/yuristy-dlya-biznesa/yuridicheskie-uslugi/','Юридическая консультация'),
 'onlayn':('/deklaratsii-3-ndfl/vernut-nalogi-onlayn/','Вернуть налоги онлайн'),
 'ofis':('/deklaratsii-3-ndfl/vernut-nalogi-v-ofise/','Вернуть налоги в офисе'),
 'ndfl3':('/deklaratsii-3-ndfl/deklaratsiya-o-dokhodakh-fizlits-po-forme-3-ndfl/','Декларация 3-НДФЛ'),
 'tz':('/tovarnyye-znaki/','Регистрация товарного знака'),
 'voin':('/voinskiy-uchet/','Воинский учёт'),
}
# откуда -> 4 ссылки (последние помечены как кросс-раздельные жирным в ТЗ)
M = {
 'abon':['upruchet', 'optnalog', 'yurobsl', 'vosst'],
 'vosst':['abon', 'audit', 'optnalog', 'otnalog'],
 'decl':['abon', 'optnalog', 'audit', 'cons'],
 'cons':['abon', 'audit', 'yurobsl', 'yurcons'],
 'malyy':['abon', 'optnalog', 'yurobsl', 'reg'],
 'sred':['abon', 'upruchet', 'yurobsl', 'glavbuh'],
 'krup':['abon', 'upruchet', 'yurobsl', 'ved'],
 'glavbuh':['abon', 'upruchet', 'yurobsl', 'sred'],
 'upruchet':['abon', 'audit', 'optnalog', 'yurobsl'],
 'audit':['abon', 'upruchet', 'optnalog', 'vosst'],
 'optnalog':['abon', 'audit', 'upruchet', 'otnalog'],
 'sudexp':['audit', 'yurobsl', 'sudy', 'pravaudit'],
 'yurobsl':['abon', 'tz', 'dogovory', 'pravaudit'],
 'dolgi':['sudy', 'dogovory', 'yurobsl', 'pravaudit'],
 'pravaudit':['abon', 'yurobsl', 'otnalog', 'audit'],
 'egrul':['reg', 'yurobsl', 'dogovory', 'yurcons'],
 'reg':['abon', 'yurobsl', 'decl', 'egrul'],
 'dogovory':['yurobsl', 'pravaudit', 'ved', 'optnalog'],
 'ved':['abon', 'yurobsl', 'krup', 'optnalog'],
 'trud':['abon', 'yurobsl', 'voin', 'sudy'],
 'sudy':['dolgi', 'trud', 'tz', 'sudexp'],
 'intell':['tz', 'yurobsl', 'sudy', 'dogovory'],
 'otnalog':['abon', 'audit', 'yurobsl', 'pravaudit'],
 'yurcons':['abon', 'yurobsl', 'dogovory', 'pravaudit'],
 'onlayn':['ofis', 'ndfl3', 'cons', 'decl'],
 'ofis':['onlayn', 'ndfl3', 'cons', 'decl'],
 'ndfl3':['onlayn', 'ofis', 'decl', 'cons'],
 'tz':['abon', 'intell', 'reg', 'yurobsl'],
 'voin':['abon', 'cons', 'yurobsl', 'decl'],
}
from collections import Counter
inb=Counter()
for src,tg in M.items():
    assert len(tg)==4, src
    assert len(set(tg))==4, ('дубли в '+src)
    assert src not in tg, ('ссылка на себя в '+src)
    for t in tg:
        assert t in A, (src,t)
        inb[t]+=1
print('Страниц с блоком:', len(M), '| всего новых ссылок:', len(M)*4)
print('\nВходящих ссылок на страницу:')
for k,(u,n) in sorted(A.items(), key=lambda x:-inb[x[0]]):
    bar='█'*inb[k]
    print(f'  {inb[k]:>2} {bar:<12} {n:<36} {u}')
orph=[k for k in A if inb[k]==0]
print('\nБез входящих ссылок:', orph or 'нет')
print('Макс:', inb.most_common(1)[0], '| Мин:', min(inb.values()))
# кросс-раздельность
def sec(c):
    u=A[c][0]
    return u.split('/')[1]
cross=sum(1 for s,t in M.items() for x in t if sec(x)!=sec(s))
print(f'\nКросс-раздельных ссылок: {cross} из {len(M)*4} ({round(cross/(len(M)*4)*100)}%)')
no_cross=[s for s,t in M.items() if all(sec(x)==sec(s) for x in t)]
print('Страницы без единой кросс-ссылки:', [A[x][1] for x in no_cross] or 'нет')
