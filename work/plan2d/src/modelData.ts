import data from './data.json';
export type Point=typeof data.points[number];
export const points=data.points;
export const rooms=data.rooms;
export const colors:Record<string,string>={'强电':'#c36b38','弱电':'#367ca4','控制':'#8566aa','水路':'#218b83'};
export const SCALE=1/64;
export const modelHeights={interior:2.7,kitchen:2.4};
export type Site={key:string;p:Point;index:number;x:number;z:number;h:number;provisional:boolean;displayHeight:string;note:string;normal:[number,number,number];remote:boolean;quantity?:string};
// Non-numeric/conditional heights are model placeholders, never installation decisions.
const illustrative:Record<string,number>={E01:.4,N01:.4,L03:.75,L05:.5,D03:1.9,K04:.65,K05:.65,K06:.65,S07:.7,M06:2.15,A01:.8,A02:1.2,A04:.8,N09:2.1,W01:.45,W02:.45,W03:1.3,W04:.5,W05:.225,W06:1.1,W07:.5,W08:.225,W09:1.1,W10:.8,W12:.55,W13:.4,C08:.725,K12:.5,K13:2.1};
const remotePower:Record<string,string>={C01:'L06',C02:'S04',C03:'M05',C04:'B05',A05:'A06'};
export function normalFor(p:Point,x:number,z:number):[number,number,number]{
 if(p.id==='A06'||p.id==='A05'||(['T05','U05'].includes(p.id)&&z<400))return [0,1,0];
 if(p.room==='厨房'){if(z<545)return[0,0,1];if(z>695&&x>410)return[0,0,-1];return[1,0,0]}
 if(p.room==='阳台')return z<540?[0,0,1]:[-1,0,0];
 if(p.room==='主卧'){if(z<290)return[0,0,1];if(z>475)return[0,0,-1];return x<930?[1,0,0]:[-1,0,0]}
 if(p.room==='书房')return z<820?[0,0,1]:z>930?[0,0,-1]:[1,0,0];
 if(p.room==='老人房')return z<350?[0,0,1]:[0,0,-1];
 if(p.room==='公卫')return z>415?[0,0,-1]:x>700?[-1,0,0]:[1,0,0];
 if(p.room==='主卫')return z>420?[0,0,1]:x>820?[-1,0,0]:[1,0,0];
 if(p.room==='玄关')return p.id==='E03'||p.id==='C05'?[1,0,0]:[0,0,-1];
 return z<560?[0,0,1]:[0,0,-1];
}
export const sites:Site[]=points.flatMap(p=>p.anchors.flatMap((anchor,index)=>{
 const request=p.requestedSites[index];let [x,z]=p.installAt[index]||[request?.x??anchor[0],request?.y??anchor[1]];
 let note='按当前2D点位的安装部位投影；平面坐标为图纸示意，非现场放线尺寸。';
 // V9 places the oven below the counter, its supply in the adjacent drawer service zone.
 if(p.id==='K05'){x=477;z=521;note='M1柜体适配建议：移至相邻420抽屉柜后方的可开启检修格，中心H650。图上位置不代表可穿过抽屉，需柜厂预留独立检修空间；2D原需求区仍保留。'}
 if(['K04','K06'].includes(p.id)){x=341;z=p.id==='K04'?605:643;note='M1建议：电源改放相邻水槽柜侧后部干区，中心H650，与水阀侧向错开，避开T20机身。柜内坐标和高度尚需柜图、盆深与安装图核对；2D保留原需求区。'}
 if(['W01','W02'].includes(p.id)){x=341;z=p.id==='W01'?626:620;note='M1建议：阀门中心H450，水槽柜内可触及后墙；排水接口高度未定。当前标记只代表给水阀组，不能将450用于排水施工。'}
 if(p.id==='K01')note='按已确认要求保留冰箱背后；V9提出的上柜方案未采用。插头厚度、散热与整机前抽检修待安装图核对。';
 const remote=!!remotePower[p.id];let h:number;let provisional=false;
 if(remote){h=p.id==='A05'?2.7:2.2;provisional=true;note=`设备遥控功能位置，墙面面板0处；实际电源见${remotePower[p.id]}。`}
 else if(p.id==='A06'){h=2.7;provisional=true}
 else if(['T05','U05'].includes(p.id)){h=index===0?2.4:1.3;provisional=index===0}
 else if(['W06','W09'].includes(p.id)){h=index===1?.03:1.1;provisional=index===0}
 else if(p.id in illustrative){h=illustrative[p.id];provisional=true}
 else {const m=p.spec.height.match(/(\d{3,4})\s*(?:mm|～|—|–)/);h=m?Number(m[1])/1000:1.3;provisional=!m}
 if(p.id==='K08'){h=1.6;provisional=true}
 if(p.id==='S01')return [.9,.35].map((height,j)=>({key:`${p.id}-${index}-${j}`,p,index,x:x+(j?3:-3),z,h:height,provisional:false,displayHeight:`${height*1000} mm · 参考`,quantity:'五孔插座1个',note:`${j?'桌下':'桌上'}每处1个五孔；两组共4个。`,normal:normalFor(p,x,z),remote:false}));
 if(p.id==='D01')return [1.3,.5].map((height,j)=>({key:`${p.id}-${index}-${j}`,p,index,x:x+(j?5:-5),z,h:height,provisional:!!j,displayHeight:j?'H待定 · 模型500 mm':'1300 mm · 参考',quantity:j?'柜内五孔插座1个':'台面五孔插座3个（组合）',note:j?'柜内1个，随柜格深化；不重复计岛台供电。':'台面3个，按实际设备横向展开；图中为组合位置。',normal:normalFor(p,x,z),remote:false}));
 return [{key:`${p.id}-${index}`,p,index,x,z,h,provisional,displayHeight:remote?'遥控设备 · 无墙面面板':provisional?`${['K04','K05','K06','K08','W01','W02'].includes(p.id)?'M1建议待核':'H待定 · 模型'}${Math.round(h*1000)} mm`:`${Math.round(h*1000)} mm · 参考`,note,normal:normalFor(p,x,z),remote}];
}));
export const kitchenNotes=[
 'M1水电深化建议：K04/K05/K06电源中心650、W01/W02冷/热水阀中心450、K08中心1600 mm；仅用于3D协调，未转为施工定值。',
 'B面：1970 = 20收口 + 600微蒸烤 + 420抽屉 + 886冰箱围柜 + 44收口，均待完成面复尺。',
 'A/B面台面900、C面台面850、A/B进深650、吊柜底1500/深350，均为V9建议尺寸。',
 'A面窗侧墙始终平直，仅台面和地柜前缘斜角收浅；L形转角贯通，无中柱及竖隔板。',
 '厨房移门不建模，原墙垛保留。窗洞、柜体净长、烟机和设备检修空间仍需现场核对。',
 '厨房V9文本中的“K10电饭煲”按用途映射为本方案K11；本方案K10仍为厨房灯光开关，避免编号冲突。'
];
