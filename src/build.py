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
for a in [('Ivory','F2F1E9',.14,.26),('Pearl','D4D4C9',.25,.35),('Navy','142B4A',.13,.31),('Blue','4296C8',.1,.32),('Red','C82830',.13,.31),('Rubber','22252A',0,.84),('Tread','2A2C30',0,.88),('Charcoal','252B30',.25,.47),('Black','141A20',.14,.5),('Gunmetal','515B61',.62,.39),('Steel','9CA7AA',.8,.31),('Silver','CBCECA',.75,.28),('Alloy','E2DFD3',.48,.31),('Glass','344955',.43,.15),('Lens','DCE3E0',.48,.16),('Amber','E39B31',.18,.22),('Tail','AD2725',.15,.2),('Gold','B39663',.67,.35),('Exhaust','8D7562',.7,.39),('Seat','30363B',0,.9),('Belt','B9282D',0,.78),('Engine','912B2B',.48,.37),('Decal','FFFFFF',0,.44)]:mat(*a)
glassmat=materials[mids['Glass']];glassmat['alphaMode']='BLEND';glassmat['pbrMetallicRoughness']['baseColorFactor'][3]=.55
materials[-1]['pbrMetallicRoughness']['baseColorTexture']={'index':0}
materials[-1]['alphaMode']='MASK';materials[-1]['alphaCutoff']=.32
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
    x,y,X,Y=rect;face(p,'Decal',uv=[(x/1024,Y/512),(X/1024,Y/512),(X/1024,y/512),(x/1024,y/512)])
def width(z):return interp(z,[(-2,.77),(-1.81,.91),(-1.24,.935),(-.63,.866),(-.47,.837),(.56,.823),(1.18,.907),(1.56,.888),(1.9,.81),(2,.775)])
def top(z):return interp(z,[(-2,.716),(-1.74,.779),(-1.23,.813),(-.56,.80),(0,.734),(.57,.737),(1.12,.681),(1.47,.636),(1.79,.583),(2,.536)])
def surface(u,z):
    wave=.077*math.exp(-((z-1.22)/.45)**2)+.024*math.exp(-((z+1.22)/.47)**2)
    a=abs(u);return (u*width(z),top(z)+wave*min(1,a/.79)**3-.035*max(0,(a-.86)/.14),z)
def arch(z):
    d=min(abs(z-1.22),abs(z+1.22));return .319+sqrt(max(0,.356**2-d**2)) if d<=.356 else max(.208,.319-(d-.356)*3.3)
def side(s,v,z):
    high=surface(1,z)[1];low=arch(z)
    return (s*(width(z)-.019*(1-v)),low*(1-v)+high*v,z)
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
            face([fn(a+(b-a)*k,c+(d-c)*h) for k,h in coords],'Decal',uv=[((x+(X-x)*k)/1024,(Y+(y-Y)*h)/512) for k,h in coords])
def hoodstripe(lo,hi):
    for s in [-1,1]:
        for u,U,m in [(.55,.588,'Navy'),(.588,.616,'Blue'),(.616,.664,'Red'),(.664,.692,'Blue'),(.692,.736,'Navy')]:
            grid(lambda a,z:add(surface(a*s,z),(0,.003,0)),[u,U],seq(lo,hi,24),m)
def plate(p,m,depth=(0,-.013,0)):
    face(p,m);q=[add(i,depth) for i in p];face(q[::-1],m)
    for i in range(len(p)):face([p[i],q[i],q[(i+1)%len(p)],p[(i+1)%len(p)]],m)
group('nose','Front clamshell','前翻式车头',(0,.49,.77),'四圆灯、中央格栅、百叶散热口及一体式前翼子板。')
part('Front body moulding');bodysection(.604,1.97)
part('Nose fascia');z=1.97
face([(-.778,.536,z),(.778,.536,z),(.774,.346,z+.026),(-.774,.346,z+.026)],'Ivory')
box((0,.302,1.957),(1.56,.088,.10),'Ivory');box((0,.239,1.934),(1.51,.048,.107),'Charcoal')
for s in [-1,1]:
    x=s*.56
    box((x,.449,1.994),(.377,.158,.038),'Black')
    for dx in [-.091,.091]:
        X=x+dx
        cyl((X,.45,2.002),(X,.45,2.024),.075,'Silver',32)
        cyl((X,.45,2.025),(X,.45,2.039),.064,'Lens',32,.060)
        for j in range(-3,4):
            half=sqrt(max(0,.054**2-(j*.014)**2));cyl((X+j*.014,.45-half,2.039),(X+j*.014,.45+half,2.039),.0017,'Silver',5)
    box((s*.695,.305,2.01),(.115,.033,.018),'Amber')
box((0,.439,1.99),(.695,.154,.042),'Charcoal')
for j in range(-13,14):box((j*.025,.439,2.014),(.005,.142,.012),'Gunmetal')
for j in range(4): box((0,.383+j*.036,2.02),(.682,.005,.008),'Steel')
decal([(-.225,.261,2.013),(.225,.261,2.013),(.225,.337,2.013),(-.225,.337,2.013)],(7,264,568,335))
part('Bonnet louvres and fasteners')
for s in [-1,1]:
    for j in range(8):
        z=.665+j*.032
        face([add(surface(s*u,Z),(0,.006,0)) for u,Z in [(.12,z),(.42,z),(.42,z+.018),(.12,z+.018)]],'Charcoal')
    for z in [.671,1.77]:
        q=surface(s*.82,z);cyl(q,add(q,(0,.007,0)),.019,'Steel',14);cyl(add(q,(-.013,.009,0)),add(q,(.013,.009,0)),.003,'Black',6)
conform(lambda u,z:add(surface(u,z),(0,.006,0)),(-.294,.294,1.58,1.19),(256,0,705,205))
group('tail','Rear clamshell','后翻式发动机罩',(-.45,1.44,-1.07),'后翼子板、透明发动机盖、通风百叶与车尾扰流板。')
part('Rear body and engine aperture')
# Side decks leave a real opening for the engine cover.
zs=seq(-1.979,-.504,44)
for s in [-1,1]:
    grid(lambda u,z:surface(s*u,z),[.63,.78,.86,.94,1],zs,'Ivory',s>0)
    grid(lambda v,z:side(s,v,z),[0,.23,1],sorted(set(zs+[-1.22+.356*cos(i*pi/32) for i in range(33)])),'Ivory',s<0)
for a,b in [(-1.979,-1.68),(-.68,-.504)]:grid(surface,[-.63,0,.63],seq(a,b,4),'Ivory',True)
hoodstripe(-1.977,-1.682)
for s in [-1,1]:
    for u,U,m in [(.66,.695,'Navy'),(.695,.72,'Blue'),(.72,.76,'Red'),(.76,.786,'Blue'),(.786,.82,'Navy')]:
        grid(lambda a,z:add(surface(a*s,z),(0,.004,0)),[u,U],seq(-1.68,-.51,24),m)
part('Rear quarter stripes and cooling slots')
for s in [-1,1]:
    for h,k,m in [(0,.020,'Navy'),(.020,.038,'Blue'),(.038,.072,'Red'),(.072,.091,'Blue'),(.091,.112,'Navy')]:
        for za,zb in zip(zs,zs[1:]):
            def stripe_y(z):return .423+.087*max(0,-z-.5)
            if min(stripe_y(za)+k-arch(za),stripe_y(zb)+k-arch(zb))<=.001:continue
            face([fixedside(s,max(arch(z),stripe_y(z)+y),z,.003) for z,y in [(za,h),(zb,h),(zb,k),(za,k)]],m)
    for j in range(5):
        za=-.552-j*.052
        ya=.55+j*.018
        face([fixedside(s,y,z,.005) for z,y in [(za,ya),(za-.024,ya+.008),(za-.073,.735),(za-.043,.743)]],'Charcoal')
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
    plate([(s*.655,.73,-1.91),(s*.655,.854,-1.994),(s*.655,.844,-1.866)],'Gunmetal',(s*.02,0,0))
plate([(-.882,.814,-1.868),(.882,.814,-1.868),(.894,.865,-2.046),(-.894,.865,-2.046)],'Ivory')
for s in [-1,1]:plate([(s*.889,.803,-1.86),(s*.889,.875,-1.885),(s*.889,.895,-2.055),(s*.889,.833,-2.035)],'Ivory',(s*.009,0,0))
decal([(.25,.51,-2.02),(-.25,.51,-2.02),(-.25,.592,-2.02),(.25,.592,-2.02)],(7,264,568,335))
group('canopy','Roof and windscreen','车顶与风挡',(-.45,1.72,.015),'弧面前风挡、A 柱、车顶和雨刮器组成的可拆展示单元。')
part('Windscreen, surround and wipers')
def wind(u,t):
    return (u*(.752-.126*t),.747+.386*t+.013*(1-u*u),.637-.439*t+.046*(1-u*u))
grid(wind,seq(-1,1,12),seq(0,1,5),'Glass')
for s in [-1,1]:
    path([wind(s,t) for t in seq(0,1,6)],.022,'Ivory')
for t in [0,1]:path([wind(u,t) for u in seq(-1,1,10)],.013,'Black')
grid(lambda u,t:add(wind(u,t),(0,.002,.003)),seq(-1,1,10),[.858,.99],'Ivory')
conform(lambda u,t:add(wind(u,t),(0,.004,.006)),(-.58,.58,.858,.995),(457,354,974,424),16,2)
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
    for a,b,m in [(.6,.64,'Navy'),(.64,.674,'Blue'),(.674,.72,'Red'),(.72,.75,'Blue'),(.75,.79,'Navy')]:grid(lambda u,z:add(roof(u*s,z),(0,.002,0)),[a,b],seq(-.52,.195,9),m)
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
    def badge(z0,z1,y0,y1,rect,off=.007):
        za,zb=(z1,z0) if s>0 else (z0,z1)
        decal([fixedside(s,y,z,off) for z,y in [(za,y0),(zb,y0),(zb,y1),(za,y1)]],rect)
    badge(-.198,.146,.385,.699,(0,0,247,248),.013)
    badge(.18,.50,.485,.66,(258,0,705,205))
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
        for p,q in [(a,b),(b,c),(c,d),(d,a),(a,c)]:cyl(p,q,.021,'Steel',10)
        cyl((s*.57,.257,end*1.25),(s*.588,.594,end*1.24),.020,'Steel',10)
    for z,y,w in [(length,.26,.54),(1.24,.586,.59),(.65,.24,.65)]:cyl((-w,y,end*z),(w,y,end*z),.018,'Steel',10)
    cyl((-.54,.26,end*length),(.58,.56,end*1.245),.013,'Steel',10)
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
part('Steering, gear selector and pedals')
cyl((.376,.645,.421),(.376,.678,.212),.023,'Gunmetal')
tor((.376,.687,.183),(0,.32,-1),.135,.013,'Rubber',48)
for a in [0,pi,1.5*pi]:
    cyl((.376,.687,.183),(.376+.122*cos(a),.687+.119*sin(a),.183+.038*sin(a)),.009,'Gunmetal',8)
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
group('susp','Suspension and brakes','悬架与制动',(0,-.27,0),'双横臂、弹簧减振器、半轴和四轮制动盘，后桥采用双减振器示意。')
for z in [-1.22,1.22]:
    for s in [-1,1]:
        part(('Front' if z>0 else 'Rear')+' corner '+str(s))
        for y,dy in [(.244,0),(.423,-.009)]:
            for dz in [-.188,.188]:
                cyl((s*.443,y+dy,z+dz),(s*.771,y,z),.014,'Gunmetal',10)
        cyl((s*.768,.24,z),(s*.768,.441,z),.031,'Gunmetal')
        for d in ([0] if z>0 else [-.079,.079]):
            a=(s*.713,.252,z+d);b=(s*.527,.566,z+d)
            cyl(a,b,.017,'Steel');cyl(a,mix(a,b,.54),.031,'Gunmetal')
            if z>0:spring(mix(a,b,.07),mix(a,b,.925),.038,.0075,'Gold')
            for point in [a,b]:sleeve(point,Z,.024,.009,.030,'Gunmetal',20)
        if z<0:
            spring((s*.712,.270,z),(s*.535,.542,z),.043,.008,'Gold')
            for c in [(s*.712,.270,z),(s*.535,.542,z)]:cyl(c,add(c,(0,.005,0)),.051,'Gunmetal',24)
        pipe([(s*.73,.357,z-.105),(s*.69,.417,z-.107),(s*.60,.428,z-.16),(s*.53,.391,z-.21)],.004,'Rubber',8)
        cyl((s*.174,.315,-1.291),(s*.267,.346,z),.023,'Gunmetal') if z<0 else None
        if z<0:
            cyl((s*.207,.352,z),(s*.752,.318,z),.018,'Steel')
            for x in [.262,.703]:
                for i in range(4):cyl((s*(x+i*.011),.329,z),(s*(x+i*.011+.009),.329,z),.033+.006*sin(i*pi/3),'Rubber')
        cyl((s*.759,.319,z),(s*.796,.319,z),.134,'Steel',40)
        tor((s*.798,.319,z),(1,0,0),.113,.003,'Gunmetal',36,5)
        cyl((s*.792,.319,z),(s*.815,.319,z),.067,'Gunmetal',20)
        box((s*.782,.331,z-.119),(.061,.098,.050),'Gold')
        for j in range(36):
            a=j*pi/18
            for r in [.09,.111]:
                y=.319+r*cos(a+.14*(r>.1));Zp=z+r*sin(a+.14*(r>.1))
                cyl((s*.7962,y,Zp),(s*.7966,y,Zp),.00265,'Black',8)
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
        sleeve(wx((xc-w*.50+outer-.014)/2),X,.195,.175,w-.014,'Gunmetal',72)
        tor(wx(outer-.027),X,.168,.006,'Steel',64,8)
        tor(wx(outer-.002),(1,0,0),.183,.012,'Alloy',64,10)
        tor(wx(outer-.004),(1,0,0),.153,.013,'Alloy',64,8)
        cyl(wx(outer-.018),wx(outer+.001),.105,'Alloy',48,.096)
        for j in range(12):
            a=j*2*pi/12
            def rp(x,r,t):return(s*x,.319+r*cos(t),z+r*sin(t))
            p=[rp(outer+.002,.084,a-.192),rp(outer-.008,.157,a-.155),rp(outer-.008,.157,a+.145),rp(outer+.002,.084,a+.186)]
            plate(p,'Alloy',(-s*.019,0,0))
        for j in range(4):
            a=pi/4+j*pi/2;y=.319+.055*cos(a);Z=z+.055*sin(a)
            cyl((s*(outer+.001),y,Z),(s*(outer+.010),y,Z),.014,'Gunmetal',6)
        cyl(wx(outer+.001),wx(outer+.014),.033,'Gunmetal',20)
        cyl(wx(outer+.014),wx(outer+.017),.022,'Red',24)

group('lamps','Auxiliary light pod','夜赛辅助灯组',(0,.55,1.58),'四盏辅助拉力灯及管式支架，安装在车头前缘。')
part('Lamp carrier and stays')
path([(-.443,.608,1.932),(.443,.608,1.932)],.014,'Charcoal',12)
for k in [-1,1]:
    path([(k*.34,.559,1.853),(k*.34,.608,1.932),(k*.34,.658,1.945)],.014,'Gunmetal',10)
part('Four competition driving lamps')
for x in [-.349,-.121,.121,.349]:
    y=.671 if abs(x)>.2 else .700
    Z=1.955-.077*abs(x)
    cyl((x,y,Z-.098),(x,y,Z-.035),.043,'Charcoal',32,.104)
    cyl((x,y,Z-.035),(x,y,Z+.007),.104,'Black',40,.108)
    cyl((x,y,Z+.007),(x,y,Z+.020),.108,'Silver',48,.104)
    cyl((x,y,Z+.020),(x,y,Z+.033),.097,'Lens',48,.089)
    tor((x,y,Z+.034),(0,0,1),.09,.0025,'Silver',48,6)
    for k in range(-5,6):
        dx=k*.015;h=sqrt(max(0,.084**2-dx*dx))
        cyl((x+dx,y-h,Z+.034),(x+dx,y+h,Z+.034),.0024,'Silver',6)
    for k in [-2,-1,0,1,2]:
        dy=k*.026;w=sqrt(.084**2-dy*dy)
        cyl((x-w,y+dy,Z+.0345),(x+w,y+dy,Z+.0345),.0014,'Pearl',6)

exec(compile((ROOT/'src/trim.py').read_text(encoding='utf-8-sig'),'trim.py','exec'))
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
        if meta:
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

