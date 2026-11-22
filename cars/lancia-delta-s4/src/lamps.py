# Night-stage pod of four driving lamps on the bonnet nose (Martini cars at night stages), mud
# flaps and the roof aerial.
def rally_lamp(x,y,z,r,depth):
    back=(x,y,z-depth);front=(x,y,z)
    shell(back,(0,0,1),[(0,r*.40),(depth*.35,r*.86),(depth*.80,r*.99),(depth,r*1.02)],'Black',40)
    tor(front,(0,0,1),r*.99,r*.07,'Black',48,8)
    cyl(add(front,(0,0,-.030)),add(front,(0,0,-.026)),r*.92,'Reflector',40)
    cyl(add(front,(0,0,-.002)),add(front,(0,0,.001)),r*.93,'Optical glass',40)
    for k in range(-6,7):
        w=sqrt(max(0,(r*.9)**2-(k*r*.13)**2));box((x+k*r*.13,y,z+.003),(.0016,2*w,.0016),'Lens')
group('lamps','Auxiliary lamp pod','夜赛辅助灯组',(0,.10,.65),'夜间赛段使用的四盏辅助灯，固定在车头前缘。')
part('Lamp carrier')
path([(-.46,.700,2.000),(.46,.700,2.000)],.012,'Black',10)
for k in (-1,1):path([(k*.30,.660,1.900),(k*.30,.700,2.000)],.012,'Black',10)
part('Four driving lamps')
for x in (-.345,-.115,.115,.345):rally_lamp(x,.735,2.055,.100,.085)

current='tail';part('Mud flaps')
for s in (-1,1):
    plate([(s*.62,.36,-1.62),(s*.92,.36,-1.62),(s*.92,.04,-1.66),(s*.62,.04,-1.66)],'Ivory',(0,0,-.008))
current='canopy';part('Roof aerial')
cyl((.10,1.300,-.10),(.10,1.312,-.10),.014,'Black',16);cyl((.10,1.312,-.10),(.10,1.78,-.30),.0022,'Gunmetal',8)
