param([string]$OutputFile=(Join-Path $PSScriptRoot 'decals.png'))
# Decal atlas for the HB Audi Team S1 E2 (Nº 2, Röhrl / Geistdörfer). 2048 x 2048, transparent.
Add-Type -AssemblyName System.Drawing
$b=New-Object Drawing.Bitmap 2048,2048
$g=[Drawing.Graphics]::FromImage($b)
$g.SmoothingMode='AntiAlias';$g.TextRenderingHint='AntiAlias'
$g.Clear([Drawing.Color]::Transparent)
function ink($html){New-Object Drawing.SolidBrush ([Drawing.ColorTranslator]::FromHtml($html))}
function rect($x,$y,$w,$h,$c){$br=ink $c;$g.FillRectangle($br,$x,$y,$w,$h);$br.Dispose()}
function ellipse($x,$y,$w,$h,$c){$br=ink $c;$g.FillEllipse($br,$x,$y,$w,$h);$br.Dispose()}
function poly($pts,$c){$br=ink $c;$g.FillPolygon($br,[Drawing.PointF[]]$pts);$br.Dispose()}
function pt($x,$y){New-Object Drawing.PointF ([single]$x),([single]$y)}
function word($t,$x,$y,$w,$h,$c,$family='Arial',$style=1){
 $font=New-Object Drawing.FontFamily $family
 $p=New-Object Drawing.Drawing2D.GraphicsPath
 $p.AddString($t,$font,[int]$style,100,[Drawing.PointF]::Empty,[Drawing.StringFormat]::GenericTypographic)
 $r=$p.GetBounds();$sx=$w/$r.Width;$sy=$h/$r.Height
 $m=New-Object Drawing.Drawing2D.Matrix ([single]$sx),0,0,([single]$sy),([single]($x-$r.X*$sx)),([single]($y-$r.Y*$sy))
 $p.Transform($m);$br=ink $c;$g.FillPath($br,$p);$br.Dispose();$p.Dispose();$m.Dispose();$font.Dispose()
}
function slant($t,$x,$y,$w,$h,$c,$family='Arial',$style=1,$k=-.22){
 # Italic by shearing the glyph outlines, for the Audi Sport / Castrol / Bosch lettering.
 $font=New-Object Drawing.FontFamily $family
 $p=New-Object Drawing.Drawing2D.GraphicsPath
 $p.AddString($t,$font,[int]$style,100,[Drawing.PointF]::Empty,[Drawing.StringFormat]::GenericTypographic)
 $sh=New-Object Drawing.Drawing2D.Matrix 1,0,([single]$k),1,0,0;$p.Transform($sh)
 $r=$p.GetBounds();$sx=$w/$r.Width;$sy=$h/$r.Height
 $m=New-Object Drawing.Drawing2D.Matrix ([single]$sx),0,0,([single]$sy),([single]($x-$r.X*$sx)),([single]($y-$r.Y*$sy))
 $p.Transform($m);$br=ink $c;$g.FillPath($br,$p);$br.Dispose();$p.Dispose();$m.Dispose();$font.Dispose()
}
$black='#111214';$red='#C8152B';$gold='#C9A146';$white='#FFFFFF';$cream='#FBF6E6'
$fam=@('Arial');try{$null=New-Object Drawing.FontFamily 'Century Gothic';$geo='Century Gothic'}catch{$geo='Arial'}

# 1. HB international logo (0,0)-(400,440): crown, red-edged triangle with gold rim, red oval banner.
$cx=200
ellipse ($cx-34) 6 68 30 $red
poly @((pt ($cx-44) 34),(pt ($cx-30) 8),(pt ($cx-14) 30),(pt $cx 2),(pt ($cx+14) 30),(pt ($cx+30) 8),(pt ($cx+44) 34)) $red
foreach($dx in -30,0,30){ellipse ($cx+$dx-6) 0 12 12 $gold}
rect ($cx-44) 34 88 12 $gold
poly @((pt $cx 52),(pt 392 380),(pt 8 380)) $red
poly @((pt $cx 74),(pt 366 366),(pt 34 366)) $gold
poly @((pt $cx 84),(pt 354 360),(pt 46 360)) $cream
word 'HB' 112 178 176 140 $red 'Times New Roman' 1
ellipse 20 318 360 110 $white
ellipse 28 324 344 98 $red
word 'international' 62 352 276 46 $white 'Times New Roman' 0

# 2. MICHELIN (420,8)-(1020,104)
word 'MICHELIN' 420 8 600 96 $black 'Arial Black' 0
# 3. Castrol (1040,4)-(1440,104)
slant 'Castrol' 1040 4 400 100 $black 'Arial' 1 -.18
# 4. Audi Sport (1460,10)-(2040,96)
slant 'Audi Sport' 1460 10 580 86 $black 'Arial' 1 -.20
# 5. quattro (420,130)-(1420,226)
slant 'quattro' 420 130 1000 96 $black $geo 1 -.10
# 6. SKF on blue (1440,120)-(1800,260)
rect 1440 120 360 140 '#1D4F9C';rect 1450 130 340 120 '#1D4F9C'
word 'SKF' 1478 148 284 84 $white 'Arial Black' 0
# 7. BOGE in boxes (1440,280)-(1900,410)
for($i=0;$i -lt 4;$i++){$x=1440+$i*115;rect $x 280 110 130 $black;rect ($x+8) 288 94 114 $white;word ('BOGE'[$i]) ($x+20) 302 70 86 $black 'Arial Black' 0}
# 8. BOSCH fuel injection (0,460)-(1000,540)
word 'BOSCH' 0 462 330 76 $black 'Arial Black' 0
slant 'fuel injection' 370 462 630 76 $black 'Arial' 3 -.14
# 9. Number 2 (1020,440)-(1200,760)
word '2' 1020 440 180 320 $black 'Arial' 1
# 10. Crew names with German flags (0,560)-(820,690)
foreach($row in 0,1){$y=566+$row*64;rect 0 $y 60 16 '#111111';rect 0 ($y+16) 60 16 '#D2232A';rect 0 ($y+32) 60 16 '#F0C41C'}
word 'CH. GEISTDOERFER O+' 80 566 740 50 $black 'Arial' 0
word 'W. ROEHRL A+' 80 630 470 50 $black 'Arial' 0
# 11. KKK Turbolader (0,700)-(700,770)
poly @((pt 30 700),(pt 60 770),(pt 0 770)) $black;word 'KKK' 10 742 40 22 $white 'Arial Black' 0
slant 'Turbolader' 80 704 620 64 $black 'Arial' 1 -.12
# 12. Audi wordmark (1220,440)-(1500,540)
word 'Audi' 1220 440 280 100 $black $geo 1
# 13. HB Audi TEAM windscreen banner (0,800)-(1600,900): white lettering on transparent.
word 'HB' 0 806 170 88 $white 'Arial Black' 0
word 'Audi' 210 806 300 88 $white $geo 1
slant 'TEAM' 560 806 420 88 $white 'Arial Black' 0 -.15
# 14. Registration plate IN-NL 24 (1520,560)-(2000,660)
rect 1520 560 480 100 '#111111';rect 1524 564 472 92 $white
rect 1528 568 34 84 '#1D3F9C'
word 'IN-NL 24' 1580 578 400 66 $black 'Arial' 1
# 15. Small Audi Sport rings badge for the bonnet front (1220,560)-(1500,640)
for($i=0;$i -lt 4;$i++){$p=New-Object Drawing.Pen ([Drawing.ColorTranslator]::FromHtml('#C9CCCF')),9;$g.DrawEllipse($p,1226+$i*62,566,78,68);$p.Dispose()}
$b.Save($OutputFile,[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose();$b.Dispose()
