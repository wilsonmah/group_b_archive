// Keep model identifiers and select values independent of the display language.
const englishText = {
  '整车':'Car', '发动机':'Engine', '变速箱':'Gearbox', '悬挂':'Suspension', '运转':'Run',
  '模型视图':'Model views', '蓝旗亚 Delta S4 拉力赛车':'Lancia Delta S4', '蓝旗亚 Delta S4 三维模型，可拖动旋转和滚轮缩放':'3D Lancia Delta S4. Drag to orbit and scroll to zoom.', '蓝旗亚 Delta S4 · Martini Racing · 1 号':'Lancia Delta S4 · Martini Racing · No. 1', '双叉臂悬挂、转向与制动':'Double-wishbone suspension, steering and brakes', '1.8 升双增压直列四缸':'1.8-litre twin-charged inline-four', '五速变速箱与全时四驱':'Five-speed gearbox and permanent four-wheel drive', '前传动轴':'Front propshaft', '后传动轴':'Rear propshaft', '中央差速器与传动轴':'Centre differential and shafts', '弹簧与减振器':'Springs and dampers', '四缸行程':'Four-cylinder strokes', '点火顺序 1 → 3 → 4 → 2，每 180° 点火一次。蓝色为进气机构，红色为排气机构。':'Firing order 1 → 3 → 4 → 2, one firing every 180°. Blue marks the intake valvetrain and red the exhaust.', '整车透视 · 全时四驱':'See-through car · permanent four-wheel drive', '前差速器':'Front differential', '中央差速器':'Centre differential', '后差速器':'Rear differential', '传动轴':'Propshaft', '左前半轴':'Front left driveshaft', '右前半轴':'Front right driveshaft', '左后半轴':'Rear left driveshaft', '右后半轴':'Rear right driveshaft', '左前轮':'Front left wheel', '右前轮':'Front right wheel', '车轮':'Wheels', '五缸行程':'Five-cylinder strokes', '5 缸':'Cyl 5', '点火顺序 1 → 2 → 4 → 5 → 3，每 144° 点火一次。蓝色为进气机构，红色为排气机构。':'Firing order 1 → 2 → 4 → 5 → 3, one firing every 144°. Blue marks the intake valvetrain and red the exhaust.', '传动比取自模型齿数，主减速比 37∶9。配气采用简化的四冲程正时。转向按阿克曼几何计算，方向盘转 15° 前轮转 1°。中央与前后差速器按理想开放式差速计算，每个车轮按各自的转弯半径滚动。轮速单位为 r/min，负值表示倒转。':'Gear ratios come from the modelled tooth counts, with a 37:9 final drive. Valve timing is a simplified four-stroke cycle. Steering follows Ackermann geometry at 15° of steering wheel per degree of road wheel. The centre, front and rear differentials are treated as ideal open differentials, so each wheel rolls at its own turning radius. Wheel speeds are in rpm; negative values mean reverse.', '进气与燃油':'Intake and fuel', '涡轮增压与排气':'Turbocharging and exhaust', '附件':'Ancillaries', '前差速器':'Front differential', '中央与后差速器':'Centre and rear differentials', '传动轴与半轴':'Propshaft and driveshafts', '滑柱与弹簧':'Struts and springs', '转向节与轮毂':'Hub carriers', '摆臂与连杆':'Arms and links', '制动':'Brakes', '转向':'Steering', '奥迪 Sport quattro S1 E2 拉力赛车':'Audi Sport quattro S1 E2', '奥迪 Sport quattro S1 E2 三维模型，可拖动旋转和滚轮缩放':'3D Audi Sport quattro S1 E2. Drag to orbit and scroll to zoom.', '奥迪 Sport quattro S1 E2 · HB Audi Team · 2 号':'Audi Sport quattro S1 E2 · HB Audi Team · No. 2', '麦弗逊悬挂、转向与制动':'MacPherson suspension, steering and brakes', '2.1 升涡轮增压直列五缸':'2.1-litre turbocharged inline-five', '六速变速箱与全时四驱':'Six-speed gearbox and permanent four-wheel drive', '蓝旗亚 037 拉力赛车':'Lancia Rally 037',
  '蓝旗亚037三维模型，可拖动旋转和滚轮缩放':'3D Lancia 037. Drag to orbit and scroll to zoom.',
  '辅助灯 · 开':'Aux lamps · on', '辅助灯 · 关':'Aux lamps · off', '初始视角':'Home view', '侧视':'Side', '俯视':'Top',
  '▶ 拆解':'▶ Explode', '◀ 复原':'◀ Assemble', '拆解进度':'Exploded view', '完全展开':'Fully exploded',
  'Ⅱ 暂停':'Ⅱ Pause', '▶ 运转':'▶ Run', '曲轴转角 · 四冲程循环':'Crank angle · four-stroke cycle', '步进 15°':'Step 15°',
  '部件目录':'Parts', '筛选零件类别':'Filter by part family', '整车总览':'Vehicle overview',
  '选择部件可定位总成，拖动下方进度条可查看拆解过程。':'Select an assembly, then move the slider to take it apart.',
  '单件拆出':'Remove part', '进入内部拆解':'Open assembly', '清除单件调整':'Reset individual parts',
  '单独查看':'Isolate', '返回总成视图':'Show assembly', '点选零件 · 拖动旋转 · 滚轮缩放':'Select a part · Drag to orbit · Scroll to zoom', '点选零件 · 拖动旋转 · 滚轮缩放 · 双击设为观察中心 · 右键拖动平移':'Select a part · Drag to orbit · Scroll to zoom at the cursor · Double-click to set the orbit centre · Right-drag to pan',
  '运转观察':'Motion study', '观察范围':'View', '动力总成':'Powertrain', '差速器':'Differential',
  '前桥转向':'Front steering', '后桥悬挂':'Rear suspension', '逐件拆解悬挂':'Explore suspension parts',
  '转弯演示':'Steering', '方向盘':'Steering wheel', '左转':'Turn left', '回正':'Centre', '右转':'Turn right',
  '拖动轮缘转动方向盘':'Drag the rim to turn the steering wheel', '左前轮':'Front left', '右前轮':'Front right',
  '随差速器壳观察':'Follow the differential carrier', '左半轴齿轮':'Left side gear', '右半轴齿轮':'Right side gear', '行星齿轮':'Spider gear',
  '观察差速器内部':'Inspect differential', '返回整车观察':'Return to car', '变速箱挡位':'Gear selection', '挡位传动比':'Gear ratio',
  '输出轴 r/min':'Output shaft · rpm', '左右后轮转速':'Rear wheel speeds', '左后轮':'Rear left', '右后轮':'Rear right',
  '点选动力路径':'Trace the power flow', '半轴':'Half-shafts', '后轮':'Rear wheels', '输入':'Input', '接合':'Engaged', '输出':'Output',
  '四缸行程':'Cylinder strokes', '1 缸':'Cyl. 1', '2 缸':'Cyl. 2', '3 缸':'Cyl. 3', '4 缸':'Cyl. 4',
  '点火顺序 1 → 3 → 4 → 2。蓝色为进气机构，红色为排气机构。':'Firing order 1 → 3 → 4 → 2. Blue marks the intake train and red the exhaust train.',
  '车身可见度':'Body opacity', '外壳可见度':'Casing opacity', '演示转速':'Demo speed', '结构示意模型':'Mechanical study',
  '传动比取自模型齿数。配气采用简化的四冲程正时，转向按齿条及定长横拉杆求解，以认证表 16.8∶1 校准中位附近的转向比。轮速按左右前轮推算的平均曲率及理想差速关系计算。轮速单位为 r/min，负值表示倒转。':'Gear ratios follow the model’s tooth counts. Valve motion uses simplified four-stroke timing. Rack travel and fixed-length tie rods set the steering angles, calibrated to the homologated 16.8:1 on-centre ratio. Wheel speeds in rpm use the mean turning curvature and ideal differential action. Negative values indicate reverse.',
  '倒挡':'Reverse', '空挡':'Neutral', '1 挡':'First gear', '2 挡':'Second gear', '3 挡':'Third gear', '4 挡':'Fourth gear', '5 挡':'Fifth gear',
  '总成拆解进度':'Assembly disassembly', '整车拆解进度':'Vehicle disassembly', '装配位置':'Assembled',
  '前后桥、转向与制动':'Suspension, steering and brakes', '2.0 升机械增压直列四缸':'2.0-litre supercharged inline-four',
  '五速手动变速驱动桥':'Five-speed manual transaxle', '蓝旗亚 037 · Rallye de France · 5 号':'Lancia 037 · Rallye de France · No. 5',
  '零件目录':'Parts index', '总成目录':'Assembly index', '全部零件':'All parts',
  '拖动总成进度可展开全部零件，也可在目录中选择单件。':'Move the slider to explode the assembly, or select a single part from the list.',
  '可查看整车爆炸图，或进入发动机、变速箱或悬挂逐件拆解。':'Explode the whole car, or open the engine, gearbox or suspension to inspect individual parts.',
  '前桥 · 转向传动':'Front axle · steering linkage', '后桥 · 弹簧与减振':'Rear axle · springs and dampers',
  '转动方向盘，观察两处万向节、输入小齿轮、滑动齿条和两根横拉杆。转向节绕上下球铰连线摆动。':'Turn the steering wheel to follow the two universal joints, pinion, rack and tie rods. Each upright pivots about its upper and lower ball joints.',
  '每个后轮配一根中央螺旋弹簧，前后各有一支减振器。下方的反置叉臂和纵向定位杆共同约束轮毂立柱。':'Each rear wheel has a central coil spring with a damper ahead of it and another behind. A reversed lower wishbone and a radius rod locate the upright.',
  '整车透视 · 后轮驱动':'Vehicle cutaway · rear-wheel drive', '差速器 · 半轴齿轮与行星齿轮':'Differential · side gears and spider gears',
  '动力总成运转':'Powertrain in motion', '齿轮齿条转向 · 上叉臂与下横臂':'Rack-and-pinion steering · upper wishbone and lower link',
  '反置下叉臂 · 单弹簧与双减振器':'Reversed lower wishbone · single spring and twin dampers',
  '左半轴':'Left half-shaft', '右半轴':'Right half-shaft', '做功':'Power', '排气':'Exhaust', '进气':'Intake', '压缩':'Compression',
  '前桥定位与承载':'Front suspension links', '前桥弹簧与减振':'Front springs and dampers', '前桥轮端':'Front wheel ends',
  '后桥定位与承载':'Rear suspension links', '后桥弹簧与减振':'Rear springs and dampers', '后桥轮端':'Rear wheel ends',
  '壳体与轴承':'Casings and bearings', '差速与终传':'Differential and final drive', '曲柄连杆机构':'Crank and rods', '气门与弹簧':'Valves and springs',
  '活塞组':'Pistons', '点火与正时':'Ignition and timing', '离合器':'Clutch', '缸体与润滑':'Block and lubrication',
  '缸盖与配气':'Cylinder head and valve train', '转向传动':'Steering linkage', '进气与排气':'Intake and exhaust', '选挡与倒挡':'Selection and reverse', '齿轮传动':'Gear train',
  '四圆灯、中央格栅、百叶散热口及一体式前翼子板。':'Four round headlamps, a split grille, bonnet vents and integral front wings.',
  '后翼子板、透明发动机盖、通风百叶与车尾扰流板。':'Rear wings, glazed engine cover, ventilation louvres and rear spoiler.',
  '弧面前风挡、A 柱、车顶和雨刮器组成的可拆展示单元。':'Curved windscreen, A-pillars, roof and wipers.',
  '独立车门带侧窗、车号板、拉手与外后视镜。':'Door with side glazing, rally number panel, handle and mirror.',
  '中央承载结构与前后管式副车架，作为拆解定位基准。':'Central tub and tubular front and rear subframes. The chassis anchors the exploded view.',
  '双桶椅、四点式安全带、方向盘、仪表台与钢管防滚架。':'Bucket seats, four-point harnesses, steering wheel, dashboard and roll cage.',
  '2.0 升纵置直列四缸。选择上方发动机页签可拆开曲柄连杆机构、十六气门缸盖与机械增压器。':'Longitudinal 2.0-litre inline-four. Open Engine to inspect the crank and rods, 16-valve head and supercharger.',
  '纵置五速手动变速箱，包含离合器、两根传动轴、五组常啮合齿轮、倒挡组件与差速器。':'Longitudinal five-speed transaxle with clutch, twin shafts, five constant-mesh gear pairs, reverse train and differential.',
  '前桥上叉臂、下横臂及纵向定位杆；后桥反置下叉臂、中央弹簧及双减振器。可进入内部拆解。':'Front upper wishbones, lower transverse arms and radius rods. Rear reversed lower wishbones, central springs and twin dampers. Open the assembly to inspect each part.',
  '拉力胎、白色多孔合金轮圈、轮毂与紧固螺栓。':'Rally tyre, perforated alloy wheel, hub and fasteners.',
  '四盏辅助拉力灯及管式支架，安装在车头前缘。':'Four auxiliary driving lamps on a braced carrier at the leading edge of the bonnet.',
  '悬挂行程':'Suspension travel', '同向跳动':'Bounce', '车身侧倾':'Body roll', '左轮单跳':'Left wheel only', '车轮行程':'Wheel travel',
  '完全回弹':'Full droop', '静态车高':'Ride height', '完全压缩':'Full bump', '▶ 路面起伏':'▶ Rough road', 'Ⅱ 停止起伏':'Ⅱ Stop road',
  '前桥':'Front axle', '后桥':'Rear axle', '左':'Left', '右':'Right', '外倾角变化':'Camber change', '弹簧长度':'Spring length', '轮心横移':'Hub lateral shift',
  '每个车轮按上下叉臂铰点求解横向平面内的四连杆。弹簧与减振器沿轴线伸缩，纵向定位杆、半轴与横拉杆随之摆动。未计算轮跳转向与稳定杆扭转。':'Each wheel is solved as a four-bar linkage in the transverse plane from the wishbone pivots. Springs and dampers extend and compress along their axes; radius rods, half-shafts and track rods follow. Bump steer and anti-roll bar twist are not modelled.',
  '此浏览器无法启动 WebGL。请启用硬件加速，或在三维软件中打开配套 GLB 文件。':'WebGL could not start. Enable hardware acceleration or open the GLB model in a 3D viewer.'
};
const languageKey='wilson-rally-language';
const langQuery=new URLSearchParams(location.search).get('lang');
let lang='zh';
try {if(localStorage.getItem(languageKey)==='en')lang='en'} catch {}
if(langQuery==='zh'||langQuery==='en')lang=langQuery;
function tr(value){return lang==='en'?(englishText[value.trim().replace(/\s+/g,' ')]??value):value}
function englishName(item){
    let name=item.en.replace(/(\d) 缸(进气|排气)门 (\d)( spring)?/,(_,c,type,n,spring)=>
        'Cylinder '+c+' '+(type==='进气'?'intake':'exhaust')+' valve '+n+(spring||''));
    for(const [from,to] of [['输入','Input'],['输出','Output'],['前 bearing',' front bearing'],['后 bearing',' rear bearing'],['进气','Intake'],['排气','Exhaust']])name=name.replace(from,to);
    if(item.zone&&item.side){
        name=name.replace(/ -?1$/,'').replace('damper -0.123','aft damper').replace('damper 0.123','forward damper').replace('damper 0','coilover damper');
        name=(item.side>0?'Left ':'Right ')+name.toLowerCase();
    }
    return name;
}
function partName(item){return lang==='en'?englishName(item):item.zh}
const staticLabels=[];
for(const region of document.querySelectorAll('header,main,footer')){
    const walker=document.createTreeWalker(region,NodeFilter.SHOW_TEXT);
    while(walker.nextNode()){
        const node=walker.currentNode;
        if(englishText[node.data.trim().replace(/\s+/g,' ')])staticLabels.push({node,text:node.data});
    }
}
const translatedAttributes=[];
for(const node of document.querySelectorAll('[aria-label],[title]')){
    for(const attr of ['aria-label','title']){
        const text=node.getAttribute(attr);
        if(text&&englishText[text])translatedAttributes.push({node,attr,text});
    }
}
function showLanguage(){
    document.documentElement.lang=lang==='en'?'en':'zh-CN';
    for(const {node,text} of staticLabels)if(node.isConnected)node.data=tr(text);
    for(const {node,attr,text} of translatedAttributes)node.setAttribute(attr,tr(text));
    const button=document.getElementById('language');
    button.textContent=lang==='en'?'中文':'English';
    button.lang=lang==='en'?'zh-CN':'en';
    button.setAttribute('aria-label',lang==='en'?'切换至中文':'Switch to English');
}
showLanguage();
document.getElementById('language').onclick=()=>{
    lang=lang==='zh'?'en':'zh';
    try{localStorage.setItem(languageKey,lang)}catch{}
    if(/^https?:$/.test(location.protocol)){
        const url=new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url);
    }
    showLanguage();document.dispatchEvent(new Event('viewer-language'));
};
const aboutDialog=document.getElementById('aboutDialog');
document.getElementById('aboutOpen').onclick=()=>aboutDialog.showModal();
document.getElementById('aboutClose').onclick=()=>aboutDialog.close();
aboutDialog.addEventListener('close',()=>document.getElementById('aboutOpen').focus({preventScroll:true}));
aboutDialog.addEventListener('click',e=>{if(e.target===aboutDialog){
    const r=aboutDialog.getBoundingClientRect();
    if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)aboutDialog.close();
}});
