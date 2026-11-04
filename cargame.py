
from flask import Flask
from flask import Response

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>APEX | Supercar Racing</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background: #050711;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#game {
    position: fixed;
    inset: 0;
}

canvas {
    display: block;
    width: 100%;
    height: 100%;
}

.hud {
    position: fixed;
    inset: 0;
    z-index: 5;
    pointer-events: none;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 35px;
}

.brand {
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 7px;
}

.brand span {
    color: #00e5ff;
}

.level {
    text-align: right;
    font-size: 11px;
    letter-spacing: 3px;
    color: #00e5ff;
}

.level strong {
    display: block;
    font-size: 22px;
    color: white;
    margin-top: 5px;
}

.stats {
    position: absolute;
    top: 105px;
    left: 35px;
    display: flex;
    gap: 12px;
}

.stat {
    min-width: 105px;
    padding: 13px;
    background: #080d1bbd;
    border: 1px solid #ffffff25;
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

.stat small {
    display: block;
    color: #8b9bb5;
    font-size: 9px;
    letter-spacing: 2px;
}

.stat strong {
    display: block;
    font-size: 22px;
    margin-top: 7px;
}

.bottom {
    position: absolute;
    bottom: 30px;
    left: 35px;
    right: 35px;
    display: flex;
    justify-content: space-between;
    align-items: end;
}

.carname {
    font-size: 12px;
    letter-spacing: 4px;
    color: #00e5ff;
    margin-bottom: 7px;
}

.carname strong {
    display: block;
    font-size: 26px;
    letter-spacing: 2px;
    color: white;
}

.progress {
    width: 210px;
    height: 5px;
    margin-top: 12px;
    background: #ffffff30;
    border-radius: 20px;
    overflow: hidden;
}

.progress div {
    height: 100%;
    width: 0%;
    background: #00e5ff;
    transition: width .2s;
}

.controls {
    display: flex;
    gap: 12px;
    pointer-events: auto;
}

.control {
    width: 60px;
    height: 55px;
    border: 1px solid #ffffff55;
    border-radius: 12px;
    background: #10182baf;
    color: white;
    font-size: 24px;
    cursor: pointer;
    touch-action: none;
}

.control:active {
    background: #00bcd4;
}

.overlay {
    position: fixed;
    z-index: 10;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: #030611c9;
    backdrop-filter: blur(9px);
    padding: 20px;
}

.overlay.hide {
    display: none;
}

.panel {
    max-width: 650px;
    width: 100%;
    padding: 35px 25px;
    border: 1px solid #00e5ff50;
    border-radius: 20px;
    background: #0a1022eF;
    box-shadow: 0 0 70px #00d9ff18;
}

.tag {
    color: #00e5ff;
    font-size: 11px;
    letter-spacing: 5px;
    margin-bottom: 20px;
}

h1 {
    font-size: clamp(40px, 9vw, 85px);
    letter-spacing: 7px;
    font-weight: 1000;
}

h1 span {
    color: #00e5ff;
}

.description {
    margin: 20px auto;
    color: #a5b1c9;
    font-size: 13px;
    line-height: 1.8;
    max-width: 450px;
}

button.start {
    padding: 16px 45px;
    border: 0;
    border-radius: 7px;
    background: linear-gradient(90deg, #00e5ff, #007bff);
    color: #001018;
    font-weight: 900;
    letter-spacing: 3px;
    cursor: pointer;
    margin-top: 15px;
}

button.start:hover {
    filter: brightness(1.2);
}

.levelcards {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 22px 0;
    flex-wrap: wrap;
}

.levelcard {
    padding: 12px;
    border: 1px solid #ffffff22;
    border-radius: 9px;
    min-width: 110px;
    font-size: 10px;
    color: #aab5ca;
    letter-spacing: 1px;
}

.levelcard b {
    display: block;
    color: white;
    font-size: 13px;
    margin-bottom: 6px;
}

@media(max-width:650px) {
    .topbar {
        padding: 17px;
    }

    .brand {
        font-size: 15px;
        letter-spacing: 4px;
    }

    .stats {
        top: 85px;
        left: 12px;
        gap: 5px;
    }

    .stat {
        min-width: 75px;
        padding: 8px;
    }

    .stat strong {
        font-size: 17px;
    }

    .bottom {
        left: 15px;
        right: 15px;
        bottom: 18px;
    }

    .carname strong {
        font-size: 16px;
    }

    .progress {
        width: 130px;
    }

    .control {
        width: 48px;
        height: 48px;
    }
}
</style>
</head>

<body>

<div id="game"></div>

<div class="hud">

    <div class="topbar">
        <div class="brand">APEX<span>.</span>RACING</div>
        <div class="level">
            CURRENT LEVEL
            <strong id="level">01 / 03</strong>
        </div>
    </div>

    <div class="stats">
        <div class="stat">
            <small>SPEED</small>
            <strong><span id="speed">0</span> <small>KM/H</small></strong>
        </div>

        <div class="stat">
            <small>DISTANCE</small>
            <strong id="distance">0</strong>
        </div>

        <div class="stat">
            <small>SCORE</small>
            <strong id="score">0</strong>
        </div>
    </div>

    <div class="bottom">
        <div>
            <div class="carname">
                YOUR SUPERCAR
                <strong id="carname">APEX GT</strong>
            </div>
            <div class="progress">
                <div id="progress"></div>
            </div>
        </div>

        <div class="controls">
            <button class="control" id="left">◀</button>
            <button class="control" id="right">▶</button>
        </div>
    </div>

</div>

<div class="overlay" id="overlay">
    <div class="panel">
        <div class="tag">ULTIMATE SUPERCAR EXPERIENCE</div>

        <h1>APEX<span>.</span></h1>

        <div class="description" id="description">
            ENTER THE WORLD OF EXTREME RACING.
            DRIVE THREE SUPERCARS THROUGH SNOW,
            MUD AND HIGH-SPEED HIGHWAYS.
        </div>

        <div class="levelcards">
            <div class="levelcard">
                <b>01 — SNOW</b>
                ICE STORM
            </div>
            <div class="levelcard">
                <b>02 — MUD</b>
                OFF ROAD
            </div>
            <div class="levelcard">
                <b>03 — HIGHWAY</b>
                MAXIMUM SPEED
            </div>
        </div>

        <button class="start" id="start">START ENGINE</button>
        <p style="margin-top:20px;color:#71809c;font-size:10px;letter-spacing:2px">
            W / A / S / D OR ARROW KEYS TO DRIVE
        </p>
    </div>
</div>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>

<script type="module">

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// --------------------------------------------------
// CONFIGURATION
// --------------------------------------------------

const CONFIG = {
    // Add Blender-exported GLB files here when available.
    // Example: '/static/cars/snow_supercar.glb'
    models: [
        '',
        '',
        ''
    ],

    levelThresholds: [0, 500, 1200],

    cars: [
        {
            name: 'APEX GT',
            color: 0x00dfff,
            speed: 180,
            acceleration: 1.0
        },
        {
            name: 'APEX STORM',
            color: 0xff6a00,
            speed: 260,
            acceleration: 1.3
        },
        {
            name: 'APEX HYPER',
            color: 0xc7d2ff,
            speed: 360,
            acceleration: 1.7
        }
    ]
};

// --------------------------------------------------
// THREE JS SCENE
// --------------------------------------------------

const container = document.getElementById('game');

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x101a30);
scene.fog = new THREE.Fog(0x101a30, 35, 150);

const camera = new THREE.PerspectiveCamera(
    65,
    window.innerWidth / window.innerHeight,
    0.1,
    300
);

camera.position.set(0, 5.5, 11);

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    powerPreference: 'high-performance'
});

renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;

container.appendChild(renderer.domElement);

// --------------------------------------------------
// LIGHTING
// --------------------------------------------------

const ambient = new THREE.HemisphereLight(
    0xb8d9ff,
    0x24202a,
    2.0
);

scene.add(ambient);

const sun = new THREE.DirectionalLight(0xffffff, 3);

sun.position.set(-10, 20, 10);
sun.castShadow = true;
scene.add(sun);

const glow = new THREE.PointLight(0x00dfff, 35, 35);
glow.position.set(0, 5, 1);
scene.add(glow);

// --------------------------------------------------
// MATERIALS
// --------------------------------------------------

function material(color, roughness = 0.45, metalness = 0.2) {
    return new THREE.MeshStandardMaterial({
        color,
        roughness,
        metalness
    });
}

const roadMat = material(0x252a35, 0.85);
const snowMat = material(0xe4f2ff, 0.9);
const mudMat = material(0x493021, 0.95);
const grassMat = material(0x263d30);
const lineMat = material(0xf5f5f5);
const wheelMat = material(0x111318, 0.9);
const glassMat = new THREE.MeshPhysicalMaterial({
    color: 0x102d45,
    roughness: 0.12,
    metalness: 0.7,
    transparent: true,
    opacity: 0.88
});

// --------------------------------------------------
// WORLD
// --------------------------------------------------

const world = new THREE.Group();
scene.add(world);

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(200, 250),
    grassMat
);

ground.rotation.x = -Math.PI / 2;
ground.position.set(0, -0.16, -65);
ground.receiveShadow = true;
world.add(ground);

const road = new THREE.Mesh(
    new THREE.PlaneGeometry(12, 250),
    roadMat
);

road.rotation.x = -Math.PI / 2;
road.position.set(0, -0.1, -65);
road.receiveShadow = true;
world.add(road);

// Road boundaries
for (const x of [-6, 6]) {
    const edge = new THREE.Mesh(
        new THREE.BoxGeometry(0.13, 0.04, 250),
        material(0x00cfff, 0.4, 0.3)
    );

    edge.position.set(x, 0.01, -65);
    world.add(edge);
}

// Road lane markings
const roadLines = [];

for (let z = -180; z < 30; z += 12) {
    for (const x of [-2, 2]) {
        const line = new THREE.Mesh(
            new THREE.BoxGeometry(0.10, 0.035, 5),
            lineMat
        );

        line.position.set(x, 0.02, z);
        world.add(line);
        roadLines.push(line);
    }
}

// --------------------------------------------------
// SUPERCAR CREATION
// Procedural 3D design; replace with Blender GLB
// --------------------------------------------------

let car = new THREE.Group();
scene.add(car);

function createCar(level) {

    const spec = CONFIG.cars[level - 1];

    const group = new THREE.Group();

    const bodyMat = material(spec.color, 0.22, 0.75);
    const darkMat = material(0x111827, 0.18, 0.5);
    const rubberMat = material(0x080a0d, 0.95);
    const metalMat = material(0x9ba7b8, 0.25, 0.9);

    // Main chassis
    const body = new THREE.Mesh(
        new THREE.BoxGeometry(2.1, 0.48, 4.1),
        bodyMat
    );

    body.position.y = 0.78;
    body.castShadow = true;
    group.add(body);

    // Sculpted front nose
    const nose = new THREE.Mesh(
        new THREE.BoxGeometry(1.9, 0.22, 1.15),
        bodyMat
    );

    nose.position.set(0, 0.63, -2.25);
    group.add(nose);

    // Front spoiler
    const spoiler = new THREE.Mesh(
        new THREE.BoxGeometry(2.4, 0.09, 0.35),
        darkMat
    );

    spoiler.position.set(0, 0.45, -2.55);
    group.add(spoiler);

    // Cabin
    const cabin = new THREE.Mesh(
        new THREE.BoxGeometry(1.55, 0.58, 1.8),
        glassMat
    );

    cabin.position.set(0, 1.22, -0.1);
    cabin.castShadow = true;
    group.add(cabin);

    // Roof
    const roof = new THREE.Mesh(
        new THREE.BoxGeometry(1.48, 0.12, 1.35),
        bodyMat
    );

    roof.position.set(0, 1.56, 0.0);
    group.add(roof);

    // Rear wing: higher levels get a larger wing
    const wing = new THREE.Group();

    const wingBar = new THREE.Mesh(
        new THREE.BoxGeometry(2.5 + level * 0.15, 0.13, 0.45),
        darkMat
    );

    wingBar.position.y = 1.6;
    wing.add(wingBar);

    for (const x of [-0.8, 0.8]) {
        const support = new THREE.Mesh(
            new THREE.BoxGeometry(0.09, 0.55, 0.09),
            metalMat
        );

        support.position.set(x, 1.28, 0);
        wing.add(support);
    }

    wing.position.z = 1.65;
    group.add(wing);

    // Wheels
    const wheels = [];

    for (const x of [-1.12, 1.12]) {
        for (const z of [-1.35, 1.4]) {

            const wheel = new THREE.Mesh(
                new THREE.CylinderGeometry(
                    0.43 + level * 0.025,
                    0.43 + level * 0.025,
                    0.25,
                    32
                ),
                rubberMat
            );

            wheel.rotation.z = Math.PI / 2;
            wheel.position.set(x, 0.48, z);
            wheel.castShadow = true;
            group.add(wheel);
            wheels.push(wheel);

            const rim = new THREE.Mesh(
                new THREE.CylinderGeometry(0.23, 0.23, 0.26, 20),
                metalMat
            );

            rim.rotation.z = Math.PI / 2;
            rim.position.copy(wheel.position);
            group.add(rim);
        }
    }

    // Headlights
    for (const x of [-0.68, 0.68]) {
        const lamp = new THREE.Mesh(
            new THREE.BoxGeometry(0.45, 0.12, 0.06),
            new THREE.MeshBasicMaterial({
                color: 0xc8f7ff
            })
        );

        lamp.position.set(x, 0.78, -2.31);
        group.add(lamp);
    }

    // Rear lights
    for (const x of [-0.7, 0.7]) {
        const lamp = new THREE.Mesh(
            new THREE.BoxGeometry(0.5, 0.12, 0.06),
            new THREE.MeshBasicMaterial({
                color: 0xff1f45
            })
        );

        lamp.position.set(x, 0.78, 2.07);
        group.add(lamp);
    }

    // Level-specific neon strip
    const neon = new THREE.Mesh(
        new THREE.BoxGeometry(2.15, 0.035, 2.6),
        new THREE.MeshBasicMaterial({
            color: spec.color
        })
    );

    neon.position.set(0, 0.48, 0);
    group.add(neon);

    group.userData.wheels = wheels;

    return group;
}

// --------------------------------------------------
// BLENDER GLB MODEL LOADER
// --------------------------------------------------

const loader = new GLTFLoader();

async function loadCar(level) {

    const modelURL = CONFIG.models[level - 1];

    if (!modelURL) {
        return createCar(level);
    }

    try {
        const gltf = await loader.loadAsync(modelURL);

        const model = gltf.scene;

        model.scale.setScalar(1);
        model.position.y = 0;

        model.traverse(obj => {
            if (obj.isMesh) {
                obj.castShadow = true;
                obj.receiveShadow = true;
            }
        });

        return model;

    } catch (error) {
        console.warn('Blender model unavailable. Using procedural car.', error);
        return createCar(level);
    }
}

let currentCarLevel = 1;

async function upgradeCar(level) {

    if (level === currentCarLevel) return;

    currentCarLevel = level;

    const oldCar = car;
    const newCar = await loadCar(level);

    if (currentCarLevel !== level) return;

    newCar.position.copy(oldCar.position);
    newCar.rotation.copy(oldCar.rotation);

    scene.remove(oldCar);
    scene.add(newCar);

    car = newCar;

    document.getElementById('carname').textContent =
        CONFIG.cars[level - 1].name;
}

// --------------------------------------------------
// ENVIRONMENT OBJECTS
// --------------------------------------------------

const scenery = [];

function createTree(x, z, type) {

    const group = new THREE.Group();

    if (type === 'snow') {

        const trunk = new THREE.Mesh(
            new THREE.CylinderGeometry(0.13, 0.25, 2.2, 7),
            material(0x49372d)
        );

        trunk.position.y = 1;
        group.add(trunk);

        for (let i = 0; i < 3; i++) {
            const cone = new THREE.Mesh(
                new THREE.ConeGeometry(1.0 - i * 0.15, 2, 8),
                material(0xccecff)
            );

            cone.position.y = 2 + i * 0.75;
            group.add(cone);
        }

    } else {

        const rock = new THREE.Mesh(
            new THREE.DodecahedronGeometry(0.8 + Math.random()),
            material(type === 'mud' ? 0x493126 : 0x344a40)
        );

        rock.position.y = 0.5;
        rock.scale.y = 0.7;
        group.add(rock);
    }

    group.position.set(x, 0, z);
    world.add(group);
    scenery.push(group);
}

function populateScenery() {

    scenery.forEach(obj => world.remove(obj));
    scenery.length = 0;

    const env = currentEnvironment;

    for (let z = -160; z < 20; z += 12) {

        for (const side of [-1, 1]) {

            createTree(
                side * (9 + Math.random() * 15),
                z + Math.random() * 5,
                env
            );
        }
    }
}

// --------------------------------------------------
// TRAFFIC / OBSTACLES
// --------------------------------------------------

const obstacles = [];

function spawnObstacle() {

    const group = new THREE.Group();

    const obstacleMat = material(
        Math.random() > 0.5 ? 0xff3c52 : 0xffa928,
        0.3,
        0.3
    );

    const box = new THREE.Mesh(
        new THREE.BoxGeometry(1.6, 1.4, 2.5),
        obstacleMat
    );

    box.position.y = 0.85;
    box.castShadow = true;
    group.add(box);

    const cabin = new THREE.Mesh(
        new THREE.BoxGeometry(1.25, 0.6, 1.1),
        glassMat
    );

    cabin.position.set(0, 1.7, -0.15);
    group.add(cabin);

    const lane = [-3.8, 0, 3.8][
        Math.floor(Math.random() * 3)
    ];

    group.position.set(lane, 0, -120);

    scene.add(group);

    obstacles.push(group);
}

// --------------------------------------------------
// PARTICLE SYSTEM
// --------------------------------------------------

const particleCount = 500;

const particleGeometry = new THREE.BufferGeometry();

const particlePositions = new Float32Array(particleCount * 3);

for (let i = 0; i < particleCount; i++) {

    particlePositions[i * 3] = (Math.random() - 0.5) * 45;
    particlePositions[i * 3 + 1] = Math.random() * 25;
    particlePositions[i * 3 + 2] = -Math.random() * 180;
}

particleGeometry.setAttribute(
    'position',
    new THREE.BufferAttribute(particlePositions, 3)
);

const particleMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.12,
    transparent: true,
    opacity: 0.8
});

const particles = new THREE.Points(
    particleGeometry,
    particleMaterial
);

scene.add(particles);

// --------------------------------------------------
// GAME STATE
// --------------------------------------------------

let running = false;
let gameOver = false;

let distance = 0;
let score = 0;
let speed = 0;
let targetX = 0;

let currentLevel = 1;
let currentEnvironment = 'snow';

let obstacleTimer = 0;
let animationTime = 0;

const keys = {};

function setEnvironment(env) {

    currentEnvironment = env;

    const settings = {
        snow: {
            sky: 0x91b7d5,
            fog: 0xc3d8e9,
            ground: snowMat,
            road: 0x7c8996
        },

        mud: {
            sky: 0x40332e,
            fog: 0x8a6b54,
            ground: mudMat,
            road: 0x4b352b
        },

        road: {
            sky: 0x26394b,
            fog: 0x70808e,
            ground: grassMat,
            road: 0x292e36
        },

        highway: {
            sky: 0x090d23,
            fog: 0x222c48,
            ground: material(0x161c27),
            road: 0x151922
        },

        mixed: {
            sky: 0x747c87,
            fog: 0xaaaeb4,
            ground: material(0x8b775e),
            road: 0x42434b
        }
    };

    const s = settings[env];

    scene.background.setHex(s.sky);
    scene.fog.color.setHex(s.fog);

    ground.material = s.ground;
    road.material = s.road;

    if (env === 'highway') {
        ambient.intensity = 0.6;
        glow.intensity = 70;
        sun.intensity = 0.5;
    } else {
        ambient.intensity = 2;
        glow.intensity = 35;
        sun.intensity = 3;
    }

    populateScenery();
}

// --------------------------------------------------
// LEVEL PROGRESSION
// --------------------------------------------------

function updateLevel() {

    let newLevel = 1;

    if (distance >= 1200) newLevel = 3;
    else if (distance >= 500) newLevel = 2;

    if (newLevel !== currentLevel) {

        currentLevel = newLevel;

        upgradeCar(currentLevel);

        document.getElementById('level').textContent =
            '0' + currentLevel + ' / 03';

        if (currentLevel === 2) {
            setEnvironment('mud');
        }

        if (currentLevel === 3) {
            setEnvironment('highway');
        }
    }

    // Mixed terrain sections periodically appear.
    if (currentLevel === 3 && Math.floor(distance) % 400 < 2) {
        setEnvironment('mixed');
    }

    if (currentLevel === 3 && Math.floor(distance) % 400 === 30) {
        setEnvironment('highway');
    }
}

// --------------------------------------------------
// CONTROLS
// --------------------------------------------------

function moveLeft() {
    if (running) targetX = Math.max(-4, targetX - 3.8);
}

function moveRight() {
    if (running) targetX = Math.min(4, targetX + 3.8);
}

document.addEventListener('keydown', e => {

    keys[e.code] = true;

    if ([
        'ArrowLeft', 'ArrowRight',
        'ArrowUp', 'ArrowDown', 'Space'
    ].includes(e.code)) {
        e.preventDefault();
    }

    if (e.code === 'ArrowLeft' || e.code === 'KeyA') moveLeft();
    if (e.code === 'ArrowRight' || e.code === 'KeyD') moveRight();
});

document.addEventListener('keyup', e => {
    keys[e.code] = false;
});

function bindButton(id, action) {

    const button = document.getElementById(id);

    button.addEventListener('pointerdown', e => {
        e.preventDefault();
        action();
    });
}

bindButton('left', moveLeft);
bindButton('right', moveRight);

// --------------------------------------------------
// START / RESET
// --------------------------------------------------

const overlay = document.getElementById('overlay');
const startButton = document.getElementById('start');
const description = document.getElementById('description');

function resetWorld() {

    obstacles.forEach(obj => scene.remove(obj));
    obstacles.length = 0;

    distance = 0;
    score = 0;
    speed = 0;
    targetX = 0;
    currentLevel = 1;
    currentCarLevel = 1;
    obstacleTimer = 0;

    car.position.set(0, 0, 4);
    car.rotation.set(0, 0, 0);

    document.getElementById('level').textContent = '01 / 03';
    document.getElementById('carname').textContent = 'APEX GT';

    document.getElementById('distance').textContent = '0';
    document.getElementById('score').textContent = '0';
    document.getElementById('speed').textContent = '0';

    document.getElementById('progress').style.width = '0%';

    setEnvironment('snow');
}

async function startGame() {

    resetWorld();

    if (currentCarLevel !== 1) {
        scene.remove(car);
        car = createCar(1);
        scene.add(car);
    }

    running = true;
    gameOver = false;

    overlay.classList.add('hide');

    speed = 80;
}

function finishGame() {

    running = false;
    gameOver = true;

    description.innerHTML =
        'RACE FINISHED!<br><br>' +
        'DISTANCE: ' + Math.floor(distance) +
        '<br>SCORE: ' + score;

    startButton.textContent = 'RACE AGAIN';

    overlay.classList.remove('hide');
}

startButton.addEventListener('click', startGame);

// --------------------------------------------------
// COLLISION
// --------------------------------------------------

function checkCollision() {

    for (const obstacle of obstacles) {

        if (
            Math.abs(obstacle.position.z - car.position.z) < 2.0 &&
            Math.abs(obstacle.position.x - car.position.x) < 2.0
        ) {
            finishGame();
            return;
        }
    }
}

// --------------------------------------------------
// UPDATE GAME
// --------------------------------------------------

const clock = new THREE.Clock();

function update(delta) {

    animationTime += delta;

    if (!running) return;

    // Speed gradually increases
    const maxSpeed = CONFIG.cars[currentLevel - 1].speed;

    speed = Math.min(
        maxSpeed,
        speed + delta * 9
    );

    const multiplier = speed / 100;

    distance += delta * speed * 0.18;
    score = Math.floor(distance * 10);

    updateLevel();

    // Smooth steering
    car.position.x = THREE.MathUtils.lerp(
        car.position.x,
        targetX,
        Math.min(1, delta * 8)
    );

    // Car movement animation
    car.rotation.z = THREE.MathUtils.lerp(
        car.rotation.z,
        (targetX - car.position.x) * 0.12,
        delta * 5
    );

    // Suspension
    car.position.y = Math.sin(animationTime * 15) * 0.025;

    if (car.userData.wheels) {
        car.userData.wheels.forEach(wheel => {
            wheel.rotation.x += delta * speed * 0.05;
        });
    }

    // Camera follow
    camera.position.x = THREE.MathUtils.lerp(
        camera.position.x,
        car.position.x * 0.3,
        delta * 2
    );

    camera.lookAt(car.position.x * 0.25, 0.7, -7);

    // Move road markings
    roadLines.forEach(line => {

        line.position.z += delta * speed * 0.14;

        if (line.position.z > 15) {
            line.position.z = -180;
        }
    });

    // Move scenery
    scenery.forEach(obj => {

        obj.position.z += delta * speed * 0.14;

        if (obj.position.z > 18) {
            obj.position.z = -170 - Math.random() * 30;
        }
    });

    // Move particles
    const positions = particleGeometry.attributes.position.array;

    for (let i = 0; i < particleCount; i++) {

        positions[i * 3 + 2] += delta * speed * 0.12;

        if (positions[i * 3 + 2] > 12) {
            positions[i * 3 + 2] = -180;
        }
    }

    particleGeometry.attributes.position.needsUpdate = true;

    particleMaterial.color.setHex(
        currentEnvironment === 'mud' ? 0x9a775b :
        currentEnvironment === 'highway' ? 0x8bcfff :
        0xffffff
    );

    // Obstacle spawning
    obstacleTimer += delta;

    const spawnRate = Math.max(
        0.65,
        1.8 - speed / 350
    );

    if (obstacleTimer > spawnRate) {
        spawnObstacle();
        obstacleTimer = 0;
    }

    // Move obstacles
    obstacles.forEach(obj => {
        obj.position.z += delta * speed * 0.14;
    });

    for (let i = obstacles.length - 1; i >= 0; i--) {

        if (obstacles[i].position.z > 15) {
            scene.remove(obstacles[i]);
            obstacles.splice(i, 1);
            score += 100;
        }
    }

    checkCollision();

    // Update interface
    document.getElementById('speed').textContent =
        Math.floor(speed);

    document.getElementById('distance').textContent =
        Math.floor(distance);

    document.getElementById('score').textContent = score;

    const levelStart = CONFIG.levelThresholds[currentLevel - 1];

    const levelEnd = currentLevel === 3
        ? 1700
        : CONFIG.levelThresholds[currentLevel];

    const progress = Math.min(
        100,
        Math.max(0, (distance - levelStart) /
        (levelEnd - levelStart) * 100)
    );

    document.getElementById('progress').style.width =
        progress + '%';
}

// --------------------------------------------------
// RENDER LOOP
// --------------------------------------------------

function animate() {

    requestAnimationFrame(animate);

    const delta = Math.min(clock.getDelta(), 0.04);

    update(delta);

    renderer.render(scene, camera);
}

window.addEventListener('resize', () => {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );
});

// --------------------------------------------------
// INITIALIZATION
// --------------------------------------------------

car = createCar(1);
car.position.set(0, 0, 4);
scene.add(car);

setEnvironment('snow');

animate();

</script>
</body>
</html>
"""


@app.route("/")
def home():
    return Response(HTML, mimetype="text/html")


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
