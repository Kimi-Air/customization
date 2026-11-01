"""Confirmed 1500 mm bed widths and 2000 mm wall-backed study desk."""
def apply(d):
    p = {x['id']:x for x in d['points']}
    p['S01'].update(anchors=[[964,811],[1060,811]], installAt=[[974,757],[1048,757]],
        placement='书房上侧实墙，2000 mm宽贴墙书桌背后；桌上与桌下分高度布置。',
        designReason='两组接口都落在2 m宽书桌范围内，分别服务桌面充电及桌下电脑设备，避免桌子缩窄后插座落到桌外。',
        positionCheck='按桌面高度、显示器和桌腿布置核定横向偏距；贴墙桌需留走线孔或线槽，不挤压插头。',
        reason='书桌宽度明确为2000 mm且贴上侧墙；供电点随桌宽微调，原数量与高度建议保留。')
    p['N04'].update(anchors=[[1012,811]],installAt=[[1012,757]],
        placement='书房上侧实墙，2000 mm宽书桌背后的电脑设备区，与S01强电分盒。',
        positionCheck='接口位于2 m桌宽内，按设备、桌板走线孔及桌腿复核，桌上/桌下网口分配待定。',
        reason='网络点随2 m贴墙书桌调整，网口数量保持。')
    p['B01'].update(installAt=[[391,320],[517,320]],
        placement='老人房上侧床头墙，1500 mm宽床面两侧的床头柜上方。',
        positionCheck='床面宽1500 mm已确认；床架外宽、床头柜尺寸与插拔空间按选型核定。',
        reason='床面改为1500 mm宽，床头供电随床面两侧微调，仍为每侧1个五孔。')
    for pid in ['S02','S07','C08']:
        p[pid]['positionCheck'] += ' 沙发床展开床面宽1500 mm，床架外宽及展开长度待选型；展开时座椅需收拢或移开。'
    next(r for r in d['rooms'] if r['name']=='书房')['label']=[881,867]
    d['reviewNotes'].append('老人房床面及书房沙发床展开床面均宽1500 mm；书房书桌宽2000 mm、贴上侧墙。床架外廓、床长、桌深和椅子占位为示意，按家具选型复核。')
