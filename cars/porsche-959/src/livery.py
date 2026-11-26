# Rothmans Porsche 959 Paris-Dakar (1986), after museum and auction photographs of the 186 and 187
# cars; the Nº 185 car carried the same scheme. A white roof, bonnet and upper body above a royal-blue
# lower body; a wide gold band edged in red sweeps from the headlamp bezels back over the front wings
# and along the shoulder to the tail. Graphics keep the aspect ratio of their artwork in decals.png.
mat('Rblue','1F3F9A',.12,.30)
NUM=(20,20,520,430);R_WHITE=(20,480,820,630);PORSCHE_W=(20,670,660,740);DUNLOP=(20,790,580,870);BILSTEIN=(20,910,660,990)
BANNER=(20,1040,1520,1150);R_BLUE=(20,1200,920,1350);SHELL=(20,1400,540,1560);TAIL_SCRIPT=(20,1620,1120,1710)
BLU=[(2.02,.470),(1.94,.540),(1.78,.650),(1.52,.735),(1.25,.765),(.90,.790),(.40,.805),(-.50,.805),(-1.10,.805),(-1.60,.795),(-2.05,.760),(-2.24,.640)]
BLU.sort()
def blu(z):return sinterp(z,BLU)
def stripe_cur(z,s):
    global cur
    key=('nose' if z>DZ1 else 'tail' if z<DZ0 else 'door'+str(s),'Livery panels')
    if key not in parts:parts[key]={}
    cur=key
def skin_x(z,y):return side_x(z,y)+(.011 if DZ0<=z<=DZ1 else .006)
def band(s,y0f,y1f,m,dx=0,steps=4):
    """A band on the side skin between two height functions, skipping the wheel openings."""
    zs=zstations(ZT+.02,ZN-.02,150)
    for a,b in zip(zs,zs[1:]):
        la,lb=y0f(a),y0f(b);ha,hb=y1f(a),y1f(b)
        if la>=ha-.006 or lb>=hb-.006:continue
        stripe_cur((a+b)/2,s)
        for t0,t1 in zip(seq(0,1,steps),seq(0,1,steps)[1:]):
            q=[]
            for z,lo,hi,t in [(a,la,ha,t0),(b,lb,hb,t0),(b,lb,hb,t1),(a,la,ha,t1)]:
                y=lo+(hi-lo)*t;q.append((s*(skin_x(z,y)+dx),y,z))
            face(q if s>0 else q[::-1],m)
GB=.052;RB=.016                              # gold and red band widths
for s in (-1,1):
    band(s,lambda z:bottom(z),blu,'Rblue')
    band(s,blu,lambda z:blu(z)+GB,'Gold',.0012)
    band(s,lambda z:blu(z)+GB,lambda z:blu(z)+GB+RB,'Red',.0012)
def side_decal(s,z0,z1,y0,y1,rect,nu=6,nv=3):
    a,b=(z0,z1) if s<0 else (z1,z0)
    conform(lambda u,v:(s*(skin_x(u,v)+.003),v,u),(a,b,y0,y1),rect,nu,nv)
for s in (-1,1):
    current='door'+str(s);part('Door decals')
    side_decal(s,.24,.58,.500,.760,NUM,5,5)                       # number panel at the front of the door
    side_decal(s,-.50,.20,.610,.741,R_WHITE,10,2)                 # sponsor stack behind it, on the blue
    side_decal(s,-.50,.00,.545,.600,PORSCHE_W,8,1)
    side_decal(s,-.50,-.10,.478,.535,DUNLOP,6,1);side_decal(s,-.50,-.05,.410,.466,BILSTEIN,6,1)
current='nose';part('Front decals')
def front(u,v):return (u,v,face_zf(v)+.004)
# Blue valance, with a gold and red stripe across the nose between the headlamps.
grid(lambda u,y:(u*side_x(ZN,y)*.995,y,face_zf(y)+.003),seq(-1,1,30),[FY0,.440],'Rblue')
grid(lambda u,y:(u*side_x(ZN,y)*.995,y,face_zf(y)+.003),seq(-1,1,30),[.440,.482],'Gold')
grid(lambda u,y:(u*side_x(ZN,y)*.995,y,face_zf(y)+.003),seq(-1,1,30),[.482,.500],'Red')
conform(lambda u,z:add(bonnet(u,z),(0,.004,0)),(-.30,.30,1.66,1.56),R_BLUE,10,2)       # Rothmans on the bonnet
conform(lambda u,z:add(bonnet(u,z),(0,.004,0)),(-.15,.15,1.48,1.388),SHELL,6,2)
current='canopy';part('Windscreen banner')
grid(lambda u,t:add(wind(u,t),(0,.002,.003)),seq(-1,1,10),[.855,.995],'Rblue')
conform(lambda u,t:add(wind(u,t),(0,.004,.006)),(-.90,.90,.875,.978),BANNER,16,2)
# Blue, white and red stripes across the front edge of the roof.
for k,m in enumerate(('Rblue','Ivory','Red')):
    t0=.0+k*.020;grid(lambda u,z:add(roof(u,z),(0,.004,0)),seq(-.72,.72,12),[HZ-.004-(k+1)*.030,HZ-.004-k*.030],m)
current='tail';part('Tail panel livery')
def tail(u,v):return (u,v,ZT-.0105)
grid(lambda u,y:(u*side_x(ZT,y)*.995,y,ZT-.003),seq(-1,1,24),[.34,.52],'Rblue')
conform(tail,(.52,-.52,.700,.780),TAIL_SCRIPT,12,1)
