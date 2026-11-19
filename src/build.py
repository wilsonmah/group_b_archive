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
for a in [('Ivory','F2F1E9',.14,.26),('Pearl','D4D4C9',.25,.35),('Navy','0C1B33',.13,.31),('Blue','50A7D3',.1,.32),('Red','DC182B',.13,.31),('Rubber','22252A',0,.84),('Tread','2A2C30',0,.88),('Charcoal','252B30',.25,.47),('Black','141A20',.14,.5),('Gunmetal','515B61',.62,.39),('Steel','9CA7AA',.8,.31),('Silver','CBCECA',.75,.28),('Alloy','E2DFD3',.48,.31),('Glass','344955',.43,.15),('Lens','DCE3E0',.48,.16),('Amber','E39B31',.18,.22),('Tail','AD2725',.15,.2),('Gold','B39663',.67,.35),('Exhaust','8D7562',.7,.39),('Seat','30363B',0,.9),('Belt','B9282D',0,.78),('Engine','912B2B',.48,.37),('Decal','FFFFFF',0,.44)]:mat(*a)
glassmat=materials[mids['Glass']];glassmat['alphaMode']='BLEND';glassmat['pbrMetallicRoughness']['baseColorFactor'][3]=.55
materials[-1]['pbrMetallicRoughness']['baseColorTexture']={'index':0}
materials[-1]['alphaMode']='MASK';materials[-1]['alphaCutoff']=.32
mat('Optical glass','E4F0ED',.08,.11)
materials[-1]['alphaMode']='BLEND';materials[-1]['pbrMetallicRoughness']['baseColorFactor'][3]=.20
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
def decal(p,rect):
    x,y,X,Y=rect;face(p,'Decal',uv=[(x/2048,Y/2048),(X/2048,Y/2048),(X/2048,y/2048),(x/2048,y/2048)])
def width(z):return interp(z,[(-2,.77),(-1.81,.91),(-1.24,.935),(-.63,.866),(-.47,.837),(.56,.823),(1.18,.907),(1.56,.888),(1.9,.81),(2,.775)])
def top(z):return interp(z,[(-2,.716),(-1.74,.779),(-1.23,.813),(-.56,.80),(0,.734),(.57,.737),(1.12,.681),(1.47,.636),(1.79,.583),(2,.536)])
def surface(u,z):
    wave=.077*math.exp(-((z-1.22)/.45)**2)+.024*math.exp(-((z+1.22)/.47)**2)
    a=abs(u);return (u*width(z),top(z)+wave*min(1,a/.79)**3-.035*max(0,(a-.86)/.14),z)
def arch(z):
    d=min(abs(z-1.22),abs(z+1.22));return .319+sqrt(max(0,.356**2-d**2)) if d<=.356 else max(.153,.319-(d-.356)*3.3)
def side(s,v,z):
    high=surface(1,z)[1];low=arch(z)
    return (s*(width(z)-.035*(1-v)+.007*sin(pi*v)),low*(1-v)+high*v,z)
def fixedside(s,y,z,offset=0):
    v=clamp((y-arch(z))/max(.014,surface(1,z)[1]-arch(z)),0,1)
    return (side(s,v,z)[0]+s*offset,y,z)
def strip(p,thick,m):
    for a,b in zip(p,p[1:]):face([a,b,add(b,thick),add(a,thick)],m)
def bodysection(z0,z1):
    zz=sorted(set(seq(z0,z1,max(4,int((z1-z0)*26)))+[z for center in [-1.22,1.22] for z in [center+.356*cos(i*pi/28) for i in range(29)] if z0<z<z1]))
    grid(surface,[-1,-.93,-.86,-.77,-.68,-.47,0,.47,.68,.77,.86,.93,1],zz,'Ivory',True)
    for s in [-1,1]:
        grid(lambda v,z:side(s,v,z),[0,.14,.8,1],zz,'Ivory',s<0)
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
part('Front body moulding');bodysection(.604,1.97)
part('Recessed twin headlamps and split grille')
z=1.97
face([(-.778,.536,z),(.778,.536,z),(.788,.326,z+.031),(-.788,.326,z+.031)],'Ivory')
for s in [-1,1]:
    # Rounded oblong headlamp recess, with two separate ribbed lenses.
    x=s*.591
    box((x,.432,1.991),(.363,.172,.030),'Pearl')
    for dx in [-.093,.093]:
        xx=x+dx;cy=.433
        tor((xx,cy,2.016),(0,0,1),.083,.005,'Ivory',48,8)
    box((s*.196,.431,1.990),(.360,.142,.038),'Black')
    for k in range(23):box((s*(.027+.0155*k),.431,2.011),(.0026,.135,.004),'Gunmetal')
    for k in range(8):box((s*.196,.372+k*.017,2.013),(.35,.0028,.003),'Gunmetal')
box((0,.222,1.979),(1.569,.207,.067),'Ivory')
box((0,.249,2.015),(.825,.112,.010),'Black')
for j in range(12):box((0,.200+j*.0086,2.022),(.811,.0027,.004),'Gunmetal')
for s in [-1,1]:
    box((s*.556,.238,2.015),(.133,.058,.01),'Black')
    box((s*.70,.229,2.019),(.113,.065,.016),'Amber')
    box((s*.658,.229,2.029),(.033,.060,.009),'Lens')
    for a,b in zip(seq(1.594,1.971,16),seq(1.594,1.971,16)[1:]):
        def cheek(z,y):return fixedside(s,y,z,0)
        low=lambda z:interp(z,[(1.594,.153),(1.82,.132),(1.971,.118)])
        face([cheek(a,low(a)),cheek(b,low(b)),cheek(b,.168),cheek(a,.168)],'Ivory')
plate([(-.807,.117,2.051),(.807,.117,2.051),(.815,.119,1.957),(-.815,.119,1.957)],'Ivory',(0,-.009,0))
part('Bonnet louvres and fasteners')
for s in [-1,1]:
    for j in range(8):
        z=.665+j*.032
        face([add(surface(s*u,Z),(0,.006,0)) for u,Z in [(.12,z),(.42,z),(.42,z+.018),(.12,z+.018)]],'Charcoal')
    for z in [.671,1.77]:
        q=surface(s*.82,z);cyl(q,add(q,(0,.007,0)),.019,'Steel',14);cyl(add(q,(-.013,.009,0)),add(q,(.013,.009,0)),.003,'Black',6)
conform(lambda u,z:add(surface(u,z),(0,.006,0)),(-.220,.220,1.87,1.65),(259,0,702,200))
group('tail','Rear clamshell','后翻式发动机罩',(-.45,1.44,-1.07),'后翼子板、透明发动机盖、通风百叶与车尾扰流板。')
part('Rear body and engine aperture')
# Side decks leave a real opening for the engine cover.
zs=seq(-1.979,-.504,44)
for s in [-1,1]:
    grid(lambda u,z:surface(s*u,z),[.63,.78,.86,.94,1],zs,'Ivory',s>0)
    grid(lambda v,z:side(s,v,z),[0,.23,1],sorted(set(zs+[-1.22+.356*cos(i*pi/32) for i in range(33)])),'Ivory',s<0)
for a,b in [(-1.979,-1.68),(-.68,-.504)]:grid(surface,[-.63,0,.63],seq(a,b,4),'Ivory',True)
part('Wheel arch return lips')
for s in [-1,1]:
    for center in [-1.22]:
        lip=[side(s,0,center+.356*cos(i*pi/44)) for i in range(45)]
        strip(lip,(-s*.045,0,0),'Gunmetal')
part('Fastback glazing and flying buttresses')
for s in [-1,1]:
    p=[(s*.608,1.116,-.475),(s*.644,1.088,-.579),(s*.836,.817,-1.46),(s*.832,.791,-.516)]
    plate(p,'Ivory',(-s*.045,0,0))
    p=[(s*.665,1.029,-.618),(s*.783,.844,-1.18),(s*.764,.841,-.663)]
    face(p,'Black')
    # Raised rear quarter intake with five louvres on the sloping sail.
    sail=[(s*.669,1.045,-.61),(s*.797,.855,-1.21),(s*.81,.846,-.616)]
    face(sail,'Charcoal')
    for j in range(5):
        z=-.69-j*.074;y=1.015-j*.027;x=.685+j*.019
        cyl((s*x,.85,z),(s*(x-.026),y,z-.006),.007,'Gunmetal',6)
def hatch(x,z):return (x,.812+clamp((z+1.67)/1.16,0,1)*.283,z)
grid(hatch,[-.568,0,.568],[-1.68,-.51],'Glass',True)
for x in [-.582,.582]:path([hatch(x,-1.69),hatch(x,-.51)],.022,'Black')
for j in range(5):
    z=-1.64+j*.14;plate([add(hatch(x,Z),(0,.016,0)) for x,Z in [(-.573,z),(.573,z),(.573,z+.039),(-.573,z+.039)]],'Charcoal')
part('Tail panel and spoiler')
box((0,.553,-1.978),(1.56,.256,.057),'Ivory');box((0,.393,-1.958),(1.57,.083,.10),'Charcoal')
box((0,.55,-2.01),(.72,.152,.014),'Black')
for s in [-1,1]:
    box((s*.572,.566,-2.014),(.334,.11,.04),'Charcoal')
    for i,m in enumerate(['Tail','Amber']):
        x=s*(.493+i*.15)
        cyl((x,.565,-2.029),(x,.565,-2.045),.067,'Black',48)
        cyl((x,.565,-2.045),(x,.565,-2.058),.059,m,48,.054)
        for rad in [.024,.042,.051]:tor((x,.565,-2.059),(0,0,1),rad,.0017,m,40,6)
        for dx in [-.044,.044]:cyl((x+dx,.565,-2.055),(x+dx,.565,-2.061),.0025,'Silver',10)
    plate([(s*.804,.754,-1.709),(s*.804,1.020,-2.001),(s*.804,.752,-2.008)],'Ivory',(s*.012,0,0))
def wing(x,t):return (x*(1+.018*t),.765+.257*t-.009*sin(pi*t),-1.720-.281*t)
grid(wing,seq(-.817,.817,16),seq(0,1,10),'Ivory')
grid(lambda x,t:add(wing(x,t),(0,-.007,-.005)),[-.817,.817],seq(0,1,10),'Pearl')
for s in [-1,1]:strip([wing(s*.817,t) for t in seq(0,1,12)],(0,-.008,-.005),'Pearl')
conform(lambda x,t:add(wing(x,t),(0,.003,.004)),(-.745,.745,.29,.88),(13,659,1444,776),32,4)
decal([(.25,.51,-2.02),(-.25,.51,-2.02),(-.25,.592,-2.02),(.25,.592,-2.02)],(7,264,568,335))
group('canopy','Roof and windscreen','车顶与风挡',(-.45,1.72,.015),'弧面前风挡、A 柱、车顶和雨刮器组成的可拆展示单元。')
part('Windscreen, surround and wipers')
def wind(u,t):
    return (u*(.752-.126*t),.747+.386*t+.013*(1-u*u),.637-.439*t+.046*(1-u*u))
grid(wind,seq(-1,1,12),seq(0,1,5),'Glass')
for s in [-1,1]:
    path([wind(s,t) for t in seq(0,1,6)],.022,'Ivory')
for t in [0,1]:path([wind(u,t) for u in seq(-1,1,10)],.013,'Black')
grid(lambda u,t:add(wind(u,t),(0,.002,.003)),seq(-1,1,10),[.844,.995],'Navy')
conform(lambda u,t:add(wind(u,t),(0,.004,.006)),(-.91,.91,.855,.982),(10,524,1293,643),16,2)
for s in [-1,1]:
    pts=[add(wind(s*.57,.025),(0,.006,.009)),add(wind(s*.27,.19),(0,.006,.011))]
    path(pts,.006,'Charcoal')
    path([add(wind(s*.57,.134),(0,.011,.014)),add(wind(-s*.04,.235),(0,.011,.014))],.007,'Black')
part('Crowned roof')
def roof(u,z):
    w=interp(z,[(-.53,.60),(-.44,.648),(.125,.649),(.205,.628)])
    return (u*w,1.146+.016*(1-u*u)+.027*math.exp(-((abs(u)-.51)/.27)**2)*max(0,1-((z+.16)/.39)**4)-.021*(abs(z+.16)/.39)**2,z)
grid(roof,seq(-1,1,44),seq(-.53,.205,18),'Ivory',True)
for s in [-1,1]:
    path([roof(s,z) for z in seq(-.53,.205,7)],.012,'Pearl')
for s in [-1,1]:
    group('door'+str(s),'Left door' if s>0 else 'Right door','左侧车门' if s>0 else '右侧车门',(s*1.22,.33,.16),'独立车门带侧窗、车号板、拉手与外后视镜。')
    part('Door outer skin and trim')
    zz=seq(-.501,.60,22)
    grid(lambda v,z:side(s,v,z),[0,.16,.65,1],zz,'Ivory',s<0)
    for z in [-.501,.60]:
        path([side(s,v,z) for v in [0,.5,1]],.005,'Black')
    for a,b,m in []:
        grid(lambda v,z:fixedside(s,v,z,.003),[a,b],zz,m)
    for v in [0,1]:
        strip([side(s,v,z) for z in zz],(-s*.070,0,0),'Pearl')
    for z in [-.495,.59]:
        strip([side(s,v,z) for v in [0,1]],(-s*.07,0,0),'Pearl')
    part('Side glass, window frames and door mirror')
    pts=[(s*.807,.75,.55),(s*.64,1.108,.172),(s*.641,1.11,-.425),(s*.783,.798,-.49)]
    face(pts,'Glass')
    rail=[side(s,1,z) for z in seq(-.49,.55,16)]
    for j in range(16):
        k=j/16;K=(j+1)/16
        face([rail[j],rail[j+1],mix(pts[3],pts[0],K),mix(pts[3],pts[0],k)],'Ivory')
    path(pts+[pts[0]],.014,'Black')
    path([pts[1],pts[2],pts[3]],.014,'Ivory')
    path([mix(pts[0],pts[3],.7),mix(pts[1],pts[2],.73)],.008,'Charcoal')
    box((s*.849,.68,-.331),(.027,.031,.116),'Charcoal')
    cyl((s*.795,.774,.416),(s*.934,.795,.426),.019,'Charcoal',10)
    def mirror(a,t):
        r=sqrt(max(.065,1-t*t))
        return (s*(.949+.060*r*cos(a)),.815+.044*r*sin(a),.375+.119*t)
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
for end,length in [(1,1.83),(-1,1.89)]:
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
box((0,.649,.497),(1.32,.119,.206),'Charcoal')
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
    pts=[(-.638,.288,z),(-.635,y-.11,z),(-.558,y,z),(.558,y,z),(.635,y-.11,z),(.638,.288,z)]
    path(pts,.023,'Steel',10)
for s in [-1,1]:
    path([(s*.57,1.046,-.446),(s*.594,1.061,.16),(s*.647,.775,.501)],.021,'Steel',10)
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
                        u*=.020/(rmid*pi/count);v*=.020/(hi-rmid)
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
path([(-.443,.608,1.932),(.443,.608,1.932)],.014,'Charcoal',12)
for k in [-1,1]:
    path([(k*.34,.559,1.853),(k*.34,.608,1.932),(k*.34,.658,1.945)],.014,'Gunmetal',10)
part('Four competition driving lamps')
for x in [-.349,-.121,.121,.349]:
    y=.671 if abs(x)>.2 else .700
    Z=1.955-.077*abs(x)
    cyl((x,y,Z-.098),(x,y,Z-.035),.044,'Charcoal',40,.103)
    tor((x,y,Z+.010),(0,0,1),.102,.008,'Ivory',56,10)
exec(compile((ROOT/'src/trim.py').read_text(encoding='utf-8-sig'),'trim.py','exec'))

# Retain the 2.440 m axle spacing. Set the outer coachwork to the nominal
# 3.915 m length, 1.850 m maximum body width and 1.245 m roof height.
def calibrate_coachwork():
    width_scale=.925/.93495
    overhang_scale=(3.915-3.16)/(4.112-3.16)
    for (assembly,name),primitives in parts.items():
        body=assembly in ('nose','tail','canopy','door1','door-1','lamps')
        if not body and assembly not in ('cockpit','chassis') and name!='Silencer and outlets':continue
        for positions,normals,_,_ in primitives.values():
            for k in range(0,len(positions),3):
                x,y,z=positions[k:k+3]
                sx=width_scale if body else 1.
                sy=1.;sz=1.
                if body or assembly=='cockpit':
                    u=clamp((y-.740)/.445,0,1)
                    y+=.060*u*u*(3-2*u)
                    sy+=.060*6*u*(1-u)/.445
                if abs(z)>1.58:
                    z=math.copysign(1.58+(abs(z)-1.58)*overhang_scale,z);sz=overhang_scale
                positions[k:k+3]=array.array('f',(x*sx,y,z))
                nx,ny,nz=normals[k:k+3]
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

