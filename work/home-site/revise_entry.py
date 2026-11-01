import json
from pathlib import Path
r=Path('.');p=r/'src-data.json';d=json.loads(p.read_text())
d['walls']=[([625,740,165,8] if a==[570,740,220,8] else a) for a in d['walls']]
d['points']=[a for a in d['points'] if a['id']!='D05']
for a in d['points']:
 if a['id']=='E04':a.update(name='进门左手灯光控制面板',x=550,y=722,note='用户确认位置：从图纸下方向上进门，左手侧。建议分控玄关灯、餐灯及公共照明；最终按灯光回路表确认。离家场景不切断冰箱与网络。')
 if a['id']=='E09':a.update(x=565,y=702,note='可选；入户门上方或附近，朝室内入口。实际镜头视角及供电方式待确认。')
 if a['id']=='D01':a.update(x=665,y=731)
 if a['id']=='D02':a.update(x=778,y=640)
 if a['id']=='D03':a.update(x=706,y=617,note='四座餐桌＋缩小岛台上方，结合最终家具中心与灯型放样。')
d['rooms'][0][2]='入户门在餐边柜靠厨房端，朝图纸下方外开；从下方向上进门，灯光控制面板在左手。玄关柜仍在沙发背景墙侧。'
d['rooms'][2][2]='四座餐桌连接缩小岛台，两侧各两椅；岛台仅做电源。餐边柜与电视墙同侧，并避让入户门洞。'
p.write_text(json.dumps(d,ensure_ascii=False))
p=r/'app-src.js';s=p.read_text()
s=s.replace("['D',625,587,125,68,45,'#514a3d'],['D',750,580,65,82,55,'#bca990'],['D',575,716,200,30,55,'#b19a6d']","['D',645,595,100,56,45,'#514a3d'],['D',745,591,45,64,55,'#bca990'],['D',640,716,135,30,55,'#b19a6d']")
s=s.replace("r==='D'&&x===750","r==='D'&&x===745")
s=s.replace('[635,680,725].forEach(x=>[559,658]','[655,705].forEach(x=>[565,659]')
s=s.replace('[635,680,725,770].forEach(x=>','[667,705,743].forEach(x=>')
s=s.replace("box(580,736,190,3,1.8,'#baa991');box(590,710,170,25,.6,'#6a6859',1.45);for(let i=0;i<7;i++){box(592+i*24,708,1,1,.6,'#c9bc9d',1.45);", "box(640,736,135,3,1.8,'#baa991');box(650,710,115,25,.6,'#6a6859',1.45);for(let i=0;i<7;i++){if(i<5)box(652+i*24,708,1,1,.6,'#c9bc9d',1.45);")
s=s.replace("{id:'E',poly:[[790,740]", "{id:'E',poly:[[550,710],[625,710],[625,765],[550,765]]},{id:'E',poly:[[790,740]")
# Door frame and closed ghost leaf; arrow specifies outswing without guessing hinge side.
s=s.replace("//NO_SUCH_MARKER",'')
anchor="[[550,525,550,700]"
door="""box(555,737,4,10,2.2,'#604e3d');box(621,737,4,10,2.2,'#604e3d');box(555,737,70,10,.09,'#604e3d',2.2);const doorLeaf=box(559,741,62,3,2.13,'#947858');doorLeaf.material.transparent=true;doorLeaf.material.opacity=.35;const outward=new THREE.ArrowHelper(new THREE.Vector3(0,0,1),v(590,750,.05),.9,0xb45e36,.2,.12);scene.add(outward);box(546,717,3,9,.2,'#243c34',1.1);"""
s=s.replace(anchor,door+anchor)
s=s.replace("const roomLabels=DATA.rooms.map(r=>", "const entryLabel=document.createElement('span');entryLabel.className='pointlabel roomlabel';entryLabel.textContent='入户大门 · 外开 ↓';$('overlay').append(entryLabel);const roomLabels=[{el:entryLabel,pos:v(590,765,.15)},...DATA.rooms.map(r=>")
s=s.replace("return {el,pos:v(x+w*.5,y+h*.73,.06)}});$('load')", "return {el,pos:v(x+w*.5,y+h*.73,.06)}})];$('load')")
s=s.replace("if(r==='E'){x=570;y=420;w=300;h=140}","if(r==='E'){x=530;y=425;w=340;h=380}")
s=s.replace("out+='<path d=\"M550 525", "out+='<path d=\"M559 742H621\" stroke=\"#9c704a\" stroke-width=\"5\"/><path d=\"M555 735V752 M625 735V752 M590 754V791 M584 782L590 791L596 782\" fill=\"none\" stroke=\"#af603c\" stroke-width=\"2.5\"/><text x=\"590\" y=\"806\" text-anchor=\"middle\" font-size=\"10\" fill=\"#af603c\">入户大门 · 外开↓</text><rect x=\"545\" y=\"715\" width=\"7\" height=\"12\" fill=\"#896b9d\"/><path d=\"M550 525")
s=s.replace("['餐桌',678,628],['岛台·仅电',780,675]","['四座餐桌',695,628],['岛台·仅电',768,674]")
# draw all four chairs in plan too
s=s.replace("[['老人房',455,465]", "[655,705].forEach(x=>[565,659].forEach(y=>out+=`<rect x=\"${x}\" y=\"${y}\" width=\"23\" height=\"23\" rx=\"4\" fill=\"#a3947d\" stroke=\"#6f7567\"/>`));[['老人房',455,465]")
s=s.replace('回家先开公共照明，随身物品放在玄关柜；','从下方向上进门，先用左手边灯光面板开公共照明，随身物品放在玄关柜；')
s=s.replace('玄关柜在沙发背景墙侧，不等于迁移建筑入户门。弱电箱能否随柜体调整须现场确认，不能把柜位当作已获准迁箱。','入户门位置按用户截图，向图纸下方外开；左右合页尚未确认，暂以闭合门扇＋外开箭头表达。门洞尺寸和门外公共通道净空须现场复核。')
s=s.replace('餐桌与岛台是一组家具','四座餐桌与小一号岛台')
s=s.replace('吃饭时桌面有重点照明；','两侧各两座，餐桌与岛台整体缩小，给入口留出空间。吃饭时桌面有重点照明；')
p.write_text(s)
p=r/'dist/index.html';s=p.read_text().replace('餐桌连岛台 · 岛台只供电','四座餐桌＋缩小岛台 · 岛台只供电').replace('玄关柜在沙发背景墙侧<br>','入户门外开↓ · 进门左手灯控<br>玄关柜在沙发背景墙侧<br>').replace('玄关柜的位置已确认，但不据视频改变建筑入户门。','入户门按用户截图补回，朝图纸下方外开，进门左手为灯光面板；合页侧及门洞实测尺寸待确认。');p.write_text(s)
