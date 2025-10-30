# SCARY_MODE: Membrane Distortion with a Skull

Make the page “skin” (a screenshot of your viewport) behave like a stretchy membrane that dents and ripples when a skull pushes into it — without full cloth physics. Two proven, shippable techniques:

---

## Approach 1 — Fast Pressure Map (simple, convincing)
Treat the membrane as a subdivided plane. Each frame you generate a **pressure texture** from the skull’s projection onto the plane, blur it to spread force, then **displace vertices** along the plane normal using that texture.

### High‑level pipeline
1. **Pressure pass:** orthographic camera aligned to the membrane. Render only the skull to a floating‑point render target (white where skull overlaps the plane UVs).
2. **Diffuse (ping‑pong blur):** 4–10 iterations of a small Laplacian/box blur to spread pressure like rubber/fabric.
3. **Main pass:** plane uses a `ShaderMaterial` that samples the pressure to push vertices; use the viewport screenshot as the plane’s albedo.

### Three.js setup sketch
```js
// Geometry: enough segments for smooth dents
const planeGeo = new THREE.PlaneGeometry(1, 1, 256, 256);

// RenderTargets for pressure + ping-pong
const rtA = new THREE.WebGLRenderTarget(512, 512, {
  type: THREE.HalfFloatType,
  minFilter: THREE.LinearFilter,
  magFilter: THREE.LinearFilter,
  depthBuffer: false,
  stencilBuffer: false
});
const rtB = rtA.clone();

// Camera facing out of the membrane (membrane is at z=0 facing +z)
const membraneCam = new THREE.OrthographicCamera(-0.5, 0.5, 0.5, -0.5, 0.01, 5.0);
membraneCam.position.set(0, 0, 1);
membraneCam.lookAt(0, 0, 0);

// Skull scene/mesh (example)
const skull = await loadGLTF('/assets/skull.glb');
scene.add(skull.scene);

// Fullscreen quad for post passes
const fsq = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), null);
const postScene = new THREE.Scene();
const postCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
postScene.add(fsq);
```

### Shaders
**Membrane vertex (displace along normal by pressure)**
```glsl
// membrane.vert
uniform sampler2D uPressure;
uniform float uAmp; // displacement scale (meters per unit pressure)
varying vec2 vUv;

void main() {
  vUv = uv;
  vec3 pos = position;
  float p = texture2D(uPressure, vUv).r;   // 0..1
  float disp = (p - 0.5) * 2.0 * uAmp;     // -uAmp..+uAmp
  pos += normal * disp;                     // plane normal is +Z by default
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

**Membrane fragment (shade the screenshot + subtle darkening by pressure)**
```glsl
// membrane.frag
varying vec2 vUv;
uniform sampler2D uAlbedo;   // viewport screenshot or any texture
uniform sampler2D uPressure; // for cheap shading

void main() {
  vec3 base = texture2D(uAlbedo, vUv).rgb;
  float p = texture2D(uPressure, vUv).r;
  float shade = 1.0 - 0.2 * (p - 0.5); // darken where pressed
  gl_FragColor = vec4(base * shade, 1.0);
}
```

**Pressure pass (render skull mask)**
```glsl
// pressure.frag (drawn on a fullscreen quad while sampling a depth or mask)
varying vec2 vUv;
uniform sampler2D uSkullMask; // Alternate: render skull directly with white material
void main(){
  float mask = texture2D(uSkullMask, vUv).r; // white where skull projects
  gl_FragColor = vec4(mask, mask, mask, 1.0);
}
```

**Jacobi/box blur (spread force)**
```glsl
// blur.frag
varying vec2 vUv;
uniform sampler2D uIn;
uniform vec2 uTexel; // 1/width, 1/height
void main(){
  float c = texture2D(uIn, vUv).r;
  float s = 0.0;
  s += texture2D(uIn, vUv + vec2( uTexel.x, 0.0)).r;
  s += texture2D(uIn, vUv + vec2(-uTexel.x, 0.0)).r;
  s += texture2D(uIn, vUv + vec2(0.0,  uTexel.y)).r;
  s += texture2D(uIn, vUv + vec2(0.0, -uTexel.y)).r;
  float outV = (c + s * 0.5) / 2.0; // light diffusion
  gl_FragColor = vec4(outV);
}
```

### Wiring the passes
```js
// Materials for post passes
const blurMat = new THREE.ShaderMaterial({
  vertexShader: passthroughVS, fragmentShader: blurFS,
  uniforms: { uIn: { value: rtA.texture }, uTexel: { value: new THREE.Vector2(1/512, 1/512) } }
});
fsq.material = blurMat;

// Membrane material
const membraneMat = new THREE.ShaderMaterial({
  vertexShader: membraneVS, fragmentShader: membraneFS, transparent: false,
  uniforms: {
    uPressure: { value: rtA.texture },
    uAlbedo: { value: screenshotTexture },
    uAmp: { value: 0.02 }
  }
});
const membrane = new THREE.Mesh(planeGeo, membraneMat);
scene.add(membrane);

function renderPressure() {
  // Option A: render skull with a pure-white material into rtA
  const prevOverride = scene.overrideMaterial;
  scene.overrideMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });

  renderer.setRenderTarget(rtA);
  renderer.setClearColor(0x000000, 1);
  renderer.clear(true, true, false);
  renderer.render(scene, membraneCam); // only skull should be visible to this cam

  scene.overrideMaterial = prevOverride;
}

function blurPressure(iter=6) {
  let src = rtA, dst = rtB;
  for (let i=0; i<iter; i++) {
    blurMat.uniforms.uIn.value = src.texture;
    renderer.setRenderTarget(dst);
    renderer.render(postScene, postCam);
    // swap
    const tmp = src; src = dst; dst = tmp;
  }
  membraneMat.uniforms.uPressure.value = src.texture; // final
}

function tick(){
  renderPressure();
  blurPressure(6);
  renderer.setRenderTarget(null);
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
```

### Commentary & gotchas
- **Projection alignment:** The orthographic frustum must map exactly to the membrane UVs. If your plane spans `[-0.5,0.5]` x/y in world, use the same in the ortho camera.
- **Only skull in pressure pass:** Hide everything else for `membraneCam` (layers or `visible` flags).
- **Scale:** Start with `uAmp ≈ 0.01–0.03` for a 1‑meter plane.
- **Performance:** 512×512 RT + 6 blurs is cheap on desktop. Mobile: 256×256 and 4 blurs.

---

## Approach 2 — Cloth‑lite Heightfield (ripples & recoil)
Add physically‑inspired motion with a GPGPU wave equation on a height map.

### Update equation (done in a fragment shader)
`H_next = (2 - damp) * H_t - (1 - damp) * H_{t-1} + c2 * Laplacian(H_t) + force`

- `H_t`/`H_{t-1}`: two textures you ping‑pong each frame.
- `damp` ∈ [0,1] (e.g., 0.03).
- `c2` controls wave speed (stability: keep small when resolution is high).
- `force` is the smoothed pressure texture from the skull.

**Height update shader**
```glsl
// height_update.frag
varying vec2 vUv;
uniform sampler2D uH;      // H_t
uniform sampler2D uHprev;  // H_{t-1}
uniform sampler2D uForce;  // pressure map
uniform vec2 uTexel;
uniform float uC2;
uniform float uDamp;

void main(){
  float h  = texture2D(uH, vUv).r;
  float hm = texture2D(uHprev, vUv).r;
  // 4-neighbor Laplacian
  float l = texture2D(uH, vUv + vec2( uTexel.x, 0.0)).r
          + texture2D(uH, vUv + vec2(-uTexel.x, 0.0)).r
          + texture2D(uH, vUv + vec2(0.0,  uTexel.y)).r
          + texture2D(uH, vUv + vec2(0.0, -uTexel.y)).r
          - 4.0 * h;
  float f = texture2D(uForce, vUv).r - 0.5; // centered
  float hNext = (2.0 - uDamp) * h - (1.0 - uDamp) * hm + uC2 * l + f * 0.5;
  gl_FragColor = vec4(hNext, 0.0, 0.0, 1.0);
}
```

**Membrane vertex using heightfield**
```glsl
// membrane_height.vert
uniform sampler2D uH; // current height
uniform float uAmp;
varying vec2 vUv;
void main(){
  vUv = uv;
  vec3 pos = position;
  float h = texture2D(uH, vUv).r * 2.0 - 1.0; // map to -1..1 if stored 0..1
  pos += normal * (h * uAmp);
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

**Normals for lighting (fragment)**
```glsl
// membrane_height.frag (excerpt)
uniform sampler2D uH; uniform vec2 uTexel; varying vec2 vUv;
vec3 normalFromHeight(){
  float hL = texture2D(uH, vUv - vec2(uTexel.x, 0.0)).r;
  float hR = texture2D(uH, vUv + vec2(uTexel.x, 0.0)).r;
  float hD = texture2D(uH, vUv - vec2(0.0, uTexel.y)).r;
  float hU = texture2D(uH, vUv + vec2(0.0, uTexel.y)).r;
  vec3 dx = vec3(1.0, 0.0, (hR - hL));
  vec3 dy = vec3(0.0, 1.0, (hU - hD));
  return normalize(cross(dy, dx));
}
```

### Frame loop for cloth‑lite
```js
// Height textures
const hA = new THREE.WebGLRenderTarget(512,512,{ type: THREE.HalfFloatType });
const hB = hA.clone();
const heightMat = new THREE.ShaderMaterial({
  vertexShader: passthroughVS, fragmentShader: heightUpdateFS,
  uniforms: { uH: { value: hA.texture }, uHprev: { value: hB.texture }, uForce: { value: rtA.texture }, uTexel: { value: new THREE.Vector2(1/512,1/512) }, uC2: { value: 0.12 }, uDamp: { value: 0.03 } }
});

function stepHeight(){
  fsq.material = heightMat;
  renderer.setRenderTarget(hB);
  renderer.render(postScene, postCam);
  // swap H_t/H_{t-1}
  const tmp = hA.texture; hA.texture = hB.texture; hB.texture = tmp;
}
```

---

## Capturing the viewport as the membrane skin
- **DOM → texture:** use `html2canvas` and upload to a `THREE.Texture` (update on demand, not every frame).
- **Three scene → texture:** render to an offscreen target and reuse that as `uAlbedo`.

```js
// Example: turn a screenshot canvas into a Three texture
const screenshotCanvas = await html2canvas(document.body);
const screenshotTexture = new THREE.CanvasTexture(screenshotCanvas);
membraneMat.uniforms.uAlbedo.value = screenshotTexture;
```

---

## Performance tips
- Prefer **HalfFloat** RTs; full float is often unnecessary.
- Reduce blur passes on mobile; compensate with larger kernel (two‑pass separable blur if needed).
- Keep membrane geometry under ~300×300 segments; the displacement is in the vertex shader.
- Use **layers** to exclude everything except the skull from the pressure pass.

---

## Debug checklist
- Membrane not moving? Confirm the pressure RT is non‑black (blit to screen for a frame).
- Dents are spiky? Increase blur passes or reduce `uAmp`.
- Pressure appears offset/rotated? Your ortho camera bounds don’t match the plane’s world‑space extents; fix those first.
- Too bouncy in cloth‑lite mode? Increase `uDamp` or reduce `uC2`.

---

### Minimal passthrough vertex for post passes
```glsl
// passthrough.vert
attribute vec3 position; attribute vec2 uv; varying vec2 vUv;
void main(){ vUv = uv; gl_Position = vec4(position, 1.0); }
```

That’s enough to ship a creepy, convincing membrane without wrestling a full cloth solver. Drop in your skull asset and tune `uAmp`, blur passes, and (for cloth‑lite) `uC2/uDamp` until it feels right.
