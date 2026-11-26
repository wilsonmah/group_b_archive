# Rothmans livery of Porsche 959 Nº 185 (Metge / Lemoyne), Paris-Dakar 1986. White body, a navy
# lower band edged with gold and red pinstripes, ROTHMANS lettering, number roundels and crew
# names. Graphics keep the aspect ratio of their artwork in decals.png. This livery is drawn from
# the usual descriptions of the car, not calibrated against photographs.
NUM=(20,10,440,250);R_NAVY=(20,280,980,490);R_WHITE=(20,520,1120,670);R_DARK=(20,700,1120,850)
PD_WHITE=(20,880,1220,1000);PD_DARK=(20,1020,1220,1140);PORSCHE_W=(20,1160,920,1290);PORSCHE_D=(20,1310,920,1440)
N959_W=(960,1160,1280,1290);N959_D=(1320,1160,1640,1290);CREW=(20,1480,780,1660);ROUNDEL=(1200,20,1640,460)
TAILBAND=(20,1700,1300,1860);STRIPTXT=(20,1900,1520,1990)
BAND=.440                                  # top of the navy lower band
def stripe_cur(z,s):
    global cur
    key=('nose' if z>DZ1 else 'tail' if z<DZ0 else 'door'+str(s),'Livery bands')
    if key not in parts:parts[key]={}
    cur=key
def skin_x(z,y):return side_x(z,y)+(.006 if DZ0<=z<=DZ1 else .004)
def band(s,y0f,y1,m,dx=0):
    """A horizontal band on the side skin from y0f(z) up to y1, skipping the wheel openings."""
    zs=zstations(ZT+.02,ZN-.02,120)
    for a,b in zip(zs,zs[1:]):
        la,lb=y0f(a),y0f(b)
        if max(bottom(a),bottom(b))>BAND-.012:continue
        stripe_cur((a+b)/2,s)
        for t0,t1 in zip(seq(0,1,5),seq(0,1,5)[1:]):
            q=[]
            for z,lo,t in [(a,la,t0),(b,lb,t0),(b,lb,t1),(a,la,t1)]:
                y=lo+(y1-lo)*t;q.append((s*(skin_x(z,y)+dx),y,z))
            face(q if s>0 else q[::-1],m)
for s in (-1,1):
    band(s,lambda z:bottom(z)+.0,BAND,'Navy')
    band(s,lambda z:BAND,BAND+.012,'Gold',.001)
    band(s,lambda z:BAND+.012,BAND+.020,'Red',.001)
    band(s,lambda z:BAND+.020,BAND+.026,'Navy',.001)
def side_decal(s,z0,z1,y0,y1,rect,nu=6,nv=3):
    a,b=(z0,z1) if s<0 else (z1,z0)
    conform(lambda u,v:(s*(skin_x(u,v)+.003),v,u),(a,b,y0,y1),rect,nu,nv)
for s in (-1,1):
    current='door'+str(s);part('Door decals')
    side_decal(s,-.40,.56,.255,.385,R_WHITE,12,2)               # ROTHMANS on the navy band
    side_decal(s,.04,.38,.560,.760,ROUNDEL,6,6)                # number roundel
    side_decal(s,-.40,-.08,.650,.735,CREW,6,2)                 # crew names
    current='nose';part('Front decals')
    side_decal(s,1.55,1.99,.330,.392,R_WHITE,8,2)
    current='tail';part('Rear decals')
    side_decal(s,-2.03,-1.59,.330,.392,R_WHITE,8,2)
current='nose';part('Front decals')
def front(u,v):return (u,v,ZN-.035*(1-(v-.20)/(bonnet_y(ZN)-.20))**2+.004)
conform(front,(-.22,.22,.395,.445),PORSCHE_D,10,2)
conform(lambda u,z:add(bonnet(u,z),(0,.004,0)),(-.31,.31,1.80,1.665),R_NAVY,10,3)       # Rothmans panel on the bonnet
conform(lambda u,z:add(bonnet(u,z),(0,.004,0)),(-.17,.17,1.28,.94),ROUNDEL,10,8)         # bonnet roundel
current='canopy';part('Windscreen banner and roof lettering')
grid(lambda u,t:add(wind(u,t),(0,.002,.003)),seq(-1,1,10),[.87,.995],'Navy')
conform(lambda u,t:add(wind(u,t),(0,.004,.006)),(-.82,.82,.89,.978),PD_WHITE,16,2)
current='tail';part('Tail decals')
def tail(u,v):return (u,v,ZT-.0105)
box((0,.718,ZT-.004),(.88,.088,.006),'Navy')
conform(tail,(.42,-.42,.680,.756),TAILBAND,12,2)
conform(tail,(.22,-.22,.455,.505),PORSCHE_D,8,2)
