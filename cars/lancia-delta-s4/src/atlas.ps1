param([string]$OutputFile=(Join-Path $PSScriptRoot 'decals.png'))
Add-Type -AssemblyName System.Drawing
$b=New-Object Drawing.Bitmap 2048,2048
$g=[Drawing.Graphics]::FromImage($b)
$g.SmoothingMode='AntiAlias'
$g.Clear([Drawing.Color]::Transparent)
function ink($html){New-Object Drawing.SolidBrush ([Drawing.ColorTranslator]::FromHtml($html))}
function rect($x,$y,$w,$h,$color){$br=ink $color;$g.FillRectangle($br,$x,$y,$w,$h);$br.Dispose()}
function ellipse($x,$y,$w,$h,$color){$br=ink $color;$g.FillEllipse($br,$x,$y,$w,$h);$br.Dispose()}
function word($t,$x,$y,$w,$h,$color,$family='Arial',$style=1){
 $font=New-Object Drawing.FontFamily $family
 $p=New-Object Drawing.Drawing2D.GraphicsPath
 $p.AddString($t,$font,[int]$style,100,[Drawing.PointF]::Empty,[Drawing.StringFormat]::GenericTypographic)
 $r=$p.GetBounds()
 $sx=$w/$r.Width;$sy=$h/$r.Height
 $m=New-Object Drawing.Drawing2D.Matrix ([single]$sx),0,0,([single]$sy),([single]($x-$r.X*$sx)),([single]($y-$r.Y*$sy))
 $p.Transform($m);$br=ink $color;$g.FillPath($br,$p);$br.Dispose();$p.Dispose();$m.Dispose();$font.Dispose()
}
$dark='#0e1626';$red='#de1726';$white='#fffefa'
function martini($x,$y,$w,$h){
 # Round red disc behind a gold-edged black bar, as printed: bar 0.53 x 0.16 m, disc 0.28 m.
 ellipse ($x+($w-$h)/2) $y $h $h $red
 rect $x ($y+$h*.214) $w ($h*.572) '#967946'
 rect ($x+$w*.010) ($y+$h*.236) ($w*.980) ($h*.528) '#15171b'
 word 'MARTINI' ($x+$w*.055) ($y+$h*.300) ($w*.89) ($h*.400) $white
}
function pirelli($x,$y,$w,$h,$color){
 word 'PIRELLI' $x ($y+$h*.2) $w ($h*.79) $color 'Arial' 3
 rect ($x+$w*.08) $y ($w*.91) ($h*.15) $color
}
word '1' 60 6 120 235 $dark
martini 262 3 436 229
word 'L A N C I A' 10 265 554 66 $white
word 'RALLY 037' 8 355 415 66 $dark
word 'LANCIA' 461 352 505 70 $dark
word 'ABARTH' 681 240 318 53 $white
pirelli 707 33 302 61 '#d1d2c8'
word 'LANCIA MARTINI' 16 530 1268 106 $white 'Arial' 3
word 'MARTINI RACING' 16 665 1420 105 $white 'Arial' 3
word 'LANCIA MARTINI' 330 1520 1268 106 $dark 'Arial' 3
word '1' 1510 525 92 264 '#101112'
rect 14 795 768 122 $red
word 'RALLYE DE FRANCE' 70 814 661 81 $white 'Arial' 3
foreach($x in @(25,741)){ellipse $x 836 28 30 $white;ellipse ($x+5) 841 18 20 $red}
rect 797 795 440 122 '#192748'
word 'Rothmans' 817 812 401 87 $white 'Times New Roman'
word 'MAGNETI' 22 950 283 57 $dark
word 'MARELLI' 17 1013 296 58 $dark
# Sponsor stack drawn at the 0.22 x 0.28 m panel on the door, so it is printed unstretched.
rect 26 1504 286 66 $dark
word 'speedline' 40 1513 258 46 $white 'Arial' 3
word 'BILSTEIN' 34 1586 270 54 $dark
word 'brembo' 46 1658 246 58 $dark
word 'FERODO' 44 1736 250 52 $dark
word 'sabelt' 62 1808 214 58 $dark 'Arial' 3
word 'olivetti' 682 950 344 77 $dark
word 'pininfarina' 690 1069 402 49 $dark 'Times New Roman' 3
pirelli 1120 948 421 100 '#171819'
word '◆ SIEM' 1580 953 430 75 '#191b1b'
rect 17 1197 682 128 '#f9f9f6'
foreach($y in @(1204,1260)){rect 23 $y 95 50 '#fafbfd';rect 23 ($y+20) 95 11 '#255d91';rect 49 $y 13 50 '#255d91'}
word 'M. ALÉN' 125 1204 338 44 $dark
word 'I. KIVIMÄKI' 125 1260 444 43 $dark
foreach($row in @(0,1)){
 $txt=@('OLIO','VSFIAT')[$row]
 $cw=64
 for($i=0;$i -lt $txt.Length;$i++){
  $x=733+(6-$txt.Length)*$cw+$i*$cw;$y=1196+65*$row
  rect $x $y 60 60 $dark
  word ([string]$txt[$i]) ($x+9) ($y+7) 42 46 $white 'Arial' 3
 }
}
# Hood roundel: wheel, steering spoke and pennant.
ellipse 1187 1162 365 318 $dark;ellipse 1200 1175 339 292 $white
ellipse 1226 1195 289 250 $dark;ellipse 1236 1204 269 232 $white
rect 1343 1232 15 172 $dark
rect 1214 1260 271 82 $dark
word 'LANCIA' 1227 1274 245 52 $white 'Times New Roman' 3
rect 1592 1169 367 143 '#fffefa';word '1' 1735 1179 56 116 $dark
word 'VX' 23 1394 125 69 '#f9f9f9'
word 'WEBER' 1616 1356 360 66 '#d1202a' 'Arial Black' 0
$b.Save($OutputFile,[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose();$b.Dispose()
