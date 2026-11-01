"""Apply the owner's network, left-bedside and remote-control selections."""
def apply(d):
    p={v['id']:v for v in d['points']}
    old=p['W11']
    d['excluded'].append({**{k:old[k] for k in ['id','name','room','kind','source']},'reason':'阳台不设置独立洗衣池，取消其冷热水与排水预留；洗烘和扫地机水路保留。'})
    d['points']=[v for v in d['points'] if v['id']!='W11']
    for pid,location,text,check in [
        ('N04','书房上侧2000 mm宽贴墙书桌背后、桌下低位；与S01电源分盒。','书桌下方保留有线网口2个，建议中心高350 mm，数量不增加。','复核桌腿、柜格和走线孔，保证桌下网口可检修。'),
        ('N05','主卧下侧墙M02预留插座附近低位，与电源分盒。','主卧有线网口1个，随M02预留电源做低位，建议中心高400 mm。','核对后续柜体、踢脚线及强弱电底盒排布。'),
        ('N06','老人房床尾下侧墙B03插座附近低位，与电源分盒。','老人房床尾有线网口1个，建议中心高350 mm，与B03备用插座配合。','避开门洞、踢脚线及家具遮挡；网口与B03分别设盒。'),
        ('N08','入户门上方室内侧摄像机附近，与E04独立电源协调，强弱电分盒。','入户摄像机旁预留网线1根；终端采用网口或直连按摄像机确定。E04独立电源保留。','有线预留已确认；终端形式、预留线长及高度按摄像机和门套复核，不因预留网线自动改为PoE供电。')]:
        p[pid].update(placement=location,text=text,positionCheck=check,requirement='已确认需要',status='已确认',
            positionStatus='布置方式已确认，安装尺寸待深化',reason='采用已确认的低位网口及入户监控有线预留方案，保留原接口数量。')
    p['N06'].update(anchors=[[464,466]],installAt=[[480,501]],requestedSites=[],
        designReason='床尾网口与备用电源就近配合，可供后续网络设备使用；低位布置减少墙面视觉干扰，独立底盒方便检修。')
    p['N04']['designReason']='两个有线接口统一放在桌下，可连接电脑与其他网络设备，减少桌面外露接口；随2 m书桌组织走线，保持检修空间。'
    p['N05']['designReason']='网口与主卧预留电源位于同一低位设备区域，便于后续设备接入有线网络，避免恢复已取消的梳妆台位置假设。'
    p['N08']['designReason']='在门上方摄像机旁预留网线，为有线连接保留条件；独立电源仍由E04提供，终端连接形式按机型确定。'
    for pid,anchor,site,location in [
        ('C07',[382,365],[382,320],'老人房平面图左侧床头墙，1500 mm床面左端外侧，邻近左侧床头柜。'),
        ('C08',[913,920],[918,958],'书房平面图左侧沙发床旁的下侧墙面，靠床面左端外侧。')]:
        p[pid].update(anchors=[anchor],installAt=[site],requestedSites=[],placement=location,
            status='已确认',positionStatus='左侧操作位置已确认，尺寸待深化',
            text='左侧床头场景面板1处，用于照明场景，与门口灯光控制协调；窗帘由独立遥控器操作。',
            designReason='左侧就近操作便于躺卧时控制照明，减少起身绕行；窗帘使用各自遥控器，不占此面板的窗帘控制功能。',
            positionCheck='使用侧已确定；横向位置与高度按床头柜或沙发床扶手、床架外廓核定，与电源分盒。',
            reason='床头场景面板明确位于平面图左侧；只保留照明场景，窗帘采用独立遥控。')
    for pid,power in [('C01','L06'),('C02','S04'),('C03','M05'),('C04','B05'),('A05','A06')]:
        v=p[pid];device='晾衣架' if pid=='A05' else '窗帘'
        v.update(name=v['name'].replace('控制','')+'（遥控）',status='已确认',requirement='已确认需要',
            text=f'{device}采用各自遥控器操作，不另设独立墙面控制面板，不纳入床头或门口场景面板；设备电源见{power}。',
            designReason=f'使用设备自带遥控器即可就近操作{device}，减少独立墙面面板；图中保留功能标记以便核对设备电源。',
            placement=p[power]['placement']+' 本标记仅对应遥控设备位置，不是遥控器存放位或墙面面板。',
            positionStatus='独立遥控已确认，无墙面面板',
            positionCheck=f'墙面面板及底盒数量为0；遥控器配置随设备套装核对，设备电源尺寸仍按{power}深化。',
            positionReview='图上标记表示遥控设备所在区域，不新增控制底盒或墙面控制布线。',
            reason=f'{device}改为各自遥控器操作，不另设墙面控制面板。')
        if pid=='A05':
            v.update(anchors=[[1178,664]],installAt=[],requestedSites=[dict(x=1177.5,y=621,label='晾衣架设备（遥控）',reason='标记指向顶面设备，不是墙面开关；电源见A06。')])
        else:
            v['requestedSites']=[{**s,'label':s['label']+'·遥控设备','reason':'仅标记窗帘电机区域；独立遥控，不另设墙面控制面板。'} for s in v['requestedSites']]
    p['C06']['text']='主卧床头照明场景面板2处，左右各1处，参考750 mm；窗帘使用独立遥控器，不纳入床头场景。'
    p['C06']['positionCheck']+=' 窗帘不占用场景按键，照明功能与智能系统按选型深化。'
    d['reviewNotes']=[n.replace('墙面操作面板需单独确定','窗帘及晾衣架采用各自遥控，不另设墙面面板') for n in d['reviewNotes']]
    d['reviewNotes'].extend([
        '取消W11独立洗衣池水路；洗衣机、烘干机和扫地机原服务区域保留。',
        '网口方案已确认：书房2口桌下，主卧1口随M02低位，老人房1口随B03低位，入户摄像机旁预留网线1根。',
        '老人房C07、书房C08床头照明场景面板均放在图纸左侧。窗帘和晾衣架各用遥控器，无新增独立墙面面板。'])
