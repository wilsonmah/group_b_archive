X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
current='nose'
part('Wraparound wing livery and front air ducts')
for s in [-1,1]:
    # The upper colour sweep follows the leading edge from the sill to the bonnet.
    for v,V,m in [(.65,.70,'Navy'),(.70,.74,'Blue'),(.755,.82,'Navy'),(.82,.868,'Blue'),(.868,.99,'Red')]:
        grid(lambda u,z:add(side(s,u,z),(s*.0028,0,0)),[v,V],seq(.606,1.97,64),m,s<0)
    for a,b,m in [(.65,.688,'Navy'),(.688,.729,'Blue'),(.751,.799,'Navy'),(.799,.861,'Blue'),(.861,.995,'Red')]:
        grid(lambda u,z:add(surface(s*u,z),(0,.004,0)),[a,b],seq(.608,1.965,44),m)
    box((s*.56,.287,2.011),(.142,.060,.007),'Black')
    box((s*.7,.287,2.012),(.099,.055,.009),'Amber')
    for j in range(6):box((s*(.659+j*.015),.287,2.018),(.002,.047,.003),'Gold')
    for z in [.765,1.713]:
        q=surface(s*.806,z)
        tor(add(q,(0,.008,0)),Y,.014,.0026,'Silver',20,6)
        path([add(q,(-.012,.008,.003)),add(q,(.022,.008,.009))],.002,'Steel',6)
box((0,.311,2.011),(.83,.073,.009),'Black')
for j in range(-24,25):box((j*.016,.311,2.018),(.003,.062,.003),'Gunmetal')
decal([(-.17,.228,1.993),(.17,.228,1.993),(.17,.262,1.993),(-.17,.262,1.993)],(5,262,573,335))
for s in [-1,1]:
    current='door'+str(s);part('Door furniture and inner trim')
    box((s*.761,.508,.02),(.014,.29,.78),'Charcoal')
    path([(s*.751,.555,.173),(s*.735,.507,.152),(s*.735,.513,.058),(s*.751,.551,.048)],.008,'Belt',8)
    for z in [-.337,.389]:
        bolt((s*.751,.57,z),(-s,0,0),.006,'Steel')
    # Side racing stripe tapering below the window.
    for lo,hi,m in [(0,.016,'Navy'),(.016,.029,'Blue'),(.037,.054,'Navy'),(.054,.069,'Blue'),(.069,.104,'Red')]:
        for a,b in zip(seq(-.496,.597,26),seq(-.496,.597,26)[1:]):
            def dye(z):return .573+.026*z
            if a<.147 and b>-.20:continue
            face([fixedside(s,dye(z)+u,z,.004) for z,u in [(a,lo),(b,lo),(b,hi),(a,hi)]],m)
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
conform(lambda u,v:(u,.816+.047*v+.004,-1.879-.151*v),(-.57,.57,0,1),(456,347,975,430),12,2)


current='lamps';part('Moulded lamp pod and reflector bowls')
for x in [-.349,-.121,.121,.349]:
    yy=.671 if abs(x)>.2 else .700
    zz=1.955-.077*abs(x)
    shell((x,yy,zz+.0338),Z,[(0,.090),(.0005,.083),(-.009,.055),(-.016,.019),(-.015,.014)],'Silver',48)
    for rad in [.018,.038,.064,.083]:
        tor((x,yy,zz+.035),Z,rad,.0013,'Lens',52,5)
    cyl((x,yy,zz+.035),(x,yy,zz+.038),.012,'Lens',20)
for j in range(24):
    x=-.45+j*.0375;xx=x+.0375
    def podedge(q):
        return .576+.029*(1-(q/.46)**2)
    face([(x,podedge(x),1.874),(xx,podedge(xx),1.874),(xx,podedge(xx)+.029,1.970),(x,podedge(x)+.029,1.970)],'Ivory')
current='nose';part('Front valance and bumper ducts')
for s in [-1,1]:
    strip([(s*.753,.248,2.004),(s*.786,.251,1.972),(s*.823,.254,1.89),(s*.852,.258,1.79)],(0,.052,0),'Ivory')
    for x in [.18,.32,.69]:
        bolt((s*x,.354,2.01),Z,.004,'Gunmetal')
