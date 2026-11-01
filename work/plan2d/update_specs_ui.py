from pathlib import Path
p=Path('src/App.tsx');s=p.read_text()
s=s.replace('Table, Empty, Tooltip, Popover,', 'Table, Descriptions, Empty, Tooltip, Popover,')
insert='''function PointSpecs({p,index}:{p:Point,index:number}){
 const s=p.spec;
 return <section className="point-specs" aria-label="点位安装参数"><h4>安装参数</h4><Descriptions column={1} size="small" colon={false} styles={{label:{width:64,color:'#73817d',fontSize:12},content:{fontSize:12,lineHeight:1.7}} items={[
  {key:'quantity',label:'本处数量',children:<div><strong>{s.perMarker[index]}</strong><div className="spec-status">{s.quantityStatus}</div></div>},
  ...(p.anchors.length>1?[{key:'total',label:'本组合计',children:s.quantity}]:[]),
  {key:'height',label:'安装高度',children:<div><strong>{s.height}</strong><div className="spec-status">{s.heightStatus} · 非施工定值</div></div>},
  {key:'position',label:'安装位置',children:s.location}
 ]}/><details className="spec-basis"><summary>高度依据与测量口径</summary><p>{s.basis}</p><p>{s.measurement}</p></details>{s.counting&&<p className="spec-counting">核量说明：{s.counting}</p>}</section>
}
'''
s=s.replace('function App(){',insert+'function App(){')
s=s.replace('</Tag></div><h4>设计原因</h4>', '</Tag></div><PointSpecs p={p} index={i}/><h4>设计原因</h4>')
s=s.replace("关联编号 {p.related}：同一设备或面板，核量时合并。", "关联编号 {p.related}：{p.spec.counting||'接口及设备数量按安装参数核量。'}")
s=s.replace("'需求状态','接口说明'", "'需求状态','数量','数量状态','安装高度','高度状态','高度依据','测量口径','分处数量','核量说明','接口说明'")
s=s.replace('p.powerZone,p.requirement,p.text,', "p.powerZone,p.requirement,p.spec.quantity,p.spec.quantityStatus,p.spec.height,p.spec.heightStatus,p.spec.basis,p.spec.measurement,p.spec.perMarker.join('；'),p.spec.counting,p.text,")
s=s.replace("scroll={{x:1290}}", "scroll={{x:1750}}")
s=s.replace("{title:'需求状态',dataIndex:'requirement',width:100},{title:'设计原因'", "{title:'需求状态',dataIndex:'requirement',width:100},{title:'数量',width:200,render:(_:unknown,p:Point)=><div>{p.spec.quantity}<div className=\"spec-status\">{p.spec.quantityStatus}</div></div>},{title:'安装高度',width:240,render:(_:unknown,p:Point)=><div>{p.spec.height}<div className=\"spec-status\">{p.spec.heightStatus}</div></div>},{title:'设计原因'")
s=s.replace('同一设备的关联编号合并核量', '数量及关联编号按详情核量')
s=s.replace('关联项目不重复核量', '数量与高度见点位详情')
p.write_text(s)
p=Path('src/style.css');s=p.read_text();s+='\n.point-specs{padding:10px 12px;background:#f3f7f6;border:1px solid #dce8e3;border-radius:6px;margin:10px 0 14px}.point-popover-body .point-specs h4{margin:0 0 10px;color:#246b66;font-size:12px}.spec-status{font-size:10px;color:#8a7751;margin-top:3px}.point-specs strong{font-weight:600;color:#2e4940}.spec-basis{font-size:11px;color:#687d72;margin-top:10px}.spec-basis summary{cursor:pointer}.point-popover-body .spec-basis p{font-size:11px;margin-top:6px;color:#687d72}.point-popover-body .spec-counting{font-size:11px;color:#5f756a;line-height:1.7;border-top:1px solid #dce8e3;padding-top:8px;margin-top:10px}\n';p.write_text(s)
p=Path('deliver.py');s=p.read_text().replace('import json,base64,csv','import json,base64,csv\nfrom point_specs import validate')
s=s.replace("with (out/", "validate(d)\nwith (out/",1)
s=s.replace("'需求状态','接口说明'", "'需求状态','数量','数量状态','安装高度','高度状态','高度依据','测量口径','分处数量','核量说明','接口说明'")
s=s.replace("  row.append('；'.join", "  spec=p['spec']\n  row[6:6]=[spec[k] for k in ['quantity','quantityStatus','height','heightStatus','basis','measurement']]+['；'.join(spec['perMarker']),spec['counting']]\n  row.append('；'.join")
p.write_text(s)
p=Path('package.json');import json;d=json.loads(p.read_text());d['scripts']['check']='python3 point_specs.py && tsc --noEmit';d['scripts']['build']='python3 point_specs.py && node build.mjs';p.write_text(json.dumps(d,indent=2)+'\n')
