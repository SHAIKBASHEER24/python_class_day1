from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VENOM BIKE 3D - POLICE CHASE NYC - DAY EVENING NIGHT RAIN</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
 *{margin:0;padding:0;box-sizing:border-box}
 body{background:#000;font-family:'Rajdhani',sans-serif;overflow:hidden;color:#fff}
 #wrap{position:relative;width:100vw;height:100vh;overflow:hidden}
 #wrap::before{content:'';position:absolute;inset:0;z-index:25;pointer-events:none;background:radial-gradient(ellipse at center,transparent 48%,rgba(0,0,0,.55) 100%)}
 .bar{position:absolute;left:0;width:100%;height:52px;background:#000;z-index:30;display:flex;align-items:center;justify-content:center;letter-spacing:3px;font-family:'Orbitron';font-size:11px;color:#a3e635;text-align:center;padding:0 10px}
 .bar.top{top:0;border-bottom:2px solid #a3e635}
 .bar.bottom{bottom:0;border-top:2px solid #a3e635}
 canvas{display:block;width:100%;height:calc(100vh - 104px);margin-top:52px}
 #hud{position:absolute;top:62px;left:0;width:100%;display:flex;justify-content:space-between;padding:0 12px;z-index:40;pointer-events:none;gap:8px}
 .box{background:rgba(0,0,0,.68);backdrop-filter:blur(10px);border:1px solid rgba(163,230,53,.6);border-left:4px solid #a3e635;padding:7px 13px;border-radius:10px;min-width:98px}
 .box h3{font-family:'Orbitron';font-size:10px;color:#a3e635}
 .box p{font-family:'Orbitron';font-size:23px;font-weight:900;line-height:1.1}
 #speedBox{border-left-color:#fff;text-align:center;min-width:168px}
 #speedBox p{font-size:36px;color:#a3e635;text-shadow:0 0 20px #a3e635}
 #speedBox span{font-size:12px;color:#fff}
 #symBar{height:8px;background:#222;border-radius:10px;margin-top:5px;overflow:hidden}
 #symFill{height:100%;width:100%;background:linear-gradient(90deg,#000,#a3e635,#fff)}
 #heatBar{height:8px;background:#222;border-radius:10px;margin-top:4px;overflow:hidden}
 #heatFill{height:100%;width:10%;background:linear-gradient(90deg,#facc15,#ff2d00,#ff0000)}
 #levelBar{position:absolute;top:62px;left:50%;transform:translateX(-50%);z-index:41;background:rgba(0,0,0,.75);border:1px solid #a3e635;padding:7px 16px;border-radius:20px;font-family:'Orbitron';font-size:11px;letter-spacing:1px;text-align:center;min-width:210px}
 #levelProgress{height:6px;background:#222;border-radius:10px;margin-top:4px;overflow:hidden}
 #levelFill{height:100%;width:0%;background:#a3e635}
 #weatherBadge{font-size:10px;color:#00e5ff;margin-top:2px}
 #policeAlert{position:absolute;top:125px;left:50%;transform:translateX(-50%);z-index:42;background:linear-gradient(90deg,#ff0000,#0000ff);padding:8px 18px;border-radius:20px;font-family:'Orbitron';font-weight:900;font-size:13px;letter-spacing:2px;display:none;animation:blink .4s infinite}
 @keyframes blink{50%{opacity:.4}}
 #menu{position:absolute;inset:0;z-index:50;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(rgba(0,0,0,.3),rgba(0,0,0,.93));text-align:center;padding:20px;overflow-y:auto}
 #menu h1{font-family:'Orbitron';font-size:clamp(36px,8vw,76px);font-weight:900;line-height:.95;margin:10px 0;background:linear-gradient(90deg,#fff,#a3e635,#00e5ff,#ff2d00,#fff);background-size:300% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shine 2s linear infinite}
 @keyframes shine{to{background-position:300% 0}}
 #menu p{color:#eee;font-size:15px;margin-bottom:12px}
 .btn{padding:14px 44px;font-family:'Orbitron';font-size:17px;font-weight:900;letter-spacing:2px;color:#000;background:linear-gradient(90deg,#a3e635,#fff);border:none;border-radius:50px;cursor:pointer;box-shadow:0 0 35px #a3e635;margin:6px}
 .btn2{background:linear-gradient(90deg,#ff2d00,#ffb300);color:#fff;box-shadow:0 0 25px #ff2d00}
 .levels{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:12px 0}
 .levelCard{background:rgba(255,255,255,.08);border:2px solid rgba(163,230,53,.4);padding:12px 14px;border-radius:14px;width:170px;text-align:left;cursor:pointer}
 .levelCard.active{border-color:#a3e635;background:rgba(163,230,53,.15);box-shadow:0 0 20px rgba(163,230,53,.4)}
 .levelCard h3{font-family:'Orbitron';font-size:13px;color:#a3e635}
 .levelCard p{font-size:12px;color:#ccc;margin:6px 0 0;line-height:1.4}
 .controls{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:10px}
 .key{background:#111;border:1px solid #444;border-bottom:3px solid #a3e635;padding:7px 11px;border-radius:8px;font-weight:700;font-size:12px}
 #mobile{position:absolute;bottom:65px;left:0;width:100%;display:none;justify-content:space-between;padding:0 16px;z-index:45}
 #mobile button{width:68px;height:68px;border-radius:50%;background:rgba(163,230,53,.9);border:2px solid #fff;color:#000;font-size:22px;font-weight:900}
 @media(max-width:768px){#mobile{display:flex}}
 #over,#win,#levelUp{position:absolute;inset:0;z-index:60;display:none;flex-direction:column;align-items:center;justify-content:center;background:rgba(0,0,0,.9);text-align:center;padding:20px}
 #over h2{font-family:'Orbitron';font-size:46px;color:#ff2d00}
 #win h2{font-family:'Orbitron';font-size:46px;color:#a3e635;text-shadow:0 0 30px #a3e635}
 #levelUp h2{font-family:'Orbitron';font-size:52px;color:#a3e635;text-shadow:0 0 30px #a3e635}
 #speedLines{position:absolute;inset:0;pointer-events:none;z-index:15;opacity:0;background:repeating-linear-gradient(90deg,transparent 0 70px,rgba(163,230,53,.18) 70px 72px)}
 .sym #speedLines{opacity:1}
 #toast{position:absolute;top:155px;left:50%;transform:translateX(-50%);z-index:43;background:#a3e635;color:#000;font-family:'Orbitron';font-weight:900;padding:10px 20px;border-radius:20px;display:none;letter-spacing:1px;text-align:center}
</style>
</head>
<body>
<div id="wrap">
 <div class="bar top">★ VENOM 3D • POLICE CHASE • DAY ☀️ EVENING 🌇 NIGHT RAIN 🌧️ • SPEED INCREASES EVERY LEVEL ★</div>
 <div class="bar bottom">W / ↑ SPEED &nbsp;•&nbsp; A D STEER &nbsp;•&nbsp; SPACE SYMBIOTE &nbsp;•&nbsp; S BRAKE &nbsp;•&nbsp; P POLICE SIREN</div>
 <div id="speedLines"></div><div id="toast"></div><div id="policeAlert">🚨 POLICE CHASE! ESCAPE! 🚨</div>
 <canvas id="game"></canvas>
 <div id="levelBar"><span id="levelName">LEVEL 1 • DAY SUN • TIMES SQUARE</span><div id="levelProgress"><div id="levelFill"></div></div><div id="weatherBadge">☀️ DAY SUN • CLEAR • 240 KM/H MAX</div><div style="font-size:10px;color:#a3e635" id="levelDist">0 / 1200m</div></div>
 <div id="hud">
   <div class="box"><h3>VENOM SCORE</h3><p id="score">0</p><div style="font-size:11px;color:#ffb300" id="combo">COMBO x1</div></div>
   <div class="box" id="speedBox"><h3>VENOM • GEAR <span id="gear">1</span> • <span id="heatTxt">HEAT 1★</span></h3><p><span id="speed">0</span> <span>KM/H</span></p><div id="symBar"><div id="symFill"></div></div><div style="font-size:10px;margin-top:3px">SYMBIOTE • POLICE HEAT</div><div id="heatBar"><div id="heatFill"></div></div></div>
   <div class="box"><h3>DISTANCE</h3><p id="dist">0m</p><div style="font-size:11px;color:#00e5ff" id="near">ESCAPED: 0</div></div>
 </div>
 <div id="mobile"><button onclick="moveL()">◀</button><button onclick="toggleSym()">🖤</button><button onclick="moveR()">▶</button></div>
 <div id="menu">
   <div style="color:#a3e635;letter-spacing:4px;font-weight:700;border:1px solid #a3e635;padding:6px 14px;border-radius:20px;font-size:12px">🚨 POLICE CHASE 3D • DAY → EVENING → NIGHT RAIN</div>
   <h1>VENOM<br>POLICE CHASE 3D</h1>
   <p>Escape NYPD! Every Level Completed = Speed Increases + New Time + New Weather</p>
   <div class="levels">
     <div class="levelCard active" id="card1" onclick="selectLevel(1)"><h3>LEVEL 1 • DAY ☀️</h3><p><b>Times Square</b><br>Sun, Blue Sky, 1 Police Car<br>1200m • Max 240 KM/H</p></div>
     <div class="levelCard" id="card2" onclick="selectLevel(2)"><h3>LEVEL 2 • EVENING 🌇</h3><p><b>Brooklyn Bridge</b><br>Sunset, 2 Police Cars<br>1500m • Max 275 KM/H</p></div>
     <div class="levelCard" id="card3" onclick="selectLevel(3)"><h3>LEVEL 3 • NIGHT RAIN 🌧️</h3><p><b>Manhattan Storm</b><br>Night, Rain, Lightning, 3 Police<br>1800m • Max 320 KM/H</p></div>
   </div>
   <button class="btn" onclick="startGame(0)">🚨 START POLICE CHASE - ALL LEVELS</button>
   <button class="btn btn2" onclick="startGame(selectedLevel)">▶ PLAY LEVEL <span id="startLevelTxt">1</span> ONLY</button>
   <div class="controls"><span class="key">◀ ▶ Steer</span><span class="key">▲ / W Speed</span><span class="key">SPACE Symbiote</span><span class="key">S Brake</span><span class="key">P Siren</span></div>
   <div style="font-size:12px;color:#aaa;margin-top:10px">⚡ TIP: Near Miss Police = +100 Score & Heat Increases. Don't let Police touch you for 3 sec or you get BUSTED!</div>
 </div>
 <div id="levelUp"><h2>LEVEL COMPLETE! 🔥</h2><h3 id="levelUpTxt" style="margin:14px 0"></h3><p id="levelUpInfo" style="color:#ccc"></p><button class="btn" onclick="continueNext()">▶ NEXT LEVEL - FASTER!</button></div>
 <div id="over"><h2 id="overTitle">BUSTED BY POLICE!</h2><h3 id="final" style="margin:12px 0 20px"></h3><button class="btn" onclick="retryLevel()">↻ RETRY LEVEL</button><button class="btn btn2" onclick="showMenu()">🏠 MENU</button></div>
 <div id="win"><h2>🏆 YOU ESCAPED NYC!</h2><h3 id="winTxt" style="margin:12px 0 20px"></h3><button class="btn" onclick="showMenu()">🏠 PLAY AGAIN</button></div>
</div>
<script>
const canvas=document.getElementById('game');const ctx=canvas.getContext('2d');
let W,H,running=false,score=0,distance=0,levelDist=0,speed=0,keys={},traffic=[],police=[],particles=[],rain=[],lightning=0,buildings=[],poles=[],sym=false,symVal=100,nearMiss=0,combo=1,selectedLevel=1,currentLevel=1,playAll=true,tongue=0,shake=0,roadCurve=0,curveTarget=0,heat=1,policeTouchTime=0,escaped=0,sirenOn=true,timeOfDay='day';
let bike={x:0,y:0,tilt:0};
let levelData={1:{target:1200,max:240,policeCount:1,weather:'☀️ DAY SUN • CLEAR',name:'LEVEL 1 • DAY SUN • TIMES SQUARE'},2:{target:1500,max:275,policeCount:2,weather:'🌇 EVENING SUNSET • ORANGE SKY',name:'LEVEL 2 • EVENING • BROOKLYN BRIDGE'},3:{target:1800,max:320,policeCount:3,weather:'🌧️ NIGHT RAIN • LIGHTNING • WET ROAD',name:'LEVEL 3 • NIGHT RAIN • MANHATTAN STORM'}};
function resize(){W=canvas.width=window.innerWidth;H=canvas.height=window.innerHeight-104;bike.x=W/2;bike.y=H-175}window.addEventListener('resize',resize);resize();
function selectLevel(n){selectedLevel=n;document.getElementById('startLevelTxt').innerText=n;document.querySelectorAll('.levelCard').forEach(c=>c.classList.remove('active'));document.getElementById('card'+n).classList.add('active')}
function showMenu(){running=false;document.getElementById('menu').style.display='flex';document.getElementById('over').style.display='none';document.getElementById('win').style.display='none';document.getElementById('levelUp').style.display='none'}
function moveL(){bike.x-=50;bike.tilt=-1}function moveR(){bike.x+=50;bike.tilt=1}function toggleSym(){sym=!sym}
document.addEventListener('keydown',e=>{keys[e.key.toLowerCase()]=true;if(e.code==='Space'){sym=true;e.preventDefault()}if(e.key.toLowerCase()==='p'){sirenOn=!sirenOn;showToast(sirenOn?'🚨 SIREN ON':'🔇 SIREN OFF')}});
document.addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=false;if(e.code==='Space')sym=false});
function showToast(t){let el=document.getElementById('toast');el.innerText=t;el.style.display='block';setTimeout(()=>el.style.display='none',2200)}
function retryLevel(){startLevel(currentLevel)}
function continueNext(){document.getElementById('levelUp').style.display='none';if(currentLevel<3){currentLevel++;startLevel(currentLevel)}else{showWin()}}
function showWin(){running=false;document.getElementById('win').style.display='flex';document.getElementById('winTxt').innerText=`Total Score: ${score} • Escaped: ${escaped} Police • Max Speed Reached: 320 KM/H • You Are The Venom Legend of NYC!`}
function startGame(mode){if(mode===0){playAll=true;currentLevel=1}else{playAll=false;currentLevel=selectedLevel}startLevel(currentLevel)}
function startLevel(lv){currentLevel=lv;levelDist=0;if(lv===1){score=0;distance=0;escaped=0;heat=1}speed=70;traffic=[];police=[];particles=[];rain=[];symVal=100;nearMiss=0;combo=1;policeTouchTime=0;running=true;document.getElementById('menu').style.display='none';document.getElementById('over').style.display='none';document.getElementById('win').style.display='none';document.getElementById('levelUp').style.display='none';document.getElementById('levelName').innerText=levelData[lv].name;document.getElementById('weatherBadge').innerText=levelData[lv].weather+' • '+levelData[lv].max+' KM/H MAX';spawnTraffic();spawnPolice();showToast(lv===1?'☀️ DAY - POLICE CHASE START!':lv===2?'🌇 EVENING - SPEED INCREASED TO 275! 2 POLICE!':'🌧️ NIGHT RAIN - 320 KM/H! 3 POLICE! SURVIVE!');requestAnimationFrame(loop)}
function spawnTraffic(){if(!running)return;let roadW=Math.min(W*0.7,700);let roadX=(W-roadW)/2;let lanes=[roadX+roadW*0.18,roadX+roadW*0.5,roadX+roadW*0.82];let lane=lanes[Math.floor(Math.random()*3)];let taxi=Math.random()>0.5;let truck=Math.random()>0.82;let base=currentLevel===1?75:currentLevel===2?90:110;traffic.push({x:lane,y:-220,w:truck?76:60,h:truck?190:120,color:taxi?'#facc15':['#fff','#111','#ff1744','#00e5ff'][Math.floor(Math.random()*4)],speed:base+Math.random()*35,truck,taxi});setTimeout(spawnTraffic,Math.max(360,1000-speed*1.8))}
function spawnPolice(){if(!running)return;let count=levelData[currentLevel].policeCount;police=[];let roadW=Math.min(W*0.7,700);let roadX=(W-roadW)/2;for(let i=0;i<count;i++){police.push({x:roadX+roadW*0.5+(i-1)*70,y:H+200+i*160,w:64,h:125,speed:0,offset:i,flash:0,aggressive:0.6+currentLevel*0.25})} }
function drawWorld(){
  let hy=H*0.48;let lv=currentLevel;
  // SKY BY TIME
  if(lv===1){
    let g=ctx.createLinearGradient(0,0,0,hy);g.addColorStop(0,'#0ea5e9');g.addColorStop(.6,'#7dd3fc');g.addColorStop(1,'#fef9c3');ctx.fillStyle=g;ctx.fillRect(0,0,W,hy);
    // Day Sun Big
    ctx.fillStyle='rgba(255,255,0,.35)';ctx.beginPath();ctx.arc(W*0.85,H*0.12,72,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff700';ctx.beginPath();ctx.arc(W*0.85,H*0.12,38,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(W*0.85,H*0.12,20,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(255,255,255,.95)';for(let i=0;i<4;i++){let cx=((i*280+distance*0.4)%(W+200))-100;ctx.beginPath();ctx.ellipse(cx,50+i*28,52,16,0,0,Math.PI*2);ctx.ellipse(cx+28,56+i*28,36,12,0,0,Math.PI*2);ctx.fill()}
  } else if(lv===2){
    let g=ctx.createLinearGradient(0,0,0,hy);g.addColorStop(0,'#1e1b4b');g.addColorStop(.45,'#7c2d12');g.addColorStop(.8,'#ff6a00');g.addColorStop(1,'#facc15');ctx.fillStyle=g;ctx.fillRect(0,0,W,hy);
    // Evening Sun Low
    ctx.fillStyle='#ff3d00';ctx.beginPath();ctx.arc(W/2,hy-40,52,0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(255,100,0,.4)';ctx.beginPath();ctx.arc(W/2,hy-40,85,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(255,150,0,.7)';for(let i=0;i<5;i++){ctx.fillRect(0,40+i*18,W,4)}
  } else {
    let g=ctx.createLinearGradient(0,0,0,hy);g.addColorStop(0,'#020617');g.addColorStop(.6,'#0f172a');g.addColorStop(1,'#1e293b');ctx.fillStyle=g;ctx.fillRect(0,0,W,hy);
    // Night Moon + Lightning
    ctx.fillStyle='#e2e8f0';ctx.beginPath();ctx.arc(W*0.85,70,28,0,Math.PI*2);ctx.fill();ctx.fillStyle='#0f172a';ctx.beginPath();ctx.arc(W*0.85-8,66,24,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#fff';for(let i=0;i<40;i++){ctx.fillRect(Math.random()*W,Math.random()*hy*0.6,2,2)}
    if(lightning>0){ctx.fillStyle='rgba(255,255,255,.85)';ctx.fillRect(0,0,W,hy);lightning--}
    if(Math.random()<0.008)lightning=6;
    // Rain
    if(rain.length<120)for(let i=0;i<6;i++)rain.push({x:Math.random()*W,y:-20,vy:14+Math.random()*10});ctx.strokeStyle='rgba(200,220,255,.6)';ctx.lineWidth=1.5;for(let r of rain){ctx.beginPath();ctx.moveTo(r.x,r.y);ctx.lineTo(r.x-4,r.y+14);ctx.stroke();r.y+=r.vy;r.x-=3}rain=rain.filter(r=>r.y<H);
  }
  roadCurve+=(curveTarget-roadCurve)*0.02;if(Math.random()<0.006)curveTarget=(Math.random()-0.5)*70;
  // Background by level
  if(lv===1){ctx.fillStyle='#1e293b';for(let i=0;i<14;i++){let bw=W/14;let h=80+(i*73)%120;ctx.fillRect(i*bw+roadCurve*0.3,hy-h,bw-6,h);ctx.fillStyle='#ff2d00';ctx.font='900 11px Orbitron';ctx.textAlign='center';ctx.fillText(i%2?'TIMES':'NYC',i*bw+bw/2,hy-h+18);ctx.fillStyle='#1e293b';for(let y=0;y<3;y++){ctx.fillStyle='#fef08a';ctx.fillRect(i*bw+8,hy-h+28+y*18,8,10);ctx.fillStyle='#1e293b'}}}
  else if(lv===2){ctx.strokeStyle='#94a3b8';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(0,hy-40);ctx.quadraticCurveTo(W*0.5,hy-95,W,hy-40);ctx.stroke();ctx.fillStyle='#64748b';for(let i=0;i<6;i++)ctx.fillRect(i*W/6+W/12-6,hy-110,12,110);ctx.fillStyle='#1e293b';for(let i=0;i<8;i++){let bw=W/8;ctx.fillRect(i*bw,hy-50-(i*17)%60,bw-8,60+(i*17)%60)}ctx.fillStyle='#ff6a00';ctx.font='900 13px Orbitron';ctx.textAlign='center';ctx.fillText('BROOKLYN BRIDGE • EVENING',W/2,hy-115)}
  else{ctx.fillStyle='#0f172a';for(let i=0;i<12;i++){let bw=W/12;let h=110+(i*53)%130;ctx.fillRect(i*bw,hy-h-20,bw-8,h);ctx.fillStyle='#facc15';for(let y=0;y<4;y++)ctx.fillRect(i*bw+8,hy-h+10+y*20,7,9);ctx.fillStyle='#0f172a'}ctx.fillStyle='#38bdf8';ctx.font='900 12px Orbitron';ctx.textAlign='center';ctx.fillText('MANHATTAN • NIGHT RAIN STORM',W/2,hy-135)}
  // 3D ROAD
  let roadW=Math.min(W*0.7,700);let roadX=(W-roadW)/2+roadCurve;
  let roadColor=lv===3?'#0f172a':'#1a1a1a'; // Wet road dark in rain
  ctx.fillStyle='#0a0a0a';ctx.beginPath();ctx.moveTo(roadX+roadW*0.18,hy);ctx.lineTo(roadX+roadW*0.82,hy);ctx.lineTo(roadX+roadW+18,H+10);ctx.lineTo(roadX-18,H+10);ctx.closePath();ctx.fill();
  ctx.fillStyle=roadColor;ctx.beginPath();ctx.moveTo(roadX+roadW*0.18,hy);ctx.lineTo(roadX+roadW*0.82,hy);ctx.lineTo(roadX+roadW,H);ctx.lineTo(roadX,H);ctx.closePath();ctx.fill();
  // Wet reflection in night rain
  if(lv===3){ctx.fillStyle='rgba(0,229,255,.08)';ctx.fillRect(roadX,hy+40,roadW,H-hy-40)}
  ctx.fillStyle=lv===3?'#475569':'#94a3b8';ctx.fillRect(roadX-28,hy,28,H-hy);ctx.fillRect(roadX+roadW,hy,28,H-hy);
  ctx.lineWidth=5;ctx.shadowBlur=16;ctx.strokeStyle='#a3e635';ctx.shadowColor='#a3e635';ctx.beginPath();ctx.moveTo(roadX+roadW*0.18,hy);ctx.lineTo(roadX,H);ctx.stroke();ctx.strokeStyle=lv===3?'#00e5ff':'#ff2d00';ctx.shadowColor=ctx.strokeStyle;ctx.beginPath();ctx.moveTo(roadX+roadW*0.82,hy);ctx.lineTo(roadX+roadW,H);ctx.stroke();ctx.shadowBlur=0;
  ctx.strokeStyle=lv===3?'rgba(255,255,255,.5)':'#facc15';ctx.lineWidth=6;ctx.setLineDash([38,30]);ctx.lineDashOffset=-distance*1.9;for(let p of [0.42,0.62]){ctx.beginPath();ctx.moveTo(roadX+roadW*p,hy);ctx.lineTo(roadX+roadW*(p-0.13),H);ctx.stroke()}ctx.setLineDash([]);
  if(Math.random()<0.08)poles.push({y:hy});for(let pl of poles)pl.y+=speed/10;poles=poles.filter(p=>p.y<H);ctx.fillStyle='#334155';for(let pl of poles){ctx.fillRect(roadX-12,pl.y,6,30);ctx.fillRect(roadX+roadW+6,pl.y,6,30)}
  return {roadX,roadW,hy};
}
function drawVenom(){
  ctx.save();ctx.translate(bike.x,bike.y+shake);ctx.rotate(bike.tilt*0.18);
  ctx.fillStyle='rgba(0,0,0,.6)';ctx.beginPath();ctx.ellipse(0,68,58,14,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(163,230,53,.25)';ctx.beginPath();ctx.ellipse(0,20,44,78,0,0,Math.PI*2);ctx.fill();
  if(sym&&symVal>0){ctx.strokeStyle='#000';ctx.lineWidth=6;for(let i=0;i<5;i++){let tx=Math.sin(Date.now()/70+i*1.4)*26;ctx.beginPath();ctx.moveTo(i*10-20,52);ctx.quadraticCurveTo(tx,78,tx*1.3,102+Math.random()*12);ctx.stroke()}ctx.fillStyle='#a3e635';for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(Math.sin(Date.now()/80+i)*22,84+i*8,3.5,0,Math.PI*2);ctx.fill()}}
  if(sym&&symVal>0){let fl=24+Math.random()*30;let gg=ctx.createLinearGradient(0,62,0,62+fl+38);gg.addColorStop(0,'#fff');gg.addColorStop(.35,'#a3e635');gg.addColorStop(1,'transparent');ctx.fillStyle=gg;ctx.beginPath();ctx.moveTo(-15,62);ctx.lineTo(15,62);ctx.lineTo(0,62+fl+40);ctx.closePath();ctx.fill()}
  ctx.fillStyle='#050505';ctx.beginPath();ctx.ellipse(0,-52,10,30,0,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.ellipse(0,52,11,30,0,0,Math.PI*2);ctx.fill();
  let bg=ctx.createLinearGradient(-36,-72,36,66);bg.addColorStop(0,'#000');bg.addColorStop(.4,'#111');bg.addColorStop(.7,'#1f2937');bg.addColorStop(1,'#000');ctx.fillStyle=bg;ctx.beginPath();ctx.moveTo(0,-74);ctx.lineTo(26,-32);ctx.lineTo(32,8);ctx.lineTo(24,50);ctx.lineTo(12,64);ctx.lineTo(-12,64);ctx.lineTo(-24,50);ctx.lineTo(-32,8);ctx.lineTo(-26,-32);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(255,255,255,.95)';ctx.lineWidth=2.2;ctx.beginPath();ctx.moveTo(-12,-42);ctx.quadraticCurveTo(0,-12,12,-42);ctx.moveTo(-18,10);ctx.quadraticCurveTo(0,32,18,10);ctx.stroke();
  ctx.fillStyle='#fff';ctx.beginPath();ctx.ellipse(-10,-36,7,11,-0.4,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.ellipse(10,-36,7,11,0.4,0,Math.PI*2);ctx.fill();ctx.fillStyle='#000';ctx.beginPath();ctx.arc(-9,-34,2.5,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(9,-34,2.5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#7f1d1d';ctx.beginPath();ctx.ellipse(0,-8,14,8,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';for(let i=-2;i<=2;i++){ctx.fillRect(i*4-1,-13,2,5);ctx.fillRect(i*4-1,-2,2,5)}
  tongue+=0.18;let tl=10+Math.sin(tongue)*7;ctx.fillStyle='#ef4444';ctx.beginPath();ctx.moveTo(-4,-2);ctx.lineTo(4,-2);ctx.lineTo(0,tl);ctx.closePath();ctx.fill();
  ctx.fillStyle='#a3e635';ctx.shadowColor='#a3e635';ctx.shadowBlur=24;ctx.beginPath();ctx.arc(0,-56,6,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  ctx.fillStyle='#000';ctx.beginPath();ctx.roundRect(-15,10,30,36,10);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(0,20,5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#000';ctx.beginPath();ctx.arc(0,-8,16,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.ellipse(-7,-9,5,7,-0.4,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.ellipse(7,-9,5,7,0.4,0,Math.PI*2);ctx.fill();ctx.fillStyle='#7f1d1d';ctx.beginPath();ctx.ellipse(0,2,9,4,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.fillRect(-6,0,3,2);ctx.fillRect(0,0,3,2);ctx.fillRect(4,0,3,2);
  ctx.fillStyle='#a3e635';ctx.font='900 10px Orbitron';ctx.textAlign='center';ctx.fillText('VENOM',0,58);ctx.font='700 7px Arial';ctx.fillStyle='#fff';ctx.fillText('3D • NYC',0,67);
  ctx.restore();
}
function drawPolice(p){
  ctx.save();ctx.translate(p.x,p.y);p.flash++;
  let flashRed=p.flash%20<10;
  ctx.fillStyle='rgba(0,0,0,.5)';ctx.beginPath();ctx.ellipse(0,68,52,12,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=flashRed?'#ff0000':'#0000ff';ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=20;ctx.beginPath();ctx.arc(0,-70,14,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  ctx.fillStyle='#fff';ctx.beginPath();ctx.roundRect(-32,-62,64,130,14);ctx.fill();
  ctx.fillStyle='#111';ctx.beginPath();ctx.roundRect(-32,-20,64,40,8);ctx.fill();
  ctx.fillStyle='#000';ctx.fillRect(-32,10,64,6);
  ctx.fillStyle='#ff0000';ctx.fillRect(-30,-62,12,6);ctx.fillStyle='#0000ff';ctx.fillRect(18,-62,12,6);
  ctx.fillStyle='#000';ctx.font='900 12px Orbitron';ctx.textAlign='center';ctx.fillText('NYPD',0,0);ctx.font='700 8px Arial';ctx.fillText('POLICE',0,12);
  ctx.fillStyle='#111';ctx.fillRect(-8,-72,16,10);
  ctx.restore();
}
function drawCar(c){
  ctx.save();ctx.translate(c.x,c.y);let scale=0.7+(c.y/H)*0.5;ctx.scale(scale,scale);ctx.fillStyle='rgba(0,0,0,.45)';ctx.beginPath();ctx.ellipse(0,c.h/2,c.w/2+6,10,0,0,Math.PI*2);ctx.fill();
  if(c.taxi){ctx.fillStyle='#facc15';ctx.beginPath();ctx.roundRect(-c.w/2,-c.h/2,c.w,c.h,10);ctx.fill();ctx.fillStyle='#000';ctx.font='900 11px Arial';ctx.textAlign='center';ctx.fillText('TAXI',0,0);ctx.fillStyle='#111';ctx.fillRect(-c.w/2+6,-c.h/2+24,c.w-12,22);ctx.restore();return}
  ctx.fillStyle=c.color;ctx.beginPath();ctx.roundRect(-c.w/2,-c.h/2,c.w,c.h,14);ctx.fill();ctx.fillStyle='#0d0d0d';ctx.fillRect(-c.w/2+6,-c.h/2+24,c.w-12,28);ctx.fillStyle='#fff';ctx.fillRect(-c.w/2+8,-c.h/2+8,10,6);ctx.fillRect(c.w/2-18,-c.h/2+8,10,6);ctx.fillStyle='#ff1744';ctx.fillRect(-c.w/2+8,c.h/2-14,10,6);ctx.fillRect(c.w/2-18,c.h/2-14,10,6);if(c.truck){ctx.fillStyle='#111';ctx.font='900 12px Arial';ctx.textAlign='center';ctx.fillText('TRUCK',0,10)}ctx.restore();
}
function loop(){
  if(!running)return;
  if(sym&&symVal>0)symVal-=0.55;else if(!sym)symVal=Math.min(100,symVal+0.32);if(symVal<=0)sym=false;
  let brake=keys['s']||keys['arrowdown'];
  let maxSpeed=levelData[currentLevel].max;
  let target=brake?40:sym&&symVal>0?maxSpeed:(keys['w']||keys['arrowup']?185+currentLevel*10:120);
  speed+=(target-speed)*0.03+0.18;if(speed>maxSpeed)speed=maxSpeed;
  if(keys['a']||keys['arrowleft']){bike.x-=7+speed/24;bike.tilt=-1}else if(keys['d']||keys['arrowright']){bike.x+=7+speed/24;bike.tilt=1}else bike.tilt*=0.88;
  let {roadX,roadW}=drawWorld();distance+=speed/55;levelDist+=speed/55;score+=Math.floor(speed/85)*combo;
  // Heat increases over time
  heat=Math.min(5,1+Math.floor(levelDist/400)); 
  // Level Complete
  let targetDist=levelData[currentLevel].target;
  if(levelDist>=targetDist){
    running=false;document.getElementById('policeAlert').style.display='none';
    if(playAll&&currentLevel<3){document.getElementById('levelUp').style.display='flex';let next=levelData[currentLevel+1];document.getElementById('levelUpTxt').innerText=`You Escaped Level ${currentLevel}! Score: ${score}`;document.getElementById('levelUpInfo').innerText=`NEXT: ${next.name} • Speed Increases to ${next.max} KM/H • ${next.weather} • +${currentLevel} Police Cars!`;return}
    else if(playAll&&currentLevel===3){showWin();return}
    else{document.getElementById('levelUp').style.display='flex';document.getElementById('levelUpTxt').innerText=`Level ${currentLevel} Complete! Score: ${score}`;document.getElementById('levelUpInfo').innerText=`You escaped! Max Speed was ${maxSpeed} KM/H`;return}
  }
  if(bike.x<roadX+32)bike.x=roadX+32;if(bike.x>roadX+roadW-32)bike.x=roadX+roadW-32;
  // Traffic
  for(let c of traffic)c.y+=(speed-c.speed)*0.98+2;traffic=traffic.filter(c=>c.y<H+240);
  for(let c of traffic){drawCar(c);if(Math.abs(c.x-bike.x)<50&&Math.abs(c.y-bike.y)<84){running=false;document.getElementById('overTitle').innerText='CRASHED!';document.getElementById('over').style.display='flex';document.getElementById('final').innerText=`Level: ${currentLevel} • Score: ${score} • Distance: ${Math.floor(levelDist)}m / ${targetDist}m • Top: ${Math.floor(speed)} KM/H`;document.getElementById('policeAlert').style.display='none';return}if(!c.passed&&c.y>bike.y+95){c.passed=true;score+=60*combo;nearMiss++;combo=Math.min(6,combo+1);if(nearMiss%3===0)symVal=Math.min(100,symVal+20)}}
  // POLICE CHASE - 3D Real
  let policeTouch=false;
  for(let p of police){
    // Police AI - Chase bike X, try to ram
    let dx=bike.x-p.x; p.x+=dx*0.012*p.aggressive + Math.sin(Date.now()/300+p.offset)*0.6;
    p.y-= (speed*0.85 - 18) * 0.9; // Police coming from behind, catch up if you slow
    if(p.y < bike.y+120) p.y=bike.y+120+Math.random()*40; // Keep behind
    if(p.y > H+200) {p.y=H+100; escaped++; score+=100}
    // If police is close behind, show alert
    if(Math.abs(p.x-bike.x)<60 && Math.abs(p.y-bike.y)<130){policeTouch=true}
    drawPolice(p);
    // Near miss police = bonus
    if(!p.passed && p.y < bike.y-100){p.passed=true; score+=100; escaped++}
  }
  if(policeTouch){policeTouchTime+=1;shake=3;document.getElementById('policeAlert').style.display='block';if(policeTouchTime>90){running=false;document.getElementById('overTitle').innerText='BUSTED BY NYPD! 🚨';document.getElementById('over').style.display='flex';document.getElementById('final').innerText=`Police caught you for 3 seconds! Score: ${score} • Level: ${currentLevel} • Distance: ${Math.floor(levelDist)}m`;document.getElementById('policeAlert').style.display='none';return}}else{policeTouchTime=Math.max(0,policeTouchTime-2);shake*=0.9;if(policeTouchTime===0)document.getElementById('policeAlert').style.display='none'}
  drawVenom();
  if(speed>170)for(let i=0;i<4;i++)particles.push({x:Math.random()*W,y:H,vy:-14-Math.random()*10});ctx.fillStyle=currentLevel===3?'rgba(163,230,53,.6)':'rgba(255,255,255,.6)';for(let p of particles){ctx.fillRect(p.x,p.y,2,22);p.y+=p.vy}particles=particles.filter(p=>p.y>-20);
  let gear=speed<40?1:speed<80?2:speed<120?3:speed<170?4:speed<220?5:6;
  document.getElementById('score').innerText=score;document.getElementById('speed').innerText=Math.floor(speed);document.getElementById('dist').innerText=Math.floor(distance)+'m';document.getElementById('gear').innerText=gear;document.getElementById('near').innerText='ESCAPED: '+escaped;document.getElementById('combo').innerText='COMBO x'+combo;document.getElementById('symFill').style.width=symVal+'%';document.getElementById('heatFill').style.width=heat*20+'%';document.getElementById('heatTxt').innerText='HEAT '+heat+'★';document.getElementById('levelFill').style.width=Math.min(100,levelDist/targetDist*100)+'%';document.getElementById('levelDist').innerText=Math.floor(levelDist)+' / '+targetDist+'m • Speed +'+(currentLevel-1)*35+' KM/H';document.getElementById('wrap').classList.toggle('sym',sym&&symVal>0);
  requestAnimationFrame(loop);
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(debug=True, port=5000)