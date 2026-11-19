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
for a in [('Ivory','F2F1E9',.14,.26),('Pearl','D4D4C9',.25,.35),('Navy','0C1B33',.13,.31),('Blue','50A7D3',.1,.32),('Red','DC182B',.13,.31),('Rubber','22252A',0,.84),('Tread','2A2C30',0,.88),('Charcoal','252B30',.25,.47),('Black','141A20',.14,.5),('Gunmetal','515B61',.62,.39),('Steel','9CA7AA',.8,.31),('Silver','CBCECA',.75,.28),('Alloy','E2DFD3',.48,.31),('Glass','344955',.43,.15),('Lens','DCE3E0',.48,.16),('Amber','E39B31',.18,.22),('Tail','AD2725',.15,.2),('Gold','B39663',.67,.35),('Exhaust','A9A69D',.72,.46),('Seat','30363B',0,.9),('Belt','B9282D',0,.78),('Engine','912B2B',.48,.37),('Decal','FFFFFF',0,.44)]:mat(*a)
glassmat=materials[mids['Glass']];glassmat['alphaMode']='BLEND';glassmat['pbrMetallicRoughness']['baseColorFactor'][3]=.69
materials[-1]['pbrMetallicRoughness']['baseColorTexture']={'index':0}
materials[-1]['alphaMode']='MASK';materials[-1]['alphaCutoff']=.32
mat('Optical glass','E4F0ED',.08,.11)
materials[-1]['alphaMode']='BLEND';materials[-1]['pbrMetallicRoughness']['baseColorFactor'][3]=.20
mat('Reflector','D5D9D7',.96,.11)
# Engine-bay finishes: gold crinkle cam covers, red silicone boots and couplers, black braided hose.
mat('Crinkle','B88F48',.52,.66)
mat('Silicone','C9301F',0,.52)
mat('Braid','23272B',.42,.62)
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
def width(z):return sinterp(z,[(-1.83,.812),(-1.759,.897),(-1.604,.925),(-1.24,.935),(-.89,.907),(-.54,.853),(-.30,.839),(.47,.836),(.69,.851),(.99,.894),(1.22,.909),(1.45,.907),(1.67,.875),(1.86,.837),(1.97,.794)])
# Centreline deck height; the side references give a level 0.845 m waist from the
# rear wings to the screen base and fender crowns falling to a 0.62 m nose.
def top(z):return sinterp(z,[(-1.83,.785),(-1.663,.812),(-1.23,.830),(-.75,.856),(-.56,.872),(-.30,.878),(.40,.878),(.72,.858),(.90,.818),(1.12,.780),(1.30,.773),(1.46,.745),(1.58,.700),(1.76,.683),(1.91,.652),(1.97,.613),(2.0,.598)])
def surface(u,z):
    wave=.064*math.exp(-((z-1.20)/.55)**2)+.030*math.exp(-((z+1.22)/.52)**2)
    a=abs(u)
    return (u*width(z),top(z)+wave*math.exp(-((a-.82)/.25)**2)-.026*max(0,(a-.91)/.09)**1.5,z)
def arch(z):
    d=min(abs(z-1.22),abs(z+1.22));return .319+sqrt(max(0,.356**2-d**2)) if d<=.356 else max(.153,.319-(d-.356)*3.3)
def side(s,v,z):
    high=surface(1,z)[1];low=arch(z)
    y=low*(1-v)+high*v
    # The moulding turns under at the sill and has a shallow return below the waist.
    waist=.010*clamp((.44-y)/.045,0,1)-.017*clamp((.30-y)/.145,0,1)
    return (s*(width(z)-.030*(1-v)+.007*sin(pi*v)+waist),y,z)
def fixedside(s,y,z,offset=0):
    v=clamp((y-arch(z))/max(.014,surface(1,z)[1]-arch(z)),0,1)
    return (side(s,v,z)[0]+s*offset,y,z)
def strip(p,thick,m):
    for a,b in zip(p,p[1:]):face([a,b,add(b,thick),add(a,thick)],m)
def bodysection(z0,z1):
    zz=sorted(set(seq(z0,z1,max(4,int((z1-z0)*26)))+[z for center in [-1.22,1.22] for z in [center+.356*cos(i*pi/28) for i in range(29)] if z0<z<z1]))
    grid(surface,seq(-1,1,40),zz,'Ivory',True)
    for s in [-1,1]:
        grid(lambda v,z:side(s,v,z),seq(0,1,12),zz,'Ivory',s<0)
        for a,b in zip(zz,zz[1:]):
            p=side(s,0,a);q=side(s,0,b)
            face([p,q,add(q,(-s*.035,.002,0)),add(p,(-s*.035,.002,0))],'Charcoal')
        # Thin painted beltline, segmented by wheel openings.
        def sy(z):return .387+.045*max(0,-z-.45)+.014*max(0,z-.45)
        for h,k,m in []:
            for a,b in zip(zz,zz[1:]):
                if min(sy(a)+k-arch(a),sy(b)+k-arch(b))<=.001:continue
                face([fixedside(s,max(arch(a),sy(a)+h),a,.0015),fixedside(s,max(arch(b),sy(b)+h),b,.0015),fixedside(s,sy(b)+k,b,.0015),fixedside(s,sy(a)+k,a,.0015)],m)
def conform(fn,uvrect,rect,nu=12,nv=6):
    a,b,c,d=uvrect;x,y,X,Y=rect
    for i in range(nu):
        for j in range(nv):
            u=i/nu;U=(i+1)/nu;v=j/nv;V=(j+1)/nv
            coords=[(u,v),(U,v),(U,V),(u,V)]
            face([fn(a+(b-a)*k,c+(d-c)*h) for k,h in coords],'Decal',uv=[((x+(X-x)*k)/2048,(Y+(y-Y)*h)/2048) for k,h in coords])
def hoodstripe(lo,hi):
    for s in [-1,1]:
        for u,U,m in [(.55,.588,'Navy'),(.588,.616,'Blue'),(.616,.664,'Red'),(.664,.692,'Blue'),(.692,.736,'Navy')]:
            grid(lambda a,z:add(surface(a*s,z),(0,.003,0)),[u,U],seq(lo,hi,24),m)
def plate(p,m,depth=(0,-.013,0)):
    face(p,m);q=[add(i,depth) for i in p];face(q[::-1],m)
    for i in range(len(p)):face([p[i],q[i],q[(i+1)%len(p)],p[(i+1)%len(p)]],m)
group('nose','Front clamshell','前翻式车头',(0,.49,.77),'四圆灯、中央格栅、百叶散热口及一体式前翼子板。')
part('Front body moulding');bodysection(.722,1.995)
part('Recessed twin headlamps and split grille')
z=1.995
grid(lambda u,t:(u*(.778+.010*t),surface(u*.98,z)[1]*(1-t)+.326*t,z+.006*t),seq(-1,1,48),[0,1],'Ivory')
for s in [-1,1]:
    # Rounded oblong headlamp recess, with two separate ribbed lenses.
    x=s*.591
    pocket=[]
    for k in range(64):
        a=2*pi*k/64
        dx=.094*(1 if cos(a)>=0 else -1)+.096*cos(a)
        pocket.append((x+dx,.435+.096*sin(a),2.012))
    face([(px,py,pz-.024) for px,py,pz in pocket],'Gunmetal')
    for i,p in enumerate(pocket):
        q=pocket[(i+1)%len(pocket)]
        face([p,q,add(q,(0,0,-.024)),add(p,(0,0,-.024))],'Pearl')
    path(pocket+[pocket[0]],.0050,'Ivory',10)
    for dx in [-.093,.093]:
        xx=x+dx;cy=.433
        tor((xx,cy,2.016),(0,0,1),.090,.004,'Gunmetal',48,8)
    box((s*.196,.431,1.990),(.360,.142,.038),'Black')
    for k in range(23):box((s*(.027+.0155*k),.431,2.011),(.0026,.135,.004),'Gunmetal')
    for k in range(8):box((s*.196,.372+k*.017,2.013),(.35,.0028,.003),'Gunmetal')
def apron(x,y):return (x,y,2.013+.014*math.exp(-((y-.15)/.046)**2)-.021*clamp((y-.27)/.06,0,1))
def intake_edge(y):return .454+.040*(y-.186)/.126
for a,b in zip([.116,.149,.186,.22,.266,.312],[.149,.186,.22,.266,.312,.332]):
    if a>=.186 and b<=.312:
        for s in [-1,1]:
            grid(lambda t,y:apron(s*((1-t)*intake_edge(y)+t*.785),y),seq(0,1,16),[a,b],'Ivory')
    else:grid(apron,seq(-.785,.785,64),[a,b],'Ivory')
for s in [-1,1]:
    outer=[apron(s*intake_edge(y),y) for y in [.186,.312]]
    strip(outer,(0,0,-.040),'Gunmetal')
for y in [.186,.312]:
    strip([apron(x,y) for x in seq(-intake_edge(y),intake_edge(y),32)],(0,0,-.040),'Charcoal')
box((0,.249,1.966),(.989,.127,.009),'Black')
for j in range(12):box((0,.192+j*.0105,1.976),(2*intake_edge(.192+j*.0105),.0018,.004),'Gunmetal')
for s in [-1,1]:
    box((s*.556,.238,2.015),(.133,.058,.01),'Black')
    box((s*.70,.229,2.019),(.113,.065,.016),'Amber')
    box((s*.658,.229,2.029),(.033,.060,.009),'Lens')
    for a,b in zip(seq(1.594,1.971,16),seq(1.594,1.971,16)[1:]):
        def cheek(z,y):return fixedside(s,y,z,0)
        low=lambda z:interp(z,[(1.594,.153),(1.82,.132),(1.971,.118)])
        face([cheek(a,low(a)),cheek(b,low(b)),cheek(b,.168),cheek(a,.168)],'Ivory')
for a,b in zip(seq(-.807,.807,40),seq(-.807,.807,40)[1:]):
    plate([(a,.117,2.051),(b,.117,2.051),(b,.119,1.957),(a,.119,1.957)],'Ivory',(0,-.009,0))
part('Bonnet louvres and fasteners')
# Three separate louvred outlets sit in a row just ahead of the screen.
for u0,u1 in [(-.62,-.34),(-.155,.155),(.34,.62)]:
    za,zb=.832,.952
    def vent(u,z,dy=.0035):return add(surface(u,z),(0,dy,0))
    grid(lambda u,z:vent(u,z),seq(u0,u1,8),seq(za,zb,4),'Black')
    for u in (u0,u1):strip([vent(u,z,.001) for z in seq(za,zb,6)],(0,.009,0),'Pearl')
    for z in (za,zb):strip([vent(u,z,.001) for u in seq(u0,u1,8)],(0,.009,0),'Pearl')
    for k in range(6):
        z=za+.010+k*.019
        face([vent(u0+.006,z),vent(u1-.006,z),vent(u1-.006,z+.013,.0085),vent(u0+.006,z+.013,.0085)],'Charcoal')
for s in [-1,1]:
    for z in [.80,1.77]:
        q=surface(s*.82,z);cyl(q,add(q,(0,.007,0)),.019,'Steel',14);cyl(add(q,(-.013,.009,0)),add(q,(.013,.009,0)),.003,'Black',6)
conform(lambda u,z:add(surface(u,z),(0,.006,0)),(-.220,.220,1.86,1.66),(259, 0, 701, 235))
group('tail','Rear clamshell','后翻式发动机罩',(-.45,1.44,-1.07),'后翼子板、透明发动机盖、通风百叶与车尾扰流板。')
part('Rear body and engine aperture')
# Side decks leave a real opening for the engine cover.
zs=seq(-1.8174,-.272,50)
for s in [-1,1]:
    grid(lambda u,z:surface(s*u,z),[.63,.78,.86,.94,1],zs,'Ivory',s>0)
    grid(lambda v,z:side(s,v,z),seq(0,1,12),sorted(set(zs+[-1.22+.356*cos(i*pi/32) for i in range(33)])),'Ivory',s<0)
for a,b in [(-1.8174,-1.36),(-.68,-.272)]:grid(surface,[-.63,0,.63],seq(a,b,6),'Ivory',True)
part('Wheel arch return lips')
for s in [-1,1]:
    for center in [-1.22]:
        lip=[side(s,0,center+.356*cos(i*pi/44)) for i in range(45)]
        strip(lip,(-s*.045,0,0),'Gunmetal')
part('Rear quarter windows and B-pillars')
for s in [-1,1]:
    # Fixed quarter glass between the door shut line and the solid buttress.
    q=[(s*.800,.853,-.285),(s*.553,1.141,-.285),(s*.546,1.125,-.588),(s*.800,.853,-.600)]
    face(q,'Glass');face([add(p,(-s*.002,0,0)) for p in q[::-1]],'Navy')
    path(q+[q[0]],.0045,'Black',6)
    plate([(s*.802,.853,-.258),(s*.553,1.148,-.258),(s*.550,1.148,-.290),(s*.802,.853,-.290)],'Ivory',(-s*.010,0,0))
    rail=[side(s,1,z) for z in seq(-.60,-.285,6)]
    for j in range(6):face([rail[j],rail[j+1],mix(q[3],q[0],(j+1)/6),mix(q[3],q[0],j/6)],'Ivory')
part('Fastback glazing and flying buttresses')
for s in [-1,1]:
    def sail(t,v):
        top_edge=mix((s*.546,1.125,-.60),(s*.792,.927,-1.40),t)
        bottom=mix((s*.800,.853,-.60),(s*.818,.835,-1.40),t)
        return add(mix(bottom,top_edge,v),(s*.012*sin(pi*v),0,0))
    grid(sail,seq(0,1,24),seq(0,1,9),'Ivory')
    path([sail(t,1) for t in seq(0,1,16)],.006,'Ivory',8)
def hatch(x,z):return (x,sinterp(z,[(-1.36,.906),(-1.20,.950),(-1.00,1.013),(-.80,1.073),(-.60,1.130)]),z)
# The engine-cover glazing tapers forward to the narrow roof between the sails.
def hatch_half(z):return sinterp(-z,[(.60,.505),(.75,.535),(1.05,.568),(1.40,.568)])
grid(lambda u,z:hatch(u*hatch_half(z),z),[-1,0,1],seq(-1.36,-.60,12),'Glass',True)
for k in [-1,1]:path([hatch(k*(hatch_half(z)+.014),z) for z in seq(-1.37,-.60,12)],.022,'Black')
for j in range(5):
    z=-1.30+j*.125;w=hatch_half(z)+.005
    plate([add(hatch(x,Z),(0,.016,0)) for x,Z in [(-w,z),(w,z),(w,z+.036),(-w,z+.036)]],'Charcoal')
part('Tail panel and spoiler')
box((0,.553,-1.8168),(1.56,.256,.040),'Ivory');box((0,.393,-1.8049),(1.57,.083,.07),'Charcoal')
box((0,.55,-1.8388),(.72,.152,.012),'Black')
for s in [-1,1]:
    box((s*.572,.566,-1.8422),(.334,.11,.030),'Charcoal')
    for i,m in enumerate(['Tail','Amber']):
        x=s*(.493+i*.15)
        cyl((x,.565,-1.840),(x,.565,-1.852),.067,'Black',48)
        cyl((x,.565,-1.852),(x,.565,-1.862),.059,m,48,.054)
        for rad in [.024,.042,.051]:tor((x,.565,-1.863),(0,0,1),rad,.0017,m,40,6)
        for dx in [-.044,.044]:cyl((x+dx,.565,-1.860),(x+dx,.565,-1.866),.0025,'Silver',10)
# The wing ramps up about 26 degrees from just behind the engine glass to a tip
# only a few centimetres below the roof, as in the side references.
def wing(x,t):
    a=abs(x)/.817;z=-1.36-.498*t
    y=sinterp(-z,[(1.36,.930),(1.414,.960),(1.47,.993),(1.525,1.026),(1.581,1.057),(1.636,1.087),(1.692,1.118),(1.747,1.142),(1.803,1.154),(1.858,1.150)])
    return (x/.817*(width(z)-.036),y+.006*a*a,z+.007*a*a*t)
for s in (-1,1):
    upper=[wing(s*.817,t) for t in seq(0,1,21)]
    # Fin side plates sweep up to a point, leaving the trailing wing open underneath.
    lower=[]
    for i,p in enumerate(upper):
        base=surface(1,p[2])[1]-.006;k=clamp((i/20-.45)/.55,0,1)**1.15
        lower.append((p[0],base+(p[1]-.030-base)*k,p[2]))
    for i in range(20):
        plate([lower[i],lower[i+1],upper[i+1],upper[i]],'Ivory',(s*.007,0,0))
path([wing(x,1) for x in seq(-.817,.817,40)],.0055,'Ivory',10)
grid(wing,seq(-.817,.817,16),seq(0,1,10),'Ivory')
grid(lambda x,t:add(wing(x,t),(0,-.007,-.005)),[-.817,.817],seq(0,1,10),'Pearl')
for s in [-1,1]:strip([wing(s*.817,t) for t in seq(0,1,12)],(0,-.008,-.005),'Pearl')
conform(lambda x,t:add(wing(x,t),(0,.003,.004)),(-.745,.745,.60,.83),(13,659,1444,776),32,4)
decal([(.25,.519,-1.844),(-.25,.519,-1.844),(-.25,.582,-1.844),(.25,.582,-1.844)],(7,264,568,335))
group('canopy','Roof and windscreen','车顶与风挡',(-.45,1.72,.015),'弧面前风挡、A 柱、车顶和雨刮器组成的可拆展示单元。')
part('Windscreen, surround and wipers')
def wind(u,t):
    corner=abs(u)**8
    # Narrow screen with strongly raked-in pillars leaves broad wing shoulders either side.
    return (u*(.700-.160*t-.020*t**6),.857+.335*t+.022*sin(pi*t)+.013*(1-u*u)+.013*corner*(1-t)**5-.021*corner*t**5,
            .695-.635*t+.040*(1-u*u)-.013*corner*(1-t)**5)
grid(wind,seq(-1,1,32),seq(0,1,12),'Glass')
for s in [-1,1]:
    path([wind(s,t) for t in seq(0,1,18)],.011,'Black')
for t in [0,1]:path([wind(u,t) for u in seq(-1,1,32)],.008,'Black')
grid(lambda u,t:add(wind(u,t),(0,.002,.003)),seq(-1,1,10),[.844,.995],'Navy')
conform(lambda u,t:add(wind(u,t),(0,.004,.006)),(-.91,.91,.855,.982),(10,524,1293,643),16,2)
for s in [-1,1]:
    pts=[add(wind(s*.57,.025),(0,.006,.009)),add(wind(s*.27,.19),(0,.006,.011))]
    path(pts,.006,'Charcoal')
    path([add(wind(s*.57,.134),(0,.011,.014)),add(wind(-s*.04,.235),(0,.011,.014))],.007,'Black')
part('Crowned roof')
def roof(u,z):
    # Crown peaks above the B-pillar and falls away to the screen and the engine cover.
    w=sinterp(z,[(-.60,.530),(-.50,.548),(-.03,.556),(.05,.535)])
    fall=(.030 if z>-.24 else .062)*((z+.24)/.37)**2
    return (u*w,1.209+.017*(1-u*u)+.020*math.exp(-((abs(u)-.51)/.27)**2)*max(0,1-((z+.24)/.40)**4)-fall-.011*abs(u)**8,z)
grid(roof,seq(-1,1,44),seq(-.60,.05,18),'Ivory',True)
grid(lambda u,t:mix(roof(u,.05),add(wind(u,1),(0,.006,0)),t),seq(-1,1,40),[0,1],'Ivory')
for s in [-1,1]:
    path([roof(s,z) for z in seq(-.60,.05,7)],.012,'Pearl')
# Close the step from the roof trailing edge down to the engine-cover glazing.
grid(lambda u,t:mix(roof(u*.95,-.60),hatch(u*hatch_half(-.60),-.60),t),seq(-1,1,20),[0,1],'Ivory')
part('Roof air scoop')
# Low NACA-style cabin intake just behind the screen header, open to the front.
def scoop(u,z,top):
    h=.026*clamp((z+.125)/.125,0,1)**.7 if top else 0
    return add(roof(u,z),(0,h,0))
su=.215;sz=seq(-.125,.005,8)
grid(lambda u,z:scoop(u,z,True),seq(-su,su,10),sz,'Ivory',True)
for k in [-1,1]:
    for a,b in zip(sz,sz[1:]):face([scoop(k*su,a,False),scoop(k*su,b,False),scoop(k*su,b,True),scoop(k*su,a,True)],'Ivory')
mouth_lo=[scoop(u,.005,False) for u in seq(-su,su,10)];mouth_hi=[scoop(u,.005,True) for u in seq(-su,su,10)]
for a,b,c,d in zip(mouth_lo,mouth_lo[1:],mouth_hi[1:],mouth_hi):face([a,b,c,d],'Black')
path(mouth_hi,.003,'Pearl',6)
for s in [-1,1]:
    group('door'+str(s),'Left door' if s>0 else 'Right door','左侧车门' if s>0 else '右侧车门',(s*1.22,.33,.16),'独立车门带侧窗、车号板、拉手与外后视镜。')
    part('Door outer skin and trim')
    zz=seq(-.268,.718,22)
    grid(lambda v,z:side(s,v,z),seq(0,1,12),zz,'Ivory',s<0)
    for z in [-.268,.718]:
        path([side(s,v,z) for v in [0,.5,1]],.005,'Black')
    for a,b,m in []:
        grid(lambda v,z:fixedside(s,v,z,.003),[a,b],zz,m)
    for v in [0,1]:
        strip([side(s,v,z) for z in zz],(-s*.070,0,0),'Pearl')
    for z in [-.262,.712]:
        strip([side(s,v,z) for v in [0,1]],(-s*.07,0,0),'Pearl')
    part('Side glass, window frames and door mirror')
    pts=[(s*.807,.853,.640),(s*.552,1.133,.085),(s*.553,1.148,-.255),(s*.800,.853,-.255)]
    # Rubber seal follows the rounded corners of the pressed door opening.
    outline=[]
    for i,P in enumerate(pts):
        a=mix(P,pts[i-1],.105);b=mix(P,pts[(i+1)%4],.105)
        curve=[mix(mix(a,P,t),mix(P,b,t),t) for t in seq(0,1,7)]
        for c,d in zip(curve,curve[1:]):face([P,c,d],'Ivory')
        outline.extend(curve)
    glass_centre=tuple(sum(q[k] for q in pts)/4 for k in range(3))
    for i,q in enumerate(outline):face([glass_centre,q,outline[(i+1)%len(outline)]],'Glass')
    rail=[side(s,1,z) for z in seq(-.255,.64,16)]
    for j in range(16):
        k=j/16;K=(j+1)/16
        face([rail[j],rail[j+1],mix(pts[3],pts[0],K),mix(pts[3],pts[0],k)],'Ivory')
    path(outline+[outline[0]],.009,'Black')
    path([pts[1],pts[2],pts[3]],.014,'Ivory')
    path([mix(pts[0],pts[3],.7),mix(pts[1],pts[2],.73)],.008,'Charcoal')
    box((s*.845,.735,-.170),(.027,.031,.116),'Charcoal')
    cyl((s*.800,.866,.585),(s*.934,.887,.575),.019,'Charcoal',10)
    def mirror(a,t):
        r=sqrt(max(.065,1-t*t))
        return (s*(.949+.060*r*cos(a)),.889+.044*r*sin(a),.495+.119*t)
    grid(mirror,seq(0,2*pi,40),seq(0,.985,15),'Navy')
    face([mirror(a,0) for a in seq(0,2*pi,40)[:-1]],'Glass')
    path([mirror(a,0) for a in seq(0,2*pi,40)],.003,'Black',6)
group('chassis','Chassis and spaceframes','底盘与管架',(0,0,0),'中央承载结构与前后管式副车架，作为拆解定位基准。')
part('Central tub and sills')
box((0,.198,0),(1.44,.071,1.52),'Gunmetal')
for s in [-1,1]:
    box((s*.711,.254,.025),(.136,.18,1.25),'Charcoal')
    box((s*.772,.207,.022),(.050,.061,1.30),'Ivory')
box((0,.447,-.525),(1.38,.462,.053),'Gunmetal')
part('Triangulated front and rear frames')
for end,length in [(1,1.83),(-1,1.764)]:
    for s in [-1,1]:
        a=(s*.656,.222,end*.63);b=(s*.539,.261,end*length);c=(s*.588,.594,end*1.24);d=(s*.598,.544,end*.64)
        for p,q in [(a,b),(b,c),(c,d),(d,a),(a,c)]:cyl(p,q,.021,'Charcoal',10)
        cyl((s*.57,.257,end*1.25),(s*.588,.594,end*1.24),.020,'Charcoal',10)
    for z,y,w in [(length,.26,.54),(1.24,.586,.59),(.65,.24,.65)]:cyl((-w,y,end*z),(w,y,end*z),.018,'Charcoal',10)
    cyl((-.54,.26,end*length),(.58,.56,end*1.245),.013,'Charcoal',10)
part('Front radiator and cooling fan')
box((0,.395,1.696),(.94,.31,.088),'Charcoal')
for i in range(25):box(((i-12)*.035,.394,1.746),(.009,.274,.007),'Steel')
for j in range(9):box((0,.278+j*.03,1.751),(.90,.004,.007),'Gunmetal')
for s in [-1,1]:
    tor((s*.234,.406,1.642),(0,0,1),.135,.012,'Black',32)
    cyl((s*.234,.406,1.626),(s*.234,.406,1.653),.038,'Black')
    for j in range(6):
        a=j*pi/3;face([(s*.234+r*cos(a+t),.406+r*sin(a+t),1.64) for r,t in [(.026,0),(.125,.18),(.133,.55),(.032,.3)]],'Gunmetal')
group('cockpit','Cockpit and roll cage','驾驶舱与防滚架',(-.18,.73,.05),'双桶椅、四点式安全带、方向盘、仪表台与钢管防滚架。')
part('Cockpit floor and dashboard')
box((0,.256,.01),(1.32,.046,1.03),'Black');box((0,.363,.04),(.203,.182,.97),'Charcoal')
box((0,.649,.560),(1.32,.119,.332),'Charcoal')
for i in range(5):
    x=.54-i*.095;r=.039 if i in [1,2] else .028
    cyl((x,.656,.385),(x,.656,.378),r,'Silver',20)
    cyl((x,.656,.378),(x,.656,.375),r*.86,'Black',20)
    path([(x-.004,.65,.372),(x+.013,.663,.372)],.0023,'Ivory',5)
part('Steering wheel')
tor((.376,.687,.183),(0,.32,-1),.135,.013,'Rubber',48)
for a in [0,pi,1.5*pi]:
    cyl((.376,.687,.183),(.376+.122*cos(a),.687+.119*sin(a),.183+.038*sin(a)),.009,'Gunmetal',8)
# Index stripe at the top of the wheel gives the driver's handwheel a visible zero.
wheel_index=(.376,.687+.135/sqrt(1+.32**2),.183+.135*.32/sqrt(1+.32**2))
cyl(add(wheel_index,(-.008,0,0)),add(wheel_index,(.008,0,0)),.0138,'Gold',20)
part('Gear selector and pedals')
cyl((0,.44,.086),(0,.599,.055),.008,'Steel')
cyl((0,.581,.055),(0,.616,.055),.021,'Black',16)
for i in range(3):box((.452-i*.076,.296,.427),(.045,.019,.072),'Silver')
for s in [-1,1]:
    part('Bucket seat and harness '+str(s));x=s*.346
    def seat(u,t):
        y,z,w= [( .327,.226,.201),(.298,-.197,.207),(.376,-.276,.212),(.614,-.343,.206),(.806,-.393,.16),(.867,-.414,.112)][t]
        return (x+u*w,y+abs(u)**3*(.08 if t<2 else .01),z+abs(u)**3*(.08 if 1<t<5 else .0))
    grid(seat,seq(-1,1,8),list(range(6)),'Seat')
    for u in [-1,1]:
        path([seat(u,j) for j in range(6)],.013,'Black')
        for j in range(5):
            a=seat(u,j);b=seat(u,j+1);face([a,b,add(b,(0,-.025,-.025)),add(a,(0,-.025,-.025))],'Black')
        pts=[(x+u*.095,.803,-.367),(x+u*.104,.637,-.308),(x+u*.078,.395,-.23),(x+u*.023,.337,-.13)]
        strip([add(p,(-.017,0,0)) for p in pts],(.034,0,0),'Belt')
        box((x+u*.097,.62,-.299),(.048,.031,.009),'Steel')
    box((x,.342,-.108),(.066,.021,.055),'Gunmetal')
part('Roll-over protection')
for z,y in [(-.445,1.058),(.495,.784)]:
    pts=[(-.638,.288,z),(-.635,y-.11,z),(-.535,y,z),(.535,y,z),(.635,y-.11,z),(.638,.288,z)]
    path(pts,.023,'Steel',10)
for s in [-1,1]:
    path([(s*.525,1.046,-.446),(s*.530,1.052,.16),(s*.640,.775,.501)],.021,'Steel',10)
    cyl((s*.627,.328,.47),(s*.627,.68,-.442),.017,'Steel',10)
cyl((-.585,.385,-.447),(.562,1.025,-.447),.018,'Steel')
exec(compile((ROOT/'src/power.py').read_text(encoding='utf-8-sig'),'power.py','exec'))
exec(compile((ROOT/'src/suspension.py').read_text(encoding='utf-8'),'suspension.py','exec'))
for z in [-1.22,1.22]:
    for s in [-1,1]:
        rear=z<0;lab=('后' if rear else '前')+('左' if s>0 else '右')
        group(('rear' if rear else 'front')+('L' if s>0 else 'R'),('Rear' if rear else 'Front')+(' left wheel' if s>0 else ' right wheel'),lab+'车轮',(s*1.02,-.055,(-.26 if rear else .26)),'拉力胎、白色多孔合金轮圈、轮毂与紧固螺栓。')
        part('Rally tyre and sidewall');xc=.79 if rear else .773;w=.257 if rear else .213;R=.318
        profile=[(-.5,.193),(-.50,.249),(-.47,.287),(-.40,.308),(-.31,.317),(0,.319),(.31,.317),(.40,.308),(.47,.287),(.50,.249),(.50,.193)]
        def tire(i,a):
            x,r=profile[i];return (s*(xc+x*w),.319+r*cos(a),z+r*sin(a))
        grid(tire,list(range(len(profile))),seq(0,2*pi,72),'Rubber')
        for i in range(54):
            a=i*2*pi/54
            for k in [-1,1]:
                def tread(u,ang):
                    radius=.3195-.007*(abs(u)/.4)**3
                    return (s*(xc+u*w),.319+radius*cos(ang),z+radius*sin(ang))
                face([tread(k*u,a+d) for u,d in [(.015,0),(.37,.036),(.38,.072),(.014,.036)]],'Tread')
        outer=xc+.50*w
        for r in [.217,.264,.282]:tor((s*(outer-.001),.319,z),(1,0,0),r,.0018,'Tread',64,6)
        part('Cast alloy wheel and lug hardware')
        def wx(x):return (s*x,.319,z)
        sleeve(wx((xc-w*.50+outer-.014)/2),X,.200,.177,w-.014,'Gunmetal',72)
        for radius,depth,wire in [(.194,.003,.005),(.187,-.009,.006),(.170,-.012,.005)]:
            tor(wx(outer+depth),X,radius,wire,'Silver',80,8)
        # Map a ring of circular holes onto a dished face in polar sectors.
        count=12
        for j in range(count):
            centre=j*2*pi/count
            rmid=.133;lo=.087;hi=.178
            def rimpoint(u,v,back=0):
                r=rmid+v*(hi-rmid if v>=0 else rmid-lo)
                a=centre+u*pi/count
                return (s*(outer-.030+.018*v*v+back),.319+r*cos(a),z+r*sin(a))
            loops=[]
            for h in [0,1]:
                ring=[]
                for angle in seq(0,2*pi,32)[:-1]:
                    u,v=cos(angle),sin(angle)
                    if h==0:
                        u*=.024/(rmid*pi/count);v*=.024/(hi-rmid)
                    else:
                        scale=max(abs(u),abs(v));u/=scale;v/=scale
                    ring.append((u,v))
                loops.append(ring)
            for k in range(32):
                K=(k+1)%32
                face([rimpoint(*a) for a in [loops[0][k],loops[0][K],loops[1][K],loops[1][k]]],'Silver')
                a,b=loops[0][k],loops[0][K]
                face([rimpoint(*a),rimpoint(*b),rimpoint(*b,-.012),rimpoint(*a,-.012)],'Gunmetal')
            a=centre+.05
            cyl((s*(outer-.009),.319+.181*cos(a),z+.181*sin(a)),(s*(outer+.001),.319+.181*cos(a),z+.181*sin(a)),.0035,'Steel',10)
        cyl(wx(outer-.039),wx(outer-.009),.088,'Silver',56,.080)
        for j in range(4):
            a=pi/4+j*pi/2;y=.319+.055*cos(a);Z=z+.055*sin(a)
            cyl((s*(outer+.001),y,Z),(s*(outer+.010),y,Z),.014,'Gunmetal',6)
        cyl(wx(outer+.001),wx(outer+.014),.033,'Gunmetal',20)
        cyl(wx(outer+.014),wx(outer+.017),.022,'Black',24)

group('lamps','Auxiliary light pod','夜赛辅助灯组',(0,.55,1.58),'四盏辅助拉力灯及管式支架，安装在车头前缘。')
part('Lamp carrier and stays')
path([(-.443,.565,1.989),(.443,.565,1.989)],.014,'Charcoal',12)
for k in [-1,1]:
    path([(k*.34,.559,1.853),(k*.34,.565,1.989),(k*.34,.590,2.003)],.014,'Gunmetal',10)
part('Four competition driving lamps')
for x in [-.349,-.121,.121,.349]:
    y=.590 if abs(x)>.2 else .596
    Z=2.023-.036*abs(x)
    cyl((x,y,Z-.098),(x,y,Z-.035),.044,'Charcoal',40,.103)
    tor((x,y,Z+.010),(0,0,1),.102,.008,'Ivory',56,10)
exec(compile((ROOT/'src/trim.py').read_text(encoding='utf-8-sig'),'trim.py','exec'))

# Retain the 2.440 m axle spacing. Set the outer coachwork to the nominal
# 3.915 m length, 1.850 m maximum body width and 1.245 m roof height.
def calibrate_coachwork():
    width_scale=.925/.93495
    for (assembly,name),primitives in parts.items():
        body=assembly in ('nose','tail','canopy','door1','door-1','lamps')
        if not body:continue
        for positions,normals,_,_ in primitives.values():
            for k in range(0,len(positions),3):
                x,y,z=positions[k:k+3]
                sx=width_scale if body else 1.
                sy=1.;sz=1.
                # Carry the fender shoulders and lamp pockets around the nose in plan.
                nx,ny,nz=normals[k:k+3]
                if assembly=='nose' and z>1.62:
                    blend=clamp((z-1.62)/.35,0,1)
                    setback=.060*(abs(x)/.8)**3
                    dzdx=-.180*x*abs(x)/.8**3*blend**2*(3-2*blend)
                    dzdz=1-setback*6*blend*(1-blend)/.35
                    z-=setback*blend**2*(3-2*blend)
                    nz/=dzdz;nx-=dzdx*nz
                positions[k:k+3]=array.array('f',(x*sx,y,z))
                normals[k:k+3]=array.array('f',unit((nx/sx,ny/sy,nz/sz)))
calibrate_coachwork()
blob=bytearray();views=[];accessors=[]
def bv(data,target=None):
    while len(blob)%4:blob.append(0)
    d=dict(buffer=0,byteOffset=len(blob),byteLength=len(data))
    if target:d['target']=target
    views.append(d);blob.extend(data);return len(views)-1
def acc(data,kind,typ,target=None,bounds=False):
    dim={'SCALAR':1,'VEC3':3,'VEC2':2}[kind];d=dict(bufferView=bv(data.tobytes(),target),componentType=typ,count=len(data)//dim,type=kind)
    if bounds:
        d['min']=[min(data[i::dim]) for i in range(dim)];d['max']=[max(data[i::dim]) for i in range(dim)]
    accessors.append(d);return len(accessors)-1
nodes=[];roots=[];meshes=[];channels=[];samplers=[]
time=acc(array.array('f',[0,3]),'SCALAR',5126,bounds=True)
internal_clips={}
for key,info in groups.items():
    info['key']=key
    idx=len(nodes);roots.append(idx)
    node=dict(name=info['zh']+' | '+info['en'],children=[],extras=info);nodes.append(node)
    if any(info['vec']):
        samplers.append(dict(input=time,output=acc(array.array('f',[0,0,0,*info['vec']]),'VEC3',5126),interpolation='LINEAR'))
        channels.append(dict(sampler=len(samplers)-1,target=dict(node=idx,path='translation')))
    for (g,n),v in parts.items():
        if g!=key:continue
        prims=[];meta=component_meta.get((g,n));pivot=(0,0,0)
        if meta:
            pivot=tuple((min(min(data[0][i::3]) for data in v.values())+max(max(data[0][i::3]) for data in v.values()))/2 for i in range(3))
        for m,(pos,nor,tex,ind) in v.items():
            P=array.array('f');N=array.array('f');T=array.array('f');ids={};mapping=[]
            for j in range(len(pos)//3):
                p=pos[j*3:j*3+3];normal=nor[j*3:j*3+3];t=tex[j*2:j*2+2];k=p.tobytes()+normal.tobytes()+t.tobytes()
                if k not in ids:
                    ids[k]=len(P)//3;P.extend(sub(p,pivot) if meta else p);N.extend(normal);T.extend(t)
                mapping.append(ids[k])
            indices=array.array('H' if len(mapping) and max(mapping)<65536 else 'I',(mapping[i] for i in ind))
            attr=dict(POSITION=acc(P,'VEC3',5126,34962,True),NORMAL=acc(N,'VEC3',5126,34962))
            if T:attr['TEXCOORD_0']=acc(T,'VEC2',5126,34962)
            prims.append(dict(attributes=attr,indices=acc(indices,'SCALAR',5123 if indices.typecode=='H' else 5125,34963),material=mids[m]))
        child=dict(name=n,mesh=len(meshes));childID=len(nodes)
        # Rigid rotor and halfshaft axes attach to real assembly-space endpoints.
        if key in ('rearL','rearR'):
            child['extras']=dict(driveRole='wheel',side=1 if key=='rearL' else -1,axis=[1,0,0],pivot=[0,.319,-1.22])
        if key in ('frontL','frontR') or (key=='susp' and n.startswith(('Front brake rotor','Front caliper'))):
            side_=(1 if key=='frontL' else -1) if key!='susp' else int(n.split()[-1])
            role='caliper' if n.startswith('Front caliper') else 'frontWheel'
            child['extras']=dict(driveRole=role,side=side_,pivot=[side_*.773,.319,1.22],axis=[1,0,0])
        if key=='cockpit' and n=='Steering wheel':
            child['extras']=dict(driveRole='handwheel',pivot=[.376,.687,.183],axis=unit((0,.32,-1)))
        if key=='susp' and n.startswith(('Rear halfshaft','Rear brake rotor')):
            side_=int(n.split()[-1])
            inner=(side_*.174,.315,-1.291);outer=(side_*.770,.319,-1.22)
            child['extras']=(dict(driveRole='axle',side=side_,pivot=inner,axis=mul(unit(sub(outer,inner)),side_))
                if n.startswith('Rear halfshaft') else dict(driveRole='disc',side=side_,pivot=outer,axis=[1,0,0]))
        if meta:
            meta.update(child.get('extras', {}))
            child.update(name=meta['zh']+' | '+n,translation=pivot,extras=meta)
            clip=internal_clips.setdefault(key,dict(name=info['en']+' - components',samplers=[],channels=[]))
            clip['channels'].append(dict(sampler=len(clip['samplers']),target=dict(node=childID,path='translation')))
            clip['samplers'].append(dict(input=time,output=acc(array.array('f',[*pivot,*add(pivot,meta['vec'])]),'VEC3',5126),interpolation='LINEAR'))
        node['children'].append(childID);nodes.append(child);meshes.append(dict(name=n,primitives=prims))
imageview=bv((ROOT/'src/decals.png').read_bytes())
gltf=dict(asset=dict(version='2.0',generator='Procedural Lancia Rally 037 study'),scene=0,scenes=[dict(name='Lancia Rally 037',nodes=roots)],nodes=nodes,meshes=meshes,materials=materials,accessors=accessors,bufferViews=views,buffers=[dict(byteLength=len(blob))],images=[dict(name='Rally markings',bufferView=imageview,mimeType='image/png')],textures=[dict(source=0,sampler=0)],samplers=[dict(magFilter=9729,minFilter=9987,wrapS=33071,wrapT=33071)],animations=[dict(name='Exploded view',channels=channels,samplers=samplers)])
gltf['animations'].extend(internal_clips.values())
j=json.dumps(gltf,separators=(',',':'),ensure_ascii=False).encode();j+=b' '*((-len(j))%4)
blob.extend(b'\0'*((-len(blob))%4))
glb=struct.pack('<4sII',b'glTF',2,28+len(j)+len(blob))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(blob),b'BIN\0')+blob
(OUT/'Lancia_037.glb').write_bytes(glb)
print(len(groups),'assemblies,',len(meshes),'parts,',sum(accessors[p['indices']]['count']//3 for mesh in meshes for p in mesh['primitives']),'triangles,',len(glb),'bytes')

