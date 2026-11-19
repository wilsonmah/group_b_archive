X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
current='nose'
part('Wraparound wing livery and front air ducts')
for s in [-1,1]:
    for z in [.86,1.713]:
        q=surface(s*.806,z)
        tor(add(q,(0,.008,0)),Y,.014,.0026,'Silver',20,6)
        path([add(q,(-.012,.008,.003)),add(q,(.022,.008,.009))],.002,'Steel',6)
for s in [-1,1]:
    current='door'+str(s);part('Door furniture and inner trim')
    box((s*.761,.508,.02),(.014,.29,.78),'Charcoal')
    path([(s*.751,.555,.173),(s*.735,.507,.152),(s*.735,.513,.058),(s*.751,.551,.048)],.008,'Belt',8)
    for z in [-.20,.62]:
        bolt((s*.751,.57,z),(-s,0,0),.006,'Steel')
    current='rear'+('L' if s>0 else 'R')
    for prefix in ['rear','front']:
        current=prefix+('L' if s>0 else 'R');part('Tyre lettering, valve and bead')
        rear=prefix=='rear';z=-1.22 if rear else 1.22
        x=.79+.257*.5 if rear else .773+.213*.5
        # Set the manufacturer's tyre marking along the circular sidewall.
        def marking(u,v):
            a=(u-.5)*.97*s
            rr=.234+.025*v
            return(s*(x+.0018),.319+rr*cos(a),z-rr*sin(a))
        conform(marking,(0,1,0,1),(700,28,1019,101),24,2)
        a=.65
        cyl((s*x,.319+.17*cos(a),z+.17*sin(a)),(s*(x+.015),.319+.17*cos(a),z+.17*sin(a)),.0045,'Rubber',10)
current='cockpit';part('Rally instrumentation and safety equipment')
for i in range(5):
    x=.54-i*.095;r=.031 if i in [1,2] else .021
    for j in range(11):
        a=.65+j*.49
        path([(x+R*cos(a),.656+R*sin(a),.373) for R in [r*.78,r]],.0013,'Ivory',5)
for j in range(5):
    x=-.06-j*.051
    cyl((x,.658,.387),(x,.66,.373),.009,'Gunmetal',16)
    cyl((x,.66,.373),(x,.671,.36),.0028,'Silver',8)
    cyl((x,.678,.382),(x,.678,.378),.0033,'Amber' if j%2 else 'Red',10)
cyl((-.57,.322,.169),(-.57,.322,.425),.047,'Red',32)
for z in [.211,.371]:tor((-.57,.322,z),Z,.047,.003,'Steel',24,6)
pipe([(-.57,.323,.436),(-.57,.383,.446),(-.502,.389,.435)],.006,'Black',8)
current='chassis';part('Dry sump reservoir, lines and rear mounts')
cyl((.45,.30,-.827),(.45,.535,-.827),.06,'Alloy',40)
for y in [.337,.476]:tor((.45,y,-.827),Y,.061,.003,'Steel',36,6)
cyl((.45,.535,-.827),(.45,.546,-.827),.023,'Gunmetal',20)
for x in [-.46,.46]:
    pipe([(x,.315,1.616),(x,.262,1.43),(x,.239,.83),(x,.236,-.61),(x,.357,-.77)],.014,'Rubber')
    for z in [-.54,.15,1.31]:
        sleeve((x,.239,z),Z,.017,.013,.011,'Silver',16)
current='tail';part('Rear wing sponsors and filler cap')
for s in [-1,1]:
    z=-.707;y=.76
    x=width(z)
    cyl((s*(x-.005),y,z),(s*(x+.006),y,z),.026,'Gunmetal',24)
    tor((s*(x+.007),y,z),X,.027,.003,'Steel',28,6)
    for j in range(3):
        a=j*pi*2/3;bolt((s*(x+.006),y+.02*cos(a),z+.02*sin(a)),(s,0,0),.0025)



current='lamps';part('Moulded lamp pod and reflector bowls')
# A one-piece brow bridges the four reflectors and blends back into the bonnet.
def brow(x,t):
    edge=clamp((abs(x)-.38)/.10,0,1)
    leading=.703-.010*(x/.48)**2-.099*edge**2
    rear_z=1.58+.103*(abs(x)/.48)**2
    rear_y=surface(x/width(rear_z),rear_z)[1]+.009
    return (x,leading*(1-t)+rear_y*t+.015*sin(pi*t),2.030*(1-t)+rear_z*t-.036*abs(x)*(1-t))
grid(brow,seq(-.477,.477,60),seq(0,1,16),'Ivory')
strip([brow(x,0) for x in seq(-.477,.477,60)],(0,-.008,0),'Pearl')
for s in (-1,1):
    grid(lambda t,h:mix(brow(s*.477,t),add(brow(s*.477,t),(0,-.094*(1-t)-.004,0)),h),seq(0,1,12),[0,1],'Ivory')
# All coordinates for the printed graphics are in atlas pixels. Side graphics
# are cropped at actual panel seams so they follow their panels on disassembly.
panel_ranges=[('tail',-1.976,-.272),('door',-.267,.717),('nose',.722,1.968)]
for kind,za,zb in panel_ranges:
    for s in [-1,1]:
        current='door'+str(s) if kind=='door' else kind
        part('Rallye de France shoulder ribbons '+str(s))
        for lo,hi,m in [(0,.047,'Red'),(.047,.063,'Navy'),(.063,.080,'Blue'),(.080,.092,'Navy'),(.092,.110,'Blue'),(.110,.126,'Navy')]:
            def band(d,z):
                high=surface(1,z)[1]
                factor=interp(z,[(-1.976,1.29),(-1.20,1.01),(-.53,.76),(.54,.74),(1.23,1.05),(1.968,1.36)])
                y=max(arch(z)+.001,high-d*factor)
                return fixedside(s,y,z,.0033)
            for a,b in zip(seq(za,zb,88),seq(za,zb,88)[1:]):
                pts=[band(lo,a),band(lo,b),band(hi,b),band(hi,a)]
                for indices in [(0,1,2),(0,2,3)]:
                    tri=[pts[k] for k in indices]
                    if dot(cross(sub(tri[1],tri[0]),sub(tri[2],tri[0])),cross(sub(tri[1],tri[0]),sub(tri[2],tri[0])))>1.e-16:face(tri,m)
        if kind=='nose':
            # The outer shoulder carries the wide red sash down to the lamps.
            for a,b,m in [(.805,.828,'Navy'),(.828,.851,'Blue'),(.851,.867,'Navy'),(.867,.887,'Blue'),(.887,.905,'Navy'),(.905,1.,'Red')]:
                grid(lambda u,z:add(surface(s*u,z),(0,.0023,0)),seq(a,b,6),seq(za,zb,92),m)
def sidesign(zlo,zhi,ylo,yhi,rect):
    for kind,za,zb in panel_ranges:
        low,high=max(zlo,za),min(zhi,zb)
        if low>=high:continue
        for s in [-1,1]:
            global current
            current='door'+str(s) if kind=='door' else kind
            part('No 5 event graphics '+str(s))
            a,b=(high,low) if s>0 else (low,high)
            def tx(z):return (zhi-z)/(zhi-zlo) if s>0 else (z-zlo)/(zhi-zlo)
            x,y,Xp,Yp=rect
            conform(lambda z,h:fixedside(s,h,z,.008),(a,b,ylo,yhi),(x+tx(a)*(Xp-x),y,x+tx(b)*(Xp-x),Yp),12,4)
sidesign(-.131,.068,.244,.613,(1479,519,1630,796))
sidesign(-.242,.164,.594,.674,(797,795,1237,917))
sidesign(-.260,.182,.175,.234,(14,794,782,917))
sidesign(-.865,-.275,.420,.752,(259,0,703,203))
sidesign(-.798,-.388,.347,.396,(685,1062,1099,1124))
sidesign(-.802,-.511,.188,.247,(676,943,1032,1033))
sidesign(.323,.601,.482,.584,(13,945,323,1078))
sidesign(.351,.550,.199,.456,(355,931,653,1155))
sidesign(.322,.588,.632,.713,(14,1195,700,1326))
sidesign(1.636,1.925,.179,.303,(729,1193,1121,1327))
current='nose';part('Bonnet roundel, rally plate and lower valance decals')
conform(lambda u,z:add(surface(u,z),(0,.004,0)),(-.224,.224,1.57,1.142),(1180,1155,1558,1486),22,12)
conform(lambda u,z:add(surface(u,z),(0,.004,0)),(-.129,.129,1.087,.914),(1590,1166,1961,1315),12,5)
def frontmark(xa,xb,ya,yb,z,rect):
    decal([(xa,ya,z),(xb,ya,z),(xb,yb,z),(xa,yb,z)],rect)
for s in [-1,1]:
    x=s*.535
    frontmark(x-.169,x+.169,.125,.179,2.033,(1116,944,1546,1052))
    frontmark(x-.078,x+.078,.278,.316,2.021,(1574,949,2014,1031))
frontmark(-.14,.14,.123,.183,2.034,(259,0,700,203))
frontmark(-.296,-.242,.401,.446,2.019,(19,1390,151,1467))
for s in [-1,1]:
    # Flexible black flaps and a small body-coloured front wheel spat.
    current='tail';part('Rear gravel flap '+str(s))
    plate([(s*.707,.263,-1.594),(s*.893,.276,-1.594),(s*.911,.061,-1.637),(s*.711,.059,-1.635)],'Rubber',(0,0,-.007))
    current='nose';part('Front wheel spat '+str(s))
    plate([(s*.737,.288,.835),(s*.865,.296,.839),(s*.877,.109,.799),(s*.748,.113,.801)],'Ivory',(0,0,-.007))
current='canopy';part('Roof aerial and mounting ferrule')
q=roof(.10,-.063)
cyl(q,add(q,(0,.012,0)),.016,'Black',24)
cyl(add(q,(0,.012,0)),add(q,(0,.069,-.006)),.0048,'Silver',12,.0038)
cyl(add(q,(0,.069,-.006)),add(q,(0,.357,-.034)),.0023,'Gunmetal',10,.001)

def optical_lamp(x,y,z,r):
    # A hollow parabolic reflector is visible through the fluted glass cover.
    c=(x,y,z)
    shell(c,Z,[(-r*.49,r*.13),(-r*.45,r*.31),(-r*.35,r*.57),(-r*.20,r*.79),(-r*.065,r*.94),(0,r*.98)],'Reflector',64)
    sleeve((x,y,z-.002),Z,r,r*.945,.016,'Silver',48)
    cyl((x,y,z-r*.49),(x,y,z-r*.11),r*.095,'Silver',16,r*.14)
    cyl((x-r*.19,y,z-r*.095),(x+r*.19,y,z-r*.095),r*.033,'Lens',16)
    def lens(a,rr):return (x+rr*cos(a),y+rr*sin(a),z+.002+.13*r*(1-(rr/r)**2))
    grid(lens,seq(0,2*pi,48),seq(r*.006,r*.943,9),'Optical glass')
    for j in range(-10,11):
        dx=j*r*.084;span=sqrt((r*.93)**2-dx*dx)
        points=[(x+dx,y+dy,z+.003+.13*r*(1-(dx*dx+dy*dy)/r**2)) for dy in seq(-span,span,9)]
        path(points,.00065,'Lens',5)
    tor((x,y,z+.002),Z,.952*r,.0024,'Reflector',48,8)
current='nose';part('SIEM optical reflectors and lenses')
for s in [-1,1]:
    for off in [-.093,.093]:optical_lamp(s*.591+off,.433,2.028,.088)
current='lamps';part('Auxiliary optical reflectors and lenses')
for x in [-.349,-.121,.121,.349]:
    y=.590 if abs(x)>.2 else .596
    optical_lamp(x,y,2.040-.036*abs(x),.102)
current='canopy';part('Pressed A-pillar flanges')
for s in [-1,1]:
    for a,b in zip(seq(0,1,18),seq(0,1,18)[1:]):
        def pillar(t):return mix((s*.805,.845,.612),(s*.550,1.095,.07),t)
        face([wind(s,a),wind(s,b),pillar(b),pillar(a)],'Ivory')
for s in [-1,1]:
    current='door'+str(s);part('Sliding side window')
    def window(u,v):
        lo=mix((s*.807,.845,.600),(s*.800,.845,-.255),u)
        hi=mix((s*.552,1.085,.080),(s*.553,1.098,-.255),u)
        return add(mix(lo,hi,v),(s*.0045,0,0))
    pts=[window(u,v) for u,v in [(.35,.17),(.63,.17),(.63,.79),(.35,.79)]]
    path(pts+[pts[0]],.0031,'Steel',7)
    for u in [.35,.63]:
        p=window(u,.49);cyl(p,add(p,(s*.004,0,0)),.006,'Black',12)

current='nose';part('Amber side repeaters and apron returns')
for s in (-1,1):
    q=fixedside(s,.58,1.58,.009)
    cyl(q,add(q,(s*.009,0,0)),.017,'Gunmetal',24)
    cyl(add(q,(s*.009,0,0)),add(q,(s*.014,0,0)),.014,'Amber',24,.012)
    grid(lambda y,t:mix((s*.785,y,1.965),apron(s*.785,y),t),seq(.117,.332,12),[0,1],'Ivory')
