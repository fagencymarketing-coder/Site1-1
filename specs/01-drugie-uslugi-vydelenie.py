# -*- coding: utf-8 -*-
"""Два типовых блока «Другие услуги».

ТИП 1 — если среди карточек есть «Бухгалтерское сопровождение»:
        она всегда первая и выделена розовым #d73a61.
ТИП 2 — если её нет: выделяем бледно-зелёным #e6e7cf до двух
        самых приоритетных услуг, в их обычном порядке.
"""
FINK = {'upruchet', 'audit', 'optnalog', 'sudexp'}
MAX_GREEN = 2

def rank(code):
    if code == 'abon':    return 0
    if code in FINK:      return 1
    if code == 'yurobsl': return 2
    return 9

def decorate(code, cards):
    """-> (тип, [ (услуга, 'accent'|'green'|'') ])"""
    if 'abon' in cards:
        assert cards[0] == 'abon', f'на странице {code} бухсопровождение не первое'
        return 1, [(t, 'accent' if i == 0 else '') for i, t in enumerate(cards)]
    green = sorted([t for t in cards if rank(t) < 9], key=rank)[:MAX_GREEN]
    return 2, [(t, 'green' if t in green else '') for t in cards]
