# Mud flaps and underbody guard of the Paris-Dakar car.
current='tail';part('Mud flaps')
for s in (-1,1):
    for zc,xc in ((RZ,RX),(FZ,FX)):
        z0=zc-RA-.03 if zc<0 else zc+RA+.02
        sg=-1 if zc<0 else 1
        plate([(s*(xc-.10),.42,z0),(s*(xc+.14),.42,z0),(s*(xc+.14),.06,z0+sg*.03),(s*(xc-.10),.06,z0+sg*.03)],'Ivory',(0,0,-sg*.008))
part('Engine underguard')
box((0,.225,-1.62),(.78,.012,.80),'Charcoal')
for k in range(7):box((0,.232,-1.28-k*.10),(.76,.006,.012),'Black')
