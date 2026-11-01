import json,re,ast
from pathlib import Path
from PIL import Image
r=Path(__file__).parent
d=json.loads((r/'data.json').read_text());t=(r/'template.html').read_text()
furn=ast.literal_eval(re.search(r'const furn=(\[.*?\]);',t,re.S).group(1));walls=ast.literal_eval(re.search(r'const walls=(\[.*?\]);',t,re.S).group(1))
d['furniture']=furn;d['walls']=walls
for n in ['028','046','054']:
 im=Image.open(f'work/video/frame-{n}.jpg');im=im.crop((0,135 if n=='028' else 240,592,1165 if n=='028' else 1040));im.save(r/f'dist/assets/video-{n}.jpg')
(r/'src-data.json').write_text(json.dumps(d,ensure_ascii=False))
