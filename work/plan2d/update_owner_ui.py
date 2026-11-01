from pathlib import Path
p=Path('src/App.tsx');s=p.read_text()
s=s.replace("'待确认':'gold'", "'待确认':'gold','已确认':'green'")
s=s.replace('const base=[240,205,1050,835];','const base=[240,205,1180,835];')
s=s.replace("'供电类别','接口说明'", "'供电类别','需求状态','接口说明'")
s=s.replace('p.kind,p.name,p.powerZone,p.text','p.kind,p.name,p.powerZone,p.requirement,p.text')
s=s.replace('<Tag>{p.room} · {p.kind}</Tag>',"<Tag>{p.room} · {p.kind}</Tag>{p.requirement&&<Tag color={p.requirement==='待定'?'gold':'green'}>{p.requirement}</Tag>}")
s=s.replace("{p.powerZone?p.powerZone+' · 需求区域':p.positionStatus}</small>", "{p.requirement==='待定'?'是否保留待定':p.powerZone?p.powerZone+' · 需求区域':p.positionStatus}</small>")
s=s.replace('<summary>附件原文 · 第 {p.page} 页</summary><p>{p.source}</p><Button size="small" onClick={()=>{setSourcePage(p.page-1);setDrawer(\'source\')}}>打开原页</Button>', '<summary>{p.sourceType===\'补充需求\'?\'补充需求 · 无附件原编号\':`附件原文 · 第 ${p.page} 页`}</summary><p>{p.source}</p>{p.sourceType!==\'补充需求\'&&<Button size="small" onClick={()=>{setSourcePage(p.page-1);setDrawer(\'source\')}}>打开原页</Button>}')
s=s.replace("{title:'供电类别',dataIndex:'powerZone',width:100}", "{title:'供电类别',dataIndex:'powerZone',width:100},{title:'需求状态',dataIndex:'requirement',width:100}")
s=s.replace('<marker id="arrow"', '<marker id="power-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#cf4b49"/></marker><marker id="arrow"')
needle='     {labels&&markers.map('
insert='''     {raw.connections.filter(c=>c.kind===kind&&points.some(p=>p.id===c.to)).map(c=><g key={c.id} data-interactive="connection" role="button" tabIndex={0} aria-label={c.label} onClick={()=>{const p=points.find(p=>p.id===c.to);if(p)pick(p)}} onKeyDown={e=>{if(e.key==='Enter'){const p=points.find(p=>p.id===c.to);if(p)pick(p)}} className="power-connection"><title>{c.note}</title><path d={c.path.map(([x,y],i)=>`${i?'L':'M'}${x} ${y}`).join(' ')} fill="none" stroke="#cf4b49" strokeWidth="2" strokeDasharray="5 3" markerEnd="url(#power-arrow)"/><text x="805" y="675" fontSize="9" fill="#bb4846"><tspan x="805">岛台 → 餐边柜</tspan><tspan x="805" dy="13">D01取电 · 不计新增</tspan><tspan x="805" dy="12" fontSize="8">仅示意连接关系</tspan></text></g>)}
'''
s=s.replace(needle,insert+needle)
s=s.replace('     <rect x="630" y="572"', '     <text x="833" y="870" className="small-map-text" textAnchor="middle" transform="rotate(-90 833 870)">衣柜</text>\n     <rect x="630" y="572"')
s=s.replace('<h3 className="drawer-heading">空间与设备修订</h3>', '''<h3 className="drawer-heading">配置调整</h3><ul className="review-notes">{raw.reviewNotes.map(t=><li key={t}>{t}</li>)}</ul><h3 className="drawer-heading">已取消的独立点位</h3><Table rowKey="id" size="small" scroll={{x:650}} dataSource={raw.excluded} pagination={{pageSize:7,showSizeChanger:false}} columns={[{title:'编号',dataIndex:'id',width:70},{title:'区域',dataIndex:'room',width:80},{title:'原点位',dataIndex:'name',width:150},{title:'取消说明',dataIndex:'reason'}]}/><h3 className="drawer-heading">空间与设备修订</h3>''')
s=s.replace('洗衣池、电动晾衣架、智能马桶、电热毛巾架及智能协议仍需确认；地暖与中央空调不在附件的完整设计范围内。', '洗衣池及智能协议仍需确认；两卫智能马桶和电热毛巾架、阳台电动晾衣架均已明确需要，安装尺寸待深化。玄关监控位置与灯光接法待补图；地暖与中央空调不在附件的完整设计范围内。')
s=s.replace('实心编号通过引线指向建议部位。', '实心编号通过引线指向建议部位，空心点表示已提出的供电需求区域。')
p.write_text(s)
p=Path('deliver.py');s=p.read_text().replace("'供电类别','接口说明'", "'供电类别','需求状态','接口说明'").replace("'powerZone','text'", "'powerZone','requirement','text'");p.write_text(s)
p=Path('src/style.css');p.write_text(p.read_text()+'\n.power-connection{cursor:pointer;outline:none}.power-connection:focus path,.power-connection:hover path{stroke-width:3}\n')
