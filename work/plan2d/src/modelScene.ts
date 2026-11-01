import * as T from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {CSS2DRenderer,CSS2DObject} from 'three/addons/renderers/CSS2DRenderer.js';
import {SCALE as S,sites,rooms,colors,Site} from './modelData';
export type View='orbit'|'top'|'north'|'south'|'west'|'east';
export type Options={room:string;kind:string;query:string;cut:number;xray:boolean;labels:boolean;selected:string;view:View};
const world=(x:number,z:number,h=0)=>new T.Vector3((x-790)*S,h,(z-600)*S);
export function createModel(host:HTMLElement,onPick:(s:Site)=>void,onError:(s:string)=>void){
 const scene=new T.Scene();scene.background=new T.Color('#edf1ef');
 const renderer=new T.WebGLRenderer({antialias:true,alpha:false});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.localClippingEnabled=true;renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.35;host.appendChild(renderer.domElement);
 renderer.domElement.setAttribute('aria-label','可旋转的房屋三维模型');renderer.domElement.style.touchAction='none';
 const labels=new CSS2DRenderer();labels.domElement.className='model-label-layer';host.appendChild(labels.domElement);
 const camera=new T.OrthographicCamera(-5,5,4,-4,.05,200);camera.position.set(5,9,12);
 const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.minZoom=.25;controls.maxZoom=9;controls.maxPolarAngle=Math.PI*.495;
 scene.add(new T.HemisphereLight('#ffffff','#8d9d94',2.7));const sun=new T.DirectionalLight('#fff1dc',3);sun.position.set(-6,12,7);scene.add(sun);const fill=new T.DirectionalLight('#dce7ff',1.3);fill.position.set(5,8,-8);scene.add(fill);
 const parts:T.Object3D[]=[];const clip=new T.Plane(new T.Vector3(0,-1,0),.95);const section=new T.Plane(new T.Vector3(0,0,1),1000);let options:Options={room:'厨房',kind:'强电',query:'',cut:.95,xray:false,labels:true,selected:'',view:'orbit'};
 const mats:T.Material[]=[];
 function material(c:string,role:string){const m=new T.MeshStandardMaterial({color:c,roughness:.72,metalness:c==='#788987'?.45:0,side:T.DoubleSide});m.clippingPlanes=role==='wall'?[clip,section]:[section];mats.push(m);return m}
 function register(o:T.Object3D,room:string,role:string){o.userData={room,role};scene.add(o);parts.push(o);return o}
 function box(r:string,x:number,z:number,w:number,d:number,h:number,b=0,c='#e7dfd0',role='furniture'){
  const m=new T.Mesh(new T.BoxGeometry(w*S,h,d*S),material(c,role));m.position.copy(world(x+w/2,z+d/2,b+h/2));register(m,r,role);
  const edge=new T.LineSegments(new T.EdgesGeometry(m.geometry,25),new T.LineBasicMaterial({color:role==='wall'?'#94a09b':'#9d9e94',transparent:true,opacity:.32}));edge.position.copy(m.position);(edge.material as T.LineBasicMaterial).clippingPlanes=role==='wall'?[clip,section]:[section];register(edge,r,role+'-edge');return m;
 }
 function poly(r:string,coords:number[][],h:number,b:number,c:string,role='furniture'){
  const sh=new T.Shape();coords.forEach(([x,z],i)=>{const p=world(x,z);i?sh.lineTo(p.x,-p.z):sh.moveTo(p.x,-p.z)});sh.closePath();const g=new T.ExtrudeGeometry(sh,{depth:h,bevelEnabled:false});g.rotateX(-Math.PI/2);const m=new T.Mesh(g,material(c,role));m.position.y=b;register(m,r,role);return m;
 }
 function rod(r:string,coords:number[][],c='#7b8986',radius=.014,role='furniture'){
  const curve=new T.CatmullRomCurve3(coords.map(([x,z,y])=>world(x,z,y)));return register(new T.Mesh(new T.TubeGeometry(curve,24,radius,8,false),material(c,role)),r,role);
 }
 function cylinder(r:string,x:number,z:number,rad:number,h:number,b:number,c:string,role='furniture'){
  const m=new T.Mesh(new T.CylinderGeometry(rad*S,rad*S,h,40),material(c,role));m.position.copy(world(x,z,b+h/2));register(m,r,role);return m;
 }
 const floorPolys:Record<string,number[][]>={
 '厨房':[[329,514],[555,514],[555,754],[329,754]],'餐厅':[[555,519],[811,519],[811,738],[555,738]],'玄关':[[555,738],[811,738],[811,752],[555,752]],'客厅':[[811,500],[1116,500],[1116,745],[811,745]],'阳台':[[1116,500],[1239,500],[1239,745],[1116,745]],'过道':[[585,425],[853,425],[853,519],[585,519]],
 '老人房':[[350,315],[585,315],[585,505],[350,505],[350,468],[286,450],[286,355],[350,338]],'主卧':[[855,255],[1145,255],[1145,287],[1205,304],[1205,433],[1145,452],[1145,490],[855,490]],'书房':[[805,753],[1145,753],[1145,791],[1170,805],[1170,914],[1145,925],[1145,970],[805,970]],'公卫':[[590,315],[734,315],[734,425],[590,425]],'主卫':[[734,255],[855,255],[855,425],[734,425]]};
 Object.entries(floorPolys).forEach(([r,p])=>poly(r,p,.1,-.1,['厨房','公卫','主卫','阳台'].includes(r)?'#d5d9d4':'#e2d7c3','floor'));
 poly('公共电梯间',[[424,755],[805,755],[805,885],[424,885]],.08,-.1,'#d0d7d3','floor');
 const walls:[string,number,number,number,number][]=[
 ['老人房',350,306,235,10],['老人房',350,316,9,28],['老人房',350,468,9,34],['老人房',351,502,183,12],['老人房',578,316,12,112],
 ['公卫',590,306,144,10],['公卫',585,315,10,109],['公卫',595,419,60,9],['公卫',710,419,24,9],['公卫',727,315,8,104],
 ['主卫',734,246,121,10],['主卫',734,255,8,164],['主卫',742,419,29,9],['主卫',826,419,29,9],['主卫',848,255,8,164],
 ['主卧',855,246,290,10],['主卧',855,255,9,171],['主卧',902,484,243,14],['主卧',1138,255,10,32],['主卧',1138,452,10,32],
 ['客厅',855,490,260,10],['客厅',1110,498,9,54],['客厅',871,738,244,14],
 ['厨房',329,508,226,11],['厨房',329,519,7,37],['厨房',329,710,7,45],['厨房',409,519,15.36,29],['厨房',409,667,15.36,88],['厨房',424,708,131,12],
 ['玄关',632,741,179,12],['玄关',550,720,12,33],['厨房',329,755,95,8],
 ['阳台',1116,491,130,11],['阳台',1239,502,9,28],['阳台',1239,719,9,33],['阳台',1116,742,130,11],
 ['书房',805,798,9,172],['书房',805,964,340,12],['书房',875,748,270,9],['书房',1138,756,10,36],['书房',1138,925,10,39]
 ];
 walls.forEach(([r,x,z,w,d])=>box(r,x,z,w,d,r==='厨房'?2.4:2.7,0,'#eeeae2','wall'));
 // Door lintels preserve openings. Kitchen sliding-door opening intentionally has no door or rail.
 [['玄关',562,741,70,12],['书房',805,748,70,9],['老人房',578,428,12,74],['主卧',855,426,9,58]].forEach(([r,x,z,w,d])=>box(String(r),Number(x),Number(z),Number(w),Number(d),.5,2.2,'#e5e2db','wall'));
 box('玄关',563,751,4,66,2.15,0,'#a58d6b','door');
 function windowLine(r:string,x1:number,z1:number,x2:number,z2:number,sill=.9,top=2.25){
  const a=world(x1,z1),b=world(x2,z2);const len=a.distanceTo(b);const m=new T.Mesh(new T.BoxGeometry(len,top-sill,.025),new T.MeshStandardMaterial({color:'#c3dbe0',transparent:true,opacity:.2,side:T.DoubleSide,depthWrite:false}));m.position.copy(a.clone().lerp(b,.5));m.position.y=(sill+top)/2;m.rotation.y=-Math.atan2(b.z-a.z,b.x-a.x);register(m,r,'glass');
  [sill,top].forEach(h=>rod(r,[[x1,z1,h],[x2,z2,h]],'#7e918b',.025,'frame'));
  [0,.5,1].forEach(t=>rod(r,[[x1+(x2-x1)*t,z1+(z2-z1)*t,sill],[x1+(x2-x1)*t,z1+(z2-z1)*t,top]],'#7e918b',.024,'frame'));
 }
 windowLine('厨房',333,556,333,710,1.05,2.1);windowLine('阳台',1240,530,1240,719,.25,2.55);
 [['老人房',[[350,338],[286,355],[286,450],[350,468]]],['主卧',[[1145,287],[1205,304],[1205,433],[1145,452]]],['书房',[[1145,791],[1170,805],[1170,914],[1145,925]]]].forEach(([r,ps])=>{const p=ps as number[][];for(let i=0;i<p.length-1;i++)windowLine(r as string,...p[i] as [number,number],...p[i+1] as [number,number]);});
 function cabinet(r:string,x:number,z:number,w:number,d:number,h=.9,front='south',base=.1,top=true){
  const body=h-base-.02;const thickness=1.15;box(r,x,z,w,d,.06,base,'#b8b5a9','cabinet');
  box(r,x,z,thickness,d,body,base,'#e9e5dc','cabinet');box(r,x+w-thickness,z,thickness,d,body,base,'#e9e5dc','cabinet');
  if(front==='east'){box(r,x,z,w,thickness,body,base,'#eee9e1','cabinet');box(r,x,z+d-thickness,w,thickness,body,base,'#eee9e1','cabinet');box(r,x+w-1,z+1,1,d-2,body-.01,base,'#e9e4d9','cabinet');}
  else box(r,x+1,front==='north'?z:z+d-1,w-2,1,body-.01,base,'#e9e4d9','cabinet');
  if(top)box(r,x-.5,z-.5,w+1,d+1,.02,h-.02,'#f2eee4','counter');else box(r,x,z,w,d,.018,h-.018,'#e9e5dc','cabinet');
 }
 // V9 kitchen B wall: 1150 corner + 240 pier + 1970 primary run.
 const kx=335,kz=519,px=(mm:number)=>mm*.064;
 cabinet('厨房',kx,kz,px(1150),px(650),.9);
 const start=kx+px(1410);cabinet('厨房',start,kz,px(600),px(650),.9);cabinet('厨房',start+px(600),kz,px(420),px(650),.9);
 // Oven front and adjacent drawer fronts.
 box('厨房',start+.2,kz+px(650)-4,px(595),5,.455,.395,'#353d3c','appliance');box('厨房',start+2,kz+px(650)+1.2,px(530),.8,.29,.46,'#172526','appliance');box('厨房',start+5,kz+px(650)+2,px(440),.9,.018,.81,'#a4aaa5','appliance');
 [ .36,.62 ].forEach(h=>box('厨房',start+px(600)+1,kz+px(650)+.1,px(420)-2,.4,.008,h,'#8d8f83','cabinet'));
 box('厨房',start,kz+.4,px(1020),1,.6,.9,'#cbb797','cabinet');cabinet('厨房',start,kz,px(1020),px(350),2.4,'south',1.5,false);
 cylinder('厨房',start+px(300),kz+px(390),10,.27,.9,'#eeeae0','appliance');box('厨房',start+10,kz+px(390)-5,18,10,.018,1.17,'#b8b9ad','appliance');
 const fx=kx+px(2430);box('厨房',fx,kz,px(18),px(650),2.4,0,'#ede9df','cabinet');box('厨房',fx+px(868),kz,px(18),px(650),2.4,0,'#ede9df','cabinet');
 box('厨房',fx+px(28),kz+px(56),px(830),px(594),1.925,0,'#7c8780','appliance');
 box('厨房',fx+px(443),kz+px(650)+.1,.4,.5,1.925,0,'#39453f','appliance');box('厨房',fx+px(28),kz+px(650)+.1,px(830),.5,.008,.85,'#39453f','appliance');cabinet('厨房',fx,kz,px(886),px(650),2.4,'south',1.993,false);
 // A window wall: T20 at upper end, separate sink, prep, tapered shallow storage. Wall remains straight.
 cabinet('厨房',335,560.6,px(650),38.4,.9,'east');cabinet('厨房',335,599,px(650),51.2,.9,'east');cabinet('厨房',335,650.2,px(650),25.8,.9,'east');
 box('厨房',340,564,31,32,.012,.903,'#687c7b','appliance');box('厨房',340,564,31,32,.64,.26,'#98a4a0','appliance');
 box('厨房',342,608,27,34,.025,.902,'#7e9593','appliance');box('厨房',345,611,21,28,.025,.925,'#3b5959','appliance');rod('厨房',[[339,624,.91],[339,624,1.21],[350,624,1.21],[350,624,1.1]],'#7e9390',.018,'appliance');
 cylinder('厨房',346,638,4,.35,.14,'#e8eee9','appliance');cylinder('厨房',356,638,4,.35,.14,'#e8eee9','appliance');
 poly('厨房',[[335,676],[376.6,676],[358,701],[358,752],[335,752]],.02,.88,'#f0ece2','counter');poly('厨房',[[335,677],[375,677],[357,701],[357,751],[335,751]],.78,.1,'#e8e2d6','cabinet');
 // C stove wall, read left-to-right when facing it (reverse plan x).
 const cx=424.6;cabinet('厨房',cx,669.6,px(1970),px(600),.85,'north');
 [cx+px(620),cx+px(1520)].forEach(x=>box('厨房',x,669.4,.35,.3,.7,.1,'#9c9d8e','cabinet'));
 const hob=cx+px(620);box('厨房',hob+4,676,px(780),24,.025,.852,'#263936','appliance');[hob+15,hob+41].forEach(x=>cylinder('厨房',x,688,5,.035,.88,'#111e1d','appliance'));
 cabinet('厨房',cx,685,px(1970),px(350),2.4,'north',1.58,false);box('厨房',hob,679,px(900),29,.1,1.5,'#46534d','appliance');
 // Heater on the perpendicular corner return.
 box('厨房',375,520,26,14,.6,1.5,'#eeeae1','appliance');box('厨房',382,534.2,10,.5,.11,1.6,'#364842','appliance');rod('厨房',[[388,526,2.1],[388,526,2.3],[380,519,2.3]],'#9ea7a0',.045,'appliance');
 [379,387,395].forEach(x=>rod('厨房',[[x,526,1.5],[x,526,1.25]],'#a5a18b',.012,'appliance'));
 // Rooms use the latest 2D furniture arrangement, not the deprecated 3D data.
 function bed(r:string,x:number,z:number,w:number,d:number){box(r,x,z,w,d,.22,.1,'#b9ab93');box(r,x+1,z+1,w-2,d-2,.22,.32,'#f6f2e9');box(r,x,z-3,w,4,.9,0,'#b4a68e');[.05,.53].forEach(a=>box(r,x+w*a,z+7,w*.4,20,.08,.54,'#fffaf0'))}
 bed('老人房',406,324,96,128);box('老人房',380,325,22,24,.55,0,'#c6b99f');box('老人房',506,325,22,24,.55,0,'#c6b99f');cabinet('老人房',545,321,33,134,2.4,'east',.08,false);
 bed('主卧',976,280,115.2,128);cabinet('主卧',863,265,34,158,2.4,'east',.08,false);[945,1102].forEach(x=>box('主卧',x,282,26,25,.58,0,'#c6b99f'));box('主卧',1100,451,34,28,.75,0,'#d4c8b5');
 box('书房',951,757,128,39,.035,.725,'#d8c9ab');[955,1072].forEach(x=>box('书房',x,760,2,32,.725,0,'#8a9b8d'));box('书房',994,810,34,30,.1,.45,'#9bac9d');box('书房',994,837,34,4,.45,.45,'#9bac9d');box('书房',955,903,96,49,.4,.1,'#b5c0ac');box('书房',955,946,96,6,.35,.5,'#a4b19b');cabinet('书房',814,810,32,130,2.4,'east',.08,false);
 // Sofa-bed unfolding footprint (not additional bed).
 const bedline=new T.LineLoop(new T.BufferGeometry().setFromPoints([[955,824],[1051,824],[1051,952],[955,952]].map(([x,z])=>world(x,z,.025))),new T.LineDashedMaterial({color:'#7c9785',dashSize:.08,gapSize:.06}));bedline.computeLineDistances();register(bedline,'书房','furniture');
 box('客厅',872,506,216,56,.4,.1,'#d4d2bd');box('客厅',872,506,216,9,.45,.5,'#b9bda8');[872,1080].forEach(x=>box('客厅',x,511,9,50,.5,.25,'#c1c6af'));box('客厅',874,571,207,132,.008,.005,'#a7b4a6');box('客厅',938,605,66,44,.06,.38,'#c6b893');cabinet('客厅',877,715,218,23,.4,'north',.05);box('客厅',941,735,110,2,1.05,.65,'#233d36');
 box('餐厅',637,595,100,55,.04,.73,'#b3a184');[640,729].forEach(x=>[599,644].forEach(z=>box('餐厅',x,z,3,3,.73,0,'#6a7e71')));box('餐厅',737,590,40,65,.9,0,'#ded8ca');[650,699].forEach(x=>[563,658].forEach(z=>{box('餐厅',x,z,23,23,.08,.43,'#b3bca8');box('餐厅',x,z+(z<600?0:20),23,3,.35,.5,'#9ba98e')}));cabinet('餐厅',642,712,150,26,.9,'north');
 for(const r of ['公卫','主卫']){const is=r==='公卫',bx=is?708:741,bz=is?349:376;cabinet(r,bx,bz,22,43,.83,'east',.3);box(r,bx,bz,22,43,.025,.83,'#fafbf5');const tx=is?612:754,tz=is?390:343;cylinder(r,tx,tz,10,.42,0,'#eef0e8');box(r,tx-11,tz-17,22,12,.7,0,'#eef0e8');box(r,is?592:805,is?318:258,is?62:43,is?45:65,.015,0,'#bbc8c2');}
 cabinet('阳台',1127,503,49,48,2.4,'south',.05,false);[.05,.96].forEach(h=>{box('阳台',1131,507,39,42,.85,h,'#e0e7df','appliance');const drum=new T.Mesh(new T.CylinderGeometry(.22,.22,.035,40),material('#546e69','appliance'));drum.rotation.x=Math.PI/2;drum.position.copy(world(1150.5,550,h+.44));register(drum,'阳台','appliance')});box('阳台',1190,505,37,40,.55,0,'#d6e0d5','appliance');cylinder('阳台',1208,549,10,.08,.03,'#81978a','appliance');box('阳台',1155,590,45,63,.055,2.62,'#aebdb2','appliance');
 const roomLabels=rooms.map(r=>{const element=document.createElement('span');element.className='room-3d-label';element.textContent=r.name;const label=new CSS2DObject(element);label.position.copy(world(r.label[0],r.label[1],.035));scene.add(label);return label});
 const marks=sites.map(s=>{
  const color=colors[s.p.kind];const g=new T.Group();g.position.copy(world(s.x,s.z,s.h));
  const face=new T.Mesh(new T.BoxGeometry(.086,.086,.015),new T.MeshBasicMaterial({color:s.provisional?'#fcf9e9':'#fffdf6',transparent:true,depthTest:false}));face.quaternion.setFromUnitVectors(new T.Vector3(0,0,1),new T.Vector3(...s.normal));g.add(face);
  const pin=new T.Mesh(new T.SphereGeometry(s.remote?.035:.042,12,8),new T.MeshBasicMaterial({color,depthTest:false,transparent:true,opacity:s.remote?.65:1}));g.add(pin);g.renderOrder=30;face.renderOrder=30;pin.renderOrder=31;scene.add(g);
  const button=document.createElement('button');button.className='site-label';button.style.setProperty('--pin',color);button.textContent=s.p.id;button.title=`${s.p.name} · ${s.displayHeight}`;button.setAttribute('aria-label',`${s.p.id} ${s.p.name} ${s.displayHeight}`);button.onclick=e=>{e.stopPropagation();onPick(s)};
  const label=new CSS2DObject(button);label.position.copy(world(s.x,s.z,s.h+.16));scene.add(label);
  return {s,g,button,label};
 });
 const measureMat=new T.LineDashedMaterial({color:'#a06f38',dashSize:.07,gapSize:.04,depthTest:false});const measure=new T.Line(new T.BufferGeometry(),measureMat);measure.renderOrder=40;scene.add(measure);
 const ray=new T.Raycaster();let down=[0,0];renderer.domElement.onpointerdown=e=>down=[e.clientX,e.clientY];renderer.domElement.onpointerup=e=>{if(Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;const b=host.getBoundingClientRect();ray.setFromCamera(new T.Vector2((e.clientX-b.left)/b.width*2-1,-(e.clientY-b.top)/b.height*2+1),camera);const visible=marks.filter(m=>m.g.visible);const hits=ray.intersectObjects(visible.map(m=>m.g),true);if(hits.length){const m=visible.find(m=>hits[0].object.parent===m.g);if(m)onPick(m.s)}};
 let span=6;let viewRoom='';let viewMode='';
 function frame(room:string,view:View){const r=rooms.find(r=>r.name===room);const b=r?r.box:[280,245,975,735];const target=world(b[0]+b[2]/2,b[1]+b[3]/2,view==='top'?0:1);controls.target.copy(target);span=Math.max(b[2],b[3])*S+(r?1.6:2);camera.zoom=1;
  const dist=20;const delta=view==='top'?new T.Vector3(0,dist,.001):view==='north'?new T.Vector3(0,1e-3,dist):view==='south'?new T.Vector3(0,1e-3,-dist):view==='west'?new T.Vector3(dist,1e-3,0):view==='east'?new T.Vector3(-dist,1e-3,0):new T.Vector3(dist*.75,dist*.9,dist);
  camera.position.copy(target.clone().add(delta));camera.lookAt(target);controls.update();resize();
 }
 function resize(){const w=host.clientWidth,h=host.clientHeight;if(!w||!h)return;const a=w/h;camera.left=-span*Math.max(a,1)/2;camera.right=-camera.left;camera.top=span/Math.min(a,1)/2;camera.bottom=-camera.top;camera.updateProjectionMatrix();renderer.setSize(w,h);labels.setSize(w,h)}
 const observer=new ResizeObserver(resize);observer.observe(host);
 function update(next:Options){options=next;clip.constant=next.cut;
  const roomBox=rooms.find(r=>r.name===next.room)?.box||[280,245,975,735];
  const [bx,bz,bw,bd]=roomBox;const depth=next.room==='全屋'?2000:next.room==='厨房'&&next.view==='west'?50:88;
  if(next.view==='north'){section.normal.set(0,0,-1);section.constant=world(bx,bz+depth).z;}
  else if(next.view==='south'){section.normal.set(0,0,1);section.constant=-world(bx,bz+bd-depth).z;}
  else if(next.view==='west'){section.normal.set(-1,0,0);section.constant=world(bx+depth,bz).x;}
  else if(next.view==='east'){section.normal.set(1,0,0);section.constant=-world(bx+bw-depth,bz).x;}
  else {section.normal.set(0,1,0);section.constant=1000;}
  const elevation=!['orbit','top'].includes(next.view);

  parts.forEach(o=>{o.visible=(next.room==='全屋'||o.userData.room===next.room);if(elevation&&o.userData.role==='glass')o.visible=false;const mesh=o as T.Mesh;const mat=mesh.material as T.MeshStandardMaterial|undefined;if(mat&&['furniture','cabinet','counter','appliance'].includes(o.userData.role)){mat.transparent=next.xray;mat.opacity=next.xray?.28:1;mat.depthWrite=!next.xray;}});
  roomLabels.forEach(l=>l.visible=next.room==='全屋');
  marks.forEach(m=>{const normal=m.s.normal;const onFace=!elevation||next.room==='全屋'||(next.view==='north'?normal[2]>0:next.view==='south'?normal[2]<0:next.view==='west'?normal[0]>0:normal[0]<0);const shown=onFace&&(next.room==='全屋'||m.s.p.room===next.room)&&(next.kind==='全部'||m.s.p.kind===next.kind)&&[m.s.p.id,m.s.p.name].join('').toLowerCase().includes(next.query.toLowerCase());m.g.visible=shown;m.label.visible=shown&&next.labels;m.button.classList.toggle('selected',m.s.key===next.selected);m.button.classList.toggle('pending',m.s.provisional);m.g.scale.setScalar(m.s.key===next.selected?1.5:1)});
  const chosen=sites.find(s=>s.key===next.selected);measure.visible=!!chosen;if(chosen){measure.geometry.dispose();measure.geometry=new T.BufferGeometry().setFromPoints([world(chosen.x,chosen.z,.015),world(chosen.x,chosen.z,chosen.h)]);measure.computeLineDistances();}
  if(next.room!==viewRoom||next.view!==viewMode){viewRoom=next.room;viewMode=next.view;frame(next.room,next.view)}
 }
 let raf=0;let destroyed=false;function tick(){if(destroyed)return;raf=requestAnimationFrame(tick);controls.update();renderer.render(scene,camera);labels.render(scene,camera)}
 renderer.domElement.addEventListener('webglcontextlost',()=>onError('3D绘图上下文已中断，请刷新页面；2D图和右侧点位参数仍可查看。'));
 update(options);tick();return {update,reset:()=>frame(options.room,options.view),dispose:()=>{destroyed=true;cancelAnimationFrame(raf);observer.disconnect();controls.dispose();scene.traverse(o=>{const m=o as T.Mesh;if(m.geometry)m.geometry.dispose();if(m.material){(Array.isArray(m.material)?m.material:[m.material]).forEach(m=>m.dispose())}});renderer.dispose();host.replaceChildren()}};
}
