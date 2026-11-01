from pathlib import Path
p=Path('app-src.js');s=p.read_text()
s=s.replace("let step=0,selected=null","let step=1,selected='D02'")
s=s.replace("'#e9ebe4'","'#faf9f6'").replace("'#e9ebe3'","'#eeede7'").replace("'#c5b89e'","'#d8cdb9'").replace("'#e7e2d5'","'#eeebe2'").replace("'#9caa9a'","'#b7b6ae'")
s=s.replace("camera.position.set(8,15,14);controls.target.set(0,.2,0)","camera.position.set(1.2,21,14);controls.target.set(-.2,.1,0)")
s=s.replace("stem.material.depthTest=false;stem.renderOrder=8","stem.material.depthTest=true;stem.material.opacity=.09;stem.renderOrder=8")
s=s.replace("new THREE.SphereGeometry(.085,14,10)","new THREE.SphereGeometry(.065,16,12)")
s=s.replace("const on=(modelRoom==='all'","const on=(modelRoom==='all'")
s=s.replace("m.mesh.scale.setScalar(m.p.id===selected?1.65:1)","m.mesh.scale.setScalar(m.p.id===selected?2:1)")
repls={
'入户门位置按用户截图，向图纸下方外开；左右合页尚未确认，暂以闭合门扇＋外开箭头表达。':'入户门向图纸下方外开；合页侧待现场确认。',
'四座餐桌与小一号岛台':'四人用餐，岛台供电',
'两侧各两座，餐桌与岛台整体缩小，给入口留出空间。':'餐桌两侧各两座，连接紧凑岛台，保留入户通行空间。',
'视频确认餐边柜与电视墙同侧、玄关柜与沙发背景墙同侧。':'餐边柜与电视墙同侧，玄关柜与沙发背景墙同侧。',
'14–15秒的主卧布局':'休息、阅读与夜间照明',
'视频没有床宽、柜高和吊灯底标高。':'床宽、柜高和吊灯底标高需结合实物定位。',
'主卧桌位继续参考原平面待深化':'主卧桌位尺寸待木作深化',
'老人住左上次卧':'顺手控制，安稳起夜',
'本房未在视频中展示，沿原平面和已确认用途设计。':'开关需同时满足门口与床边控制。',
'本区依据原平面，不从主卧效果图推断结构。':'保留现有排污关系。',
'不照搬原图固定床':'确保展开后仍可通行',
'① 先想象怎么使用':'使用方式','② 再安排水电接口':'接口安排','③ 定位前一起核对':'安装核对',
'碧瑶花园-V2详细点位.csv':'碧瑶花园-详细点位.csv'
}
for a,b in repls.items(): s=s.replace(a,b)
a=s.index('function showInspector()');b=s.index('function refreshMarkers()',a)
s=s[:a]+'''function showInspector(){const p=selectedData();if(!p)return;const ids=DATA.points.filter(q=>(modelRoom==='all'||q.r===modelRoom)&&(modelType==='all'||q.t===modelType)),idx=ids.indexOf(p);$('pointPosition').textContent=`${String(Math.max(0,idx)+1).padStart(2,'0')} / ${ids.length}`;$('inspector').innerHTML=`<div class="pid">${p.id}</div><h3>${p.name}</h3><dl class="detail-rows"><div><dt>区域</dt><dd>${roomName(p.r)} · ${p.t}</dd></div><div><dt>数量</dt><dd>${p.n}</dd></div><div><dt>安装位置</dt><dd>${p.h}</dd></div><div class="detail-note"><dt>说明</dt><dd>${p.id==='D02'?'岛台仅供电，不设给排水。':p.note}</dd></div></dl><details class="technical"><summary>回路与安装条件</summary><p>${p.loop} · ${p.status} · 标高为建议值</p><p>${p.note}</p></details>`;$('detailImage').hidden=p.id!=='D02';$('toGuide').querySelector('span').textContent=`查看${roomName(p.r).replace('柜 / 过道','').replace('右侧','')}平面`;}
''' +s[b:]
a=s.index('function setStep(');b=s.index('function renderGuide()',a)
s=s[:a]+'''function setStep(i){step=Math.max(0,Math.min(9,i));selected=DATA.points.find(p=>p.r===guideRoom())?.id;$('search').value='';guideType='all';$('guideType').value='all';renderGuide();showInspector();refreshMarkers();}
''' +s[b:]
s=s.replace("${roomName(r)}</button>","${shortRoom(r)}</button>")
s=s.replace("const guideRoom=()=>order[step];","const shortRoom=id=>({E:'玄关',A:'阳台',T:'左卫',U:'右卫'})[id]||roomName(id);const guideRoom=()=>order[step];")
s=s.replace("<div class=\"number\">STEP ${String(step+1).padStart(2,'0')} / 10</div>","<div class=\"number\">${String(step+1).padStart(2,'0')} / 10 · ${roomName(id)}</div>")
a=s.index('function renderCards()');b=s.index('function drawMap()',a)
s=s[:a]+'''function renderCards(){const ps=filteredGuide();$('listTitle').textContent=`${roomName(guideRoom())} · ${ps.length} 组点位`;$('pointCards').innerHTML=ps.length?ps.map(p=>`<button class="pointcard ${p.id===selected?'active':''}" data-card="${p.id}" aria-label="${p.id} ${p.name}" aria-pressed="${p.id===selected}"><div class="code" style="color:${COLORS[p.t]}">${p.id}<span class="category">${p.t}</span></div><div><h4>${p.name}</h4><p>${p.note}</p></div><div>${p.h}<div class="pointmeta">数量 ${p.n} · ${p.status}</div></div><div>${p.loop}</div></button>`).join(''):'<p class="empty">没有匹配点位，请更换类别或搜索词。</p>';document.querySelectorAll('[data-card]').forEach(b=>b.onclick=()=>selectPoint(b.dataset.card))}
''' +s[b:]
s=s.replace("${t==='all'?'全部点位':t}</button>","${t==='all'?'全部':`<span class=\"dot\" style=\"--point:${COLORS[t]}\"></span>${t}`}</button>")
s=s.replace("modelRoom=e.target.value;selected=null;focusRoom(modelRoom);refreshMarkers();showInspector()","modelRoom=e.target.value;selected=(DATA.points.find(p=>(modelRoom==='all'||p.r===modelRoom)&&(modelType==='all'||p.t===modelType))||DATA.points.find(p=>modelRoom==='all'||p.r===modelRoom)).id;focusRoom(modelRoom);refreshMarkers();showInspector()")
s=s.replace("a.classList.toggle('active',a===b));refreshMarkers()","a.classList.toggle('active',a===b));const match=DATA.points.find(p=>(modelRoom==='all'||p.r===modelRoom)&&(modelType==='all'||p.t===modelType));if(match)selected=match.id;refreshMarkers();showInspector()")
s=s.replace("$('modelRoom').value='all';resetCamera();refreshMarkers()","$('modelRoom').value='all';resetCamera();refreshMarkers();showInspector()")
s=s.replace("step=order.indexOf(id);renderGuide();","step=order.indexOf(id);$('search').value='';guideType='all';$('guideType').value='all';renderGuide();")
s=s.replace("a.click();setTimeout", "a.click();$('toast').textContent='全屋点位清单已导出';$('toast').classList.add('show');setTimeout(()=>$('toast').classList.remove('show'),2500);setTimeout")
s += '''
function movePoint(delta){const ps=DATA.points.filter(p=>(modelRoom==='all'||p.r===modelRoom)&&(modelType==='all'||p.t===modelType));if(!ps.length)return;const at=ps.findIndex(p=>p.id===selected);selectPoint(ps[(at+delta+ps.length)%ps.length].id)}
$('pointPrev').onclick=()=>movePoint(-1);$('pointNext').onclick=()=>movePoint(1);
const sections=document.querySelectorAll('main>section');new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting)document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+e.target.id))})},{rootMargin:'-80px 0px -55% 0px'}).observe($('guide'));
document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>document.querySelectorAll('nav a').forEach(n=>n.classList.toggle('active',n===a))));
'''
p.write_text(s)
