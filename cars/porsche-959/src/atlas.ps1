param([string]$OutputFile=(Join-Path $PSScriptRoot 'decals.png'))
# Decal atlas (2048 x 2048, transparent) for the Rothmans Porsche 959 Paris-Dakar, car 186.
# Every word is fitted to the exact rectangle livery.py maps it to, so graphics are unstretched.
Add-Type -AssemblyName System.Drawing
$b=New-Object Drawing.Bitmap 2048,2048
$g=[Drawing.Graphics]::FromImage($b);$g.SmoothingMode='AntiAlias';$g.Clear([Drawing.Color]::Transparent)
function ink($h){New-Object Drawing.SolidBrush ([Drawing.ColorTranslator]::FromHtml($h))}
function rect($x,$y,$w,$h,$c){$br=ink $c;$g.FillRectangle($br,$x,$y,$w,$h);$br.Dispose()}
function ellipse($x,$y,$w,$h,$c){$br=ink $c;$g.FillEllipse($br,$x,$y,$w,$h);$br.Dispose()}
function word($t,$x,$y,$w,$h,$c,$family='Arial',$style=1){
 $font=New-Object Drawing.FontFamily $family;$p=New-Object Drawing.Drawing2D.GraphicsPath
 $p.AddString($t,$font,[int]$style,100,[Drawing.PointF]::Empty,[Drawing.StringFormat]::GenericTypographic)
 $r=$p.GetBounds();$sx=$w/$r.Width;$sy=$h/$r.Height
 $m=New-Object Drawing.Drawing2D.Matrix ([single]$sx),0,0,([single]$sy),([single]($x-$r.X*$sx)),([single]($y-$r.Y*$sy))
 $p.Transform($m);$br=ink $c;$g.FillPath($br,$p);$br.Dispose();$p.Dispose();$m.Dispose();$font.Dispose()
}
$BLUE='#1f3f9a';$RED='#d3182a';$WHITE='#fffefa';$BLACK='#101214';$YEL='#f4c400';$GREEN='#1d8f3a'
# Door number panel: white plate, VSD (green) and NASA (yellow) header, black 186.
rect 20 20 500 410 $WHITE
rect 20 20 250 130 $GREEN;word 'VSD' 48 44 194 82 $YEL 'Arial Black' 0
rect 270 20 250 130 $YEL;word 'NASA' 292 46 206 78 $BLUE 'Arial Black' 0
word '186' 46 180 448 228 $BLACK 'Arial' 1
# Door stack in white on the blue.
word 'Rothmans' 20 480 800 150 $WHITE 'Times New Roman' 1
word 'P O R S C H E' 20 670 640 70 $WHITE 'Arial' 1
word 'DUNLOP' 20 790 560 80 $WHITE 'Times New Roman' 3
word 'BILSTEIN' 20 910 640 80 $WHITE 'Arial' 1
# Windscreen banner and bonnet lettering.
word 'Rothmans  VSD' 20 1040 1500 110 $WHITE 'Arial' 1
word 'Rothmans' 20 1200 900 150 $BLUE 'Times New Roman' 1
word 'Shell' 20 1400 520 160 $WHITE 'Arial' 1
word 'P O R S C H E' 20 1620 1100 90 $WHITE 'Arial' 1
# Shell pecten: yellow scalloped shell with a red outline over a red base.
$cx=1120;$cy=1520
$pts=@();for($i=0;$i -le 40;$i++){$a=[math]::PI*(1-$i/40);$r=112+8*[math]::Cos(14*[math]::PI*$i/40);$pts+=New-Object Drawing.PointF ([single]($cx+$r*[math]::Cos($a))),([single]($cy-$r*[math]::Sin($a)))}
$pts+=New-Object Drawing.PointF ([single]($cx+70)),([single]($cy+100));$pts+=New-Object Drawing.PointF ([single]($cx-70)),([single]($cy+100))
$br=ink $RED;$g.FillPolygon($br,[Drawing.PointF[]]$pts);$br.Dispose()
$in=@();foreach($p in $pts){$in+=New-Object Drawing.PointF ([single]($cx+($p.X-$cx)*.86)),([single]($cy+($p.Y-$cy)*.86))}
$br=ink $YEL;$g.FillPolygon($br,[Drawing.PointF[]]$in);$br.Dispose()
$pen=New-Object Drawing.Pen ([Drawing.ColorTranslator]::FromHtml($RED)),6
for($i=-3;$i -le 3;$i++){$g.DrawLine($pen,[single]$cx,[single]($cy+80),[single]($cx+95*[math]::Sin($i*.42)),[single]($cy-95*[math]::Cos($i*.42)))};$pen.Dispose()
# 959 oval plate on the rear quarter panel.
ellipse 1300 1400 280 160 $WHITE
$pen=New-Object Drawing.Pen ([Drawing.ColorTranslator]::FromHtml($BLACK)),8;$g.DrawEllipse($pen,1306,1406,268,148);$pen.Dispose()
word '959' 1370 1438 140 84 $BLACK 'Arial' 1
# Yellow rear registration plate.
rect 1000 20 560 120 $YEL;word 'B368 MDP' 1030 36 500 88 $BLACK 'Arial' 1
$b.Save($OutputFile,[Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$b.Dispose()
