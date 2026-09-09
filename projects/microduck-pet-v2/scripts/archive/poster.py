from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,math
P=Path(__file__).parent;parts=json.loads((P/'parts.json').read_text());im=Image.new('RGB',(1800,1700),'#eef3f5');d=ImageDraw.Draw(im);font='/workspace/scratch/cafdff7da2f9/assets/NotoSansSC-Regular.ttf';F=lambda n:ImageFont.truetype(font,n)
d.text((45,25),'内部器件布局 · 分区爆炸图 V2',font=F(42),fill='#173d4a');d.text((45,90),'按坐标绘制的空间包络；非AI生成结构图。完整交互视图见配套HTML。',font=F(23),fill='#53707c')
colors={'head':'#53b5b7','frame':'#899ca4','yaw':'#ac8ac8','pcb':'#64bc94','battery':'#e5bd6b','thermal':'#b5bec3','motor':'#6baed6','shaft':'#a1b0b9','wheel':'#efb261'}
for idx,(prefix,title) in enumerate([('H','头部：无嘴、无俯仰轴'),('Y','转台：单一竖直旋转轴'),('B','躯干：电池下置 / 电子板上置'),('R','右轮组：左侧镜像布置')]):
 x0=35+(idx%2)*890;y0=150+(idx//2)*735;d.rounded_rectangle((x0,y0,x0+860,y0+705),18,fill='white');d.text((x0+20,y0+15),title,font=F(27),fill='#173d4a');ps=[p for p in parts if p['id'].startswith(prefix) and p['group']!='shell'];recs=[]
 for j,p in enumerate(ps):
  c=p['center'][:];c[2]+=j*65;c[1]+=j*15
  def proj(v):return (v[0]*.83-v[1]*.55,(v[0]*.55+v[1]*.83)*.38-v[2],v[0]*.55+v[1]*.83+v[2]*.38)
  v=[proj([c[n]+[a,b,k][n]*p['size'][n]/2 for n in range(3)]) for k in [-1,1] for b in [-1,1] for a in [-1,1]];recs.append((p,v,proj(c)))
 allv=[v for _,vs,_ in recs for v in vs];mx=[min(v[n] for v in allv) for n in range(2)];Mx=[max(v[n] for v in allv) for n in range(2)];s=min(385/(Mx[0]-mx[0]),500/(Mx[1]-mx[1]));
 def screen(v):return (x0+25+(v[0]-mx[0])*s,y0+85+(v[1]-mx[1])*s)
 fs=[]
 for p,v,c in recs:
  for ids in [[0,1,3,2],[4,5,7,6],[0,1,5,4],[2,3,7,6],[0,2,6,4],[1,3,7,5]]:fs.append((sum(v[i][2] for i in ids),p,[screen(v[i]) for i in ids]))
 for _,p,v in sorted(fs,key=lambda f:f[0]):d.polygon(v,fill=colors[p['group']],outline='#526e7a')
 for p,v,c in recs:d.text(screen(c),p['id'],font=F(17),fill='#102d37')
 for j,p in enumerate(ps):
  yy=y0+75+j*47;d.text((x0+430,yy),p['id']+' '+p['name'],font=F(17),fill='#163c49');d.text((x0+430,yy+22),str(p['size'])+' mm · '+p['status'],font=F(14),fill='#687e87')
 d.text((x0+20,y0+650),'爆炸位移仅供辨认；原安装中心坐标见CSV / HTML。',font=F(18),fill='#687e87')
d.text((45,1640),'未定型：60mm轮SKU、转头执行器、电池、驱动PCB、轴承及孔位。壳体省略以便查看内部。',font=F(22),fill='#8a5434')
im.save(P/'Exploded_Preview.png')
