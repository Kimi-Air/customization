import React,{useEffect,useMemo,useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {ConfigProvider,Button,Segmented,Select,Switch,Slider,Input,Tag} from 'antd';
import {ApartmentOutlined,ArrowLeftOutlined,ReloadOutlined,SearchOutlined,AimOutlined,CloseOutlined} from '@ant-design/icons';
import {createModel,View} from './modelScene';
import {sites,points,rooms,colors,kitchenNotes,Site} from './modelData';
import './model.css';
function App(){
 const [room,setRoom]=useState('厨房'),[kind,setKind]=useState('强电'),[query,setQuery]=useState(''),[view,setView]=useState<View>('orbit');
 const [cut,setCut]=useState(.95),[xray,setXray]=useState(false),[labels,setLabels]=useState(true),[selected,setSelected]=useState(''),[error,setError]=useState('');
 const ref=useRef<HTMLDivElement>(null),engine=useRef<ReturnType<typeof createModel>|null>(null);
 const [notes,setNotes]=useState(false);const choose=useRef<(s:Site)=>void>(()=>{});
 choose.current=(s:Site)=>{setSelected(s.key);setRoom(s.p.room)};
 useEffect(()=>{try{engine.current=createModel(ref.current!,s=>choose.current(s),setError)}catch(e){setError('此浏览器暂不能启用3D，请尝试在系统浏览器打开；可继续使用2D页面。');console.error(e)}return()=>engine.current?.dispose()},[]);
 useEffect(()=>engine.current?.update({room,kind,query,cut,xray,labels,selected,view}),[room,kind,query,cut,xray,labels,selected,view]);
 const filtered=useMemo(()=>sites.filter(s=>(room==='全屋'||s.p.room===room)&&(kind==='全部'||s.p.kind===kind)&&[s.p.id,s.p.name].join('').toLowerCase().includes(query.toLowerCase())),[room,kind,query]);
 const visiblePoints=points.filter(p=>filtered.some(s=>s.p.id===p.id));const active=sites.find(s=>s.key===selected);
 function changeRoom(r:string){setRoom(r);setSelected('');setView('orbit');setQuery('');setCut(.95);setXray(false);setLabels(r!=='全屋')}
 function face(){if(!active)return;const [x,,z]=active.normal;setView(x>0?'west':x<0?'east':z<0?'south':'north');setXray(true);setCut(2.7)}
 function pickView(v:View){setView(v);setCut(v==='orbit'||v==='top'?.95:2.7);if(v!=='orbit'&&v!=='top')setXray(true)}
 const presetLabels:Record<View,string>={orbit:'立体',top:'俯视',north:room==='厨房'?'B 冰箱面':'上侧墙',west:room==='厨房'?'A 水槽面':'左侧墙',south:room==='厨房'?'C 灶台面':'下侧墙',east:room==='厨房'?'入口侧':'右侧墙'};
 return <ConfigProvider theme={{token:{colorPrimary:'#2c665a',colorText:'#243c33',colorTextSecondary:'#728479',borderRadius:7,fontSize:13,fontFamily:'-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif',controlHeight:34}}}>
  <div className="model-app"><header className="model-header"><div className="model-brand"><span><ApartmentOutlined/></span><div><h1>碧瑶花园 <small>16–1203</small></h1><p>空间与水电 · 三维定位</p></div></div><div className="header-right"><Button onClick={()=>setNotes(!notes)}>模型依据</Button><Button href="./" icon={<ArrowLeftOutlined/>}>2D 平面图</Button></div></header>
  <section className="model-toolbar"><Select aria-label="选择3D房间" value={room} onChange={changeRoom} style={{width:136}} options={['全屋',...rooms.map(r=>r.name)].map(value=>({value,label:value}))}/><Segmented aria-label="选择3D图层" value={kind} onChange={v=>{setKind(String(v));setSelected('')}} options={['全部',...Object.keys(colors)].map(value=>({value,label:<span style={{color:colors[value]}}>{value}</span>}))}/><Input aria-label="搜索3D点位" value={query} allowClear onChange={e=>setQuery(e.target.value)} prefix={<SearchOutlined/>} placeholder="编号或设备" style={{width:190}}/><span className="model-count">{visiblePoints.length} 组点位 · 与2D共用数据</span></section>
  <main className="model-workspace"><section className="model-stage" aria-label="三维模型工作区"><div className="stage-heading"><div><span className="eyebrow">SPATIAL / 03</span><h2>{room} <small>{view==='orbit'?'空间关系':presetLabels[view]}</small></h2></div><Button aria-label="重置三维视角" icon={<ReloadOutlined/>} onClick={()=>engine.current?.reset()}/></div>
   <div className="view-presets">{(['orbit','top','west','north','south','east'] as View[]).map(v=><Button key={v} size="small" type={view===v?'primary':'default'} onClick={()=>pickView(v)}>{presetLabels[v]}</Button>)}</div>
   <div className="three-host" ref={ref}/>{error&&<div className="model-error">{error}<a href="./">打开2D点位图</a></div>}
   <div className="scene-hint"><span>拖动旋转 · 滚轮缩放 · 右键平移</span><span>点击编号查看安装参数</span></div>
   <div className="model-options"><label><Switch size="small" checked={xray} onChange={setXray} aria-label="柜体家具透视"/> 柜体 / 家具透视</label><label><Switch size="small" checked={labels} onChange={setLabels} aria-label="显示3D点位编号"/> 编号</label><div className="cut-slider"><span>墙体剖切 {Math.round(cut*1000)} mm</span><Slider aria-label="墙体剖切高度" min={.35} max={2.7} step={.05} value={cut} onChange={setCut} tooltip={{formatter:v=>`${Math.round((v||0)*1000)} mm`}}/></div></div>
   <footer className="stage-foot"><span><i/> 标注穿透显示 · 正视仅显示对应面接口</span><span>虚线编号：高度待定，模型仅示意</span></footer>
  </section><aside className="model-sidebar">
   {active?<section className="model-detail"><div className="detail-top"><span style={{color:colors[active.p.kind]}}>{active.p.id}</span><Button aria-label="关闭3D点位详情" type="text" icon={<CloseOutlined/>} onClick={()=>setSelected('')}/></div><h2>{active.p.name}</h2><div className="detail-tags"><Tag>{active.p.room}</Tag><Tag color={colors[active.p.kind]}>{active.p.kind}</Tag>{active.remote&&<Tag>遥控功能</Tag>}</div>
    <div className={`height-readout ${active.provisional?'provisional':''}`}><small>{active.provisional?'示意高度 · 尚未定施工标高':'参考标高 · 距完成地面'}</small><strong>{active.displayHeight}</strong></div>
    <Button block icon={<AimOutlined/>} onClick={face}>正对点位 · 透视查看</Button>
    <dl><dt>本处数量</dt><dd>{active.quantity||active.p.spec.perMarker[active.index]||active.p.spec.quantity}</dd>{sites.filter(s=>s.p.id===active.p.id).length>1&&<><dt>本组合计</dt><dd>{active.p.spec.quantity}</dd></>}<dt>安装高度要求</dt><dd>{active.p.spec.height}<small>{active.p.spec.heightStatus}</small></dd><dt>安装部位</dt><dd>{active.p.spec.location}</dd><dt>3D定位说明</dt><dd>{active.note}</dd><dt>设计原因</dt><dd>{active.p.designReason}</dd><dt>待核对</dt><dd>{active.p.positionCheck}</dd></dl><details><summary>测量口径与核量说明</summary><p>{active.p.spec.measurement}</p><p>{active.p.spec.basis}</p><p>{active.p.spec.counting}</p></details>
   </section>:<div className="sidebar-intro"><span className="eyebrow">POINT INDEX</span><h2>从空间找到接口</h2><p>选择编号，看清电位与墙面、台面和柜内设备的关系。正视模式剖开近侧遮挡，并只标注朝向该面的接口。</p></div>}
   <section className="model-point-list"><div className="list-caption">{room} · {visiblePoints.length} 组</div>{visiblePoints.length===0&&<p className="no-points">没有匹配点位，请调整筛选。</p>}{visiblePoints.map(p=><div className="point-group" key={p.id}><button className={active?.p.id===p.id?'picked':''} onClick={()=>choose.current(filtered.find(s=>s.p.id===p.id)!)}><b style={{color:colors[p.kind]}}>{p.id}</b><span>{p.name}<small>{p.spec.quantity}</small></span><i>›</i></button>{active?.p.id===p.id&&filtered.filter(s=>s.p.id===p.id).length>1&&<div className="site-choices">{filtered.filter(s=>s.p.id===p.id).map((s,i)=><Button key={s.key} size="small" type={selected===s.key?'primary':'default'} onClick={()=>choose.current(s)}>位置{i+1} · {Math.round(s.h*1000)}{s.provisional?'示意':''}</Button>)}</div>}</div>)}</section>
  </aside></main>
  {notes&&<section className="model-notes"><div><h2>模型依据与尺度</h2><Button onClick={()=>setNotes(false)}>收起</Button></div><p>户型与家具按当前2D平面，厨房按V9橱柜方案及M1水电深化建议。室内净高暂用2700 mm、厨房吊顶净高暂用2400 mm；不是原房实测层高。</p><ul>{kitchenNotes.map(n=><li key={n}>{n}</li>)}</ul><p>位置已定但高度未定的接口以虚线编号展示，详情明确给出模型示意值。其余数值为既有方案参考值；当前模型不用于直接下单、放线或开槽。</p></section>}
  <div className="model-bottom"><span>厨房V9 + 水电M1 · 窗侧直墙 / 斜角柜前缘 · 不含厨房移门</span><span>净高：全屋2700 / 厨房2400 mm（示意）</span></div>
  </div>
 </ConfigProvider>
}
createRoot(document.getElementById('root')!).render(<App/>);
