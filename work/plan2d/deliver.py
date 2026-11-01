from pathlib import Path
import json,base64,csv
from point_specs import validate
root=Path(__file__).parent
out=root.parent.parent/'outputs'
js=(root/'dist/app.js').read_text()
for f in (root/'dist/assets').glob('*.png'):
 js=js.replace('assets/'+f.name,'data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode())
css=(root/'dist/app.css').read_text()
html=(root/'dist/index.html').read_text().replace('<link rel="stylesheet" href="app.css">','<style>'+css+'</style>').replace('<script src="app.js"></script>','<script>'+js.replace('</script','<\\/script')+'</script>')
(out/'碧瑶花园-水电点位图-2D.html').write_text(html)
d=json.loads((root/'src/data.json').read_text())
validate(d)
with (out/'碧瑶花园-水电点位图-点位清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['编号','区域','图层','点位','供电类别','需求状态','数量','数量状态','安装高度','高度状态','高度依据','测量口径','分处数量','核量说明','接口说明','设计原因','建议安装部位','定位状态','待核对条件','需求位置说明','状态','附件原文','修订记录','原附件页码'])
 for p in d['points']:
  row=[p.get(k,'') for k in ['id','room','kind','name','powerZone','requirement','text','designReason','placement','positionStatus','positionCheck']]
  spec=p['spec']
  row[6:6]=[spec[k] for k in ['quantity','quantityStatus','height','heightStatus','basis','measurement']]+['；'.join(spec['perMarker']),spec['counting']]
  row.append('；'.join(s['label']+'：'+s['reason'] for s in p.get('requestedSites',[])))
  row.extend(p.get(k,'') for k in ['status','source','reason','page'])
  w.writerow(row)
print('Self-contained HTML:',len(html.encode()),'bytes; CSV:',len(d['points']),'point groups.')
