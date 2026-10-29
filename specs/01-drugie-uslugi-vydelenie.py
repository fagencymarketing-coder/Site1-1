# -*- coding: utf-8 -*-
"""Два типовых блока «Другие услуги».

ТИП 1 — если среди карточек есть «Бухгалтерское сопровождение»:
        она всегда первая и выделена розовым #d73a61.
ТИП 2 — если её нет: выделяем бледно-зелёным #e6e7cf две самые
        приоритетные услуги, в их обычном порядке.

Полностью белых блоков не бывает: в блоке всегда есть либо розовая,
либо две зелёных карточки.
"""
FINK = {'upruchet', 'audit', 'optnalog', 'sudexp'}   # финансовый и налоговый консалтинг
BRIDGE = ('cons', 'decl')                            # мостики из B2C в платные услуги
GREEN = 2

def rank(code):
    if code == 'abon':      return 0
    if code in FINK:        return 1
    if code == 'yurobsl':   return 2
    if code in BRIDGE:      return 3 + BRIDGE.index(code)
    return 9

def decorate(code, cards):
    """-> (тип, [ (услуга, 'accent'|'green'|'') ])"""
    if 'abon' in cards:
        assert cards[0] == 'abon', f'на странице {code} бухсопровождение не первое'
        return 1, [(t, 'accent' if i == 0 else '') for i, t in enumerate(cards)]
    green = sorted(cards, key=lambda t: (rank(t), cards.index(t)))[:GREEN]
    return 2, [(t, 'green' if t in green else '') for t in cards]
