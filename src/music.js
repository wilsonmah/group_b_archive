// Procedural lofi-jazz background music in the spirit of a racing-sim café / menu soundtrack.
// Everything is synthesized with WebAudio, so the page stays a single self-contained file.
// Character: slow lazy swing, muffled Rhodes with tape wobble, round upright-style bass,
// dusty boom-bap drums, sparse mellow melody and a layer of vinyl crackle.
(()=>{
const KEY='lancia-music-off';
const Q={
  maj9:[0,4,7,11,14],maj13:[0,4,11,14,21],maj7:[0,4,7,11,16],m69:[0,3,7,9,14],
  min9:[0,3,7,10,14],min11:[0,3,10,14,17],min7:[0,3,7,10,15],
  dom9:[0,4,10,14,16],dom13:[0,4,10,14,21],s9:[0,4,10,15,20],sus:[0,5,7,10,14]
};
// chords: [semitones from key root, quality, beats]. Each track loops its progression twice, then moves on.
const TRACKS=[
 {name:'Paddock Café',bpm:76,key:53,swing:.3,groove:0,scale:[0,2,4,7,9],
  prog:[[2,'min9',4],[7,'dom13',4],[0,'maj9',4],[9,'s9',4],[2,'min9',4],[7,'dom13',4],[0,'maj13',2],[5,'min7',2],[4,'min7',2],[9,'dom13',2]]},
 {name:'Rainy Pit Lane',bpm:70,key:50,swing:.32,groove:1,scale:[0,3,5,7,10],
  prog:[[0,'min9',4],[5,'min11',4],[3,'maj9',4],[10,'dom13',4],[0,'min9',4],[8,'maj7',4],[7,'s9',4],[0,'min11',4]]},
 {name:'Late Night Service',bpm:82,key:55,swing:.28,groove:2,scale:[0,2,4,7,9],
  prog:[[0,'maj9',4],[9,'min9',4],[2,'min9',4],[7,'dom13',4],[5,'maj9',4],[4,'min7',2],[9,'s9',2],[2,'min9',4],[7,'sus',4]]},
 {name:'Dusk on the Coast Road',bpm:72,key:48,swing:.3,groove:1,scale:[0,2,4,7,9],
  prog:[[0,'maj13',4],[5,'maj9',4],[4,'min7',2],[9,'dom9',2],[2,'min9',4],[7,'dom13',4],[0,'maj9',4],[10,'dom9',4],[5,'maj7',4],[7,'s9',4]]},
 {name:'Garage After Hours',bpm:80,key:45,swing:.3,groove:2,scale:[0,3,5,7,10],
  prog:[[0,'min9',4],[0,'m69',4],[5,'dom9',4],[5,'min11',4],[3,'maj9',4],[10,'dom13',4],[0,'min9',4],[7,'s9',4]]}
];
const mtof=m=>440*2**((m-69)/12);
let ctx,master,verb,wob,bus,timer,idx=0,playing=false,wantOff=false,gen=0,noiseBuf,rnd;
try{wantOff=localStorage.getItem(KEY)==='1'}catch{}
const $=id=>document.getElementById(id);

function seeded(s){return()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}}

function init(){
  if(ctx)return;
  ctx=new (window.AudioContext||window.webkitAudioContext)();
  master=ctx.createGain();master.gain.value=.65;
  // muffled "cassette" tone: roll the top off, keep the low mids warm
  const tone=ctx.createBiquadFilter();tone.type='lowpass';tone.frequency.value=3400;tone.Q.value=.5;
  const warm=ctx.createBiquadFilter();warm.type='lowshelf';warm.frequency.value=200;warm.gain.value=3;
  const comp=ctx.createDynamicsCompressor();comp.threshold.value=-20;comp.ratio.value=3.5;comp.attack.value=.02;comp.release.value=.25;
  master.connect(tone);tone.connect(warm);warm.connect(comp);comp.connect(ctx.destination);
  // generated reverb impulse (dark, short plate)
  const len=ctx.sampleRate*2.2,imp=ctx.createBuffer(2,len,ctx.sampleRate);
  for(let c=0;c<2;c++){const d=imp.getChannelData(c);let lp=0;for(let i=0;i<len;i++){lp+=((Math.random()*2-1)-lp)*.25;d[i]=lp*Math.pow(1-i/len,2.8)}}
  verb=ctx.createConvolver();verb.buffer=imp;
  const vg=ctx.createGain();vg.gain.value=.3;verb.connect(vg);vg.connect(master);
  noiseBuf=ctx.createBuffer(1,ctx.sampleRate,ctx.sampleRate);
  const nd=noiseBuf.getChannelData(0);for(let i=0;i<nd.length;i++)nd[i]=Math.random()*2-1;
  // tape wobble: a slow pitch drift (cents) shared by all pitched voices
  const lfo=ctx.createOscillator(),lfo2=ctx.createOscillator(),wg=ctx.createGain();
  lfo.frequency.value=.37;lfo2.frequency.value=5.3;wob=ctx.createGain();wob.gain.value=9;
  const w2=ctx.createGain();w2.gain.value=.12;lfo.connect(wob);lfo2.connect(w2);w2.connect(wob);lfo.start();lfo2.start();
  // vinyl crackle: sparse pops over faint hiss, always on
  const sr=ctx.sampleRate,cb=ctx.createBuffer(1,sr*4,sr),cd=cb.getChannelData(0);
  for(let i=0;i<cd.length;i++){cd[i]=(Math.random()*2-1)*.012;if(Math.random()<.0006)cd[i]+=(Math.random()*2-1)*(.15+Math.random()*.5)}
  const cs=ctx.createBufferSource(),cf=ctx.createBiquadFilter(),cg=ctx.createGain();
  cs.buffer=cb;cs.loop=true;cf.type='bandpass';cf.frequency.value=2800;cf.Q.value=.4;cg.gain.value=.55;
  cs.connect(cf);cf.connect(cg);cg.connect(master);cs.start();
}

function env(g,t,a,peak,d,end=0.0001){g.gain.setValueAtTime(0.0001,t);g.gain.linearRampToValueAtTime(peak,t+a);g.gain.exponentialRampToValueAtTime(end,t+a+d)}
function send(node,amt){node.connect(bus);if(amt){const s=ctx.createGain();s.gain.value=amt;node.connect(s);s.connect(verb)}}
function drift(o){wob.connect(o.detune)}

// Rhodes-like electric piano: soft FM bell with a gentle low-passed bark
function epiano(f,t,dur,vel){
  const car=ctx.createOscillator(),mod=ctx.createOscillator(),mg=ctx.createGain(),g=ctx.createGain();
  car.frequency.value=f;mod.frequency.value=f;drift(car);drift(mod);
  mg.gain.setValueAtTime(f*vel*.7,t);mg.gain.exponentialRampToValueAtTime(f*.02,t+dur*.5);
  mod.connect(mg);mg.connect(car.frequency);
  env(g,t,.008,.15*vel,dur);
  const lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=1000+vel*500;lp.Q.value=.3;
  car.connect(lp);lp.connect(g);send(g,.4);
  for(const o of[car,mod]){o.start(t);o.stop(t+dur+.5)}
}
// round upright-style bass
function bass(f,t,dur,vel){
  const o=ctx.createOscillator(),o2=ctx.createOscillator(),lp=ctx.createBiquadFilter(),g=ctx.createGain();
  o.type='triangle';o2.type='sine';o.frequency.value=f;o2.frequency.value=f;drift(o);drift(o2);
  lp.type='lowpass';lp.frequency.setValueAtTime(520,t);lp.frequency.exponentialRampToValueAtTime(150,t+dur);
  env(g,t,.012,.4*vel,dur);o.connect(lp);o2.connect(lp);lp.connect(g);send(g,0);
  o.start(t);o2.start(t);o.stop(t+dur+.1);o2.stop(t+dur+.1);
}
// very soft string-ish bed
function pad(freqs,t,dur){
  const g=ctx.createGain(),lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=480;
  g.gain.setValueAtTime(0.0001,t);g.gain.linearRampToValueAtTime(.04,t+dur*.4);g.gain.linearRampToValueAtTime(0.0001,t+dur+.5);
  lp.connect(g);send(g,.6);
  for(const f of freqs)for(const dt of[-7,7]){const o=ctx.createOscillator();o.type='sawtooth';o.frequency.value=f;o.detune.value=dt;drift(o);
    const og=ctx.createGain();og.gain.value=.22;o.connect(og);og.connect(lp);o.start(t);o.stop(t+dur+.6)}
}
// mellow lead: sine/triangle with slow attack and a tiny scoop up into the note
function lead(f,t,dur,vel){
  const o=ctx.createOscillator(),o2=ctx.createOscillator(),g=ctx.createGain(),lp=ctx.createBiquadFilter();
  o.type='triangle';o2.type='sine';o.frequency.setValueAtTime(f*.985,t);o.frequency.exponentialRampToValueAtTime(f,t+.07);
  o2.frequency.value=f*2;drift(o);drift(o2);
  lp.type='lowpass';lp.frequency.value=1100;
  const g2=ctx.createGain();g2.gain.value=.08;o2.connect(g2);g2.connect(lp);o.connect(lp);lp.connect(g);
  env(g,t,.04,.1*vel,dur*1.3);send(g,.8);
  const end=t+dur*1.3+.4;o.start(t);o2.start(t);o.stop(end);o2.stop(end);
}
function noise(t,dur,type,freq,peak,q=1){
  const s=ctx.createBufferSource(),f=ctx.createBiquadFilter(),g=ctx.createGain();
  s.buffer=noiseBuf;s.loop=true;f.type=type;f.frequency.value=freq;f.Q.value=q;
  env(g,t,.001,peak,dur);s.connect(f);f.connect(g);send(g,.12);s.start(t);s.stop(t+dur+.05);
}
function kick(t,vel){
  const o=ctx.createOscillator(),g=ctx.createGain();
  o.frequency.setValueAtTime(110,t);o.frequency.exponentialRampToValueAtTime(44,t+.1);
  env(g,t,.003,.5*vel,.26);o.connect(g);send(g,0);o.start(t);o.stop(t+.35);
}
// lazy boom-bap snare: muffled noise plus a short body tone
function snare(t,vel){
  noise(t,.2,'bandpass',1400,.11*vel,.7);
  const o=ctx.createOscillator(),g=ctx.createGain();o.frequency.setValueAtTime(220,t);o.frequency.exponentialRampToValueAtTime(150,t+.08);
  env(g,t,.002,.1*vel,.1);o.connect(g);send(g,.2);o.start(t);o.stop(t+.2);
}

function playTrack(i){
  const myGen=++gen,trk=TRACKS[i];
  if(bus){const old=bus;old.gain.cancelScheduledValues(ctx.currentTime);old.gain.setTargetAtTime(0,ctx.currentTime,.15);setTimeout(()=>old.disconnect(),1500)}
  bus=ctx.createGain();bus.gain.value=0;bus.connect(master);
  bus.gain.setTargetAtTime(1,ctx.currentTime+.05,.4);
  rnd=seeded(1000+i*77+Date.now()%1000);
  const beat=60/trk.bpm,step=beat/4;
  const lane=[];for(const[r,q,b]of trk.prog)for(let s=0;s<b*4;s++)lane.push([r,q,s,b*4]);
  const total=lane.length,loops=2;
  let n=0,when=ctx.currentTime+.2,last=67,rest=0;
  $('musicTitle').textContent=trk.name;
  const human=()=>(rnd()-.5)*.018;   // loose, slightly late hands
  function pump(){
    if(myGen!==gen)return;
    while(when<ctx.currentTime+.6){
      if(n>=total*loops){setTimeout(()=>{if(myGen===gen&&playing)next(true)},Math.max(0,(when-ctx.currentTime)*1000));return}
      const[root,q,s,len]=lane[n%total];
      // swing: every off-beat 16th is pushed late; drums lag a hair behind the chords
      const sw=(n%2)?trk.swing*step*1.0:0,t=when+sw,b16=n%16,bar=Math.floor(n/16),vel=.7+rnd()*.3;
      const base=trk.key+root,ch=Q[q].map(x=>base+x);
      if(s===0){pad(ch.slice(1,4).map(mtof),t,len*step);bass(mtof(base-12),t,beat*1.6,1)}
      // Rhodes comping: lazy rolled chords on syncopated hits, rootless voicings
      const comp=trk.groove===1?[0,10]:trk.groove===2?[0,6,10,14]:[0,6,10];
      if(comp.includes(s%16)&&s<len-1){
        const v=ch.slice(1,5).map((m,k)=>k===3?m-12:m);
        v.forEach((m,k)=>epiano(mtof(m),t+k*.014+human(),beat*(s%16?1.2:2.4),vel*(s%16?.75:1)));
      }
      // bass: root, then fifth/approach-note answers
      if(s>0&&s%16===10&&rnd()<.8)bass(mtof(base-12+(rnd()<.5?7:0)),t,beat*.9,.65);
      if(s%16===14&&rnd()<.45)bass(mtof(base-12+(rnd()<.5?-1:2)),t,beat*.6,.5);
      // drums: boom-bap with ghost kicks, snare on 2 and 4, soft swung hats
      const dt=t+.012;
      if(b16===0)kick(dt,1);else if(b16===7||b16===10){if(rnd()<(b16===10?.75:.4))kick(dt,.55)}
      if(b16===4||b16===12)snare(dt,b16===4?1:.9);
      if(b16%2===0)noise(dt,.05,'bandpass',4800,b16%4===0?.022:.013,.6);
      else if(rnd()<.35)noise(dt,.04,'bandpass',5200,.008,.6);
      if(b16===15&&rnd()<.3)noise(dt,.12,'bandpass',3800,.02,.8); // open-hat breath
      // sparse melody: phrases with plenty of space, silent every fourth bar
      if(bar%4!==3&&b16%2===0&&rnd()<(trk.groove===1?.2:.28)){
        const pool=[];for(let o=57;o<=77;o++)if(trk.scale.includes(((o-trk.key)%12+12)%12))pool.push(o);
        pool.sort((a,b)=>Math.abs(a-last)-Math.abs(b-last));
        const m=pool[Math.floor(rnd()*Math.min(3,pool.length))];last=m;
        lead(mtof(m),t+human(),beat*(rnd()<.35?2:1.2),.6+rnd()*.4);
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
