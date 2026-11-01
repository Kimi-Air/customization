"""Apply the 23-item owner review; preserve source quotes and removed-item audit."""
from copy import deepcopy

def apply(d):
    by={p['id']:p for p in d['points']}
    for p in d['points']:
        p['requirement']=''
        p['sourceType']='原附件'
    removals={
        'N03':'取消电视高位网络。','N07':'不设置吸顶PoE AP。','N10':'不纳入智能门锁点位。',
        'S05':'书房左侧为衣柜，取消书柜灯电源。','E02':'取消鞋柜与玄关备用插座。',
        'L02':'取消电视高位插座。','D02':'取消餐厅备用插座。','B06':'取消次卧衣柜灯电源。',
        'B02':'取消次卧书桌或梳妆台插座。','A03':'取消洗衣池上方插座。','H01':'取消过道备用插座。',
        'K03':'取消燃气灶备用插座。','K09':'取消吊柜灯电源。',
        'D05':'岛台不计新增独立电位；改为从D01餐边柜设备插座取电的连接关系示意。'}
    d['excluded']=[dict(id=k,name=by[k]['name'],room=by[k]['room'],kind=by[k]['kind'],source=by[k]['source'],reason=v) for k,v in removals.items()]
    d['points']=[p for p in d['points'] if p['id'] not in removals]
    def confirmed(pid,**changes):
        p=by[pid];p.update(requirement='已确认需要',status='已确认',**changes);return p
    def demand(pid,site,anchor,label,placement,check,**changes):
        p=confirmed(pid,installAt=[],anchors=[anchor],requestedSites=[{'x':site[0],'y':site[1],'label':label,'reason':''}],placement=placement,positionCheck=check,positionStatus='需求位置已确认，安装尺寸待深化',positionReview='标注为需求区域的平面投影，具体安装高度、设备占位和检修条件需深化。',**changes)
        return p
    def new(pid,room,kind,name,text,design,placement,check,site,anchor,label,zone='',source='本轮新增需求；原附件无独立编号。'):
        p=dict(id=pid,room=room,kind=kind,name=name,text=text,source=source,page=1 if kind=='强电' else 2,status='已补充',reason='按已确认的使用需求新增。',designReason=design,placement=placement,positionCheck=check,installAt=[],anchors=[anchor],positionStatus='需求位置已确认，安装尺寸待深化',positionReview='需求区域示意；不代替现场安装尺寸。',powerZone=zone,requestedSites=[{'x':site[0],'y':site[1],'label':label,'reason':''}],requirement='已确认需要',sourceType='补充需求')
        d['points'].append(p);by[pid]=p;return p
    # 1–3: keep existing wired outlets, remove only non-entry sensors and the named exclusions.
    confirmed('N09',name='入户人体与门窗传感器',text='仅保留入户区域的人体与门窗传感器需求；电池式免预埋市电，具体类型及数量按选型确认。',anchors=[[610,711]],installAt=[],requestedSites=[{'x':595,'y':735,'label':'入户区域','reason':''}],designReason='入户感应服务进出门照明或安防联动；人体感应与门窗感应按检测任务选型，仅在入户区域配置，避免为未需要的其他区域增加设备。',placement='入户区域的门框或室内检测位置，具体载体随传感器类型确定。',positionCheck='门磁安装侧、人体检测范围、型号和数量待确认；不在其他房间布置。',positionStatus='仅入户区域，安装部位待深化',reason='仅保留入户传感器，删除过道及其他房间传感器标注。')
    for pid in ['E01','N01']:
        demand(pid,[970,501],[940,544],'沙发背后弱电箱','客厅沙发背后的弱电箱区域。','实际箱体中心、高度及箱门开启范围需现场核实；与沙发靠背留出检修、散热及走线空间。',reason='弱电箱及对应电源统一由电视下方调整到沙发背后。')
        by[pid]['positionStatus']='沙发背后，实际箱位待核实'
    by['E01'].update(designReason='弱电箱内的网络设备需要持续供电，电源随沙发背后的箱体布置，避免另拉明线；箱门应能开启，方便断电维护和更换设备。',text='沙发背后弱电箱内电源；原附件五孔×2作为设备配电建议，数量和形式按箱内设备核定。')
    by['N01'].update(designReason='网络线集中汇入沙发背后的弱电箱，便于配线、排障和设备维护；保留电视低位及各房间有线网口，管路依实际箱位组织。',text='沙发背后弱电箱：入户光纤、光猫及网络配线设备汇聚；保留未取消的各房间有线接口。')
    by['N06']['positionCheck']='书桌或梳妆台电源已取消，但有线网口继续保留；需另按实际设备或可用墙面确认位置。'
    # 4: elder scene already existed; retain it once, add the study scene.
    confirmed('C07',name='次卧床头场景',text='次卧床头场景面板预留1处，与门口B07联动；原建议H750，具体按床头柜与使用习惯核定。',reason='保留次卧床头场景需求，不重复增加原C07。',positionStatus='需求已确认，床头使用侧待定')
    new('C08','书房','控制','书房床头场景','书房沙发床休息位增加床头场景面板1处，与S06门口照明控制协调。','沙发床用于休息时，可就近关灯、开夜灯或操作窗帘，减少起身绕过展开床面的需要。','书房下侧沙发床一端的可触及墙面；图示为需求区域。','具体使用侧、安装高度与沙发床展开范围确认后定点；智能协议和控制清单待深化。',[1083,958],[1088,915],'沙发床休息位')
    # 7: exact monitor position and shared-light wiring await the promised image.
    confirmed('E04',text='玄关监控电源需求已确认；与玄关灯光的具体位置、共用关系及接法待补图确认。',anchors=[[624,666]],installAt=[],requestedSites=[],designReason='玄关监控用于观察入户动线，电源应配合摄像机视角和实际安装载体布置，并留出维护条件。',placement='入户玄关区域，精确位置待补图。',positionCheck='等待补图确认监控位置及与玄关灯光的接法；暂不指定共用开关、常电或照明回路。',positionStatus='等待补图确认位置与接法',reason='明确保留玄关监控；与灯光的共享含义尚未确认。')
    by['N08'].update(anchors=[[624,666]],text='玄关监控网络预留需求保留；是否采用有线、PoE或无线方式，随监控方案确认。',placement='随E04监控实际安装位置，等待补图。',positionCheck='补图确认视角与位置；供电及网络方式需结合设备选型，不默认与照明共用开关。',positionStatus='随监控补图确认',reason='与E04同位置深化；不擅自指定共享接法。')
    # 9: pending need is different from an approved installation target.
    by['L04'].update(requirement='待定',status='待确认',installAt=[],requestedSites=[],positionStatus='是否保留待定',positionCheck='暂不计为已确认施工点；保留与否确定后再复核电视柜端部和插拔空间。',text='客厅备用插座需求待定；原附件五孔×1、H350仅供对照。',reason='由保留项转为待定项。')
    # 10–11: distinguish appliance receptacles from lighting supply. Island is a relation, not another point.
    by['D01'].update(name='餐边柜设备插座',text='餐边柜设备插座：原建议台面3个＋柜内1个；岛台电源线从本组取电，接口分配和同时使用负荷需核定。',designReason='餐边柜插座服务台面小电器及柜内设备，并作为岛台的取电来源；按设备分配接口，避免把柜灯驱动电源当成设备插座。',positionCheck='台面高度、柜格和设备负荷待深化；核对岛台接电口是否占用原柜内接口及线路收纳方式。',reason='明确为设备插座，供岛台取电；与D03柜灯驱动电源区分。',requirement='已确认需要',status='已确认')
    by['D03'].update(name='餐边柜柜灯驱动电源',text='餐边柜灯及驱动器电源1路，设在可检修柜格；与D01设备插座用途不同，不作为岛台取电端。',reason='名称明确为柜灯驱动电源，避免与D01设备插座混淆。')
    d['connections']=[{'id':'ISLAND-D01','kind':'强电','room':'餐厅','to':'D01','path':[[779,631],[800,674],[800,730],[708,738]],'label':'岛台 → D01 餐边柜设备插座','labelAt':[812,683],'note':'仅示意供电连接关系；线缆隐藏、固定、检修与通行避让另行深化。岛台不计新增独立电位。'}]
    # 15–16: both bathrooms' four loads are required; don't certify electrical zoning or install dimensions.
    for prefix in ['T','U']:
        for n in range(1,5):
            pid=f'{prefix}{n:02d}';p=confirmed(pid)
            p['reason']='设备需求已确认保留；安装位置仍配合设备、隔断和浴室电气分区深化。'
            p['designReason']=p['designReason'].replace('若采用智能马桶，','智能马桶').replace('若设置电热毛巾架，','电热毛巾架').replace('若设置','设置')
        by[prefix+'01']['positionCheck']='智能马桶需求已确定；核对机型、淋浴隔断、电气分区与保护措施后定安装位置和高度。'
        by[prefix+'04']['positionCheck']='电热毛巾架需求已确定；架体位置、干区可用墙面、设备要求和浴室电气分区仍需深化。'
    # 17–18: anchor all wash/dry points behind the stack; spread index labels to the right.
    laundry={
       'A01':([1145,503],[1265,455],'洗衣机','洗衣机电源1处，位于洗烘叠放设备后方墙面；高度和插座规格按机型核定。'),
       'A02':([1158,503],[1300,500],'烘干机','烘干机电源1处，与洗衣机分接口，位于洗烘叠放设备后方墙面；规格按功率核定。'),
       'A04':([1171,503],[1335,545],'洗烘区备用','洗烘区备用插座1处，锚定洗衣机后方墙面；具体高度与可操作空间配合柜图确定。')}
    for pid,(site,anchor,label,desc) in laundry.items():
        demand(pid,site,anchor,label,'阳台上端洗衣机/烘干机叠放设备后方墙面；图上横向微分开表示不同接口。','按机身背部预留空间、插头突出量、叠放支架、水路接头与检修方式核对高度；需避免设备压线，检修断电方式在柜图中落实。',text=desc,designReason='电源集中在洗烘设备后方，缩短设备接线并隐藏外露线缆；洗衣机、烘干机和备用接口分别表达，方便按用途配置。',reason='明确保留，位置锚定洗衣机后方；编号标签向右移开，避免重叠。')
    by['A04']['name']='洗烘区备用插座'
    demand('L05',[1211,503],[1370,590],'扫地机后方','洗烘右侧扫地机器人基站后方墙面。','结合基站背部余量、水路连接和机器抽出检修方式定高度，避免插头与水管互相挤压；设备需能维护断电。',text='自动上下水扫地机电源1处，锚定基站后方；规格与高度按机型确认。',designReason='基站后方取电便于隐藏电线并缩短连接，位置随洗烘右侧的基站固定；插头、水管和检修空间需共同安排。',reason='明确保留，锚定扫地机背后，标签向右分散。')
    # 19: ceiling power is a strong-current point; A05 becomes control only.
    confirmed('A05',name='电动晾衣架控制',anchors=[[1128,697]],installAt=[],requestedSites=[],text='电动晾衣架控制需求；遥控、墙面面板或智能联动方式按机型确认。强电电源见A06，不重复计量。',designReason='晾衣架控制应在日常使用时容易操作，控制方式随机型配置；把控制需求与顶面电源分开，可避免遗漏供电或重复核量。',placement='控制方式待定；如设墙面面板，优先在阳台入口可达实墙。',positionCheck='确认墙面面板、遥控或智能控制方式及实际安装位置。',positionStatus='设备需要，控制方式待选型',reason='电源独立列入强电A06，本项仅保留控制需求。')
    new('A06','阳台','强电','电动晾衣架顶面电源','电动晾衣架强电电源1处，位于阳台水平、垂直居中的顶面位置。','顶面电源靠近居中的晾衣架，可缩短接线并减少外露线缆，便于与设备安装位统一安排。','阳台平面中心对应的顶面；不是地面插座。','具体供电形式按机型确认；吊顶、承重安装、升降和窗帘柜门的避让需现场复核。',[1177.5,621],[1178,664],'阳台中心顶面')
    by['A06']['reason']='新增强电图层中的晾衣架供电标注，控制A05不重复计电源。'
    # 22: refrigerator power behind the appliance as requested.
    demand('K01',[516,521],[514,554],'冰箱后方','厨房上侧冰箱后方墙面。','按冰箱安装图核对背部空间、插头突出量、散热与断电检修方式，避免影响冰箱推入及压线。',text='冰箱电源1处，调整到冰箱后方；高度、规格与回路按机型和电气深化核定。',designReason='电源随冰箱设在后方，便于隐藏设备接线；安装时需给插头、散热及后续断电检修留出条件。',reason='由相邻柜内调整到冰箱后方。')
    # 23: additional countertop point above K05; do not invent an unconfirmed socket quantity.
    new('K11','厨房','强电','蒸烤箱上方台面电源','冰箱左侧、蒸烤箱柜上方增加台面电源1处；插座数量与形式待确认，与K07三处各1个五孔分别计量。','在蒸烤箱柜上方操作面提供就近电源，便于台面设备使用；台面插拔与柜内蒸烤箱电源分高度布置，互不占用。','与K05相同平面位置的上方台面安装区；K05在柜内，本项在台面上方。','确认台面高度、挡水或背板及设备开启散热空间，插座数量和规格待确定。',[457,520],[453,483],'蒸烤箱柜上方','台面电位')
    by['K05']['positionCheck']+=' 与K11为同一平面位置、不同高度的电源，避免混用。'
    d['reviewNotes']=[
        '未点名取消的有线网口保留；人体与门窗传感器仅留入户区域。',
        '书房左侧为衣柜；书柜灯S05及次卧衣柜灯B06取消。',
        'D01为设备插座，D03为柜灯驱动电源；岛台从D01取电，不新增D05独立点位。',
        '两卫T01–T04、U01–U04全部需要；位置与浴室电气分区仍需深化。',
        '玄关监控E04的精确位置及与灯光的接法等待补图。']
