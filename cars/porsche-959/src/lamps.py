# Mud flaps and underbody guard of the Paris-Dakar car.
for zc,xc,g in ((RZ,RX,'tail'),(FZ,FX,'nose')):          # a flap behind every wheel
  current=g;part('Mud flaps')
  for s in (-1,1):
        z0=zc-RA-.03;sg=-1
        plate([(s*(xc-.10),.42,z0),(s*(xc+.14),.42,z0),(s*(xc+.14),.06,z0+sg*.03),(s*(xc-.10),.06,z0+sg*.03)],'Ivory',(0,0,-sg*.008))
current='tail';part('Engine underguard')
box((0,.225,-1.62),(.78,.012,.80),'Charcoal')
for k in range(7):box((0,.232,-1.28-k*.10),(.76,.006,.012),'Black')
