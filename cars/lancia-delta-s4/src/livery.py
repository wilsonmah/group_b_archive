# 1986 Martini Racing livery of car Nº 1, from the studio and event photos: Martini ribbons along
# the bonnet edges that turn down across the front of the doors, a second set rising diagonally
# across the rear quarters, MARTINI roundels, number, sponsor stack and the front and tail graphics.
# Every graphic keeps the aspect ratio of its artwork in decals.png.
NUM=(60,6,180,241);MART=(259,0,701,235);PIRELLI_D=(1116,944,1546,1052);SIEM=(1574,949,2014,1031)
MAGNETI=(13,945,323,1078);STACK=(18,1500,320,1885);OLIVETTI=(676,943,1032,1033);ROUNDEL=(1180,1155,1558,1486)
LM_WHITE=(10,524,1293,643);MR_DARK=(13,659,1444,776);LM_DARK=(330,1520,1598,1626);WEBER=(1612,1352,1978,1426);OLIO=(729,1193,1121,1327)

def stripe_cur(z,s):
    """Each ribbon quad belongs to the panel it is painted on, so it follows that panel when exploded."""
    global cur
    key=('nose' if z>DZ1 else 'tail' if z<DZ0 else 'door'+str(s),'Martini ribbons')
    if key not in parts:parts[key]={}
    cur=key
def skin_x(z,y):
    if y<=upper(z)[0]+1e-6:
        return side_x(z,y)+(.004 if DZ0<=z<=DZ1 else .002)
    if z<DZ0:return .835-(.835-.507)*(y-.858)/(1.29-.858)+.003
    return None
RIBBON_REAR=[(.040,'Blue'),(.012,None),(.040,'Navy'),(.012,None),(.040,'Blue'),(.012,None),(.040,'Navy'),(.012,None),(.120,'Red')]
RIBBON_FRONT=[(.110,'Red'),(.012,None),(.036,'Navy'),(.012,None),(.036,'Blue'),(.012,None),(.036,'Navy'),(.012,None),(.036,'Blue')]
def diagonal(s,P0,P1,bands,n=26):
    d=(P1[0]-P0[0],P1[1]-P0[1]);L=sqrt(d[0]**2+d[1]**2);d=(d[0]/L,d[1]/L);nrm=(-d[1],d[0])
    total=sum(w for w,_ in bands);o=-total/2
    for w,m in bands:
        if m:
            for t0,t1 in zip(seq(0,1,n),seq(0,1,n)[1:]):
                q=[]
                for t,oo in [(t0,o),(t1,o),(t1,o+w),(t0,o+w)]:
                    z=P0[0]+(P1[0]-P0[0])*t+nrm[0]*oo;y=P0[1]+(P1[1]-P0[1])*t+nrm[1]*oo
                    if y<bottom(z)+.004:q=None;break
                    x=skin_x(z,y)
                    if x is None:q=None;break
                    q.append((s*x,y,z))
                if not q:continue
                stripe_cur(sum(p[2] for p in q)/4,s)
                face(q if s>0 else q[::-1],m)
        o+=w
for s in (-1,1):
    diagonal(s,(-.66,.24),(-1.42,1.30),RIBBON_REAR)
    diagonal(s,(.80,.92),(.50,.24),RIBBON_FRONT)
    # Along the bonnet edges, red outermost, narrowing slightly towards the screen.
    stripe_cur(1.5,s)
    edges=[(.835,1.000,'Red'),(.775,.820,'Navy'),(.715,.760,'Blue'),(.655,.700,'Navy'),(.595,.640,'Blue')]
    def bon(u,z):
        k=clamp((ZN-z)/(ZN-DZ1),0,1);x=(.80-.14*k)*u*bonnet_w(z)/.80
        return add(bonnet(s*x,z),(0,.0025,0))
    for a,b,m in edges:
        grid(bon,[a,b],seq(DZ1+.02,ZN-.01,30),m,s<0)

def side_decal(s,z0,z1,y0,y1,rect,nu=6,nv=4):
    a,b=(z0,z1) if s<0 else (z1,z0)
    conform(lambda u,v:(s*skin_x(u,v)+s*.002,v,u),(a,b,y0,y1),rect,nu,nv)
for s in (-1,1):
    current='door'+str(s);part('Door decals')
    side_decal(s,-.36,.10,.470,.715,MART,8,4)
    side_decal(s,.135,.225,.470,.690,NUM,3,5)
    side_decal(s,.255,.415,.455,.659,STACK,3,5)
    current='nose';part('Front decals')
    side_decal(s,1.32,1.58,.600,.712,MAGNETI,5,3)
    current='tail';part('Rear decals')
    side_decal(s,-1.86,-1.44,.555,.635,PIRELLI_D,6,2)
current='nose';part('Front decals')
def front(u,v):return (u,v,face_z(u)+.012)
conform(front,(-.10,.10,.245,.352),MART,6,3)
conform(lambda u,z:add(bonnet(u,z),(0,.004,0)),(-.150,.150,1.985,1.905),MART,6,3)
for s in (-1,1):
    conform(front,(min(s*.42,s*.70),max(s*.42,s*.70),.245,.342),OLIO,6,3)
    conform(front,(min(s*.22,s*.40),max(s*.22,s*.40),.452,.488),WEBER,4,2)
    conform(front,(min(s*.60,s*.84),max(s*.60,s*.84),.420,.500),MAGNETI,5,3)
    conform(front,(min(s*.62,s*.86),max(s*.62,s*.86),.180,.240),PIRELLI_D,6,2)
conform(lambda u,z:add(bonnet(u,z),(0,.004,0)),(-.200,.200,1.82,1.47),ROUNDEL,10,8)
current='canopy';part('Windscreen banner and wing lettering')
grid(lambda u,t:add(wind(u,t),(0,.002,.003)),seq(-1,1,10),[.84,.995],'Navy')
conform(lambda u,t:add(wind(u,t),(0,.004,.006)),(-.90,.90,.855,.982),LM_WHITE,16,2)
conform(lambda u,t:add(wing(u,t),(0,-.020,.004)),(.92,-.92,.22,.82),LM_WHITE,16,3)
current='tail';part('Tail decals')
def tail(u,v):return (u,v,ZT-.006)
grid(lambda x,y:(x,y,ZT-.005),seq(-.62,.62,8),[.800,.870],'Black')
conform(tail,(.46,-.46,.806,.862),(13,659,1444,776),12,2)
for s in (-1,1):conform(tail,(max(s*.64,s*.20),min(s*.64,s*.20),.438,.510),PIRELLI_D,6,2)
box((0,.474,ZT-.008),(.300,.060,.006),'Ivory');path([(-.15,.444,ZT-.012),(.15,.444,ZT-.012),(.15,.504,ZT-.012),(-.15,.504,ZT-.012),(-.15,.444,ZT-.012)],.003,'Black',4)
# MARTINI roundels on the rear mud flaps.
for s in (-1,1):conform(lambda u,v:(u,v,-1.672),(max(s*.68,s*.86),min(s*.68,s*.86),.14,.24),MART,4,3)
