from pathlib import Path
import json, csv, math, zipfile
P=Path(__file__).parent
parts=[]
def add(id,name,c,s,group,status,note):parts.append(dict(id=id,name=name,center=c,size=s,group=group,status=status,note=note))
# mm; x lateral, y front/rear, z up; all dimensions are envelopes
add('H01','一体头壳 / 无嘴',[0,0,327],[110,86,92],'shell','暂定','2 mm壳厚；仅外包络，内部需掏空')
add('H02','2.8英寸屏幕整板',[0,-32,315],[79.9,15,50.8],'head','混合','平面外形来自厂家；15 mm厚度含连接空间暂定')
add('H03','IMX219摄像头',[0,-30,355],[25,12,24],'head','混合','25×24板外形；厚度/光轴位置待确认')
add('H04','VL53L5CX载板',[32,-30,355],[12.7,10,17.78],'head','混合','板外形来自Pololu3417；10为含线包络')
add('H05','头内模组托架',[0,0,331],[94,4,74],'frame','暂定','孔位待厂家图；不能压屏幕玻璃')
add('Y01','头转台承重轴承',[0,0,279],[42,42,10],'yaw','暂定','环形件占位；内孔留线束；型号未定')
add('Y02','转台轮毂 / 限位',[0,0,267],[38,38,10],'yaw','暂定','带机械限位；±35°仅设计目标')
add('Y03','转向执行器',[0,0,244],[40,32,30],'yaw','未选型','只驱动左右转动；承重由Y01承担；扭矩待惯量计算')
add('Y04','竖直承力颈座',[0,0,248],[56,56,55],'shell','暂定','空心件；后侧独立走线；无俯仰轴')
add('B01','躯干后盖',[0,48,193],[164,4,72],'shell','暂定','散热孔与接口开口待定')
add('B02','ZERO 3W主控',[0,20,214],[65,30,14],'pcb','混合','65×30已确认；14为器件高度预算')
add('B03','主控散热器预留',[0,20,228],[55,25,10],'thermal','暂定','与主板接触；禁止被排线覆盖')
add('B04','电源及实时控制板',[0,-22,214],[75,40,14],'pcb','未设计','MCU/四编码器接口/IMU/降压/保险/电源开关接口，非现成PCB')
add('B05','3S电池组含BMS',[0,0,177],[75,58,24],'battery','未选型','容量、放电率、保护板及绝缘都须在此包络内；不能按裸电芯算')
add('B06','电池托盘',[0,0,162],[82,65,4],'frame','暂定','绑带固定；下拆维护；与PCB分层')
add('B07','充电口/总开关',[66,0,183],[20,30,24],'pcb','未选型','外置3S CC/CV充电器；禁止仅用BMS当充电器')
add('B08','躯干外壳',[0,0,196],[164,100,78],'shell','暂定','空心件占位；不代表与原身体直接兼容')
add('L01','左承力腿',[ -69,0,122],[28,38,65],'frame','暂定','封闭线槽+检修盖；行驶姿态刚性固定')
add('L02','右承力腿',[69,0,122],[28,38,65],'frame','暂定','可动腿关节未设计；本版不能演示下蹲')
add('L03','横向承力连接',[0,12,131],[110,14,16],'frame','暂定','维持四轮轮距，连接双腿')
for side,x,sgn in [('L',69,-1),('R',69,1)]:
 x*=sgn
 add(side+'01',side+'脚部检修盖',[x,0,88],[84,150,4],'shell','暂定','驱动板上方留拆线空间')
 add(side+'02',side+'双路轮驱动板',[x,0,69],[64,54,16],'pcb','未设计','两路H桥/电流检测/限流/散热；每脚一块')
 add(side+'03',side+'电机承力托架',[x,0,46],[84,150,67],'shell','暂定','带轴承座空心结构；内部不可实心')
 for j,y in [('F',-48),('B',48)]:
  add(side+j+'M',side+j+'轮电机 #4846',[x,y,30],[69,25,25],'motor','已知外包络','Ø25×69本体；输出轴另占12.5；尾线另留10')
  add(side+j+'C',side+j+'输出轴/联轴器',[sgn*110,y,30],[13,16,16],'shaft','暂定','4mm电机D轴适配独立轮轴；联轴器未选')
  add(side+j+'A',side+j+'承重轴承座',[sgn*119,y,30],[5,24,24],'shaft','暂定','仅占位；需成对轴承或足够跨距，载荷核算未完成')
  add(side+j+'W',side+j+'麦克纳姆轮',[sgn*132,y,30],[30,60,60],'wheel','未选型','目标Ø60×30；左右旋各2；不能据此采购')
# Compute non-shell envelope intersections, whitelist intentional contacts separately
ignore={'shell','frame','shaft','wheel','thermal','yaw'}
checks=[]
for i,a in enumerate(parts):
 if a['group'] in ignore:continue
 for b in parts[i+1:]:
  if b['group'] in ignore:continue
  overlaps=[min(a['center'][k]+a['size'][k]/2,b['center'][k]+b['size'][k]/2)-max(a['center'][k]-a['size'][k]/2,b['center'][k]-b['size'][k]/2) for k in range(3)]
  if min(overlaps)>0:checks.append([a['id'],b['id'],overlaps])
(P/'parts.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2))
with (P/'parts.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['编号','器件','中心X/Y/Z mm','包络X/Y/Z mm','尺寸状态','备注'])
 for p in parts:w.writerow([p['id'],p['name'],p['center'],p['size'],p['status'],p['note']])
(P/'envelope_check.json').write_text(json.dumps({'electronics_motor_positive_volume_overlaps':checks,'excluded':'shell/frame/shaft/wheel/thermal/yaw；不含线束/孔位/曲面/装配运动；不是完整DRC'},ensure_ascii=False,indent=2))
print('parts',len(parts),'electronics/motor overlaps',checks)
colors={'shell':'#becdd3','head':'#39a6aa','frame':'#637780','yaw':'#965bad','pcb':'#2a9c73','battery':'#deaf50','thermal':'#8d969c','motor':'#5399c5','shaft':'#76818e','wheel':'#ed982f'}
intro='''<h1>内部布局与爆炸装配 V2</h1><p>取消嘴部及俯仰轴，仅保留头部左右转动。42个编号是器件/空间包络，不是42个可打印零件。滚轮、壳体、轴承均用简化包络显示。</p><p><b>重新设计结果：</b>底部总宽294 mm、前后156 mm；头110×86×92 mm；整机包络高373 mm。此前图片的窄轮罩容不下已选电机，不能直接照图打样。此版承力腿按固定行驶姿态处理，未完成可动腿机构。</p>'''
notes='''<h2>补齐和重新安排的内容</h2><ul><li>头部：屏幕整板、摄像头、ToF分别固定；后侧留线束通道。转台承重轴承独立于执行器；取消嘴舵机、俯仰舵机。转向执行器尚未选型，不用轮电机替代。</li><li>躯干：电池在下，主控与实时控制/配电板在上；散热器在主控上方。充电接口和总开关独立预留，采用外置3S专用充电器。BMS不承担充电控制。</li><li>双脚：每脚前后两台横置电机，电机本体69mm，输出轴另留12.5mm，尾部线束另留10mm；驱动板位于电机上方，避免塞入电机尾线空间。</li><li>承力：独立轮轴/轴承座将车重送到托架；联轴器只传扭。轴承、联轴器、轮毂孔尚未选型，当前图中占位尺寸不能用于加工。</li><li>走线：躯干至左右脚各走电源线和通信线；脚内实时控制采集两路编码器更利于减少跨腿线数（需落实到驱动板）。动力线与编码器线分槽，出入口加护套及应力释放。头部排线走转轴旁的活动弯，不穿实心执行器；有±35°机械限位，无滑环。</li><li>热与电源：四台轮电机12V堵转外推电流合计20A，必须限流并校核电池、线径、连接器与保险；不是默认连续耗电20A。3S满电12.6V，需核查电机电压与PWM限制；主控另降压5V，转头电源按最终执行器单独设计。制动回灌不能只靠BMS切断，应在配电设计中处理。</li></ul><h2>重量与电机复核</h2><p>重设计后不再沿用3kg已满足的说法。新预算：头颈0.40kg，躯干电子电池0.80kg，腿与轮架0.85kg，电机和轮0.85kg，线束紧固件0.25kg，余量0.35kg，总设计校核质量3.5kg（估算）。</p><p>轮径60mm、坡度5°、加速度0.5m/s²、滚阻系数0.05、综合效率0.5、四轮均分时，T=[ma+mg(sinθ+μcosθ)]r/(4η)=0.097N·m/轮；再取2倍为0.194N·m/轮。系数是假设，横移摩擦和单轮载荷不均必须实测。Pololu #4846仅作为初选，连续0.194N·m的温升能力尚未核实。130rpm空载对应约0.408m/s，负载速度更低。</p><h2>验证边界与剩余工作</h2><p>已做已布置电子板、电池、轮电机之间的三维矩形包络相交检查，结果无正体积重叠。排除了壳体、承力件、轴承、轮子及转台；它们存在有意接触或包络嵌套。本检查不覆盖孔位、线束、材料、螺钉、轮子扫掠、散热和装配运动，不等于完整无干涉。</p><p><b>未冻结：</b>60mm轮具体SKU及轮宽、独立轮轴/双轴承布置、转头执行器与驱动、3S电池成品尺寸、配电与脚部驱动PCB、所有安装孔、头部排线弯曲半径、保护器件和关节锁止。没有把未设计的PCB冒充现成模块。本包无生产STL/Gerber。</p><p>主控沿用ZERO3W作现有项目集成基准；IMX219模块与Radxa的排线针脚必须核对。没有新增扬声器和麦克风：当前需求未包含语音交互，如需语音必须重新留音腔和声学开孔。ToF是前向8×8深度测距，不是360°扫描雷达。</p><h2>资料依据</h2><ul><li><a href="https://www.pololu.com/product/4846">Pololu #4846：Ø25×69，12V，130rpm，输出轴12.5mm</a></li><li><a href="https://www.radxa.com/products/zeros/zero3w/">Radxa ZERO3W：65×30mm</a></li><li><a href="https://www.waveshare.com/2.8inch-resistive-touch-lcd.htm">Waveshare屏幕：79.9×50.8mm（本会话此前核实的平面尺寸）</a></li><li><a href="https://www.waveshare.com/pi5-imx219.htm">IMX219模组平面25×24mm</a></li><li><a href="https://www.pololu.com/product/3417/specs">Pololu3417 ToF载板</a></li></ul>'''
html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>内部布局爆炸图 V2</title><style>body{margin:0;background:#edf3f5;color:#213d49;font:16px/1.7 system-ui}main{max-width:1250px;margin:auto;padding:28px}canvas{width:100%;background:white;border-radius:12px}button,select{padding:10px;margin:5px;border:1px solid #adbec5;border-radius:7px;background:white}table{width:100%;border-collapse:collapse;font-size:13px}td,th{border-bottom:1px solid #c5d4da;padding:8px;text-align:left}section{background:white;padding:22px;border-radius:12px;margin-top:18px}a{color:#008b89}</style><main>'''+intro+'''<section><select id="group"><option value="all">整机</option><option value="H">头部</option><option value="Y">左右转台</option><option value="B">躯干</option><option value="L">左腿脚</option><option value="R">右腿脚</option></select><button onclick="e.value=0;draw()">装配位置</button><button onclick="e.value=1;draw()">爆炸位置</button> 爆炸量 <input id="e" type="range" min="0" max="1" value="1" step=".01"><label><input id="shell" type="checkbox">显示外壳包络</label><p>拖动图像旋转视角。点击下方清单行，高亮对应器件。灰色半透明盒子表示包络，不是实心成品。</p><canvas id="cv" width="1200" height="850"></canvas></section><section><h2>器件位置清单</h2><p>坐标单位mm；X左右、Y前后、Z向上；所有中心位置均为装配状态。</p><table><thead><tr><th>编号</th><th>器件</th><th>中心X/Y/Z</th><th>包络X/Y/Z</th><th>状态与备注</th></tr></thead><tbody>'''
for p in parts:html+=f'''<tr onclick="sel='{p['id']}';draw()"><td>{p['id']}</td><td>{p['name']}</td><td>{p['center']}</td><td>{p['size']}</td><td>{p['status']} · {p['note']}</td></tr>'''
html+='</tbody></table></section><section>'+notes+'</section></main><script>const parts='+json.dumps(parts,ensure_ascii=False)+';const colors='+json.dumps(colors)+''';let angle=.55,sel='',drag=false,px=0;const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),e=document.getElementById('e'),group=document.getElementById('group'),shell=document.getElementById('shell');
function offset(p){let x=p.center[0],y=p.center[1],z=p.center[2],t=+e.value;
 if(p.id[0]==='H'){z+=100*t;y+=(p.id==='H01'?50:(p.id==='H05'?20:-50))*t;}
 if(p.id[0]==='Y')z+=(p.id==='Y01'?75:p.id==='Y02'?50:25)*t;
 if(p.id[0]==='B'){z+=(p.id==='B01'?55:0)*t;y+=(p.id==='B01'?100:p.id==='B05'?-75:p.id==='B04'?-70:p.id==='B02'?40:0)*t;}
 if(/^[LR]/.test(p.id)){let s=p.center[0]<0?-1:1;x+=s*45*t;if(p.group==='wheel')x+=s*70*t;if(p.group==='shaft')x+=s*35*t;if(p.group==='pcb')z+=55*t;if(p.group==='shell')z+=90*t;}
 return [x,y,z];}
function draw(){let ps=parts.filter(p=>(group.value==='all'||p.id.startsWith(group.value))&&(shell.checked||p.group!=='shell'));let ca=Math.cos(angle),sa=Math.sin(angle);function proj(v){return [v[0]*ca-v[1]*sa,(v[0]*sa+v[1]*ca)*.38-v[2],v[0]*sa+v[1]*ca+v[2]*.38];}let records=ps.map(p=>{let c=offset(p),v=[];for(let k of [-1,1])for(let j of [-1,1])for(let i of [-1,1])v.push(proj(c.map((a,n)=>a+[i,j,k][n]*p.size[n]/2)));return {p,v,c:proj(c)}});let all=records.flatMap(r=>r.v),xs=all.map(v=>v[0]),ys=all.map(v=>v[1]);let minx=Math.min(...xs),maxx=Math.max(...xs),miny=Math.min(...ys),maxy=Math.max(...ys),scale=Math.min(1000/(maxx-minx),680/(maxy-miny));function screen(v){return [600+(v[0]-(minx+maxx)/2)*scale,415+(v[1]-(miny+maxy)/2)*scale];}ctx.clearRect(0,0,1200,850);let fs=[];for(let r of records)for(let ids of [[0,1,3,2],[4,5,7,6],[0,1,5,4],[2,3,7,6],[0,2,6,4],[1,3,7,5]])fs.push({r,ids,d:ids.reduce((a,i)=>a+r.v[i][2],0)/4});fs.sort((a,b)=>a.d-b.d);for(let f of fs){ctx.beginPath();f.ids.forEach((i,n)=>{let q=screen(f.r.v[i]);n?ctx.lineTo(...q):ctx.moveTo(...q)});ctx.closePath();ctx.globalAlpha=f.r.p.group==='shell'?.12:.62;ctx.fillStyle=f.r.p.id===sel?'#ff4267':colors[f.r.p.group];ctx.fill();ctx.globalAlpha=1;ctx.strokeStyle='#68808b';ctx.lineWidth=.6;ctx.stroke();}ctx.font='14px sans-serif';for(let r of records){let q=screen(r.c);ctx.fillStyle=r.p.id===sel?'#cb173d':'#12343f';ctx.fillText(r.p.id,q[0]+4,q[1]-4);}ctx.fillStyle='#234653';ctx.font='18px sans-serif';ctx.fillText(+e.value===0?'装配位置 / 包络模型':'爆炸位置 / 位移仅供查看',30,34);ctx.font='15px sans-serif';ctx.fillText('选择子装配可清楚查看内部。具体位置和未定器件见下方清单。',30,815);}
cv.onpointerdown=a=>{drag=true;px=a.clientX;cv.setPointerCapture(a.pointerId)};cv.onpointermove=a=>{if(drag){angle+=(a.clientX-px)*.01;px=a.clientX;draw()}};cv.onpointerup=()=>drag=false;e.oninput=draw;group.onchange=draw;shell.onchange=draw;draw();</script>'''
(P/'Exploded_Layout_V2.html').write_text(html)
# Editable OpenSCAD envelope assembly (not manufacture-ready solids)
s=['// mm. Space envelopes only; not printable production parts.','explode=0;','show_shell=false;']
for p in parts:
 rgb=colors[p['group']];c=[int(rgb[i:i+2],16)/255 for i in [1,3,5]]
 s.append('// '+p['id']+' '+p['name']+' '+p['status'])
 pre='if(show_shell) ' if p['group']=='shell' else ''
 s.append(pre+f'color({c},0.5) translate({p["center"]}) cube({p["size"]},center=true);')
(P/'layout_envelopes.scad').write_text('\n'.join(s))
(P/'README.txt').write_text('先打开 Exploded_Layout_V2.html；可旋转、切换装配/爆炸、选择子装配。\nparts.csv/json为装配坐标。SCAD仅包络非生产零件；explode变量暂未用于SCAD，交互爆炸在HTML中。\n'+ '已知缺项与校核边界见HTML全文。')
with zipfile.ZipFile(P/'Exploded_Layout_V2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in P.iterdir():
  if f.suffix!='.zip':z.write(f,f.name)
print('HTML and editable envelope package created')
