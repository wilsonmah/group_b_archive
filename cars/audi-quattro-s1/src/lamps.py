# Night-stage lamp pod in front of the grille: two large Bosch lamps over four Hella lamps
# (front photos), carried on a tubular frame bolted to the bumper.
def rally_lamp(x,y,z,r,depth):
    back=(x,y,z-depth);front=(x,y,z)
    shell(back,(0,0,1),[(0,r*.40),(depth*.35,r*.86),(depth*.80,r*.99),(depth,r*1.02)],'Black',40)
    tor(front,(0,0,1),r*.99,r*.07,'Black',48,8)
    cyl(add(front,(0,0,-.030)),add(front,(0,0,-.026)),r*.92,'Reflector',40)
    cyl(add(front,(0,0,-.002)),add(front,(0,0,.001)),r*.93,'Optical glass',40)
    for k in range(-6,7):
        w=sqrt(max(0,(r*.9)**2-(k*r*.13)**2))
        box((x+k*r*.13,y,z+.003),(.0016,2*w,.0016),'Lens')
    cyl(add(front,(0,0,.004)),add(front,(0,0,.006)),r*.10,'Silver',16)
group('lamps','Auxiliary lamp pod','夜赛辅助灯组',(0,.10,.65),'车头前方的六灯组：上排两盏 Bosch 远射灯，下排四盏 Hella 雾灯，装在管式支架上。')
part('Lamp frame')
for y in (.455,.665):path([(-.50,y,1.935),(.50,y,1.935)],.011,'Black',10)
for s in (-1,1):
    path([(s*.30,.455,1.935),(s*.30,.665,1.935)],.011,'Black',10)
    path([(s*.30,.455,1.935),(s*.28,.420,1.885)],.011,'Black',10)
part('Two Bosch long-range lamps')
for s in (-1,1):rally_lamp(s*.268,.665,2.000,.104,.085)
part('Four Hella fog lamps')
for x in (-.40,-.14,.14,.40):rally_lamp(x,.455,2.010,.088,.075)

current='tail';part('Rear mud flaps')
for s in (-1,1):
    plate([(s*.66,.36,-1.52),(s*.90,.36,-1.52),(s*.90,.045,-1.56),(s*.66,.045,-1.56)],'Rubber',(0,0,-.008))
current='canopy';part('Roof aerial')
cyl((.10,1.322,-.40),(.10,1.334,-.40),.014,'Black',16)
cyl((.10,1.334,-.40),(.10,1.80,-.62),.0022,'Gunmetal',8)
