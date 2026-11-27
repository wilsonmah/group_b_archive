# Rothmans Porsche 959 Paris-Dakar, car 186, from side, 3/4 and rear photographs. White upper body,
# royal-blue lower body; a gold band with a thin red line above it runs just under the side windows,
# sweeps down the front wings to cross the nose above the bumper, and follows the rear hips to the
# tail. Graphics keep the aspect ratio of their artwork in decals.png.
mat('Rblue','1F3F9A',.12,.30)
NUM=(20,20,520,430);R_WHITE=(20,480,820,630);PORSCHE_W=(20,670,660,740);DUNLOP=(20,790,580,870);BILSTEIN=(20,910,660,990)
BANNER=(20,1040,1520,1150);R_BLUE=(20,1200,920,1350);SHELL=(20,1400,540,1560);TAIL_SCRIPT=(20,1620,1120,1710)
PECTEN=(1000,1400,1240,1630);OVAL=(1300,1400,1580,1560);PLATE=(1000,20,1560,140)
# Top of the blue, by station: low on the nose, just under the window along the door, following
# the rear hip crest back to the tail.
BLU=[(ZT,.800),(-2.00,.835),(-1.70,.870),(-1.30,.895),(-.90,.890),(DZ0,.885),(.40,.882),(DZ1,.876),
     (.90,.835),(1.20,.800),(1.50,.745),(1.75,.680),(1.92,.600),(ZN,.560)]
def blu(z):return sinterp(z,BLU)
GB=.050;RB=.014                              # gold and red band widths
def stripe_cur(z,s):
    global cur
    key=('nose' if z>DZ1 else 'tail' if z<DZ0 else 'door'+str(s),'Livery panels')
    if key not in parts:parts[key]={}
    cur=key
def skin_x(z,y):return side_x(z,y)+(.011 if DZ0<=z<=DZ1 else .007)
def band(s,y0f,y1f,m,dx=0,steps=14):
    zs=zstations(ZT+.01,ZN-.01,160)
    for a,b in zip(zs,zs[1:]):
        la,lb=max(y0f(a),bottom(a)),max(y0f(b),bottom(b));ha,hb=y1f(a),y1f(b)
        if la>=ha-.004 or lb>=hb-.004:continue
        stripe_cur((a+b)/2,s)
        for t0,t1 in zip(seq(0,1,steps),seq(0,1,steps)[1:]):
            q=[]
            for z,lo,hi,t in [(a,la,ha,t0),(b,lb,hb,t0),(b,lb,hb,t1),(a,la,ha,t1)]:
                y=lo+(hi-lo)*t;q.append((s*(skin_x(z,y)+dx),y,z))
            face(q if s>0 else q[::-1],m)
for s in (-1,1):
    band(s,lambda z:bottom(z),blu,'Rblue')
    band(s,blu,lambda z:blu(z)+GB,'Gold',.0010,3)
    band(s,lambda z:blu(z)+GB,lambda z:blu(z)+GB+RB,'Red',.0010,1)
def side_decal(s,z0,z1,y0,y1,rect,nu=6,nv=3):
    a,b=(z0,z1) if s<0 else (z1,z0)
    conform(lambda u,v:(s*(skin_x(u,v)+.003),v,u),(a,b,y0,y1),rect,nu,nv)
for s in (-1,1):
    current='door'+str(s);part('Door decals')
    side_decal(s,.250,.600,.520,.800,NUM,5,5)                     # number panel at the front of the door
    side_decal(s,-.420,.200,.712,.820,R_WHITE,10,2)               # Rothmans, PORSCHE, DUNLOP, BILSTEIN
    side_decal(s,-.400,.180,.638,.690,PORSCHE_W,8,1)
    side_decal(s,-.330,.110,.566,.620,DUNLOP,6,1)
    side_decal(s,-.300,.080,.498,.550,BILSTEIN,6,1)
    current='nose';part('Front decals')
    side_decal(s,1.62,1.94,.470,.528,DUNLOP,6,1)
    side_decal(s,1.62,1.94,.405,.457,BILSTEIN,6,1)
    current='tail';part('Rear decals')
    side_decal(s,-2.05,-1.62,.660,.770,SHELL,6,2)
current='nose';part('Nose livery')
def front(u,v):return (u,v,ZN+.004)
for y0,y1,m in ((.250,.560,'Rblue'),(.560,.610,'Gold'),(.610,.624,'Red')):
    grid(lambda u,y:(u*side_x(ZN,y)*.995,y,ZN+.003),seq(-1,1,30),[y0,y1],m)
conform(lambda u,z:add(bonnet(u,z),(0,.004,0)),(-.26,.26,1.62,1.50),R_BLUE,10,2)       # Rothmans on the bonnet
current='canopy';part('Windscreen banner, roof stripes and quarter panels')
grid(lambda u,t:add(wind(u,t),(0,.002,.003)),seq(-1,1,10),[.850,.995],'Rblue')
conform(lambda u,t:add(wind(u,t),(0,.004,.006)),(-.82,.82,.870,.978),BANNER,16,2)
# Blue, red and blue stripes running fore and aft along the roof (rear photo).
for x0,x1,m in ((-.17,-.11,'Rblue'),(-.03,.03,'Red'),(.11,.17,'Rblue')):
    grid(lambda u,z:add(roof(u,z),(0,.004,0)),[x0/.54,x1/.54],seq(RZ0+.02,HZ-.02,10),m)
for s in (-1,1):
    def qp(z,v):
        p,e=belt(z),edge(z);return add(mix((s*p[0],p[1],z),(s*e[0],e[1],z),v),(s*.008,0,0))
    a,b=(-.96,-.60) if s<0 else (-.60,-.96)
    conform(lambda u,v:qp(u,.14+.40*v),(a,b,0,1),SHELL,6,2)
    a,b=(-.80,-.66) if s<0 else (-.66,-.80)
    conform(lambda u,v:qp(u,.56+.24*v),(a,b,0,1),OVAL,3,2)
    a,b=(-.92,-.82) if s<0 else (-.82,-.92)
    conform(lambda u,v:qp(u,.56+.24*v),(a,b,0,1),PECTEN,3,2)
current='tail';part('Tail livery')
def tail(u,v):return (u,v,ZT-.006)
for y0,y1,m in ((.320,.800,'Rblue'),(.800,.835,'Gold'),(.835,.846,'Red')):
    grid(lambda u,y:(u*side_x(ZT,y)*.995,y,ZT-.003),seq(-1,1,24),[y0,y1],m)
conform(lambda u,v:(u,v,ZT-.014),(.30,-.30,.742,.778),TAIL_SCRIPT,10,1)   # PORSCHE across the reflector
conform(lambda u,v:(u,v,ZT-.012),(.19,-.19,.440,.500),PLATE,6,1)
for s in (-1,1):conform(tail,(s*.42+.07,s*.42-.07,.430,.540),PECTEN,3,2)
