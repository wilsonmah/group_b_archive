"""Lancia Rally B-210 suspension arrangement. Coordinates are reconstructed, in metres."""

def build_suspension():
    group('susp', 'Suspension, steering and brakes', '悬挂、转向与制动', (0,-.27,0),
          '前桥上叉臂、下横臂及纵向定位杆；后桥反置下叉臂、中央弹簧及双减振器。可进入内部拆解。')
    mat('Spring enamel','E7B238',.25,.29)
    mat('Damper anodizing','B88A42',.71,.3)

    def fitting(en,zh,family,travel,zone,**motion):
        component(en,zh,family,travel)
        component_meta[cur].update(zone=zone, **motion)

    def eye(c,axis,r=.017):
        sleeve(c,axis,r,r*.51,.022,'Gunmetal',16)
        sleeve(c,axis,r*.51,r*.27,.026,'Silver',14)

    def lug(c,axis):
        for sense in (-1,1):
            p=add(c,mul(axis,sense*.019))
            sleeve(p,axis,.019,.005,.008,'Gunmetal',14)
            box(add(p,(0,-.010,0)),(.021,.023,.009),'Gunmetal')
        bolt(add(c,mul(axis,.024)),axis,.008)

    def linkage(points,r=.013,finish='Silver'):
        for a,b in zip(points,points[1:]):
            cyl(a,b,r,finish,14)
            for f in (.045,.905):
                cyl(mix(a,b,f),mix(a,b,f+.05),r*1.17,'Steel',12)

    def damper(a,b):
        axis=unit(sub(b,a))
        for c in (a,b):eye(c,Z)
        cyl(mix(a,b,.035),mix(a,b,.56),.022,'Damper anodizing',20)
        cyl(mix(a,b,.52),mix(a,b,.58),.024,'Gunmetal',20)
        cyl(mix(a,b,.57),mix(a,b,.968),.009,'Silver',18)
        for t in (.77,.80,.83):sleeve(mix(a,b,t),axis,.018,.009,.009,'Rubber',16)

    def spring_unit(a,b,r):
        axis=unit(sub(b,a))
        lo,hi=mix(a,b,.115),mix(a,b,.90)
        for center in (lo,hi):
            sleeve(center,axis,r+.009,r-.009,.009,'Alloy',24)
            tor(center,axis,r,.0065,'Spring enamel',28,8)
        spring(lo,hi,r,.0066,'Spring enamel')

    # Common hardpoints also feed the viewer's rigid-link solver.
    rack_y,rack_z=.319,1.066
    pinion_axis=unit((0,.55,-.835))
    normal_to_rack=(0,-pinion_axis[2],pinion_axis[1])
    pitch_radius=.009845
    pinion=add((.295,rack_y,rack_z),mul(normal_to_rack,pitch_radius+.011))
    hand=(.376,.687,.183)
    j1=add(hand,(0,-.32*.405,.405))
    j2=add(pinion,mul(pinion_axis,.252))
    shafts=[(hand,j1),(j1,j2),(j2,pinion)]
    axes=[unit(sub(a,b)) for a,b in shafts]
    hardpoints=dict(hub=[.773,.319,1.22],lower=[.748,.224,1.232],
                    upper=[.700,.452,1.207],outer=[.692,.323,1.068],
                    inner=[.431,rack_y,rack_z],mouth=.323,pitchRadius=pitch_radius,axes=axes)
    # Match the base homologation's 16.8:1 straight-ahead ratio at the road wheel.
    king=unit(sub(hardpoints['upper'],hardpoints['lower']))
    tie=sub(hardpoints['outer'],hardpoints['inner'])
    arm=sub(hardpoints['outer'],hardpoints['lower'])
    rack_per_upright=abs(dot(tie,cross(king,arm))/tie[0])
    for _ in range(4):
        pitch_radius=rack_per_upright/(16.8*king[1]*dot(axes[0],axes[1])*dot(axes[1],axes[2]))
        pinion=add((.295,rack_y,rack_z),mul(normal_to_rack,pitch_radius+.011))
        j2=add(pinion,mul(pinion_axis,.252))
        shafts=[(hand,j1),(j1,j2),(j2,pinion)]
        axes=[unit(sub(a,b)) for a,b in shafts]
    hardpoints.update(pitchRadius=pitch_radius,axes=axes)
    groups['susp']['linkage']=hardpoints
    steer_family='转向传动'
    def steer_part(en,zh,travel,**info):
        fitting(en,zh,steer_family,travel,'front',**info)

    steer_part('Rack housing and mounting saddles','齿条壳体与固定座',(0,.15,.13),driveRole='rackHousing')
    for x1,x2,r in [(-.323,.323,.021),(.266,.323,.031)]:
        sleeve(((x1+x2)/2,rack_y,rack_z),X,r,.012,x2-x1,'Gunmetal',28)
    for x in (-.264,.257):
        sleeve((x,rack_y,rack_z),X,.028,.021,.035,'Alloy',22)
        for dz in (-.030,.030):
            c=(x,rack_y-.023,rack_z+dz);box(c,(.045,.014,.027),'Gunmetal');bolt(add(c,(0,.008,0)),Y,.007)
    sleeve(pinion,pinion_axis,.025,.010,.049,'Alloy',22)

    steer_part('Sliding rack','滑动齿条',(0,-.12,.18),driveRole='rack')
    cyl((-.431,rack_y,rack_z),(.431,rack_y,rack_z),.010,'Steel',24)
    # Opposed rack teeth span the complete pinion travel. Pitch matches twelve teeth.
    pitch=2*pi*pitch_radius/12
    for j in range(-20,21):
        x=pinion[0]+pitch*j
        c=add((x,rack_y,rack_z),mul(normal_to_rack,.0105))
        corners=[add(add(c,(dx,0,0)),mul(pinion_axis,w)) for dx,w in
                 [(-pitch*.36,-.007),(pitch*.36,-.007),(pitch*.36,.007),(-pitch*.36,.007)]]
        tops=[add(add(c,(dx,0,0)),add(mul(pinion_axis,w),mul(normal_to_rack,.002))) for dx,w in
              [(-pitch*.19,-.007),(pitch*.19,-.007),(pitch*.19,.007),(-pitch*.19,.007)]]
        face(tops,'Alloy')
        for i in range(4):face([corners[i],corners[(i+1)%4],tops[(i+1)%4],tops[i]],'Steel')

    for i,((a,b),axis) in enumerate(zip(shafts,axes)):
        steer_part(['Upper steering shaft','Intermediate steering shaft','Pinion shaft'][i],
                   ['方向盘上轴与节叉','中间传动轴与双端节叉','输入小齿轮与节叉'][i],(.095*i,.08,.07*i),
                   driveRole='columnShaft',shaft=i,pivot=a,axis=axis)
        cyl(mix(a,b,.035),mix(a,b,.96),.010 if i!=1 else .008,'Steel',16)
        sleeve(mix(a,b,.48),axis,.014,.008,.072,'Gunmetal',16)
        if i==2:gear(pinion,axis,pitch_radius+.0008,.004,.014,12,'Alloy')
        for joint in (i-1,i):
            if not 0<=joint<2:continue
            centre=(j1,j2)[joint];common=unit(cross(axes[joint],axes[joint+1]))
            fork_axis=common if joint==i else unit(cross(axis,common))
            back=mul(axis,.029 if joint==i else -.029)
            for sense in (-1,1):
                end=add(centre,mul(fork_axis,.014*sense))
                linkage([add(centre,back),add(end,mul(back,.55)),end],.0045,'Gunmetal')
                sleeve(end,fork_axis,.007,.003,.006,'Steel',12)
            cyl(add(centre,mul(fork_axis,-.017)),add(centre,mul(fork_axis,.017)),.0038,'Silver',12)

    for front in (True,False):
        z=1.22 if front else -1.22
        zone='front' if front else 'rear'
        axle_name='Front' if front else 'Rear'
        loc='前' if front else '后'
        fam=loc+'桥定位与承载';damping=loc+'桥弹簧与减振';brakes=loc+'桥轮端'
        fitting(axle_name+' suspension cradle',loc+'桥管架、塔座与铰接支座',fam,(0,.27,.08 if front else -.08),zone,driveRole='cradle')
        for side in (-1,1):
            def p(x,y,dz=0):return (side*x,y,z+dz)
            lower=p(.748,.224,.012) if front else p(.733,.237)
            upper=p(.700,.452,-.013) if front else p(.723,.440)
            inner_lo=p(.413,.237,.025) if front else p(.412,.240,-.006)
            upper_pivots=[p(.475,.436,d) for d in (-.154,.151)]
            link_anchor=p(.418,.234,-.312 if front else .332)
            offsets=[0] if front else [-.123,.123]
            tops=[p(.575,.624 if front else .660,d) for d in offsets]
            foot=p(.655,.241);springtop=p(.575,.624 if front else .660)
            part(axle_name+' suspension cradle')
            for y,h,x in [(.235,.272,.413),(.435,.198,.475)]:
                path([p(x,y,-h),p(x,y,h)],.014,'Charcoal',12)
            for d in (-.19,.19):
                path([p(.413,.235,d),p(.475,.435,d),p(.575,springtop[1],d*.72)],.015,'Charcoal',12)
                cyl(p(.413,.235,d),p(.57,.256,d),.014,'Charcoal',12)
                cyl(p(.475,.435,d),p(.588,.594),.014,'Charcoal',12)
            path([p(.575,springtop[1],-.15),p(.575,springtop[1],.15)],.017,'Charcoal',12)
            for c in [inner_lo,link_anchor,*upper_pivots,*tops]:
                lug(c,Z)
            cyl(link_anchor,p(.413,.235,math.copysign(.22,link_anchor[2]-z)),.014,'Charcoal',12)
            if not front:
                sleeve(springtop,Y,.060,.032,.013,'Gunmetal',26)
            if side==1:
                # Left-hand hardpoints for the viewer's wheel-travel solver. Every arm pivots on
                # a fore-aft axis, so each corner is a four-bar linkage in the transverse plane.
                hardpoints.setdefault('travel',{})[zone]=dict(
                    z=z,lowerInner=inner_lo,lowerBall=lower if front else p(.733,.237),upperInner=upper_pivots[0][:2],
                    upperBall=upper,hub=p(.773 if front else .77,.319),foot=foot,top=springtop,
                    linkAnchor=link_anchor,locator=mix(inner_lo,lower,.80) if front else p(.733,.237,.126),
                    shaftInner=None if front else (.174,.315,-1.291))
            def corner(en,zh,family,travel,**motion):
                fitting(axle_name+' '+en+' '+str(side),('左' if side==1 else '右')+loc+' · '+zh,
                        family,travel,zone,side=side,**motion)
            corner('upper wishbone','上叉臂',fam,(side*.13,.16,0))
            linkage([upper_pivots[0],upper,upper_pivots[1]],.011)
            for c in upper_pivots:eye(c,Z)
            eye(upper,Y)
            if front:
                corner('lower transverse arm','下横臂',fam,(side*.15,-.14,.04))
                linkage([inner_lo,lower],.016)
                eye(inner_lo,Z);eye(lower,Y)
                locator=mix(inner_lo,lower,.80)
            else:
                corner('reversed lower wishbone','反置下叉臂',fam,(side*.15,-.14,-.04))
                outboard=[p(.733,.237,d) for d in (-.126,.126)]
                linkage([outboard[0],inner_lo,outboard[1]],.014)
                linkage(outboard,.013,'Gunmetal')
                for c in [inner_lo,*outboard]:eye(c,Z)
                locator=outboard[1]
            corner('radius rod','纵向定位杆',fam,(side*.06,-.06,-.17 if front else .17))
            linkage([link_anchor,locator],.011,'Gunmetal');eye(link_anchor,Z);eye(locator,Y)
            for d in offsets:
                a=add(foot,(0,0,d));b=add(springtop,(0,0,d))
                corner('damper '+str(d),('同轴减振器' if front else ('前置减振器' if d>0 else '后置减振器')),damping,
                       (side*.13,.14,d*1.3))
                damper(a,b)
            corner('road spring','螺旋弹簧与弹簧座',damping,(side*.06,.27,0))
            spring_unit(foot,springtop,.038 if front else .047)
            if not front:
                for f1,f2 in [(0,.12),(.90,1)]:
                    cyl(mix(foot,springtop,f1),mix(foot,springtop,f2),.029,'Gunmetal',22)
            corner('lower spring bridge','下弹簧座与减振器支耳',fam,(side*.07,-.12,0))
            for d in sorted(set([0,*offsets])):
                a=add(foot,(0,0,d));lug(a,Z)
                b=mix(inner_lo,lower,.72) if front else mix(inner_lo,p(.733,.237,d),.78)
                cyl(a,b,.014,'Gunmetal',14)
            if not front:cyl(add(foot,(0,0,-.125)),add(foot,(0,0,.125)),.016,'Gunmetal',16)
            corner('upright',('转向节与转向臂' if front else '轮毂立柱'),brakes,(side*.24,.04,0),
                   driveRole='upright' if front else 'fixedHub')
            hub=p(.773 if front else .77,.319)
            for c in (lower,upper):
                cyl(c,hub,.022,'Alloy',16,.042)
                sleeve(c,Y,.019,.008,.022,'Gunmetal',16)
            sleeve(hub,X,.057,.028,.062,'Alloy',26)
            if front:
                outer=tuple(side*v if i==0 else v for i,v in enumerate(hardpoints['outer']))
                inner=tuple(side*v if i==0 else v for i,v in enumerate(hardpoints['inner']))
                linkage([hub,mix(hub,outer,.53),outer],.013,'Gunmetal')
                corner('track rod','转向横拉杆与球头',steer_family,(side*.10,.08,-.13),driveRole='tieRod')
                linkage([inner,outer],.007,'Steel')
                for c in (inner,outer):eye(c,Y,.012)
                for f in (.62,.83):cyl(mix(inner,outer,f),mix(inner,outer,f+.035),.010,'Alloy',6)
                corner('rack gaiter','齿条防尘波纹套',steer_family,(side*.09,.11,0),driveRole='gaiter')
                mouth=(side*hardpoints['mouth'],rack_y,rack_z)
                profile=[(0,.021)]
                for j in range(8):
                    profile.extend([(.004+j*.007,.019-j*.0008),(.007+j*.007,.022-j*.0008)])
                profile.extend([(.066,.011),(.066,.008),(0,.017),(0,.021)])
                shell(mouth,(side,0,0),[(x*(.431-hardpoints['mouth'])/.066,r) for x,r in profile],'Rubber',20)
            else:
                for d in [-.126,.126]:linkage([p(.733,.237,d),hub],.018,'Alloy')
                corner('halfshaft','半轴与等速万向节',brakes,(side*.26,.04,-.03))
                inner=(side*.174,.315,-1.291);outer=(side*.770,.319,z);axis=unit(sub(outer,inner))
                a,b=mix(inner,outer,.045),mix(inner,outer,.955)
                cyl(a,b,.019,'Steel',28)
                for f in (.06,.94):
                    c=mix(inner,outer,f);sleeve(c,axis,.039,.018,.073,'Gunmetal',26)
                    for j in range(5):tor(add(c,mul(axis,(j-2)*.011)),axis,.036-.002*abs(j-2),.005,'Rubber',26,6)
                offset=mul(unit(cross(axis,Y)),.018)
                cyl(add(a,offset),add(b,offset),.003,'Ivory',8)
            corner('brake rotor','通风制动盘与盘帽',brakes,(side*.31,.02,0))
            for x in (.777,.790):
                sleeve(p(x,.319),X,.15,.098,.0071,'Steel',48)
            for j in range(40):
                angle=j*2*pi/40
                c=add(p(.7835,.319),(0,.122*cos(angle),.122*sin(angle)))
                cyl(c,add(c,(0,.020*cos(angle+.19),.020*sin(angle+.19))),.0033,'Gunmetal',8)
            sleeve(p(.7835,.319),X,.101,.037,.0201,'Gunmetal',32)
            sleeve(p(.800,.319),X,.065,.028,.018,'Alloy',28)
            for j in range(4):
                ang=j*pi/2+pi/4
                c=p(.807,.319+.049*cos(ang),.049*sin(ang))
                cyl(c,add(c,(side*.020,0,0)),.0054,'Steel',10)
            corner('caliper','制动卡钳',brakes,(side*.19,.08,-.12))
            for x in (.759,.807):
                box(p(x,.327,-.129),(.019,.085,.029),'Alloy')
                cyl(p(x-.011,.327,-.128),p(x+.011,.327,-.128),.024,'Gold',22)
            for y in (.297,.357):
                path([p(.757,y,-.132),p(.762,y,-.154),p(.805,y,-.154),p(.810,y,-.132)],.007,'Gold',12)
                bolt(p(.817,y,-.133),(side,0,0),.006)
        if front:
            fitting('Front anti-roll bar','前横向稳定杆与连杆',fam,(0,-.14,.16),zone)
            path([(-.635,.265,z+.028),(-.620,.261,z+.198),(-.50,.263,z+.222),
                  (.50,.263,z+.222),(.620,.261,z+.198),(.635,.265,z+.028)],.009,'Gunmetal',16)
            for s in (-1,1):
                sleeve((s*.41,.263,z+.222),X,.017,.009,.033,'Rubber',18)
                linkage([(s*.635,.265,z+.028),(s*.635,.236,z+.018)],.006)
                box((s*.413,.249,z+.222),(.036,.018,.030),'Steel')
            part('Front suspension cradle')
            cyl((-.413,.288,rack_z),(.413,.288,rack_z),.018,'Charcoal',14)
            for s in (-1,1):cyl((s*.413,.235,rack_z),(s*.413,.288,rack_z),.012,'Charcoal',12)
        else:
            part('Rear suspension cradle')
            # Return the two towers to a transverse tube above the transaxle.
            cyl((-.575,.622,z-.284),(.575,.622,z-.284),.016,'Charcoal',14)
            for s in (-1,1):
                path([(s*.575,.660,z-.15),(s*.575,.622,z-.284),(s*.413,.235,z-.22)],.015,'Charcoal',14)

build_suspension()
