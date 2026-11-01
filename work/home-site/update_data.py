import json
from pathlib import Path
from PIL import Image
r=Path(__file__).parent;d=json.loads((r/'src-data.json').read_text())
p=d['points'];by={x['id']:x for x in p}
# move vestibule cabinet to sofa-background side, without relocating structural entrance
for key,x,y in [('E01',615,498),('E02',650,498),('E03',680,498),('E04',699,505),('E09',700,490)]:by[key].update(x=x,y=y)
by['E04']['name']='玄关回家 / 离家面板';by['E09']['note']='可选；镜头与实际入户门关系现场核对；不因玄关柜调整而自行移动入户门'
by['D02'].update(name='岛台侧面插座',x=796,y=642,h='岛台侧面按台高',n=2,note='已确认仅用电、不做水槽或水路；电源路径需在铺地暖前协调，严禁后钻破坏地暖管')
by['D03'].update(x=707,y=620,note='餐桌与岛台组合上方吊灯；最终按家具中心及吊顶风口协调')
by['M06'].update(name='右床头吊灯',x=1104,y=285,n=1,h='灯底按床头台与眩光复核',note='来自视频14–15秒效果图；吊灯独立控制，不直照枕头')
p.append(dict(id='M13',r='M',t='照明',name='左床头阅读灯电源',x=956,y=285,h='床头延伸台面上方',n=1,loop='L-B',note='左侧局部灯建议；结合视频衣柜与床头延伸台，避免插座被柜板挡住',status='建议'))
d['rooms'][0][1]='玄关柜 / 过道';d['rooms'][0][2]='玄关柜位于餐桌靠沙发背景墙的一侧；实际入户门及公共电梯间按原平面保留，不据效果图迁移。'
d['rooms'][2][2]='餐桌连接岛台；岛台仅做电源。餐边柜与电视墙同侧。'
d['rooms'][4][2]='视频14–15秒：左侧通顶衣柜，居中床与背景，右侧飘窗及床头吊灯。'
# floor footprint closer to traced original, bay windows included
poly={'B':[[350,315],[585,315],[585,505],[350,505],[350,468],[286,450],[286,355],[350,338]],'M':[[865,255],[1145,255],[1145,287],[1205,304],[1205,433],[1145,452],[1145,490],[865,490]],'S':[[805,755],[1145,755],[1145,791],[1170,805],[1170,914],[1145,925],[1145,970],[805,970]]}
d['polygons']=poly
Image.open('work/video/detail-14.jpg').crop((0,470,592,831)).save(r/'dist/assets/video-master.jpg')
(r/'src-data.json').write_text(json.dumps(d,ensure_ascii=False))
