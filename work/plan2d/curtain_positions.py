"""Confirmed curtain motor power regions from the owner's three plan marks."""
def apply(d):
    by = {p['id']: p for p in d['points']}
    updates = [
        ('S04', 'C02', [1096, 757], [1130, 780], '书房', '上侧墙右端', '右侧窗的上端',
         '便于从书桌侧墙角就近为窗帘电机供电，电线收在窗帘盒附近，减少沿窗面外露走线。'),
        ('M05', 'C03', [1132, 267], [1183, 295], '主卧', '上侧床头墙右端', '右侧窗的上端',
         '电源靠近右侧窗上端的电机需求区域，便于隐藏接线，并避开床头日常充电插座的使用位置。'),
        ('B05', 'C04', [368, 499], [318, 477], '老人房', '下侧墙左端', '左侧窗的下端',
         '电源靠近左侧窗下端的电机需求区域，便于隐藏接线；电动开合减少老人伸手拉帘的动作。'),
    ]
    for power, control, site, anchor, room, wall, window, design in updates:
        location = f'{room}平面图{wall}、靠{window}的室内墙角高位，随窗帘盒及电机端安装。'
        check = '平面位置已确认；具体底盒中心、距墙角尺寸、吊顶完成标高、轨道与电机接线空间仍需联合核定。'
        for pid in (power, control):
            p = by[pid]
            p.update(anchors=[anchor], installAt=[],
                requestedSites=[dict(x=site[0], y=site[1], label=f'{wall}·窗帘高位',
                    reason='引线表示平面需求位置，图上方位不代表安装高度；电源仍设在窗帘盒及电机端高位。')],
                status='已调整', positionStatus='需求位置已确认，安装高度待深化',
                placement=location, positionCheck=check,
                positionReview='已按标注墙角调整平面需求区域；不作为精确开槽放线尺寸。',
                reason=f'窗帘电机需求区域移至{wall}、靠{window}；电源与关联控制标记同步。')
        by[power]['designReason'] = design + '插座或接线接口应留出检修空间，接口形式与电机数量按轨道配置核定。'
        by[power]['text'] = (f'{room}窗帘电源设在{wall}靠窗墙角高位；'
            + ('单电机1处供电，双电机2处，按选型核定。' if power == 'M05' else '保留窗帘电源1处的附件建议，实际电机数量按轨道复核。')
            + '具体高度随吊顶、窗帘盒及电机安装图核定。')
        by[control]['placement'] = location + f'本标记表示与{power}对应的电机控制需求，非墙面操作面板位置。'
        by[control]['text'] = f'{room}电动窗帘控制与{power}对应；保留本地操作，具体控制方式及面板数量待选型，电源不重复计量。'
        by[control]['positionCheck'] = check + '墙面操作面板如需设置，另行确定位置，不沿用此高位坐标。'
    d['reviewNotes'].append('窗帘电源定位：S04书房上侧墙右端、M05主卧上侧床头墙右端、B05老人房下侧墙左端；均为靠窗墙角高位，关联控制同步，安装高度待深化。')
