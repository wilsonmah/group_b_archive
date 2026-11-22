import math, struct, json, array, base64
from pathlib import Path
from collections import defaultdict
from math import sin,cos,pi,sqrt
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'models'
OUT.mkdir(exist_ok=True)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,f):return tuple(x*f for x in a)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(a):return mul(a,1/(sqrt(dot(a,a)) or 1))
def mix(a,b,t):return add(a,mul(sub(b,a),t))
def clamp(x,a,b):return max(a,min(b,x))
materials=[]; mids={}
def mat(n,h,m=0,r=.45):
    rgb=[((int(h[i:i+2],16)/255+.055)/1.055)**2.4 if int(h[i:i+2],16)>10 else int(h[i:i+2],16)/255/12.92 for i in (0,2,4)]
    mids[n]=len(materials)
    materials.append(dict(name=n,pbrMetallicRoughness=dict(baseColorFactor=rgb+[1],metallicFactor=m,roughnessFactor=r),doubleSided=True))
# Materials: HB Audi Team works livery (white, golden yellow, orange pinstripe) and mechanical finishes.
for a in [('Ivory','F3F2EC',.12,.27),('Yellow','E9A21C',.12,.30),('Orange','DE5F1A',.12,.32),('Pearl','D9D9D2',.25,.35),
          ('Red','C8152B',.12,.31),('Taupe','6E655C',.12,.34),('Rubber','202327',0,.84),('Tread','27292D',0,.88),
          ('Charcoal','24292E',.25,.47),('Black','111418',.14,.5),('Gunmetal','4E575D',.62,.39),('Steel','9CA7AA',.8,.31),
          ('Silver','CBCECA',.75,.28),('Alloy','DCDAD0',.5,.31),('Wheel','EEEDE6',.22,.30),('Glass','2F4350',.43,.15),
          ('Lens','DCE3E0',.48,.16),('Amber','E8902A',.18,.22),('Tail','A82222',.15,.2),('Smoke','2A1416',.3,.18),
          ('Gold','B39663',.67,.35),('Exhaust','A39C90',.72,.46),('Heat','7B5A3E',.6,.5),('Seat','2E3439',0,.9),
          ('Belt','2F5FA8',0,.78),('Engine','8C8F8E',.55,.40),('Crinkle','2B2D30',.35,.7),('Silicone','D2452C',0,.52),
          ('Braid','23272B',.42,.62),('Copper','B8743F',.7,.35),('Mesh','15181B',.3,.6),('Decal','FFFFFF',0,.44)]:mat(*a)
glassmat=materials[mids['Glass']];glassmat['alphaMode']='BLEND';glassmat['pbrMetallicRoughness']['baseColorFactor'][3]=.62
materials[mids['Decal']]['pbrMetallicRoughness']['baseColorTexture']={'index':0}
materials[mids['Decal']]['alphaMode']='MASK';materials[mids['Decal']]['alphaCutoff']=.32
mat('Optical glass','E4F0ED',.08,.11)
materials[-1]['alphaMode']='BLEND';materials[-1]['pbrMetallicRoughness']['baseColorFactor'][3]=.22
mat('Reflector','D5D9D7',.96,.11)
groups={};parts={};current=None
def group(key,en,zh,vec,desc):
    global current
    current=key; groups[key]=dict(en=en,zh=zh,vec=vec,desc=desc)
def part(n):
    global cur
    cur=(current,n)
    if cur not in parts:parts[cur]={}
def geo(m):
    if m not in parts[cur]:parts[cur][m]=[array.array('f'),array.array('f'),array.array('f'),array.array('I')]
    return parts[cur][m]
def face(p,m,norm=None,uv=None):
    pos,nor,tex,ind=geo(m);base=len(pos)//3
    n=unit(cross(sub(p[1],p[0]),sub(p[2],p[0])))
    for i,q in enumerate(p):
        pos.extend(q);nor.extend(norm[i] if norm else n)
        if uv:tex.extend(uv[i])
    for i in range(1,len(p)-1):ind.extend((base,base+i,base+i+1))
def box(c,sz,m):
    pts=[add(c,(i*sz[0]/2,j*sz[1]/2,k*sz[2]/2)) for i,j,k in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    for idx in [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)]:face([pts[i] for i in idx],m)
def basis(d):
    u=unit(cross((0,1,0) if abs(d[1])<.89 else (1,0,0),d));return u,cross(d,u)
def cyl(a,b,r,m,N=12,r2=None):
    if r2 is None:r2=r
    d=unit(sub(b,a));u,v=basis(d)
    ns=[add(mul(u,cos(i*2*pi/N)),mul(v,sin(i*2*pi/N))) for i in range(N)]
    aa=[add(a,mul(n,r)) for n in ns];bb=[add(b,mul(n,r2)) for n in ns]
    for i in range(N):
        j=(i+1)%N;face([aa[i],aa[j],bb[j],bb[i]],m,[ns[i],ns[j],ns[j],ns[i]])
    face(aa[::-1],m);face(bb,m)
def path(p,r,m,N=8):
    for a,b in zip(p,p[1:]):cyl(a,b,r,m,N)
def tor(c,axis,R,r,m,N=48,K=8):
    d=unit(axis);u,v=basis(d)
    pos,nor,tex,ind=geo(m);base=len(pos)//3
    for i in range(N):
        rr=add(mul(u,cos(i*2*pi/N)),mul(v,sin(i*2*pi/N)))
        for j in range(K):
            n=add(mul(rr,cos(j*2*pi/K)),mul(d,sin(j*2*pi/K)))
            pos.extend(add(add(c,mul(rr,R)),mul(n,r)));nor.extend(n)
    for i in range(N):
        for j in range(K):
            a=base+i*K+j;b=base+((i+1)%N)*K+j;e=base+i*K+(j+1)%K;f=base+((i+1)%N)*K+(j+1)%K
            ind.extend([a,b,e,e,b,f])
def spring(a,b,R,r,m):
    d=unit(sub(b,a));u,v=basis(d)
    pts=[add(mix(a,b,i/64),add(mul(u,R*cos(14*pi*i/64)),mul(v,R*sin(14*pi*i/64)))) for i in range(65)]
    path(pts,r,m,6)
def grid(fn,us,vs,m,flip=False):
    for u,U in zip(us,us[1:]):
        for v,V in zip(vs,vs[1:]):
            p=[fn(u,v),fn(U,v),fn(U,V),fn(u,V)]
            face(p[::-1] if flip else p,m)
def seq(a,b,N):return [a+(b-a)*i/N for i in range(N+1)]
def interp(x,points):
    if x<=points[0][0]:return points[0][1]
    for (a,p),(b,q) in zip(points,points[1:]):
        if x<=b:return p+(q-p)*(x-a)/(b-a)
    return points[-1][1]
def sinterp(x,points):
    """Fritsch-Carlson monotone cubic through (x, y) points; flat beyond the ends."""
    n=len(points)
    if x<=points[0][0]:return points[0][1]
    if x>=points[-1][0]:return points[-1][1]
    xs=[p[0] for p in points];ys=[p[1] for p in points]
    d=[(ys[i+1]-ys[i])/(xs[i+1]-xs[i]) for i in range(n-1)]
    m=[d[0]]+[0 if d[i-1]*d[i]<=0 else (d[i-1]+d[i])/2 for i in range(1,n-1)]+[d[-1]]
    for i in range(n-1):
        if d[i]==0:m[i]=m[i+1]=0
        else:
            a,b=m[i]/d[i],m[i+1]/d[i];h=a*a+b*b
            if h>9:t=3/sqrt(h);m[i]=t*a*d[i];m[i+1]=t*b*d[i]
    for i in range(n-1):
        if x<=xs[i+1]:
            h=xs[i+1]-xs[i];t=(x-xs[i])/h
            return (ys[i]*(2*t**3-3*t*t+1)+h*m[i]*(t**3-2*t*t+t)+ys[i+1]*(-2*t**3+3*t*t)+h*m[i+1]*(t**3-t*t))
def decal(p,rect):
    x,y,X,Y=rect;face(p,'Decal',uv=[(x/2048,Y/2048),(X/2048,Y/2048),(X/2048,y/2048),(x/2048,y/2048)])
def strip(p,thick,m):
    for a,b in zip(p,p[1:]):face([a,b,add(b,thick),add(a,thick)],m)
def conform(fn,uvrect,rect,nu=12,nv=6):
    a,b,c,d=uvrect;x,y,X,Y=rect
    for i in range(nu):
        for j in range(nv):
            u=i/nu;U=(i+1)/nu;v=j/nv;V=(j+1)/nv
            coords=[(u,v),(U,v),(U,V),(u,V)]
            face([fn(a+(b-a)*k,c+(d-c)*h) for k,h in coords],'Decal',uv=[((x+(X-x)*k)/2048,(Y+(y-Y)*h)/2048) for k,h in coords])
def plate(p,m,depth=(0,-.013,0)):
    face(p,m);q=[add(i,depth) for i in p];face(q[::-1],m)
    for i in range(len(p)):face([p[i],q[i],q[(i+1)%len(p)],p[(i+1)%len(p)]],m)
component_meta={}
component_meta={}
def component(en,zh,family,travel):
    part(en)
    component_meta[cur]=dict(zh=zh,en=en,family=family,vec=travel)

def radial(c,axis,angle,r):
    u,v=basis(unit(axis))
    return add(c,add(mul(u,r*cos(angle)),mul(v,r*sin(angle))))

def shell(c,axis,profile,m,N=40):
    """Surface of revolution. Profile is a closed sequence of (axial distance, radius)."""
    d=unit(axis);u,v=basis(d)
    for (h,r),(H,R) in zip(profile,profile[1:]):
        if r==R and H==h:continue
        for j in range(N):
            ns=[add(mul(u,cos(2*pi*k/N)),mul(v,sin(2*pi*k/N))) for k in (j,j+1)]
            def vertex(ax,rr,n):return add(add(c,mul(d,ax)),mul(n,rr))
            points=[vertex(h,r,ns[0]),vertex(h,r,ns[1]),vertex(H,R,ns[1]),vertex(H,R,ns[0])]
            normals=[unit(add(mul(n,H-h),mul(d,r-R))) for n in (ns[0],ns[1],ns[1],ns[0])]
            face(points,m,normals)
def sleeve(c,axis,ro,ri,length,m,N=40):
    a=length/2;b=min((ro-ri)*.22,length*.12,.0017)
    shell(c,axis,[(-a,ri),(-a,ro-b),(-a+b,ro),(a-b,ro),(a,ro-b),(a,ri),(a-.0003,ri),(-a,ri)],m,N)
def bolt(c,axis,r,m='Steel'):
    d=unit(axis);cyl(c,add(c,mul(d,r*.67)),r,m,6)
def spline(anchors,steps=6):
    """Catmull-Rom centreline through the anchor points."""
    pts=[]
    for i in range(len(anchors)-1):
        a,b,c,d=[anchors[clamp(j,0,len(anchors)-1)] for j in (i-1,i,i+1,i+2)]
        for t in seq(0,1,steps)[:-1]:
            pts.append(tuple(.5*((2*y)+(-x+z)*t+(2*x-5*y+4*z-w)*t*t+(-x+3*y-3*z+w)*t**3) for x,y,z,w in zip(a,b,c,d)))
    pts.append(anchors[-1]);return pts
def pipe(anchors,r,m,N=12):
    pts=spline(anchors);last=None
    for i,p in enumerate(pts):
        tangent=unit(sub(pts[min(i+1,len(pts)-1)],pts[max(0,i-1)]))
        if last is None:u,v=basis(tangent)
        else:u=unit(sub(u,mul(tangent,dot(tangent,u))));v=cross(tangent,u)
        ns=[add(mul(u,cos(2*pi*k/N)),mul(v,sin(2*pi*k/N))) for k in range(N)]
        ring=[add(p,mul(n,r)) for n in ns]
        if last:
            for k in range(N):
                j=(k+1)%N;face([last[k],last[j],ring[j],ring[k]],m,[ln[k],ln[j],ns[j],ns[k]])
        last,ln=ring,ns

def gear(c,axis,rad,bore,w,teeth,m='Steel',phase=0,helix=0,cone=0,witness=False):
    """Open-bore gear with chamfered faces and a flanked tooth profile."""
    d=unit(axis);u,v=basis(d)
    pts=[]
    for i in range(teeth):
        for a,f in [(0,.90),(.16,.90),(.32,1),(.58,1),(.77,.90)]:
            pts.append((2*pi*(i+a)/teeth+phase,rad*f))
    def pt(h,a,r):
        r*=1+cone*h/w
        return add(c,add(mul(d,h),add(mul(u,r*cos(a)),mul(v,r*sin(a)))))
    for j,(a,r) in enumerate(pts):
        A,R=pts[(j+1)%len(pts)]
        finish='Ivory' if witness and j<5 else m
        for h,H,f,F in [(-w*.5,-w*.40,.98,1),(-w*.4,w*.4,1,1),(w*.4,w*.5,1,.98)]:
            face([pt(h,a+helix*h/w,r*f),pt(h,A+helix*h/w,R*f),pt(H,A+helix*H/w,R*F),pt(H,a+helix*H/w,r*F)],finish)
        for h in [-w*.5,w*.5]:
            q=a+helix*h/w;Q=A+helix*h/w
            face([pt(h,q,bore),pt(h,q,r*.98),pt(h,Q,R*.98),pt(h,Q,bore)],finish)
        face([pt(-w*.5,a-helix/2,bore),pt(w*.5,a+helix/2,bore),pt(w*.5,A+helix/2,bore),pt(-w*.5,A-helix/2,bore)],finish)
Y=(0,1,0);Z=(0,0,1);X=(1,0,0)
