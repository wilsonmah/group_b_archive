# HB Audi Team livery of Nº 2 (Röhrl / Geistdörfer). Positions are measured from the side photo
# (z = (px-900)/458.6, y = (1030-py)/458.6) and the front and rear photos; every graphic keeps the
# aspect ratio of its artwork in decals.png.
HB=(0,0,400,440);MICH=(420,8,1020,104);CASTROL=(1040,4,1440,104);AUDISPORT=(1460,10,2040,96)
QUATTRO=(420,124,1420,226);SKF=(1440,120,1800,260);BOGE=(1440,280,1900,410);BOSCH=(0,460,1000,540)
NUM2=(1020,440,1200,760);CREW=(0,560,820,690);TURBO=(0,700,700,770);AUDIWORD=(1220,440,1500,540)
BANNER=(0,800,980,900);PLATE=(1520,560,2000,660)

def side_decal(s,xfun,z0,z1,y0,y1,rect,ref=None,lift=.003,nu=8,nv=3):
    """Lay artwork on a side panel. Text reads front-wards on the right flank and rear-wards on the
    left, as painted. ref(z) shifts the artwork to follow a sloping body line."""
    zm=(z0+z1)/2
    def fn(u,v):
        dy=(ref(u)-ref(zm)) if ref else 0
        return (s*(xfun(u,v+dy)+lift),v+dy,u)
    a,b=(z0,z1) if s<0 else (z1,z0)
    conform(fn,(a,b,y0,y1),rect,nu,nv)

def door_x(z,y):return XD-.020*clamp((y-.30)/.56,0,1)
def flare_x(z,y):
    if z<.74:return XD+(XF-XD)*clamp((z-.62)/.12,0,1)
    return XF-.07*clamp((z-1.86)/.21,0,1)**2
def rear_x(z,y):return XF
def inner_x(z,y):return XI-.012*clamp((y-ledge(z))/(shoulder(z)-ledge(z)+1e-6),0,1)
def skirt_x(z,y):return .848

# ── Yellow side skirts below the doors (BOSCH fuel injection) ─────────────────────────────
current='chassis';part('Side skirts')
for s in (-1,1):
    za,zb=RZ+RA-.004,FZ-RA+.004
    grid(lambda z,y:(s*(.848-.010*clamp((.200-y)/.025,0,1)),y,z),seq(za,zb,10),[.175,.200,.292],'Yellow',s<0)
    face([(s*.835,.292,za),(s*.835,.292,zb),(s*.848,.292,zb),(s*.848,.292,za)][::s],'Yellow')

current='nose';part('Front decals')
for s in (-1,1):
    side_decal(s,flare_x,.700,1.010,.588,.637,MICH,nu=10)
    side_decal(s,inner_x,1.050,1.400,.688,.740,AUDISPORT,ref=ledge,nu=10)
    side_decal(s,inner_x,1.525,1.755,.622,.708,CASTROL,ref=ledge,nu=8)
    side_decal(s,flare_x,1.505,1.744,.218,.458,HB,nu=6,nv=6)
# MICHELIN across the sloping bumper face; HB logos and the rings on the bonnet nose.
conform(lambda u,v:add(bumper(u,v),(0,.002,.003)),(-.36,.36,.82,.46),MICH,14,3)
for s in (-1,1):
    x0,x1=s*.30,s*.48
    conform(lambda u,v:(u,top_y(u,v)+.003,v),(min(x0,x1),max(x0,x1),1.79,1.60),HB,6,6)
current='canopy';part('Windscreen banner')
conform(lambda u,t:add(wind(u,t),(0,.004,.006)),(-.86,.86,.878,.982),BANNER,16,2)

for s in (-1,1):
    current='door'+str(s);part('Door decals')
    side_decal(s,door_x,-.500,-.140,.414,.785,HB,nu=6,nv=6)
    side_decal(s,door_x,.085,.231,.403,.665,NUM2,nu=3,nv=6)
    side_decal(s,door_x,.100,.580,.752,.828,CREW,nu=8,nv=2)

current='tail';part('Rear decals')
for s in (-1,1):
    side_decal(s,rear_x,-1.290,-.690,.756,.818,QUATTRO,nu=10)
    side_decal(s,rear_x,-1.830,-1.570,.786,.818,TURBO,nu=6)
    side_decal(s,rear_x,-1.860,-1.540,.560,.690,SKF,nu=6,nv=3)
    side_decal(s,rear_x,-1.830,-1.470,.437,.545,BOGE,nu=6,nv=3)
    side_decal(s,rear_x,-1.310,-.990,.611,.661,MICH,nu=8)
    # HB logo on each wing end plate.
    a,b=(-1.850,-1.710) if s<0 else (-1.710,-1.850)
    conform(lambda u,v:(s*(WX+.003),v,u),(a,b,.970,1.120),HB,4,4)
# Tail: Audi and quattro in the yellow band, registration plate and HB logo above (rear photos).
def tail(u,v):return (u,v,ZT-.004)
conform(tail,(.56,.37,.766,.834),AUDIWORD,4,2)
conform(tail,(-.24,-.66,.776,.820),QUATTRO,8,2)
conform(tail,(.40,-.08,.930,1.030),PLATE,6,2)
conform(tail,(-.40,-.52,.905,1.037),HB,3,3)

current='nose';part('Bonnet stripes')
# Three diagonal bands each side (red, taupe, black from the outside in), running from the
# screen base towards the bonnet nose and converging into a V (front photos).
for s in (-1,1):
    P0=(s*.68,.80);P1=(s*.10,1.60)
    d=unit((P1[0]-P0[0],P1[1]-P0[1]));n=(-d[1]*s,d[0]*s)
    offs=[(0,.040,'Red'),(.050,.095,'Taupe'),(.105,.185,'Black')]
    for o0,o1,m in offs:
        for t0,t1 in zip(seq(0,1,10),seq(0,1,10)[1:]):
            pts=[]
            for t,o in [(t0,o0),(t1,o0),(t1,o1),(t0,o1)]:
                x=P0[0]+(P1[0]-P0[0])*t-n[0]*o;z=P0[1]+(P1[1]-P0[1])*t-n[1]*o
                x=clamp(x,-XI+.01,XI-.01);pts.append((x,top_y(x,z)+.0025,z))
            face(pts if s>0 else pts[::-1],m)
