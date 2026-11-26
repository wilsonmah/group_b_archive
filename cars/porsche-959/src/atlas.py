# Livery artwork atlas (2048 x 2048, transparent) for the Porsche 959 Paris-Dakar study.
# Every word is stretched to the exact rectangle livery.py maps it to, so graphics are unstretched on the car.
# Run with: python3 atlas.py   (needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parent/'decals.png'
F={'sans':'/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf','serif':'/usr/share/fonts/opentype/urw-base35/NimbusRoman-Bold.otf',
   'ital':'/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf','narrow':'/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'}
img=Image.new('RGBA',(2048,2048),(0,0,0,0));d=ImageDraw.Draw(img)
BLUE='#1f3f9a';RED='#d3182a';WHITE='#fffefa';BLACK='#101214';GOLD='#c9ad6c'
def word(text,x,y,w,h,color,font='sans'):
    f=ImageFont.truetype(F[font],400);bb=f.getbbox(text)
    m=Image.new('L',(bb[2]-bb[0],bb[3]-bb[1]),0);ImageDraw.Draw(m).text((-bb[0],-bb[1]),text,font=f,fill=255)
    m=m.resize((int(w),int(h)),Image.LANCZOS);img.paste(Image.new('RGBA',m.size,color),(int(x),int(y)),m)
# Door number panel: white plate, red header bar, black number.
d.rectangle((20,20,520,430),fill=WHITE);d.rectangle((20,20,520,150),fill=RED);d.rectangle((20,150,520,160),fill=BLUE)
word('VSD',50,48,200,76,WHITE,'ital');word('NASA',290,48,200,76,WHITE,'ital')
word('185',50,190,440,220,BLACK)
# Door sponsor stack, white on the blue panel.
word('Rothmans',20,480,800,150,WHITE,'serif')
word('PORSCHE',20,670,640,70,WHITE)
word('DUNLOP',20,790,560,80,WHITE,'ital');word('BILSTEIN',20,910,640,80,WHITE,'ital')
# Windscreen banner and nose lettering.
word('NASA Rothmans VSD',20,1040,1500,110,WHITE,'ital')
word('Rothmans',20,1200,900,150,BLUE,'serif')
word('Shell',20,1400,520,160,BLUE,'ital')
# Tail script.
word('P O R S C H E',20,1620,1100,90,WHITE)
word('DUNLOP',20,1760,520,80,WHITE,'ital');word('BILSTEIN',600,1760,620,80,WHITE,'ital')
img.save(OUT);print('saved',OUT)
