"""Apply the four owner-marked power locations from the supplemental plan."""
def apply(d):
    by = {p['id']: p for p in d['points']}
    next(r for r in d['rooms'] if r['name']=='厨房')['box'] = [329, 514, 226, 250]

    def locate(p, site, anchor, label):
        p.update(anchors=[anchor], installAt=[],
                 requestedSites=[dict(x=site[0], y=site[1], label=label, reason='')],
                 positionStatus='需求位置已确认，安装尺寸待深化',
                 positionReview='引线指向墙面需求区域的平面投影；高低位以详情说明为准。')

    p = by['E04']
    locate(p, [595, 748], [610, 656], '入户门上方高位')
    p.update(name='入户门上方监控电源（独立回路）', requirement='已确认需要', status='已确认',
             text='入户门上方预留监控摄像电源1处，采用独立回路、持续供电，不受玄关灯光开关控制。',
             designReason='门上方的高位安装便于覆盖入户动线并减少家具遮挡；独立回路便于单独断电检修，监控持续供电，不随开关玄关灯中断。',
             placement='入户门上方的室内侧墙面，高位安装；图上引线落在门洞投影位置。',
             positionCheck='具体高度、视角、安装支架及适配器检修空间按门套和摄像机核定；独立回路的线缆、保护配置和配电箱编号由电气深化确定。',
             reason='补图明确为入户门上方，并确认独立回路；替代此前待确认的灯光共享方案。')
    p = by['N08']
    locate(p, [595, 748], [610, 656], '入户门上方监控网络')
    p.update(status='已纠正', text='监控网络接口随入户门上方摄像机位预留；摄像机采用有线还是无线网络，随设备选型确认。电源见独立回路E04。',
             designReason='网络接口随摄像机布置，可在采用有线连接时隐藏线缆，方便设备维护；与E04表示同一摄像机的不同接口，不重复计摄像机。',
             placement='入户门上方室内侧，与E04监控位置协调。',
             positionCheck='网络接入方式及接口形式按摄像机选型确认；已确认的监控独立电源回路见E04。',
             reason='监控位置随补图调整至入户门上方，网络方式仍待选型。')

    def add(pid, room, name, site, anchor, text, design, placement, check, label):
        p = dict(id=pid, room=room, kind='强电', name=name, text=text,
                 source='补充平面图中明确的电源需求；原附件无独立编号。', sourceType='补充需求',
                 page=1, status='已补充', requirement='已确认需要', powerZone='',
                 reason='按补充平面图新增需求位置。', designReason=design,
                 placement=placement, positionCheck=check)
        locate(p, site, anchor, label)
        d['points'].append(p)
        return p

    add('L07', '客厅', '电动沙发低位电源', [1100, 502], [1102, 582],
        '沙发右侧与墙体间隙下方电源1处，供电动沙发使用；原L03右侧插座并入本点，不重复设置或计量。',
        '靠近电动沙发的右侧低位供电，能隐藏适配器接线并减少电线跨过活动区域；插座位于侧面间隙，便于断电和检修。',
        '沙发右侧与墙体之间的间隙下方，靠墙低位安装。',
        '核对沙发完全展开时的活动机构、侧向净距、插头和适配器空间；具体高度与接口按设备确定，线缆避开运动部件。',
        '沙发右侧间隙低位')
    by['L03'].update(
        name='沙发左侧插座', anchors=by['L03']['anchors'][:1],
        installAt=by['L03']['installAt'][:1], status='已纠正',
        text='沙发左侧五孔插座1个；有边几H750、无边几H350为原建议，具体高度随家具核定。右侧电源统一见L07。',
        designReason='沙发左侧插座方便手机充电或台灯使用，设在扶手外侧可触及的墙面，减少移动家具和拖接电线。',
        placement='沙发背景墙左侧、扶手外侧可触及的墙面。',
        reason='右侧插座并入L07电动沙发电源；L03仅保留左侧1处。')
    next(p for p in d['points'] if p['id']=='L07')['reason']='合并原L03右侧插座，保留电动沙发用途，仅计1处右侧电源。'
    add('K12', '厨房', '厨房储藏区电源', [382, 749], [304, 739],
        '厨房左下角储藏区域预留电源1处；具体插座形式、数量和安装高度随储藏柜及使用设备确定。',
        '在厨房左下角储藏空间就近供电，为柜内或储藏区域设备留接口，减少从厨房操作台拖线；位置应便于使用与检修。',
        '厨房左下角储藏区域的下侧墙面，按红框对应区域定位。',
        '确认储藏柜层板、门扇、实际用电设备和插拔空间后定高度；点位不延伸到公共电梯间。',
        '厨房左下储藏区域')
    old = next(p for p in d['excluded'] if p['id']=='H01')
    p = add('H01', '过道', '过道低位备用插座（待定）', [615, 427], [598, 467],
        '过道墙体下方预留电位需求待定，用于Wi-Fi扩展器或插电小夜灯；原附件五孔×1、H350仅供对照。',
        '过道低位接口可就近接入插电小夜灯，或在需要补充无线覆盖时为扩展器供电；是否保留应结合照明和网络实际需求确定。',
        '公卫下侧、朝过道的短墙低位，位于次卧门口右侧；按红框对应墙段定位。',
        '是否保留待定；若用于Wi-Fi扩展器，需核对该处信号及设备占位；最终高度和底盒位置按用途确定。',
        '过道墙面低位（待定）')
    p.update(source=old['source'], sourceType='原附件', requirement='待定', status='待确认',
             positionStatus='位置已标明，是否保留待定', reason='恢复H01为待定项，并移动到补图标明的过道短墙低位。')
    d['excluded'] = [p for p in d['excluded'] if p['id']!='H01']
    d['reviewNotes'] = [t for t in d['reviewNotes'] if '玄关监控E04' not in t]
    d['reviewNotes'].extend([
        '沙发插座去重：L03仅保留左侧1处，右侧统一为L07电动沙发电源1处。',
        'E04位于入户门上方，采用独立回路持续供电；监控网络N08随设备选型确定。',
        '新增L07电动沙发低位电源与K12厨房左下储藏区电源。',
        'H01恢复为待定项，位置在公卫下侧朝过道的短墙低位，拟用于Wi-Fi扩展器或小夜灯。'])
    d['points'].append(dict(
        id='K13', room='厨房', kind='强电', name='燃气报警器电源',
        anchors=[[399,482]], installAt=[], requestedSites=[dict(x=403,y=519,label='燃气热水器插座旁',reason='')], powerZone='',
        requirement='已确认需要', status='已补充', sourceType='补充需求', page=1,
        source='补充需求：燃气热水器插座旁增加燃气报警器电位。',
        text='在K08燃气热水器插座旁单独预留燃气报警器电源1处，持续供电；供电接口按选定报警器确定。',
        designReason='在用气区域为燃气报警器预留持续供电接口，便于监测燃气泄漏并减少临时接线；电源位置配合报警器的检测范围和检修条件确定。',
        placement='厨房上侧墙面，K08燃气热水器插座旁；图中表示相邻供电区域，具体间距和高度待深化。',
        positionCheck='确认燃气种类及报警器型号后，按设备安装说明确定探测器及供电点的高度、间距和接口；不直接套用固定220cm高度。',
        positionStatus='热水器插座旁，安装高度待机型核对',
        positionReview='引线指向热水器插座旁的供电需求区域，非最终底盒中心；报警器本体位置另按设备说明复核。',
        reason='新增燃气报警器电源，位置确认为K08燃气热水器插座旁；型号及安装高度待深化。'))
    d['reviewNotes'].append('新增K13燃气报警器电源，位于K08燃气热水器插座旁，具体高度和接口按燃气类型及机型确认。')
    d['referenceLinks'].append(dict(
        title='石家庄市场监管局：燃气报警器需匹配燃气类型（安装提示）',
        url='https://scjg.sjz.gov.cn/columns/9704bc53-9463-4d5b-8900-cbd23118aeca/202609/01/95d4b35f-a007-4be6-be31-8eeb35b651ac.html'))
