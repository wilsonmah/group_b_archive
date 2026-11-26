# Livery artwork atlas (2048 x 2048, transparent) for the Porsche 959 Paris-Dakar study.
# Every word is stretched to the exact rectangle livery.py maps it to, so graphics are unstretched on the car.
# Run with: python3 atlas.py   (needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parent/'decals.png'
F={'sans':'/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf','serif':'/usr/share/fonts/opentype/urw-base35/NimbusRoman-Bold.otf',
   'narrow':'/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'}
img=Image.new('RGBA',(2048,2048),(0,0,0,0));d=ImageDraw.Draw(img)
DARK='#0c1a36';RED='#d3182a';WHITE='#fffefa';GOLD='#c8a24a';BLACK='#101214'
def word(text,x,y,w,h,color,font='sans'):
    f=ImageFont.truetype(F[font],400);bb=f.getbbox(text)
    m=Image.new('L',(bb[2]-bb[0],bb[3]-bb[1]),0);ImageDraw.Draw(m).text((-bb[0],-bb[1]),text,font=f,fill=255)
    m=m.resize((int(w),int(h)),Image.LANCZOS);img.paste(Image.new('RGBA',m.size,color),(int(x),int(y)),m)
word('185',20,10,420,240,BLACK)
d.rectangle((20,280,980,490),fill=DARK);d.rectangle((20,280,980,290),fill=GOLD);d.rectangle((20,480,980,490),fill=GOLD)
word('Rothmans',70,320,860,130,WHITE,'serif')
word('ROTHMANS',20,520,1100,150,WHITE);word('ROTHMANS',20,700,1100,150,DARK)
word('PARIS - DAKAR',20,880,1200,120,WHITE);word('PARIS - DAKAR',20,1020,1200,120,DARK)
word('PORSCHE',20,1160,900,130,WHITE);word('PORSCHE',20,1310,900,130,DARK)
word('959',960,1160,320,130,WHITE);word('959',1320,1160,320,130,DARK)
# Crew panel: white plate, tricolour flag, two names.
d.rectangle((20,1480,780,1660),fill='#f8f8f4')
for i,c in enumerate(('#1f3f94','#f8f8f4','#d3182a')):d.rectangle((36+i*30,1496,66+i*30,1552),fill=c)
d.rectangle((36,1496,126,1552),outline='#c8c8c0')
word('R. METGE',150,1496,590,56,DARK);word('D. LEMOYNE',150,1580,590,56,DARK)
# Number roundel: white disc, black 185.
d.ellipse((1200,20,1640,460),fill=WHITE);d.ellipse((1215,35,1625,445),outline=BLACK,width=6)
word('185',1262,170,316,150,BLACK)
# Rothmans tail band, white on navy.
d.rectangle((20,1700,1300,1860),fill=DARK);word('ROTHMANS',60,1730,1180,100,WHITE)
# Lettered sponsor strip for the door (dark on white).
word('ROTHMANS INTERNATIONAL',20,1900,1500,90,DARK,'narrow')
img.save(OUT);print('saved',OUT)
