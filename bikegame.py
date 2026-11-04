
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VENOM NYC | 3D NIGHT RIDER</title>

<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#020308;color:white;font-family:Arial}
canvas{display:block}
#hud{position:absolute;top:20px;left:25px;right:25px;
display:flex;justify-content:space-between;pointer-events:none}
.logo{font-size:25px;font-weight:1000;letter-spacing:5px}
.logo span{color:#e92348;text-shadow:0 0 20px red}
.stats{display:flex;gap:25px}
.stat{font-size:10px;letter-spacing:3px;color:#aaa}
.stat b{display:block;font-size:23px;color:white;margin-top:6px}
#nitro{position:absolute;bottom:25px;left:50%;transform:translateX(-50%);
width:220px;text-align:center;letter-spacing:4px;font-size:10px}
#bar{height:7px;background:#444;margin-top:9px}
#fill{height:100%;width:100%;background:linear-gradient(90deg,#f13,#ffb000);
box-shadow:0 0 15px red}
.overlay{position:absolute;inset:0;display:flex;align-items:center;
justify-content:center;flex-direction:column;text-align:center;
background:radial-gradient(ellipse,#111827aa,#020308ee);z-index:5}
.hidden{display:none!important}
h1{font-size:clamp(48px,9vw,105px);font-weight:1000;
font-style:italic;letter-spacing:-5px;text-shadow:0 0 35px #f13}
h1 span{color:#f13}
.subtitle{font-size:11px;letter-spacing:7px;color:#aaa;margin:15px}
button{padding:17px 48px;background:#e92348;border:0;color:white;
font-weight:900;letter-spacing:4px;cursor:pointer;margin-top:25px;
box-shadow:0 0 30px #e9234877}
button:hover{background:white;color:#e92348}
#help{position:absolute;bottom:25px;left:25px;font-size:10px;
color:#aaa;letter-spacing:2px;line-height:2}
#mobile{position:absolute;bottom:90px;width:100%;display:none;
justify-content:space-between;padding:15px;pointer-events:none}
.pad{display:flex;gap:10px}
.pad button{pointer-events:auto;width:58px;height:58px;padding:0;
border-radius:50%;margin:0;background:#111c;border:1px solid #fff6}
@media(max-width:700px){
#mobile{display:flex}
.stats{gap:10px}.stat b{font-size:16px}
.logo{font-size:17px}#help{display:none}
}
</style>
</head>

<body>

<div id="hud">
 <div class="logo">VENOM <span>NYC</span></div>
 <div class="stats">
  <div class="stat">SPEED<b id="speed">000</b></div>
  <div class="stat">DISTANCE<b id="dist">0 M</b></div>
  <div class="stat">SCORE<b id="score">0000</b></div>
 </div>
</div>

<div id="nitro">
 NITRO BOOST
 <div id="bar"><div id="fill"></div></div>
</div>

<div id="help">
 W / ↑ : ACCELERATE<br>
 S / ↓ : BRAKE<br>
 A / D : STEER<br>
 SHIFT : NITRO
</div>

<div id="mobile">
 <div class="pad">
  <button id="left">◀</button>
  <button id="right">▶</button>
 </div>
 <div class="pad">
  <button id="brake">▼</button>
  <button id="boost">⚡</button>
 </div>
</div>

<div class="overlay" id="start">
 <h1>VENOM <span>NYC</span></h1>
 <div class="subtitle">THE CITY NEVER SLEEPS</div>
 <p style="color:#aaa;font-size:11px;letter-spacing:3px">
  3D SUPERBIKE EXPERIENCE
 </p>
 <button onclick="startGame()">START RIDING</button>
</div>

<div class="overlay hidden" id="gameover">
 <h1>RIDE <span>OVER</span></h1>
 <p class="subtitle">YOUR CITY RUN HAS ENDED</p>
 <h2 id="final">SCORE: 0</h2>
 <button onclick="startGame()">RIDE AGAIN</button>
</div>

<script type="importmap">
{
 "imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"
 }
}
</script>

<script type="module">
import * as THREE from "three";

// ===================================
// VENOM NYC - 3D GAME ENGINE
// ===================================

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x030611);
scene.fog = new THREE.FogExp2(0x080c18,0.012);

const camera = new THREE.PerspectiveCamera(
 65,innerWidth/innerHeight,0.1,1000
);
camera.position.set(0,5,10);

const renderer = new THREE.WebGLRenderer({
 antialias:true, powerPreference:"high-performance"
});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.3;
document.body.appendChild(renderer.domElement);

// ===================================
// LIGHTING
// ===================================

scene.add(new THREE.HemisphereLight(0x8799c8,0x101018,2));

const moon = new THREE.DirectionalLight(0x9dbaff,2.5);
moon.position.set(-10,20,10);
moon.castShadow=true;
scene.add(moon);

const redLight = new THREE.PointLight(0xff123c,45,30);
redLight.position.set(0,3,-8);
scene.add(redLight);

const blueLight = new THREE.PointLight(0x164cff,30,25);
blueLight.position.set(8,4,-12);
scene.add(blueLight);

// ===================================
// MATERIALS
// ===================================

const black = new THREE.MeshStandardMaterial({
 color:0x090b10,metalness:0.9,roughness:0.24
});
const darkMetal = new THREE.MeshStandardMaterial({
 color:0x202631,metalness:0.85,roughness:0.3
});
const red = new THREE.MeshStandardMaterial({
 color:0xff173b,metalness:0.65,roughness:0.25,
 emissive:0x550012,emissiveIntensity:1
});
const chrome = new THREE.MeshStandardMaterial({
 color:0xaaaaaf,metalness:0.95,roughness:0.15
});
const eyeMat = new THREE.MeshStandardMaterial({
 color:0xffffff,emissive:0xffffff,emissiveIntensity:2
});
const tire = new THREE.MeshStandardMaterial({
 color:0x050507,roughness:0.9
});

// ===================================
// HELPER FUNCTIONS
// ===================================

function box(parent,x,y,z,sx,sy,sz,mat){
 const m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),mat);
 m.position.set(x,y,z);
 m.castShadow=true;
 m.receiveShadow=true;
 parent.add(m);
 return m;
}

function sphere(parent,x,y,z,sx,sy,sz,mat){
 const m=new THREE.Mesh(
  new THREE.SphereGeometry(1,24,16),mat
 );
 m.position.set(x,y,z);
 m.scale.set(sx,sy,sz);
 m.castShadow=true;
 parent.add(m);
 return m;
}

function cylinder(parent,x,y,z,r1,r2,len,mat,rotX=0,rotZ=0){
 const m=new THREE.Mesh(
  new THREE.CylinderGeometry(r1,r2,len,32),mat
 );
 m.position.set(x,y,z);
 m.rotation.set(rotX,0,rotZ);
 m.castShadow=true;
 parent.add(m);
 return m;
}

// ===================================
// NEW YORK CITY
// ===================================

const road = new THREE.Mesh(
 new THREE.PlaneGeometry(20,1000),
 new THREE.MeshStandardMaterial({
  color:0x171a22,metalness:0.25,roughness:0.3
 })
);
road.rotation.x=-Math.PI/2;
road.position.z=-300;
road.receiveShadow=true;
scene.add(road);

// Road lane markings
const stripes=[];
for(let z=20;z>-500;z-=12){
 for(let x of [-2.3,2.3]){
  const s=box(scene,x,0.025,z,0.12,0.025,5,
   new THREE.MeshBasicMaterial({color:0xc9d0dc}));
  stripes.push(s);
 }
}

// City buildings
const buildings=[];
const buildingColors=[
 0x101a2d,0x17243b,0x202335,0x111827,0x24283b
];

function createBuilding(x,z){
 const height=15+Math.random()*55;
 const width=7+Math.random()*7;
 const depth=8+Math.random()*8;

 const group=new THREE.Group();
 group.position.set(x,height/2-0.2,z);
 scene.add(group);

 const material=new THREE.MeshStandardMaterial({
  color:buildingColors[Math.floor(Math.random()*buildingColors.length)],
  metalness:0.4,roughness:0.8
 });

 box(group,0,0,0,width,height,depth,material);

 // Windows
 const windowMat=new THREE.MeshBasicMaterial({
  color:Math.random()>0.5?0xffca72:0x4d87c9
 });

 for(let y=-height/2+2;y<height/2-1;y+=3){
  for(let wx=-width/2+1;wx<width/2-1;wx+=2){
   if(Math.random()>0.24){
    box(group,wx,y,depth/2+0.015,
     0.75,1.15,0.04,windowMat);
   }
  }
 }

 // Roof structures
 box(group,0,height/2+1,0,width*0.3,2,depth*0.3,darkMetal);

 buildings.push(group);
}

for(let z=-30;z>-500;z-=24){
 createBuilding(-16-Math.random()*5,z);
 createBuilding(16+Math.random()*5,z);
}

// Street lights
const streetLights=[];
for(let z=10;z>-500;z-=32){
 for(let side of [-1,1]){
  const g=new THREE.Group();
  g.position.set(side*8,0,z);
  scene.add(g);

  cylinder(g,0,3,0,0.12,0.12,6,chrome);
  box(g,side*-0.8,5.9,0,1.8,0.12,0.15,darkMetal);

  const lamp=new THREE.PointLight(
   side===-1?0xff304b:0x498aff,8,15
  );
  lamp.position.set(-side*1.3,5.6,0);
  g.add(lamp);

  sphere(g,-side*1.3,5.6,0,0.25,0.1,0.25,eyeMat);
  streetLights.push(g);
 }
}

// ===================================
// MOTORCYCLE
// ===================================

const bike=new THREE.Group();
scene.add(bike);

// Main frame
box(bike,0,0.82,0,0.42,0.22,2.15,darkMetal);

// Engine
sphere(bike,0,0.72,0.2,0.52,0.48,0.58,black);

// Side fairings
sphere(bike,-0.38,0.92,-0.35,0.18,0.42,0.78,red);
sphere(bike,0.38,0.92,-0.35,0.18,0.42,0.78,red);

// Front nose
sphere(bike,0,1.13,-1.05,0.4,0.36,0.72,black);

// Fuel tank
sphere(bike,0,1.28,-0.15,0.43,0.33,0.55,darkMetal);

// Rear body
sphere(bike,0,1.04,0.8,0.38,0.28,0.58,red);

// Seat
box(bike,0,1.35,0.55,0.5,0.13,0.65,black);

// Windshield
const wind=new THREE.Mesh(
 new THREE.SphereGeometry(0.42,24,16,0,Math.PI*2,0,Math.PI/2),
 new THREE.MeshPhysicalMaterial({
  color:0x263d5a,transparent:true,opacity:0.6,
  metalness:0.5,roughness:0.1
 })
);
wind.position.set(0,1.45,-0.88);
wind.scale.set(1,0.7,1);
bike.add(wind);

// Headlight
const headlamp=sphere(bike,0,1.13,-1.62,0.24,0.13,0.06,eyeMat);
const headLight=new THREE.SpotLight(0xc9e5ff,90,80,0.4,0.6,1);
headLight.position.set(0,1.2,-1.5);
headLight.target.position.set(0,0,-15);
bike.add(headLight,headLight.target);

// Venom eyes on front fairing
for(let side of [-1,1]){
 const eye=sphere(bike,side*0.22,1.33,-1.48,
  0.15,0.055,0.045,eyeMat);
 eye.rotation.z=side*0.3;
}

// Exhaust
for(let side of [-1,1]){
 cylinder(bike,side*0.32,0.66,1.25,
  0.09,0.12,0.8,chrome,Math.PI/2);
}

// Wheels
const wheels=[];
for(let z of [-1.25,1.25]){
 const wheel=new THREE.Group();
 wheel.position.set(0,0.46,z);
 bike.add(wheel);

 const rubber=cylinder(wheel,0,0,0,0.46,0.46,0.23,tire,
  Math.PI/2);
 rubber.rotation.z=Math.PI/2;

 const rim=cylinder(wheel,0,0,0,0.3,0.3,0.25,chrome,
  Math.PI/2);
 rim.rotation.z=Math.PI/2;

 cylinder(wheel,0,0,0,0.12,0.12,0.27,red,Math.PI/2);

 for(let i=0;i<6;i++){
  const a=i*Math.PI/3;
  const spoke=box(wheel,
   Math.cos(a)*0.19,Math.sin(a)*0.19,0,
   0.035,0.035,0.38,chrome);
  spoke.rotation.z=a;
 }

 wheels.push(wheel);
}

// Front forks
for(let side of [-1,1]){
 const fork=cylinder(bike,side*0.17,0.76,-1.25,
  0.045,0.045,1.25,chrome);
 fork.rotation.x=0.18;
}

// ===================================
// VENOM-INSPIRED RIDER
// ===================================

const rider=new THREE.Group();
bike.add(rider);

// Torso
sphere(rider,0,1.85,0.15,0.34,0.55,0.27,black);

// Chest armor
sphere(rider,0,2.02,0.02,0.38,0.32,0.3,darkMetal);

// Neck
cylinder(rider,0,2.38,0.12,0.12,0.13,0.2,black);

// Head / helmet
sphere(rider,0,2.63,-0.15,0.32,0.38,0.32,black);

// White venom eyes
for(let side of [-1,1]){
 const eye=sphere(rider,side*0.17,2.7,-0.435,
  0.13,0.075,0.035,eyeMat);
 eye.rotation.z=side*-0.3;
}

// Helmet forehead details
sphere(rider,0,2.91,-0.3,0.2,0.08,0.1,red);

// Arms
const arms=[];
for(let side of [-1,1]){
 const arm=new THREE.Group();
 arm.position.set(side*0.28,2.1,0.05);
 rider.add(arm);

 const upper=cylinder(arm,side*0.18,-0.13,-0.17,
  0.11,0.15,0.52,black);
 upper.rotation.x=-0.7;
 upper.rotation.z=side*0.35;

 sphere(arm,side*0.35,-0.33,-0.38,
  0.12,0.12,0.13,red);

 const fore=cylinder(arm,side*0.38,-0.39,-0.55,
  0.095,0.12,0.55,darkMetal);
 fore.rotation.x=-0.7;
 fore.rotation.z=side*0.2;

 sphere(arm,side*0.39,-0.58,-0.77,
  0.12,0.1,0.13,black);

 arms.push(arm);
}

// Legs
for(let side of [-1,1]){
 const leg=new THREE.Group();
 leg.position.set(side*0.2,1.65,0.35);
 rider.add(leg);

 const thigh=cylinder(leg,side*0.08,-0.25,0.1,
  0.16,0.19,0.6,black);
 thigh.rotation.x=-0.7;

 const boot=sphere(leg,side*0.12,-0.58,-0.3,
  0.13,0.13,0.3,darkMetal);
}

// ===================================
// NITRO FLAMES
// ===================================

const flames=[];
const flameMaterial=new THREE.MeshBasicMaterial({
 color:0xff4a09,transparent:true,opacity:0.85
});

for(let side of [-1,1]){
 const flame=new THREE.Mesh(
  new THREE.ConeGeometry(0.12,1.5,12),flameMaterial
 );
 flame.position.set(side*0.31,0.7,1.9);
 flame.rotation.x=-Math.PI/2;
 flame.scale.set(1,1,1);
 bike.add(flame);
 flames.push(flame);
}

// ===================================
// TRAFFIC
// ===================================

const traffic=[];
const carColors=[0x202c46,0x9c172e,0xb5b5bd,0x121212];

function createCar(){
 const car=new THREE.Group();
 const color=new THREE.MeshStandardMaterial({
  color:carColors[Math.floor(Math.random()*carColors.length)],
  metalness:0.65,roughness:0.3
 });

 box(car,0,0.65,0,1.5,0.85,2.6,color);
 box(car,0,1.2,-0.1,1.25,0.55,1.2,darkMetal);

 for(let side of [-1,1]){
  for(let z of [-0.8,0.8]){
   const light=sphere(car,side*0.45,0.7,z<0?-1.32:1.32,
    0.16,0.1,0.05,z<0?eyeMat:red);
  }
 }

 car.position.set([-4.2,0,4.2][Math.floor(Math.random()*3)],
  0,-150-Math.random()*200);

 scene.add(car);
 traffic.push(car);
}

for(let i=0;i<8;i++) createCar();

// ===================================
// GAME STATE
// ===================================

let running=false;
let velocity=0;
let distance=0;
let score=0;
let nitro=100;
let lane=0;
let lean=0;
let time=0;

const keys={};

document.addEventListener("keydown",e=>{
 keys[e.key.toLowerCase()]=true;
 if(["arrowup","arrowdown"," "].includes(e.key.toLowerCase()))
  e.preventDefault();
});

document.addEventListener("keyup",e=>{
 keys[e.key.toLowerCase()]=false;
});

function bindButton(id,key){
 const el=document.getElementById(id);
 el.addEventListener("pointerdown",e=>{
  e.preventDefault();
  keys[key]=true;
 });
 ["pointerup","pointercancel","pointerleave"].forEach(event=>{
  el.addEventListener(event,()=>keys[key]=false);
 });
}

bindButton("left","a");
bindButton("right","d");
bindButton("brake","s");
bindButton("boost","shift");

function startGame(){
 running=true;
 velocity=0;
 distance=0;
 score=0;
 nitro=100;
 lane=0;
 bike.position.set(0,0,0);
 bike.rotation.set(0,0,0);

 traffic.forEach((car,i)=>{
  car.position.z=-100-i*65;
  car.position.x=[-4.2,0,4.2][i%3];
 });

 document.getElementById("start").classList.add("hidden");
 document.getElementById("gameover").classList.add("hidden");
}

function endGame(){
 running=false;
 document.getElementById("final").textContent="SCORE: "+score;
 document.getElementById("gameover").classList.remove("hidden");
}

window.startGame=startGame;

// ===================================
// ANIMATION LOOP
// ===================================

const clock=new THREE.Clock();
const cameraTarget=new THREE.Vector3();

function animate(){
 requestAnimationFrame(animate);

 const dt=Math.min(clock.getDelta(),0.04);
 time+=dt;

 if(running){

  const accelerating=keys["w"]||keys["arrowup"];
  const braking=keys["s"]||keys["arrowdown"];
  const boosting=keys["shift"]&&nitro>0;

  if(accelerating) velocity+=22*dt;
  else velocity-=4*dt;

  if(braking) velocity-=30*dt;
  if(boosting){
   velocity+=40*dt;
   nitro-=24*dt;
  }else{
   nitro=Math.min(100,nitro+5*dt);
  }

  velocity=THREE.MathUtils.clamp(velocity,0,boosting?110:80);

  const normalized=velocity/80;
  const movement=velocity*dt*0.12;

  if(keys["a"]||keys["arrowleft"]) lane-=5*dt;
  if(keys["d"]||keys["arrowright"]) lane+=5*dt;

  lane=THREE.MathUtils.clamp(lane,-4.8,4.8);

  bike.position.x=THREE.MathUtils.lerp(
   bike.position.x,lane,dt*5
  );

  lean=THREE.MathUtils.lerp(
   lean,(keys["a"]||keys["arrowleft"])?0.32:
   (keys["d"]||keys["arrowright"])?-0.32:0,dt*5
  );

  bike.rotation.z=lean;
  bike.rotation.x=Math.sin(time*12)*0.012*normalized;

  wheels.forEach(w=>{
   w.rotation.x-=movement*2;
  });

  // Road movement
  stripes.forEach(s=>{
   s.position.z+=movement*3;
   if(s.position.z>20) s.position.z=-500;
  });

  // Buildings
  buildings.forEach(b=>{
   b.position.z+=movement*2;
   if(b.position.z>30) b.position.z=-500;
  });

  streetLights.forEach(l=>{
   l.position.z+=movement*3;
   if(l.position.z>20) l.position.z=-500;
  });

  // Traffic
  traffic.forEach(car=>{
   car.position.z+=movement*3.5;

   if(car.position.z>12){
    car.position.z=-180-Math.random()*150;
    car.position.x=[-4.2,0,4.2][Math.floor(Math.random()*3)];
    score+=10;
   }

   const dx=Math.abs(car.position.x-bike.position.x);
   const dz=Math.abs(car.position.z);

   if(dx<1.25&&dz<1.9&&velocity>10){
    endGame();
   }
  });

  // Exhaust animation
  flames.forEach((f,i)=>{
   f.visible=boosting;
   f.scale.y=0.5+Math.random()*1.2;
   f.material=flameMaterial;
  });

  headLight.intensity=60+normalized*60;

  distance+=velocity*dt*0.12;
  score+=Math.floor(velocity*dt*0.2);

  document.getElementById("speed").textContent=
   Math.floor(velocity*3.4)+" KM/H";
  document.getElementById("dist").textContent=
   Math.floor(distance)+" M";
  document.getElementById("score").textContent=
   String(score).padStart(4,"0");
  document.getElementById("fill").style.width=nitro+"%";
 }

 // Camera follow
 cameraTarget.set(
  bike.position.x*0.5,
  3.5+velocity*0.006,
  7.5+velocity*0.015
 );

 camera.position.lerp(cameraTarget,0.07);
 camera.lookAt(bike.position.x*0.55,1.2,-9);

 // Slight cinematic camera shake at speed
 camera.position.x+=Math.sin(time*18)*0.008*(velocity/80);

 redLight.intensity=35+Math.sin(time*3)*10;

 renderer.render(scene,camera);
}

animate();

window.addEventListener("resize",()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VENOM NYC | 3D NIGHT RIDER</title>

<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#020308;color:white;font-family:Arial}
canvas{display:block}
#hud{position:absolute;top:20px;left:25px;right:25px;
display:flex;justify-content:space-between;pointer-events:none}
.logo{font-size:25px;font-weight:1000;letter-spacing:5px}
.logo span{color:#e92348;text-shadow:0 0 20px red}
.stats{display:flex;gap:25px}
.stat{font-size:10px;letter-spacing:3px;color:#aaa}
.stat b{display:block;font-size:23px;color:white;margin-top:6px}
#nitro{position:absolute;bottom:25px;left:50%;transform:translateX(-50%);
width:220px;text-align:center;letter-spacing:4px;font-size:10px}
#bar{height:7px;background:#444;margin-top:9px}
#fill{height:100%;width:100%;background:linear-gradient(90deg,#f13,#ffb000);
box-shadow:0 0 15px red}
.overlay{position:absolute;inset:0;display:flex;align-items:center;
justify-content:center;flex-direction:column;text-align:center;
background:radial-gradient(ellipse,#111827aa,#020308ee);z-index:5}
.hidden{display:none!important}
h1{font-size:clamp(48px,9vw,105px);font-weight:1000;
font-style:italic;letter-spacing:-5px;text-shadow:0 0 35px #f13}
h1 span{color:#f13}
.subtitle{font-size:11px;letter-spacing:7px;color:#aaa;margin:15px}
button{padding:17px 48px;background:#e92348;border:0;color:white;
font-weight:900;letter-spacing:4px;cursor:pointer;margin-top:25px;
box-shadow:0 0 30px #e9234877}
button:hover{background:white;color:#e92348}
#help{position:absolute;bottom:25px;left:25px;font-size:10px;
color:#aaa;letter-spacing:2px;line-height:2}
#mobile{position:absolute;bottom:90px;width:100%;display:none;
justify-content:space-between;padding:15px;pointer-events:none}
.pad{display:flex;gap:10px}
.pad button{pointer-events:auto;width:58px;height:58px;padding:0;
border-radius:50%;margin:0;background:#111c;border:1px solid #fff6}
@media(max-width:700px){
#mobile{display:flex}
.stats{gap:10px}.stat b{font-size:16px}
.logo{font-size:17px}#help{display:none}
}
</style>
</head>

<body>

<div id="hud">
 <div class="logo">VENOM <span>NYC</span></div>
 <div class="stats">
  <div class="stat">SPEED<b id="speed">000</b></div>
  <div class="stat">DISTANCE<b id="dist">0 M</b></div>
  <div class="stat">SCORE<b id="score">0000</b></div>
 </div>
</div>

<div id="nitro">
 NITRO BOOST
 <div id="bar"><div id="fill"></div></div>
</div>

<div id="help">
 W / ↑ : ACCELERATE<br>
 S / ↓ : BRAKE<br>
 A / D : STEER<br>
 SHIFT : NITRO
</div>

<div id="mobile">
 <div class="pad">
  <button id="left">◀</button>
  <button id="right">▶</button>
 </div>
 <div class="pad">
  <button id="brake">▼</button>
  <button id="boost">⚡</button>
 </div>
</div>

<div class="overlay" id="start">
 <h1>VENOM <span>NYC</span></h1>
 <div class="subtitle">THE CITY NEVER SLEEPS</div>
 <p style="color:#aaa;font-size:11px;letter-spacing:3px">
  3D SUPERBIKE EXPERIENCE
 </p>
 <button onclick="startGame()">START RIDING</button>
</div>

<div class="overlay hidden" id="gameover">
 <h1>RIDE <span>OVER</span></h1>
 <p class="subtitle">YOUR CITY RUN HAS ENDED</p>
 <h2 id="final">SCORE: 0</h2>
 <button onclick="startGame()">RIDE AGAIN</button>
</div>

<script type="importmap">
{
 "imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"
 }
}
</script>

<script type="module">
import * as THREE from "three";

// ===================================
// VENOM NYC - 3D GAME ENGINE
// ===================================

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x030611);
scene.fog = new THREE.FogExp2(0x080c18,0.012);

const camera = new THREE.PerspectiveCamera(
 65,innerWidth/innerHeight,0.1,1000
);
camera.position.set(0,5,10);

const renderer = new THREE.WebGLRenderer({
 antialias:true, powerPreference:"high-performance"
});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.3;
document.body.appendChild(renderer.domElement);

// ===================================
// LIGHTING
// ===================================

scene.add(new THREE.HemisphereLight(0x8799c8,0x101018,2));

const moon = new THREE.DirectionalLight(0x9dbaff,2.5);
moon.position.set(-10,20,10);
moon.castShadow=true;
scene.add(moon);

const redLight = new THREE.PointLight(0xff123c,45,30);
redLight.position.set(0,3,-8);
scene.add(redLight);

const blueLight = new THREE.PointLight(0x164cff,30,25);
blueLight.position.set(8,4,-12);
scene.add(blueLight);

// ===================================
// MATERIALS
// ===================================

const black = new THREE.MeshStandardMaterial({
 color:0x090b10,metalness:0.9,roughness:0.24
});
const darkMetal = new THREE.MeshStandardMaterial({
 color:0x202631,metalness:0.85,roughness:0.3
});
const red = new THREE.MeshStandardMaterial({
 color:0xff173b,metalness:0.65,roughness:0.25,
 emissive:0x550012,emissiveIntensity:1
});
const chrome = new THREE.MeshStandardMaterial({
 color:0xaaaaaf,metalness:0.95,roughness:0.15
});
const eyeMat = new THREE.MeshStandardMaterial({
 color:0xffffff,emissive:0xffffff,emissiveIntensity:2
});
const tire = new THREE.MeshStandardMaterial({
 color:0x050507,roughness:0.9
});

// ===================================
// HELPER FUNCTIONS
// ===================================

function box(parent,x,y,z,sx,sy,sz,mat){
 const m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),mat);
 m.position.set(x,y,z);
 m.castShadow=true;
 m.receiveShadow=true;
 parent.add(m);
 return m;
}

function sphere(parent,x,y,z,sx,sy,sz,mat){
 const m=new THREE.Mesh(
  new THREE.SphereGeometry(1,24,16),mat
 );
 m.position.set(x,y,z);
 m.scale.set(sx,sy,sz);
 m.castShadow=true;
 parent.add(m);
 return m;
}

function cylinder(parent,x,y,z,r1,r2,len,mat,rotX=0,rotZ=0){
 const m=new THREE.Mesh(
  new THREE.CylinderGeometry(r1,r2,len,32),mat
 );
 m.position.set(x,y,z);
 m.rotation.set(rotX,0,rotZ);
 m.castShadow=true;
 parent.add(m);
 return m;
}

// ===================================
// NEW YORK CITY
// ===================================

const road = new THREE.Mesh(
 new THREE.PlaneGeometry(20,1000),
 new THREE.MeshStandardMaterial({
  color:0x171a22,metalness:0.25,roughness:0.3
 })
);
road.rotation.x=-Math.PI/2;
road.position.z=-300;
road.receiveShadow=true;
scene.add(road);

// Road lane markings
const stripes=[];
for(let z=20;z>-500;z-=12){
 for(let x of [-2.3,2.3]){
  const s=box(scene,x,0.025,z,0.12,0.025,5,
   new THREE.MeshBasicMaterial({color:0xc9d0dc}));
  stripes.push(s);
 }
}

// City buildings
const buildings=[];
const buildingColors=[
 0x101a2d,0x17243b,0x202335,0x111827,0x24283b
];

function createBuilding(x,z){
 const height=15+Math.random()*55;
 const width=7+Math.random()*7;
 const depth=8+Math.random()*8;

 const group=new THREE.Group();
 group.position.set(x,height/2-0.2,z);
 scene.add(group);

 const material=new THREE.MeshStandardMaterial({
  color:buildingColors[Math.floor(Math.random()*buildingColors.length)],
  metalness:0.4,roughness:0.8
 });

 box(group,0,0,0,width,height,depth,material);

 // Windows
 const windowMat=new THREE.MeshBasicMaterial({
  color:Math.random()>0.5?0xffca72:0x4d87c9
 });

 for(let y=-height/2+2;y<height/2-1;y+=3){
  for(let wx=-width/2+1;wx<width/2-1;wx+=2){
   if(Math.random()>0.24){
    box(group,wx,y,depth/2+0.015,
     0.75,1.15,0.04,windowMat);
   }
  }
 }

 // Roof structures
 box(group,0,height/2+1,0,width*0.3,2,depth*0.3,darkMetal);

 buildings.push(group);
}

for(let z=-30;z>-500;z-=24){
 createBuilding(-16-Math.random()*5,z);
 createBuilding(16+Math.random()*5,z);
}

// Street lights
const streetLights=[];
for(let z=10;z>-500;z-=32){
 for(let side of [-1,1]){
  const g=new THREE.Group();
  g.position.set(side*8,0,z);
  scene.add(g);

  cylinder(g,0,3,0,0.12,0.12,6,chrome);
  box(g,side*-0.8,5.9,0,1.8,0.12,0.15,darkMetal);

  const lamp=new THREE.PointLight(
   side===-1?0xff304b:0x498aff,8,15
  );
  lamp.position.set(-side*1.3,5.6,0);
  g.add(lamp);

  sphere(g,-side*1.3,5.6,0,0.25,0.1,0.25,eyeMat);
  streetLights.push(g);
 }
}

// ===================================
// MOTORCYCLE
// ===================================

const bike=new THREE.Group();
scene.add(bike);

// Main frame
box(bike,0,0.82,0,0.42,0.22,2.15,darkMetal);

// Engine
sphere(bike,0,0.72,0.2,0.52,0.48,0.58,black);

// Side fairings
sphere(bike,-0.38,0.92,-0.35,0.18,0.42,0.78,red);
sphere(bike,0.38,0.92,-0.35,0.18,0.42,0.78,red);

// Front nose
sphere(bike,0,1.13,-1.05,0.4,0.36,0.72,black);

// Fuel tank
sphere(bike,0,1.28,-0.15,0.43,0.33,0.55,darkMetal);

// Rear body
sphere(bike,0,1.04,0.8,0.38,0.28,0.58,red);

// Seat
box(bike,0,1.35,0.55,0.5,0.13,0.65,black);

// Windshield
const wind=new THREE.Mesh(
 new THREE.SphereGeometry(0.42,24,16,0,Math.PI*2,0,Math.PI/2),
 new THREE.MeshPhysicalMaterial({
  color:0x263d5a,transparent:true,opacity:0.6,
  metalness:0.5,roughness:0.1
 })
);
wind.position.set(0,1.45,-0.88);
wind.scale.set(1,0.7,1);
bike.add(wind);

// Headlight
const headlamp=sphere(bike,0,1.13,-1.62,0.24,0.13,0.06,eyeMat);
const headLight=new THREE.SpotLight(0xc9e5ff,90,80,0.4,0.6,1);
headLight.position.set(0,1.2,-1.5);
headLight.target.position.set(0,0,-15);
bike.add(headLight,headLight.target);

// Venom eyes on front fairing
for(let side of [-1,1]){
 const eye=sphere(bike,side*0.22,1.33,-1.48,
  0.15,0.055,0.045,eyeMat);
 eye.rotation.z=side*0.3;
}

// Exhaust
for(let side of [-1,1]){
 cylinder(bike,side*0.32,0.66,1.25,
  0.09,0.12,0.8,chrome,Math.PI/2);
}

// Wheels
const wheels=[];
for(let z of [-1.25,1.25]){
 const wheel=new THREE.Group();
 wheel.position.set(0,0.46,z);
 bike.add(wheel);

 const rubber=cylinder(wheel,0,0,0,0.46,0.46,0.23,tire,
  Math.PI/2);
 rubber.rotation.z=Math.PI/2;

 const rim=cylinder(wheel,0,0,0,0.3,0.3,0.25,chrome,
  Math.PI/2);
 rim.rotation.z=Math.PI/2;

 cylinder(wheel,0,0,0,0.12,0.12,0.27,red,Math.PI/2);

 for(let i=0;i<6;i++){
  const a=i*Math.PI/3;
  const spoke=box(wheel,
   Math.cos(a)*0.19,Math.sin(a)*0.19,0,
   0.035,0.035,0.38,chrome);
  spoke.rotation.z=a;
 }

 wheels.push(wheel);
}

// Front forks
for(let side of [-1,1]){
 const fork=cylinder(bike,side*0.17,0.76,-1.25,
  0.045,0.045,1.25,chrome);
 fork.rotation.x=0.18;
}

// ===================================
// VENOM-INSPIRED RIDER
// ===================================

const rider=new THREE.Group();
bike.add(rider);

// Torso
sphere(rider,0,1.85,0.15,0.34,0.55,0.27,black);

// Chest armor
sphere(rider,0,2.02,0.02,0.38,0.32,0.3,darkMetal);

// Neck
cylinder(rider,0,2.38,0.12,0.12,0.13,0.2,black);

// Head / helmet
sphere(rider,0,2.63,-0.15,0.32,0.38,0.32,black);

// White venom eyes
for(let side of [-1,1]){
 const eye=sphere(rider,side*0.17,2.7,-0.435,
  0.13,0.075,0.035,eyeMat);
 eye.rotation.z=side*-0.3;
}

// Helmet forehead details
sphere(rider,0,2.91,-0.3,0.2,0.08,0.1,red);

// Arms
const arms=[];
for(let side of [-1,1]){
 const arm=new THREE.Group();
 arm.position.set(side*0.28,2.1,0.05);
 rider.add(arm);

 const upper=cylinder(arm,side*0.18,-0.13,-0.17,
  0.11,0.15,0.52,black);
 upper.rotation.x=-0.7;
 upper.rotation.z=side*0.35;

 sphere(arm,side*0.35,-0.33,-0.38,
  0.12,0.12,0.13,red);

 const fore=cylinder(arm,side*0.38,-0.39,-0.55,
  0.095,0.12,0.55,darkMetal);
 fore.rotation.x=-0.7;
 fore.rotation.z=side*0.2;

 sphere(arm,side*0.39,-0.58,-0.77,
  0.12,0.1,0.13,black);

 arms.push(arm);
}

// Legs
for(let side of [-1,1]){
 const leg=new THREE.Group();
 leg.position.set(side*0.2,1.65,0.35);
 rider.add(leg);

 const thigh=cylinder(leg,side*0.08,-0.25,0.1,
  0.16,0.19,0.6,black);
 thigh.rotation.x=-0.7;

 const boot=sphere(leg,side*0.12,-0.58,-0.3,
  0.13,0.13,0.3,darkMetal);
}

// ===================================
// NITRO FLAMES
// ===================================

const flames=[];
const flameMaterial=new THREE.MeshBasicMaterial({
 color:0xff4a09,transparent:true,opacity:0.85
});

for(let side of [-1,1]){
 const flame=new THREE.Mesh(
  new THREE.ConeGeometry(0.12,1.5,12),flameMaterial
 );
 flame.position.set(side*0.31,0.7,1.9);
 flame.rotation.x=-Math.PI/2;
 flame.scale.set(1,1,1);
 bike.add(flame);
 flames.push(flame);
}

// ===================================
// TRAFFIC
// ===================================

const traffic=[];
const carColors=[0x202c46,0x9c172e,0xb5b5bd,0x121212];

function createCar(){
 const car=new THREE.Group();
 const color=new THREE.MeshStandardMaterial({
  color:carColors[Math.floor(Math.random()*carColors.length)],
  metalness:0.65,roughness:0.3
 });

 box(car,0,0.65,0,1.5,0.85,2.6,color);
 box(car,0,1.2,-0.1,1.25,0.55,1.2,darkMetal);

 for(let side of [-1,1]){
  for(let z of [-0.8,0.8]){
   const light=sphere(car,side*0.45,0.7,z<0?-1.32:1.32,
    0.16,0.1,0.05,z<0?eyeMat:red);
  }
 }

 car.position.set([-4.2,0,4.2][Math.floor(Math.random()*3)],
  0,-150-Math.random()*200);

 scene.add(car);
 traffic.push(car);
}

for(let i=0;i<8;i++) createCar();

// ===================================
// GAME STATE
// ===================================

let running=false;
let velocity=0;
let distance=0;
let score=0;
let nitro=100;
let lane=0;
let lean=0;
let time=0;

const keys={};

document.addEventListener("keydown",e=>{
 keys[e.key.toLowerCase()]=true;
 if(["arrowup","arrowdown"," "].includes(e.key.toLowerCase()))
  e.preventDefault();
});

document.addEventListener("keyup",e=>{
 keys[e.key.toLowerCase()]=false;
});

function bindButton(id,key){
 const el=document.getElementById(id);
 el.addEventListener("pointerdown",e=>{
  e.preventDefault();
  keys[key]=true;
 });
 ["pointerup","pointercancel","pointerleave"].forEach(event=>{
  el.addEventListener(event,()=>keys[key]=false);
 });
}

bindButton("left","a");
bindButton("right","d");
bindButton("brake","s");
bindButton("boost","shift");

function startGame(){
 running=true;
 velocity=0;
 distance=0;
 score=0;
 nitro=100;
 lane=0;
 bike.position.set(0,0,0);
 bike.rotation.set(0,0,0);

 traffic.forEach((car,i)=>{
  car.position.z=-100-i*65;
  car.position.x=[-4.2,0,4.2][i%3];
 });

 document.getElementById("start").classList.add("hidden");
 document.getElementById("gameover").classList.add("hidden");
}

function endGame(){
 running=false;
 document.getElementById("final").textContent="SCORE: "+score;
 document.getElementById("gameover").classList.remove("hidden");
}

window.startGame=startGame;

// ===================================
// ANIMATION LOOP
// ===================================

const clock=new THREE.Clock();
const cameraTarget=new THREE.Vector3();

function animate(){
 requestAnimationFrame(animate);

 const dt=Math.min(clock.getDelta(),0.04);
 time+=dt;

 if(running){

  const accelerating=keys["w"]||keys["arrowup"];
  const braking=keys["s"]||keys["arrowdown"];
  const boosting=keys["shift"]&&nitro>0;

  if(accelerating) velocity+=22*dt;
  else velocity-=4*dt;

  if(braking) velocity-=30*dt;
  if(boosting){
   velocity+=40*dt;
   nitro-=24*dt;
  }else{
   nitro=Math.min(100,nitro+5*dt);
  }

  velocity=THREE.MathUtils.clamp(velocity,0,boosting?110:80);

  const normalized=velocity/80;
  const movement=velocity*dt*0.12;

  if(keys["a"]||keys["arrowleft"]) lane-=5*dt;
  if(keys["d"]||keys["arrowright"]) lane+=5*dt;

  lane=THREE.MathUtils.clamp(lane,-4.8,4.8);

  bike.position.x=THREE.MathUtils.lerp(
   bike.position.x,lane,dt*5
  );

  lean=THREE.MathUtils.lerp(
   lean,(keys["a"]||keys["arrowleft"])?0.32:
   (keys["d"]||keys["arrowright"])?-0.32:0,dt*5
  );

  bike.rotation.z=lean;
  bike.rotation.x=Math.sin(time*12)*0.012*normalized;

  wheels.forEach(w=>{
   w.rotation.x-=movement*2;
  });

  // Road movement
  stripes.forEach(s=>{
   s.position.z+=movement*3;
   if(s.position.z>20) s.position.z=-500;
  });

  // Buildings
  buildings.forEach(b=>{
   b.position.z+=movement*2;
   if(b.position.z>30) b.position.z=-500;
  });

  streetLights.forEach(l=>{
   l.position.z+=movement*3;
   if(l.position.z>20) l.position.z=-500;
  });

  // Traffic
  traffic.forEach(car=>{
   car.position.z+=movement*3.5;

   if(car.position.z>12){
    car.position.z=-180-Math.random()*150;
    car.position.x=[-4.2,0,4.2][Math.floor(Math.random()*3)];
    score+=10;
   }

   const dx=Math.abs(car.position.x-bike.position.x);
   const dz=Math.abs(car.position.z);

   if(dx<1.25&&dz<1.9&&velocity>10){
    endGame();
   }
  });

  // Exhaust animation
  flames.forEach((f,i)=>{
   f.visible=boosting;
   f.scale.y=0.5+Math.random()*1.2;
   f.material=flameMaterial;
  });

  headLight.intensity=60+normalized*60;

  distance+=velocity*dt*0.12;
  score+=Math.floor(velocity*dt*0.2);

  document.getElementById("speed").textContent=
   Math.floor(velocity*3.4)+" KM/H";
  document.getElementById("dist").textContent=
   Math.floor(distance)+" M";
  document.getElementById("score").textContent=
   String(score).padStart(4,"0");
  document.getElementById("fill").style.width=nitro+"%";
 }

 // Camera follow
 cameraTarget.set(
  bike.position.x*0.5,
  3.5+velocity*0.006,
  7.5+velocity*0.015
 );

 camera.position.lerp(cameraTarget,0.07);
 camera.lookAt(bike.position.x*0.55,1.2,-9);

 // Slight cinematic camera shake at speed
 camera.position.x+=Math.sin(time*18)*0.008*(velocity/80);

 redLight.intensity=35+Math.sin(time*3)*10;

 renderer.render(scene,camera);
}

animate();

window.addEventListener("resize",()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
