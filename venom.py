
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VENOM RIDE | NYC NIGHT RUN</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@400;600;700&display=swap');

*{margin:0;padding:0;box-sizing:border-box}

body{
    overflow:hidden;
    background:#02030a;
    font-family:'Orbitron',sans-serif;
    color:white;
}

canvas{display:block}

#hud{
    position:absolute;
    inset:0;
    pointer-events:none;
    z-index:5;
}

.topbar{
    position:absolute;
    top:25px;
    left:35px;
    right:35px;
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
}

.logo{
    font-size:27px;
    font-weight:900;
    letter-spacing:5px;
    color:#fff;
    text-shadow:0 0 15px #e00040,0 0 30px #e00040;
}

.logo span{color:#ff174f}

.subtitle{
    font-size:9px;
    letter-spacing:5px;
    color:#aaa;
    margin-top:7px;
}

.status{
    text-align:right;
    font-size:11px;
    letter-spacing:2px;
    color:#ff315f;
}

.status small{
    display:block;
    margin-top:8px;
    color:#aaa;
}

.speedbox{
    position:absolute;
    left:40px;
    bottom:35px;
}

.speed{
    font-size:75px;
    font-weight:900;
    color:white;
    text-shadow:0 0 20px #f00048;
    line-height:1;
}

.speed span{
    font-size:18px;
    color:#ff174f;
}

.label{
    font-size:10px;
    letter-spacing:5px;
    color:#aaa;
    margin-top:10px;
}

.stats{
    position:absolute;
    right:40px;
    bottom:40px;
    text-align:right;
    font-size:12px;
    line-height:2.2;
    letter-spacing:2px;
}

.stats strong{color:#ff315f}

.nitro{
    position:absolute;
    left:50%;
    bottom:40px;
    transform:translateX(-50%);
    width:210px;
}

.nitro-title{
    font-size:11px;
    text-align:center;
    letter-spacing:4px;
    margin-bottom:9px;
    color:#ff315f;
}

.nitro-track{
    width:100%;
    height:7px;
    background:#25202b;
    border:1px solid #773047;
    transform:skewX(-20deg);
}

#nitro-fill{
    height:100%;
    width:100%;
    background:linear-gradient(90deg,#ff174f,#ffbd35);
    box-shadow:0 0 15px #ff174f;
    transition:width .1s;
}

#intro{
    position:absolute;
    inset:0;
    z-index:20;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
    background:radial-gradient(ellipse at center,#210813 0%,#05050b 55%,#010207 100%);
    transition:opacity 1s;
}

#intro h1{
    font-size:clamp(45px,9vw,100px);
    font-weight:900;
    letter-spacing:8px;
    color:#fff;
    text-shadow:0 0 20px #ff003c,0 0 65px #ff003c;
}

#intro h1 span{color:#ff174f}

#intro p{
    font-family:'Rajdhani',sans-serif;
    font-size:20px;
    letter-spacing:7px;
    color:#aaa;
    margin-top:12px;
}

.start-btn{
    margin-top:45px;
    padding:17px 55px;
    background:transparent;
    border:1px solid #ff174f;
    color:white;
    font-family:'Orbitron',sans-serif;
    font-size:13px;
    letter-spacing:4px;
    cursor:pointer;
    box-shadow:0 0 20px #ff174f55;
    transition:.3s;
}

.start-btn:hover{
    background:#ff174f;
    box-shadow:0 0 40px #ff174f;
}

#help{
    position:absolute;
    bottom:15px;
    left:50%;
    transform:translateX(-50%);
    font-size:9px;
    letter-spacing:2px;
    color:#777;
    white-space:nowrap;
}

#pause{
    position:absolute;
    top:110px;
    right:40px;
    pointer-events:auto;
    background:#130711aa;
    color:white;
    border:1px solid #ff315f;
    padding:9px 15px;
    font-family:Orbitron;
    cursor:pointer;
    font-size:10px;
}

#flash{
    position:absolute;
    inset:0;
    background:#ff174f;
    opacity:0;
    pointer-events:none;
}

.mobile-controls{
    position:absolute;
    bottom:125px;
    left:20px;
    right:20px;
    display:none;
    justify-content:space-between;
    pointer-events:auto;
}

.mobile-controls button{
    width:65px;
    height:65px;
    border-radius:50%;
    background:#160914aa;
    color:white;
    border:1px solid #ff174f;
    font-size:23px;
}

@media(max-width:700px){
    .topbar{top:15px;left:15px;right:15px}
    .logo{font-size:18px}
    .speedbox{left:18px;bottom:22px}
    .speed{font-size:48px}
    .stats{right:18px;bottom:22px;font-size:9px}
    .nitro{bottom:100px;width:140px}
    #pause{top:75px;right:15px}
    #help{display:none}
    .mobile-controls{display:flex}
}
</style>
</head>

<body>

<div id="hud">
    <div class="topbar">
        <div>
            <div class="logo">VENOM<span> RIDE</span></div>
            <div class="subtitle">NEW YORK // NIGHT RUN</div>
        </div>
        <div class="status">
            <div>● SYSTEM ONLINE</div>
            <small>SYMBIOTE ENGINE V.01</small>
            <small id="mission">MISSION: FREE RIDE</small>
        </div>
    </div>

    <button id="pause">PAUSE</button>

    <div class="speedbox">
        <div class="speed"><span id="speed">000</span><span> KM/H</span></div>
        <div class="label">VELOCITY CONTROL</div>
    </div>

    <div class="nitro">
        <div class="nitro-title">⚡ NITRO POWER</div>
        <div class="nitro-track">
            <div id="nitro-fill"></div>
        </div>
    </div>

    <div class="stats">
        <div>DISTANCE : <strong id="distance">0.00</strong> KM</div>
        <div>BIKE : <strong>SYMBIOTE X</strong></div>
        <div>MODE : <strong id="mode">NORMAL</strong></div>
    </div>

    <div class="mobile-controls">
        <button id="left">◀</button>
        <button id="right">▶</button>
        <button id="boost">⚡</button>
    </div>

    <div id="flash"></div>
</div>

<div id="intro">
    <h1>VENOM <span>RIDE</span></h1>
    <p>THE CITY IS YOURS. OWN THE NIGHT.</p>
    <button class="start-btn" id="start">START ENGINE</button>
    <div id="help">W / ↑ ACCELERATE &nbsp; | &nbsp; A / D STEER &nbsp; | &nbsp; SHIFT NITRO</div>
</div>

<script type="importmap">
{
 "imports":{
   "three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"
 }
}
</script>

<script type="module">
import * as THREE from 'three';

/* ---------------- SCENE ---------------- */

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x030611);
scene.fog = new THREE.FogExp2(0x080c1c,0.008);

const camera = new THREE.PerspectiveCamera(
    65,window.innerWidth/window.innerHeight,0.1,3000
);

camera.position.set(0,5,10);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    powerPreference:"high-performance"
});

renderer.setSize(window.innerWidth,window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.7));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.25;

document.body.appendChild(renderer.domElement);

/* ---------------- LIGHTS ---------------- */

scene.add(new THREE.HemisphereLight(0x8295ff,0x080414,2));

const moon = new THREE.DirectionalLight(0x9caaff,2.5);
moon.position.set(-30,70,30);
moon.castShadow=true;
scene.add(moon);

const redLight = new THREE.PointLight(0xff003c,45,45);
redLight.position.set(0,5,-12);
scene.add(redLight);

const blueLight = new THREE.PointLight(0x143cff,35,60);
blueLight.position.set(10,12,-25);
scene.add(blueLight);

/* ---------------- MATERIALS ---------------- */

const roadMat = new THREE.MeshStandardMaterial({
    color:0x151923,roughness:0.85
});

const black = new THREE.MeshStandardMaterial({
    color:0x05060b,metalness:0.8,roughness:0.25
});

const red = new THREE.MeshStandardMaterial({
    color:0xff003f,emissive:0xff003f,emissiveIntensity:2
});

const silver = new THREE.MeshStandardMaterial({
    color:0x929aaa,metalness:0.95,roughness:0.2
});

const white = new THREE.MeshStandardMaterial({
    color:0xffffff,emissive:0xaaaaee,emissiveIntensity:2
});

const buildingMaterials=[
    0x10182b,0x151626,0x1b2032,0x20263b,0x121e2d
].map(c=>new THREE.MeshStandardMaterial({
    color:c,metalness:0.25,roughness:0.8
}));

/* ---------------- CITY ---------------- */

const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(100,5000),roadMat
);
floor.rotation.x=-Math.PI/2;
floor.position.set(0,-0.15,-2000);
scene.add(floor);

const road = new THREE.Mesh(
    new THREE.PlaneGeometry(18,5000),
    new THREE.MeshStandardMaterial({color:0x080b13,roughness:0.9})
);
road.rotation.x=-Math.PI/2;
road.position.set(0,-0.1,-2000);
scene.add(road);

// Sidewalks
for(const x of [-10,10]){
    const sidewalk=new THREE.Mesh(
        new THREE.BoxGeometry(3,0.25,5000),
        new THREE.MeshStandardMaterial({color:0x30313b})
    );
    sidewalk.position.set(x,0,-2000);
    scene.add(sidewalk);
}

// Lane lines
for(let z=30;z>-4900;z-=20){
    for(const x of [-3,3]){
        const line=new THREE.Mesh(
            new THREE.BoxGeometry(.12,.025,8),
            new THREE.MeshBasicMaterial({color:0xe1e3f1})
        );
        line.position.set(x,0.02,z);
        scene.add(line);
    }
}

// City buildings
function createBuilding(x,z){
    const h=THREE.MathUtils.randFloat(15,65);
    const w=THREE.MathUtils.randFloat(7,13);
    const d=THREE.MathUtils.randFloat(12,23);

    const group=new THREE.Group();

    const body=new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d),
        buildingMaterials[Math.floor(Math.random()*buildingMaterials.length)]
    );
    body.position.y=h/2;
    body.castShadow=true;
    group.add(body);

    // Glowing window rows
    const windowMat=new THREE.MeshBasicMaterial({
        color:Math.random()>.5?0xffbd72:0x6b91ff
    });

    for(let y=2;y<h-2;y+=3.5){
        for(let wx=-w/2+1;wx<w/2;wx+=2.3){
            const win=new THREE.Mesh(
                new THREE.PlaneGeometry(0.8,1.3),windowMat
            );
            win.position.set(wx,y,d/2+0.015);
            group.add(win);

            const back=new THREE.Mesh(
                new THREE.PlaneGeometry(0.8,1.3),windowMat
            );
            back.position.set(wx,y,-d/2-0.015);
            back.rotation.y=Math.PI;
            group.add(back);
        }
    }

    group.position.set(x,0,z);
    scene.add(group);
}

for(let z=20;z>-4800;z-=35){
    createBuilding(-19- Math.random()*8,z);
    createBuilding(19+ Math.random()*8,z);
}

// Streetlights
for(let z=10;z>-4800;z-=55){
    for(const x of [-9,9]){
        const pole=new THREE.Mesh(
            new THREE.CylinderGeometry(.08,.12,7,8),
            silver
        );
        pole.position.set(x,3.5,z);
        scene.add(pole);

        const lamp=new THREE.PointLight(0xffa35c,10,18);
        lamp.position.set(x,7,z);
        scene.add(lamp);

        const bulb=new THREE.Mesh(
            new THREE.SphereGeometry(.2,10,10),
            new THREE.MeshBasicMaterial({color:0xffc17a})
        );
        bulb.position.set(x,7,z);
        scene.add(bulb);
    }
}

/* ---------------- VENOM BIKE ---------------- */

const bike=new THREE.Group();
scene.add(bike);

function box(parent,x,y,z,sx,sy,sz,mat){
    const m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),mat);
    m.position.set(x,y,z);
    m.castShadow=true;
    parent.add(m);
    return m;
}

function cylinder(parent,x,y,z,r1,r2,length,mat,rotZ=0){
    const m=new THREE.Mesh(
        new THREE.CylinderGeometry(r1,r2,length,24),mat
    );
    m.position.set(x,y,z);
    m.rotation.z=rotZ;
    m.castShadow=true;
    parent.add(m);
    return m;
}

// Wheels
const wheels=[];

function makeWheel(z){
    const wheel=new THREE.Group();

    const tire=new THREE.Mesh(
        new THREE.TorusGeometry(.52,.16,16,40),
        new THREE.MeshStandardMaterial({color:0x050505,roughness:.9})
    );
    tire.rotation.y=Math.PI/2;
    wheel.add(tire);

    const rim=new THREE.Mesh(
        new THREE.TorusGeometry(.36,.045,10,32),
        red
    );
    rim.rotation.y=Math.PI/2;
    wheel.add(rim);

    const hub=new THREE.Mesh(
        new THREE.CylinderGeometry(.12,.12,.45,24),
        silver
    );
    hub.rotation.z=Math.PI/2;
    wheel.add(hub);

    wheel.position.set(0,.65,z);
    bike.add(wheel);
    wheels.push(wheel);
}

makeWheel(-1.35);
makeWheel(1.2);

// Chassis
box(bike,0,1.0,0,0.65,.35,1.7,black);

// Fuel tank
const tank=new THREE.Mesh(
    new THREE.SphereGeometry(1,32,24),
    black
);
tank.scale.set(.55,.4,.78);
tank.position.set(0,1.4,-.35);
bike.add(tank);

// Sharp body panels
const panel=box(bike,0,1.1,-.7,.95,.25,.75,red);
panel.rotation.x=-.1;

box(bike,0,1.1,.55,.75,.32,.65,black);

// Front forks
for(const x of [-.24,.24]){
    cylinder(bike,x,1.2,-1.15,.065,.065,1.2,silver);
}

// Handlebar
cylinder(bike,0,1.75,-1.0,.055,.055,.9,silver,Math.PI/2);

for(const x of [-.5,.5]){
    cylinder(bike,x,1.75,-1,.09,.09,.3,black,Math.PI/2);
}

// Front headlight
const headlight=new THREE.Mesh(
    new THREE.SphereGeometry(.22,20,20),
    white
);
headlight.scale.set(1.5,.65,.4);
headlight.position.set(0,1.55,-1.22);
bike.add(headlight);

const headBeam=new THREE.SpotLight(0xc4d5ff,90,80,.5,.6,1);
headBeam.position.set(0,1.6,-1.3);
headBeam.target.position.set(0,0,-30);
bike.add(headBeam);
bike.add(headBeam.target);

// Red rear lights
box(bike,0,1.25,1.15,.42,.12,.12,red);

// Exhaust pipes
for(const x of [-.38,.38]){
    cylinder(bike,x,.85,.65,.08,.11,.8,silver,Math.PI/2);
}

/* ---------------- RIDER ---------------- */

const rider=new THREE.Group();
bike.add(rider);

// Rider body
const torso=new THREE.Mesh(
    new THREE.CylinderGeometry(.28,.38,.85,12),
    black
);
torso.position.set(0,2.05,.12);
torso.rotation.x=-.35;
rider.add(torso);

// Shoulders
for(const x of [-.38,.38]){
    const shoulder=new THREE.Mesh(
        new THREE.SphereGeometry(.27,16,16),
        black
    );
    shoulder.position.set(x,2.35,.12);
    rider.add(shoulder);
}

// Arms
for(const x of [-.38,.38]){
    const arm=new THREE.Mesh(
        new THREE.CylinderGeometry(.11,.15,.8,12),
        black
    );
    arm.position.set(x*1.5,2.0,-.35);
    arm.rotation.z=x>0?-.3:.3;
    arm.rotation.x=-.8;
    rider.add(arm);
}

// Gloves
for(const x of [-.58,.58]){
    const glove=new THREE.Mesh(
        new THREE.SphereGeometry(.13,12,12),
        red
    );
    glove.position.set(x,1.72,-.9);
    rider.add(glove);
}

// Legs
for(const x of [-.22,.22]){
    const leg=new THREE.Mesh(
        new THREE.CylinderGeometry(.13,.19,.85,12),
        black
    );
    leg.position.set(x,1.1,.4);
    leg.rotation.x=-.45;
    rider.add(leg);

    const boot=new THREE.Mesh(
        new THREE.BoxGeometry(.22,.18,.42),
        silver
    );
    boot.position.set(x, .75,.0);
    rider.add(boot);
}

// Helmet
const helmet=new THREE.Mesh(
    new THREE.SphereGeometry(.34,32,24),
    black
);
helmet.scale.set(1,.95,1.1);
helmet.position.set(0,2.72,-.05);
rider.add(helmet);

// Glowing white superhero eyes
for(const x of [-.16,.16]){
    const eye=new THREE.Mesh(
        new THREE.SphereGeometry(.11,16,12),
        white
    );
    eye.scale.set(1.4,.65,.35);
    eye.position.set(x,2.78,-.35);
    eye.rotation.z=x>0?-.2:.2;
    rider.add(eye);
}

// Red helmet web-inspired lines
for(let i=-2;i<=2;i++){
    const web=new THREE.Mesh(
        new THREE.BoxGeometry(.025,.55,.025),red
    );
    web.position.set(i*.09,2.73,.23);
    rider.add(web);
}

// Symbiote tendrils
for(let i=0;i<4;i++){
    const curve=new THREE.CatmullRomCurve3([
        new THREE.Vector3(i%2?.3:-.3,2.3,.1),
        new THREE.Vector3(i%2?.65:-.65,2.55,.25),
        new THREE.Vector3(i%2?.8:-.8,2.25,.45)
    ]);

    const tendril=new THREE.Mesh(
        new THREE.TubeGeometry(curve,20,.035,8,false),
        red
    );
    rider.add(tendril);
}

/* ---------------- TRAFFIC ---------------- */

const cars=[];

function makeCar(z){
    const car=new THREE.Group();
    const color=[0x171d2c,0x222631,0x331522,0x101d28][
        Math.floor(Math.random()*4)
    ];

    box(car,0,.65,0,1.6,.7,3,
        new THREE.MeshStandardMaterial({
            color,metalness:.65,roughness:.3
        })
    );

    box(car,0,1.12,-.1,1.3,.48,1.5,
        new THREE.MeshStandardMaterial({
            color:0x131c2a,metalness:.7
        })
    );

    for(const x of [-.5,.5]){
        for(const zz of [-1.1,1.1]){
            const light=box(car,x,.65,zz,.18,.15,.08,red);
        }
    }

    for(const x of [-.9,.9]){
        for(const zz of [-.9,.9]){
            const tire=new THREE.Mesh(
                new THREE.CylinderGeometry(.27,.27,.15,16),
                black
            );
            tire.rotation.z=Math.PI/2;
            tire.position.set(x,.35,zz);
            car.add(tire);
        }
    }

    car.position.set(
        THREE.MathUtils.randFloat(-5,5),0,z
    );
    scene.add(car);
    cars.push(car);
}

for(let i=0;i<12;i++) makeCar(-100-i*90);

/* ---------------- PARTICLES ---------------- */

const particleGeometry=new THREE.BufferGeometry();
const particlePositions=new Float32Array(600);

for(let i=0;i<600;i++){
    particlePositions[i]=(Math.random()-.5)*35;
}

particleGeometry.setAttribute(
    'position',
    new THREE.BufferAttribute(particlePositions,3)
);

const particles=new THREE.Points(
    particleGeometry,
    new THREE.PointsMaterial({
        color:0x899bff,size:.09,transparent:true,opacity:.55
    })
);
scene.add(particles);

/* ---------------- GAME CONTROLS ---------------- */

const keys={};
let started=false;
let paused=false;
let speed=0;
let distance=0;
let nitro=100;
let boost=false;
let lastTime=0;
let cameraShake=0;
let steer=0;

window.addEventListener('keydown',e=>{
    keys[e.key.toLowerCase()]=true;

    if(e.key==="Shift") boost=true;
    if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(e.key))
        e.preventDefault();
});

window.addEventListener('keyup',e=>{
    keys[e.key.toLowerCase()]=false;
    if(e.key==="Shift") boost=false;
});

function holdButton(id,key){
    const el=document.getElementById(id);
    el.addEventListener('pointerdown',e=>{
        e.preventDefault();
        keys[key]=true;
        if(key==="shift") boost=true;
    });
    ['pointerup','pointerleave','pointercancel'].forEach(ev=>{
        el.addEventListener(ev,()=>{
            keys[key]=false;
            if(key==="shift") boost=false;
        });
    });
}

holdButton('left','a');
holdButton('right','d');
holdButton('boost','shift');

document.getElementById('start').onclick=()=>{
    started=true;
    document.getElementById('intro').style.opacity=0;
    setTimeout(()=>{
        document.getElementById('intro').style.display='none';
    },1000);
};

document.getElementById('pause').onclick=()=>{
    paused=!paused;
    document.getElementById('pause').textContent=
        paused?'RESUME':'PAUSE';
};

/* ---------------- ANIMATION ---------------- */

const clock=new THREE.Clock();

function animate(){
    requestAnimationFrame(animate);

    const dt=Math.min(clock.getDelta(),.035);
    const t=clock.elapsedTime;

    if(!started || paused){
        renderer.render(scene,camera);
        return;
    }

    const accelerating=keys['w']||keys['arrowup'];
    const braking=keys['s']||keys['arrowdown'];
    const left=keys['a']||keys['arrowleft'];
    const right=keys['d']||keys['arrowright'];

    if(accelerating) speed+=45*dt;
    else speed-=12*dt;

    if(braking) speed-=65*dt;

    speed=THREE.MathUtils.clamp(speed,0,320);

    const usingNitro=boost&&nitro>0;

    if(usingNitro){
        speed=Math.min(380,speed+95*dt);
        nitro=Math.max(0,nitro-30*dt);
        cameraShake=.12;
    }else{
        nitro=Math.min(100,nitro+9*dt);
    }

    steer+=(Number(right)-Number(left)-steer)*Math.min(1,dt*7);

    const move=speed/3.6*dt;

    bike.position.x+=steer*move*1.5;
    bike.position.x=THREE.MathUtils.clamp(bike.position.x,-6.2,6.2);

    // Ride forward
    bike.position.z-=move;

    // Wheel rotation
    wheels.forEach(w=>w.rotation.x+=move*1.8);

    // Bike leaning
    bike.rotation.z=THREE.MathUtils.lerp(
        bike.rotation.z,-steer*.35,dt*5
    );

    bike.rotation.x=Math.sin(t*5)*.008*(speed/100);

    // Rider body motion
    rider.rotation.z=THREE.MathUtils.lerp(
        rider.rotation.z,-steer*.12,dt*4
    );

    // Speed particles
    particles.position.z=bike.position.z-20;
    particles.rotation.z=t*.03;

    // Camera follow
    const targetCamera=new THREE.Vector3(
        bike.position.x*.55,
        4.3+speed*.002,
        bike.position.z+9.5
    );

    camera.position.lerp(targetCamera,dt*3.5);

    const lookTarget=new THREE.Vector3(
        bike.position.x*.45,
        1.5,
        bike.position.z-9
    );

    camera.lookAt(lookTarget);

    if(usingNitro){
        camera.fov=THREE.MathUtils.lerp(camera.fov,79,dt*3);
        redLight.intensity=75;
    }else{
        camera.fov=THREE.MathUtils.lerp(camera.fov,65,dt*2);
        redLight.intensity=45;
    }

    camera.updateProjectionMatrix();

    // Traffic moves toward the player
    cars.forEach(car=>{
        car.position.z+=move*1.05;

        if(car.position.z>bike.position.z+25){
            car.position.z=bike.position.z-450-Math.random()*250;
            car.position.x=THREE.MathUtils.randFloat(-5,5);
        }

        const dx=Math.abs(car.position.x-bike.position.x);
        const dz=Math.abs(car.position.z-bike.position.z);

        if(dx<1.3&&dz<2.2&&speed>15){
            speed*=.55;
            cameraShake=.6;
            document.getElementById('flash').style.opacity='.25';
        }
    });

    cameraShake=Math.max(0,cameraShake-dt*1.5);

    if(cameraShake>0){
        camera.position.x+=(Math.random()-.5)*cameraShake;
        camera.position.y+=(Math.random()-.5)*cameraShake;
    }

    distance+=move/1000;

    document.getElementById('speed').textContent=
        Math.round(speed).toString().padStart(3,'0');

    document.getElementById('distance').textContent=
        distance.toFixed(2);

    document.getElementById('nitro-fill').style.width=
        nitro+'%';

    document.getElementById('mode').textContent=
        usingNitro?'NITRO':'NORMAL';

    document.getElementById('flash').style.opacity=
        Math.max(0,Number(
            document.getElementById('flash').style.opacity||0
        )-dt*1.5);

    renderer.render(scene,camera);
}

/* ---------------- RESIZE ---------------- */

window.addEventListener('resize',()=>{
    camera.aspect=window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
});

animate();

</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
