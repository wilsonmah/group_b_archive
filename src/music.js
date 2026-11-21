// Procedural lounge-fusion background music in the spirit of a racing-sim menu soundtrack.
// Everything is synthesized with WebAudio, so the page stays a single self-contained file.
(()=>{
const KEY='lancia-music-off';
const Q={maj9:[0,4,7,11,14],maj7:[0,4,7,11,16],min9:[0,3,7,10,14],min7:[0,3,7,10,15],dom9:[0,4,7,10,14],dom13:[0,4,10,14,21],sus:[0,5,7,10,14]};
// chords: [semitones from key root, quality, beats]; each track loops its progression.
const TRACKS=[
 {name:'Paddock Lounge',bpm:92,key:53,swing:.18,groove:0,scale:[0,2,4,7,9],
  prog:[[0,'maj9',4],[-1,'min7',2],[4,'dom13',2],[2,'min9',4],[7,'dom13',4],[0,'maj9',4],[5,'maj7',2],[4,'dom9',2],[2,'min9',4],[7,'sus',4]]},
 {name:'Midnight Pit Lane',bpm:84,key:57,swing:.22,groove:1,scale:[0,3,5,7,10],
  prog:[[0,'min9',4],[5,'min7',4],[3,'maj9',4],[7,'dom13',4],[0,'min9',4],[8,'maj7',4],[5,'min9',4],[7,'dom9',4]]},
 {name:'Alpine Stage',bpm:104,key:50,swing:.12,groove:2,scale:[0,2,4,7,9],
  prog:[[0,'maj7',4],[7,'dom13',4],[4,'min7',4],[9,'min7',4],[2,'min9',4],[7,'dom9',4],[0,'maj9',4],[5,'maj7',4]]},
 {name:'Sunset Service Park',bpm:98,key:55,swing:.16,groove:0,scale:[0,2,4,7,9],
  prog:[[0,'maj9',4],[9,'min7',4],[2,'min9',4],[7,'dom13',4],[5,'maj9',4],[4,'min7',2],[9,'dom9',2],[2,'min9',4],[7,'sus',4]]},
 {name:'Group B Garage',bpm:110,key:52,swing:.1,groove:2,scale:[0,3,5,7,10],
  prog:[[0,'min7',4],[0,'min9',4],[5,'dom9',4],[5,'dom13',4],[3,'maj7',4],[7,'dom9',4],[0,'min9',4],[7,'sus',4]]}
];
const mtof=m=>440*2**((m-69)/12);
let ctx,master,verb,bus,timer,idx=0,playing=false,wantOff=false,gen=0,noiseBuf,rnd;
try{wantOff=localStorage.getItem(KEY)==='1'}catch{}
const $=id=>document.getElementById(id);

function seeded(s){return()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}}

function init(){
  if(ctx)return;
  ctx=new (window.AudioContext||window.webkitAudioContext)();
  master=ctx.createGain();master.gain.value=.55;
  const comp=ctx.createDynamicsCompressor();comp.threshold.value=-18;comp.ratio.value=3;
  master.connect(comp);comp.connect(ctx.destination);
  // generated reverb impulse
  const len=ctx.sampleRate*2.4,imp=ctx.createBuffer(2,len,ctx.sampleRate);
  for(let c=0;c<2;c++){const d=imp.getChannelData(c);for(let i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,2.6)}
  verb=ctx.createConvolver();verb.buffer=imp;
  const vg=ctx.createGain();vg.gain.value=.32;verb.connect(vg);vg.connect(master);
  noiseBuf=ctx.createBuffer(1,ctx.sampleRate,ctx.sampleRate);
  const nd=noiseBuf.getChannelData(0);for(let i=0;i<nd.length;i++)nd[i]=Math.random()*2-1;
}

function env(g,t,a,peak,d,end=0.0001){g.gain.setValueAtTime(0.0001,t);g.gain.linearRampToValueAtTime(peak,t+a);g.gain.exponentialRampToValueAtTime(end,t+a+d)}
function send(node,amt){node.connect(bus);if(amt){const s=ctx.createGain();s.gain.value=amt;node.connect(s);s.connect(verb)}}

function epiano(f,t,dur,vel){
  const car=ctx.createOscillator(),mod=ctx.createOscillator(),mg=ctx.createGain(),g=ctx.createGain();
  car.frequency.value=f;mod.frequency.value=f;
  mg.gain.setValueAtTime(f*vel*1.6,t);mg.gain.exponentialRampToValueAtTime(f*.05,t+dur*.8);
  mod.connect(mg);mg.connect(car.frequency);
  env(g,t,.004,.16*vel,dur);
  const tine=ctx.createOscillator(),tg=ctx.createGain();tine.frequency.value=f*7;
  env(tg,t,.002,.02*vel,.12);tine.connect(tg);tg.connect(g);
  car.connect(g);send(g,.5);
  for(const o of[car,mod,tine]){o.start(t);o.stop(t+dur+.5)}
}
function bass(f,t,dur,vel){
  const o=ctx.createOscillator(),o2=ctx.createOscillator(),lp=ctx.createBiquadFilter(),g=ctx.createGain();
  o.type='triangle';o2.type='sine';o.frequency.value=f;o2.frequency.value=f;
  lp.type='lowpass';lp.frequency.setValueAtTime(900,t);lp.frequency.exponentialRampToValueAtTime(220,t+dur);
  env(g,t,.008,.38*vel,dur);o.connect(lp);o2.connect(lp);lp.connect(g);send(g,0);
  o.start(t);o2.start(t);o.stop(t+dur+.1);o2.stop(t+dur+.1);
}
function pad(freqs,t,dur){
  const g=ctx.createGain(),lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=1100;
  g.gain.setValueAtTime(0.0001,t);g.gain.linearRampToValueAtTime(.045,t+dur*.3);g.gain.linearRampToValueAtTime(0.0001,t+dur+.4);
  lp.connect(g);send(g,.6);
  for(const f of freqs)for(const dt of[-6,6]){const o=ctx.createOscillator();o.type='sawtooth';o.frequency.value=f;o.detune.value=dt;
    const og=ctx.createGain();og.gain.value=.25;o.connect(og);og.connect(lp);o.start(t);o.stop(t+dur+.5)}
}
function pluck(f,t,dur,vel){
  const o=ctx.createOscillator(),o2=ctx.createOscillator(),g=ctx.createGain();
  o.type='triangle';o2.type='sine';o.frequency.value=f;o2.frequency.value=f*2;
  env(g,t,.01,.09*vel,dur);o.connect(g);const g2=ctx.createGain();g2.gain.value=.3;o2.connect(g2);g2.connect(g);
  send(g,.7);o.start(t);o2.start(t);o.stop(t+dur+.2);o2.stop(t+dur+.2);
}
function noise(t,dur,type,freq,peak,q=1){
  const s=ctx.createBufferSource(),f=ctx.createBiquadFilter(),g=ctx.createGain();
  s.buffer=noiseBuf;s.loop=true;f.type=type;f.frequency.value=freq;f.Q.value=q;
  env(g,t,.001,peak,dur);s.connect(f);f.connect(g);send(g,.15);s.start(t);s.stop(t+dur+.05);
}
function kick(t,vel){
  const o=ctx.createOscillator(),g=ctx.createGain();
  o.frequency.setValueAtTime(130,t);o.frequency.exponentialRampToValueAtTime(42,t+.12);
  env(g,t,.002,.55*vel,.22);o.connect(g);send(g,0);o.start(t);o.stop(t+.3);
}

function playTrack(i){
  const myGen=++gen,tr=TRACKS[i];
  if(bus){const old=bus;old.gain.cancelScheduledValues(ctx.currentTime);old.gain.setTargetAtTime(0,ctx.currentTime,.12);setTimeout(()=>old.disconnect(),1200)}
  bus=ctx.createGain();bus.gain.value=0;bus.connect(master);
  bus.gain.setTargetAtTime(1,ctx.currentTime+.05,.25);
  rnd=seeded(1000+i*77+Date.now()%1000);
  const beat=60/tr.bpm,step=beat/4;
  // flatten progression into 16th-step chord lanes
  const lane=[];for(const[r,q,b]of tr.prog)for(let s=0;s<b*4;s++)lane.push([r,q,s,b*4]);
  const total=lane.length,loops=2;
  let n=0,when=ctx.currentTime+.15,last=60;
  $('musicTitle').textContent=tr.name;
  function pump(){
    if(myGen!==gen)return;
    while(when<ctx.currentTime+.6){
      if(n>=total*loops){setTimeout(()=>{if(myGen===gen&&playing)next(true)},Math.max(0,(when-ctx.currentTime)*1000));return}
      const[root,q,s,len]=lane[n%total];
      const sw=(n%2)?tr.swing*step:0,t=when+sw,bar16=n%16,vel=.75+rnd()*.25;
      const base=tr.key+root,ch=Q[q].map(x=>base+12+x);
      if(s===0){pad(ch.slice(0,4).map(m=>mtof(m-12)),t,len*step);bass(mtof(base-12),t,beat*1.4,1)}
      const comp=tr.groove===1?[0,7,10]:tr.groove===2?[0,3,6,10,14]:[0,6,10];
      if(comp.includes(s%16)&&s<len-1)ch.slice(0,4).forEach((m,k)=>epiano(mtof(m),t+k*.012,beat*(s%16?1.1:2),vel*(s%16?.8:1)));
      // bass walking figure
      if(s>0&&[6,10,14].includes(s%16)&&rnd()<.7)bass(mtof(base-12+(rnd()<.5?0:7)),t,beat*.7,.7);
      // drums
      if(bar16%16===0||(tr.groove===2&&bar16===8)||(bar16===10&&rnd()<.5))kick(t,bar16===0?1:.6);
      if(bar16===4||bar16===12)noise(t,.16,'bandpass',2200,.1,.8);
      if(bar16%2===0)noise(t,.05,'highpass',7500,bar16%4===0?.05:.03);
      else if(rnd()<.3)noise(t,.03,'highpass',8500,.02);
      // sparse melody
      if(bar16%2===0&&rnd()<(tr.groove===1?.3:.42)){
        const pool=[];for(let o=60;o<=84;o++)if(tr.scale.includes(((o-tr.key)%12+12)%12))pool.push(o);
        pool.sort((a,b)=>Math.abs(a-last)-Math.abs(b-last));
        const m=pool[Math.floor(rnd()*Math.min(4,pool.length))];last=m;
        pluck(mtof(m),t,beat*(rnd()<.3?2:1),.6+rnd()*.4);
      }
      when+=step;n++;
    }
    timer=setTimeout(pump,120);
  }
  clearTimeout(timer);pump();
}

function setUi(){
  const b=$('musicPlay');b.textContent=playing?'Ⅱ':'▶';
  const l=playing?'暂停音乐':'播放音乐';b.dataset.zh=l;b.setAttribute('aria-pressed',playing);
  labels();
}
function labels(){
  const t=window.tr||(x=>x);
  $('musicPlay').setAttribute('aria-label',t($('musicPlay').dataset.zh||'播放音乐'));
  $('musicPlay').title=$('musicPlay').getAttribute('aria-label');
  $('musicNext').setAttribute('aria-label',t('下一首'));$('musicNext').title=t('下一首');
  $('musicBox').setAttribute('aria-label',t('背景音乐'));
}
function start(){init();playing=true;wantOff=false;try{localStorage.removeItem(KEY)}catch{}
  ctx.resume();if(!bus)playTrack(idx);setUi()}
function pause(user){playing=false;if(user){wantOff=true;try{localStorage.setItem(KEY,'1')}catch{}}
  if(ctx)ctx.suspend();setUi()}
function next(auto){init();idx=(idx+1)%TRACKS.length;playing=true;ctx.resume();playTrack(idx);setUi();if(!auto){wantOff=false}}

$('musicPlay').onclick=()=>playing?pause(true):start();
$('musicNext').onclick=()=>next(false);
document.addEventListener('viewer-language',labels);
document.addEventListener('visibilitychange',()=>{if(ctx&&playing)document.hidden?ctx.suspend():ctx.resume()});
// Browsers block audio until a gesture: begin on the first interaction unless the visitor paused it earlier.
if(!wantOff){
  const arm=()=>{removeEventListener('pointerdown',arm,true);removeEventListener('keydown',arm,true);if(!playing&&!wantOff)start()};
  addEventListener('pointerdown',arm,true);addEventListener('keydown',arm,true);
}
setUi();
$('musicTitle').textContent=TRACKS[0].name;
})();
