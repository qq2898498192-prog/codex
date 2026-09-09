import numpy as np, math, subprocess
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
out=Path(__file__).parent
import os, argparse
parser=argparse.ArgumentParser();parser.add_argument('--font',default=os.environ.get('ROBOT_FONT','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'));args=parser.parse_args();font=args.font
F=lambda s:ImageFont.truetype(font,s)
faces=[]
teal=(15,137,140); dark=(42,57,68); silver=(190,204,212); orange=(231,145,45)
def poly(v,c):faces.append((np.array(v,float),c))
def box(c,s,col):
 x,y,z=c;a,b,d=np.array(s)/2
 v=np.array([[x+i*a,y+j*b,z+k*d] for i,j,k in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]])
 for ids in [[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]:poly(v[ids],col)
def cyl(c,r,l,axis,col,n=24):
 c=np.array(c); a=np.eye(3)[axis];u=np.eye(3)[(axis+1)%3];v=np.eye(3)[(axis+2)%3]
 rings=[[c+a*h+ r*(u*math.cos(t)+v*math.sin(t)) for t in np.arange(n)*2*math.pi/n] for h in [-l/2,l/2]]
 poly(rings[0][::-1],col);poly(rings[1],col)
 for j in range(n):poly([rings[0][j],rings[0][(j+1)%n],rings[1][(j+1)%n],rings[1][j]],col)
def rounded(c,w,d,h,r,col):
 pts=[]
 for x,z,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for a in np.linspace(start,start+90,9):pts.append([x+r*math.cos(math.radians(a)),z+r*math.sin(math.radians(a))])
 rings=[[[c[0]+x,c[1]+y,c[2]+z] for x,z in pts] for y in [-d/2,d/2]]
 poly(rings[0][::-1],col);poly(rings[1],col)
 for i in range(len(pts)):j=(i+1)%len(pts);poly([rings[0][i],rings[0][j],rings[1][j],rings[1][i]],col)
def scene(yaw):
 faces.clear()
 for x in [-64,64]:
  rounded((x,0,43),48,112,28,6,teal)
  for y in [-40,40]:
   cyl((x,y,25),25,24,0,dark)
   cyl((x+np.sign(x)*13,y,25),12,2,0,silver)
   # Individual oblique tread patches, visual approximation only
   for k in range(9):
    t=k*2*math.pi/9;pts=[]
    for xx,tt in [(-11,t-.18),(-11,t+.18),(11,t+.43),(11,t+.07)]:pts.append([x+xx,y+25.7*math.sin(tt),25+25.7*math.cos(tt)])
    poly(pts,orange)
  rounded((x,0,91),29,33,79,6,teal)
  rounded((x,-17,91),19,2,59,4,dark)
 box((0,9,104),(123,14,16),dark)
 rounded((0,0,153),111,60,54,12,silver)
 box((0,0,193),(27,27,42),dark)
 cyl((0,0,215),23,10,2,teal)
 # only one moving assembly, transformed solely around vertical Z
 start=len(faces)
 rounded((0,0,262),110,66,82,12,silver)
 rounded((0,-34,262),97,2,69,9,dark)
 rounded((0,-35.3,254),62,1,44,3,(8,25,34))
 for x in [-16,16]:
  for i in range(7):
   xx=x-9+i*3;zz=256+7*math.sin(i*math.pi/6)
   box((xx,-36.2,zz),(3,1,4),(54,226,214))
 cyl((0,-36,285),3.5,2,1,(7,16,23))
 rounded((23,-36,285),9,1,5,1,(10,20,28))
 a=math.radians(yaw);R=np.array([[math.cos(a),-math.sin(a),0],[math.sin(a),math.cos(a),0],[0,0,1]])
 for i in range(start,len(faces)):v,c=faces[i];faces[i]=(v@R.T,c)
 return faces
cam=np.array([.48,-.84,.25]);cam/=np.linalg.norm(cam)
right=np.cross(cam,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,cam)
def render(yaw):
 im=Image.new('RGB',(1280,900),(239,244,246));dr=ImageDraw.Draw(im)
 dr.ellipse((215,743,765,830),fill=(218,227,230))
 fs=scene(yaw)
 for v,c in sorted(fs,key=lambda p:np.mean(p[0]@cam)):
  n=np.cross(v[1]-v[0],v[2]-v[0]);norm=np.linalg.norm(n)
  shade=.78+.22*abs(np.dot(n/norm,np.array([.4,-.6,.7]))) if norm else 1
  xy=np.stack([v@right*2.15+480,775-v@up*2.15],axis=1)
  dr.polygon([tuple(p) for p in xy],fill=tuple(min(255,int(q*shade)) for q in c))
 dr.text((42,25),'一体屏幕头 · 仅左右转动',font=F(34),fill=dark)
 dr.text((42,76),'取消嘴部 / 取消头部俯仰轴 / 竖直转台',font=F(20),fill=(77,104,115))
 dr.rounded_rectangle((850,235,1220,605),18,fill=(255,255,255))
 for yy,txt in [(263,'运动演示'),(316,f'左右转角：{yaw:+.0f}°'),(362,'俯仰角：固定 0°'),(420,'头壳没有独立下颌'),(461,'仅竖直转轴驱动头部'),(502,'轮组静止，突出头部动作')]:dr.text((875,yy),txt,font=F(22),fill=dark)
 dr.text((42,851),'简化三维运动模型；非最终外观或加工图。演示角度 ±35°，未校核线束与机械限位。',font=F(20),fill=(78,103,113))
 return im
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x900','-r','24','-i','-','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'Head_Yaw_Demo.mp4')],stdin=subprocess.PIPE)
for i in range(240):
 yaw=35*math.sin(2*math.pi*i/239)
 im=render(yaw)
 if i==40:im.save(out/'preview.png')
 p.stdin.write(im.tobytes())
p.stdin.close();assert p.wait()==0
print('Rendered 240 frames, 10 seconds, yaw only.')
