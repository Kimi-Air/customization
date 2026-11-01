from pathlib import Path
p=Path('review_points.py');s=p.read_text()
changes={
'K04':'K04|水槽内嵌式洗碗机位于厨房左侧水槽上端，电源就近留在水槽柜可触及的侧部，便于断电检修；避开洗碗功能槽下方的机身与管线占位，避免插座被设备遮住。|厨房左侧水槽柜内、洗碗功能槽以外的可检修侧板区域。|设备类型与水槽上端位置已确定；按机型核对台面开孔、柜内机身占位及开启空间，插座需避开水管接头和易受水淋处。|381,615|412,622',
'K06':'K06|净水器就近接入水槽冷水支路，电源随净水机的实际柜格设置，可缩短管线并方便维护；水槽内嵌式洗碗机会占用柜内空间，需先核对两台设备能否同时容纳。|水槽柜或相邻柜中净水器所在格的可触及侧板，避开水管接头。|需同时核对洗碗机槽体、净水器机身、换芯操作与管线空间；净水器具体柜格未定，暂不锁定插座位置。||412,579',
'W01':'W01|水槽与内嵌式洗碗机在同一区域布置，给排水集中在可开启柜内便于检修；净水器按独立冷水支路需求接入，减少跨柜长管并保留阀门操作空间。|厨房左侧水槽柜内部，避开洗碗功能槽机身，沿可检修的柜后或柜侧布置。|核对水槽与洗碗机一体组件、净水机及换芯空间；给排水接头不可被机身和柜体遮住，净水机废水接法随型号确定。|365,604|403,590',
'W02':'W02|水槽内嵌式洗碗机就近连接水槽柜内给排水，可缩短管路并集中检修；阀门和接头避开洗碗功能槽的机身占位，排水连接按该机型要求设置。|厨房左侧水槽柜内的可检修接口区，避开图纸上端的洗碗功能槽机身。|洗碗机位置已确定；冷水接口、排水高度与连接方式以选定机型安装图为准，不沿用普通下嵌式洗碗机的安装假设。|381,615|414,638'
}
lines=s.splitlines()
for i,line in enumerate(lines):
 key=line.split('|')[0]
 if key in changes:lines[i]=changes[key]
s='\n'.join(lines)+'\n'
s=s.replace("by['K04']['text']='洗碗机电源×1，设在相邻可检修柜内；插座规格与安装高度按设备和柜图确认。'", "by['K04']['text']='水槽内嵌式洗碗机电源×1；电源设在水槽柜可检修侧部，避开洗碗功能槽占位，规格与高度按机型安装图核定。'\nby['K04']['name']='水槽内嵌式洗碗机电源'\nby['W02']['name']='水槽内嵌式洗碗机给排水'\nfor pid in ['K04','W02']:\n by[pid]['status']='已纠正'\n by[pid]['reason']='设备明确为厨房左侧水槽上端的水槽内嵌式洗碗机，修正普通下嵌式机型的安装假设；保留原编号，同步核对水槽柜内电源、给排水与净水器占位。'\nby['K06']['reason']='水槽内嵌式洗碗机占用柜内空间，净水器电源需随可落实的设备格重新定位，先核对机身和换芯检修空间。'")
s=s.replace("by['W02']['text']='洗碗机冷水＋排水，接口在相邻柜内可检修；高度、软管走向与防回流做法按最终设备安装要求。'", "by['W02']['text']='水槽内嵌式洗碗机冷水＋排水接口，与水槽系统协调；接口位置、排水高度与连接方式按选定机型安装图确认，不机械套用原H500。'")
s=s.replace("{'title':'博世：洗碗机安装后应可接近电源插头','url':'https://www.bosch-home.com.hk/zh/service/get-support/connecting-dishwasher'}", "{'title':'方太：水槽洗碗机安装与净水器空间配合（机型参考）','url':'https://fotile.com.hk/zh-hans/pages/faqs'}")
p.write_text(s)
p=Path('src/App.tsx');s=p.read_text();needle='     {/* Furniture overlays express confirmed use; architectural perimeter stays source-based. */}'
s=s.replace(needle,needle+'''\n     <g aria-label="厨房左侧水槽上端：水槽内嵌式洗碗机，外形尺寸示意" role="img" pointerEvents="none"><title>水槽内嵌式洗碗机 · 外形及开孔尺寸按机型确认</title><rect x="356" y="555" width="21" height="24" rx="1.5" fill="#e7f0ed" stroke="#628c80" strokeWidth="1.2"/><rect x="359" y="558" width="15" height="16" rx="1" fill="none" stroke="#9cb8af" strokeWidth=".7"/><path d="M363 576H370 M349 567H356" stroke="#628c80" strokeWidth="1"/><text x="346" y="570" textAnchor="end" fontSize="8.5" fill="#4d766a">水槽洗碗机</text></g>''')
p.write_text(s)
