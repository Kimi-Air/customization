from pathlib import Path
import json,csv,base64,re
root=Path(__file__).parent
out=root.parent.parent/'outputs';out.mkdir(exist_ok=True)
def uri(path,mime):return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
html=(root/'dist/index.html').read_text();css=(root/'dist/style.css').read_text();icons=(root/'dist/assets/icons/style.css').read_text();js=(root/'dist/app.js').read_text()
icons=re.sub(r'src:\s*.*?;',lambda _: 'src:url("'+uri(root/'dist/assets/icons/Phosphor.woff2','font/woff2')+'") format("woff2");',icons,count=1,flags=re.S)
html=html.replace('<link rel="stylesheet" href="assets/icons/style.css">','<style>'+icons+'</style>').replace('<link rel="stylesheet" href="style.css">','<style>'+css+'</style>')
for name in ['island-outlet.png','oak-floor.png']:
 u=uri(root/'dist/assets'/name,'image/png');html=html.replace('assets/'+name,u);js=js.replace('assets/'+name,u)
html=html.replace('<script src="app.js"></script>','<script>'+js.replace('</script','<\\/script')+'</script>')
(out/'碧瑶花园-水电三维方案.html').write_text(html)
d=json.loads((root/'src-data.json').read_text());rooms={r[0]:r[1] for r in d['rooms']}
for dest in [out/'碧瑶花园-分区点位清单.csv',root/'dist/点位清单.csv']:
 with dest.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(['编号','区域','类别','功能','数量','建议高度mm','回路','状态','安装说明'])
  for p in d['points']: w.writerow([p['id'],rooms[p['r']],p['t'],p['name'],p['n'],p['h'],p['loop'],p['status'],p['note']])
print('Saved offline HTML and 102 point groups.')
