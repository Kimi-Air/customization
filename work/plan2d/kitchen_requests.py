"""Apply user-marked kitchen power zones; equipment mapping is confirmed separately."""
def apply(d, *, cabinet_mapping_confirmed=False, countertop_count=None):
    by={p['id']:p for p in d['points']}
    for p in d['points']:
        p['powerZone']=''
        p['requestedSites']=[]
    p=by['K07']
    p.update(powerZone='台面电位',anchors=[[305,557],[306,644],[531,667]],installAt=[],status='已纠正',positionStatus='需求位置已确认，安装面待核实',
      name='台面插座（三处）',
      designReason='三处台面供电分别服务左侧上段、左侧下段及灶台右侧的操作区，使小电器就近取电，减少电源线跨越水槽、灶具和备餐通道。',
      placement='左侧台面上段、左侧台面下段、下侧灶台右侧台面，共三处，按红色点位区分。',
      positionCheck='左侧两处邻窗，需结合窗台高度及橱柜立面确认可用实墙或柜侧安装面；下侧一处需复核与灶具、水槽和设备操作区的关系。数量、面板形式及安装高度另行核定。',
      reason='台面电位由原两处调整为左侧上段、左侧下段及灶台右侧三处，按台面供电需求表达，原附件四个五孔不再作为已确认数量。')
    p['requestedSites']=[
      {'x':341,'y':565,'label':'左侧上段','reason':'靠近左侧上段操作面，供该区域的小电器就近使用；安装面需避开窗框、洗碗机开启范围及溅水区域。'},
      {'x':341,'y':645,'label':'左侧下段','reason':'服务水槽下端的备餐区域，减少电源线跨过水槽；结合窗台和台面立面落实可操作的安装面。'},
      {'x':529,'y':707,'label':'灶台右侧','reason':'服务灶台右侧的操作面，避免使用此处电器时跨灶台拉线；按灶具和台面设备尺寸复核位置。'}]
    p['text']='台面电源共3处；'+('每处插座数量待确认，不沿用原附件共4个五孔的数量。' if countertop_count is None else f'每处{countertop_count}个五孔插座，共{countertop_count*3}个；规格与回路按使用设备负荷深化。')
    if countertop_count is not None:
        p['name']=f'台面插座（3处·各{countertop_count}个）'
        p['positionCheck']=p['positionCheck'].replace('数量、面板形式及安装高度另行核定。', '每处五孔插座数量已确定；安装高度、具体安装面及规格仍需核定。')
        p['reason']=f'台面电位由原两处调整为三处，每处{countertop_count}个五孔插座，共{countertop_count*3}个；替代原附件四个五孔的数量建议。'
    if not cabinet_mapping_confirmed:return
    specs={
      'K04':([347,565],[401,550],'水槽内嵌式洗碗机','左侧上段水槽柜内','洗碗机电源设在左侧上段柜内，靠近设备便于接线与断电维护；侧向避开洗碗功能槽机身及水路接头，保留可触及的检修位置。','具体安装高度、侧板或背墙位置需按洗碗机槽体和开孔图核对，避免电源被机身遮挡或处于易受水淋处。'),
      'K06':([344,603],[400,610],'净水器','左侧中部水槽柜内','净水器在左侧中部柜内就近取电、接水，减少跨柜管线；接口留在可以打开柜门操作的位置，便于断电、换芯和检修。','需核对净水器、洗碗机槽体、角阀和排水管的占位及换芯空间；插座具体安装面应避开水管接头。'),
      'K05':([457,520],[453,558],'嵌入式蒸烤箱','上侧冰箱左侧柜内','蒸烤箱嵌入冰箱左侧柜体，电源设在该柜组可开启的检修格，缩短接线并便于维护；避免直接压在蒸烤箱机身背后或占用散热通道。','蓝色位置代表柜内电源需求区域；按机型、柜体分格及散热要求确定相邻检修格与高度，不把平面图中的柜后投影当成机身背后插座。'),
      'K02':([486,708],[480,669],'油烟机','下侧灶台上方吊柜内','油烟机电源布置在灶台上方吊柜内，便于隐藏接线；接口靠可开启的柜格，避开烟管、机身和不可拆开的烟罩，便于检修。','平面位置在图纸下侧，实际安装高度在灶台上方吊柜；需结合烟管走向、烟机安装尺寸与柜门核对。')}
    for pid,(xy,anchor,device,place,why,check) in specs.items():
        p=by[pid]
        p.update(powerZone='柜内电位',requestedSites=[{'x':xy[0],'y':xy[1],'label':device,'reason':''}],anchors=[anchor],installAt=[],status='已纠正',positionStatus='需求位置已确认，柜内尺寸待深化',designReason=why,placement=place+'的可检修区域。',positionCheck=check,reason='柜内供电区域按位置标注确认；接口中心、高度和检修格仍需配合设备与橱柜立面确定。')
        p['text']=device+'柜内电源×1；规格、回路与高度按机型核定，安装后可触及。'
    by['K06']['name']='净水器柜内电源'
    by['K05']['name']='蒸烤箱柜内电源'
    by['K02']['name']='油烟机吊柜内电源'
    # Keep the other kitchen power requirements; the annotation does not cancel them.
    by['K01']['anchors']=[[511,552]]
    by['K09']['anchors']=[[495,607]]
    by['K08']['anchors']=[[365,535]]
    next(r for r in d['rooms'] if r['name']=='厨房')['label']=[470,635]
    by['K03']['anchors']=[[434,674]]
