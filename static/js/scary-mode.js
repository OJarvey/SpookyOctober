/**
 * Scary-Face Extrusion Easter Egg
 *
 * Captures the current viewport and applies a spooky 3D extrusion effect
 * using Three.js with custom shaders.
 *
 * Activation: Type "SCARY" (case-insensitive)
 * Deactivation: Press Escape
 */

class ScaryModeEasterEgg {
    constructor(options = {}) {
        this.activationSequence = ['s', 'c', 'a', 'r', 'y'];
        this.keyBuffer = [];
        this.isActive = false;
        this.isInitialized = false;
        this.autoStart = options.autoStart || false; // Testing mode

        // Three.js objects
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.mesh = null;
        this.animationId = null;

        // Interaction state
        this.mouseX = 0;
        this.mouseY = 0;
        this.extrusionDepth = 0.6; // Fixed at good spooky value
        this.eyeSocketDepth = 5.0; // Fixed at good depth
        this.cheekboneProminence = 1.3; // Fixed at good value
        this.teethProtrusion = 3.0; // Fixed at good value
        this.nasalDepth = 1.0; // Fixed nasal cavity depth
        this.time = 0;

        // UI elements
        this.container = null;
        this.canvas = null;
        this.progressContainer = null;
        this.progressBar = null;
        this.progressText = null;

        // Captured viewport
        this.viewportTexture = null;

        this.init();
    }

    init() {
        // Only activate on home page
        const isHomePage = window.location.pathname === '/' || window.location.pathname === '';

        if (!isHomePage) {
            console.log('🎃 Scary Mode: Not on home page, easter egg disabled');
            return;
        }

        // Set up keyboard listener for activation
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));

        if (this.autoStart) {
            console.log('🎃 Scary Mode: AUTO-START enabled (testing mode)');
            // Auto-activate after a short delay to let the page finish loading
            setTimeout(() => {
                console.log('🎃 Auto-activating Scary Mode...');
                this.activate();
            }, 500);
        } else {
            console.log('🎃 Scary Mode Easter Egg initialized. Type "SCARY" to activate!');
        }
    }

    handleKeyPress(event) {
        const key = event.key.toLowerCase();

        if (this.isActive) {
            // Handle controls when active
            if (key === 'escape') {
                this.deactivate();
            } else if (key === 'r') {
                this.resetExtrusion();
            }
            return;
        }

        // Check activation sequence
        this.keyBuffer.push(key);
        if (this.keyBuffer.length > this.activationSequence.length) {
            this.keyBuffer.shift();
        }

        if (this.keyBuffer.join('') === this.activationSequence.join('')) {
            this.activate();
            this.keyBuffer = [];
        }
    }

    async activate() {
        if (this.isActive) return;

        console.log('👻 Activating Scary Mode...');
        this.isActive = true;

        try {
            // Check WebGL support first
            console.log('Step 1: Checking WebGL support...');
            if (!this.checkWebGLSupport()) {
                throw new Error('WebGL is not supported in your browser. Try Chrome, Firefox, or Edge.');
            }

            console.log('Step 2: Setting up UI...');
            this.setupUI();
            this.updateProgress('Preparing spooky magic...', 10);

            await this.wait(500);
            console.log('Step 3: Capturing viewport...');
            this.updateProgress('Capturing your screen...', 30);

            await this.captureViewport();
            console.log('Step 4: Setting up Three.js...');
            this.updateProgress('Generating 3D mesh...', 60);

            await this.wait(300);
            this.setupThreeJS();
            console.log('Step 5: Creating extrusion mesh...');
            this.updateProgress('Applying scary effects...', 80);

            await this.wait(300);
            await this.createExtrusionMesh();
            console.log('Step 6: Starting animation...');
            this.updateProgress('Ready to haunt!', 100);

            await this.wait(500);
            this.hideProgress();
            this.setupInteractions();
            this.startAnimation();

            console.log('✅ Scary Mode fully activated!');
            this.showMessage('Scary Mode Activated! 👻', 'success');
        } catch (error) {
            console.error('❌ Error activating scary mode:', error);
            this.showMessage('Failed to activate Scary Mode: ' + error.message, 'error');
            this.deactivate();
        }
    }

    checkWebGLSupport() {
        try {
            const canvas = document.createElement('canvas');

            // Try to get context with all possible methods
            let gl = null;
            const contextTypes = ['webgl2', 'webgl', 'experimental-webgl'];

            for (const type of contextTypes) {
                try {
                    gl = canvas.getContext(type, {
                        failIfMajorPerformanceCaveat: false,
                        powerPreference: 'default' // Try default first
                    });
                    if (gl) {
                        console.log(`✅ WebGL supported via: ${type}`);
                        break;
                    }
                } catch (e) {
                    console.warn(`Failed to get ${type} context:`, e);
                }
            }

            if (!gl) {
                console.error('❌ WebGL not supported - no context available');
                console.log('Possible causes:');
                console.log('- Hardware acceleration disabled');
                console.log('- GPU blacklisted');
                console.log('- Too many WebGL contexts active');
                return false;
            }

            // Log WebGL capabilities
            console.log('WebGL Version:', gl.getParameter(gl.VERSION));
            console.log('WebGL Vendor:', gl.getParameter(gl.VENDOR));
            console.log('WebGL Renderer:', gl.getParameter(gl.RENDERER));
            console.log('Max Texture Size:', gl.getParameter(gl.MAX_TEXTURE_SIZE));

            return true;
        } catch (e) {
            console.error('❌ WebGL check failed:', e);
            return false;
        }
    }

    setupUI() {
        // Container for the 3D effect - transparent to show the deformed viewport
        this.container = document.createElement('div');
        this.container.id = 'scary-mode-container';
        this.container.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: transparent;  /* Transparent to show captured viewport texture */
            z-index: 9999;
            pointer-events: none;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        `;

        // Create canvas container (Three.js will create its own canvas)
        this.canvasContainer = document.createElement('div');
        this.canvasContainer.style.cssText = `
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            pointer-events: auto;
        `;

        // DEBUG: Disable ripple effect to see skull clearly
        // document.body.style.cssText += `
        //     animation: scary-ripple 4s ease-in-out infinite;
        // `;

        // Add ripple animation keyframes if not already present
        // if (!document.getElementById('scary-ripple-style')) {
        //     const style = document.createElement('style');
        //     style.id = 'scary-ripple-style';
        //     style.textContent = `
        //         @keyframes scary-ripple {
        //             0%, 100% {
        //                 transform: scale(1) translateZ(0);
        //                 filter: none;
        //             }
        //             25% {
        //                 transform: scale(1.005) translateZ(0);
        //                 filter: hue-rotate(5deg);
        //             }
        //             50% {
        //                 transform: scale(0.995) translateZ(0);
        //                 filter: hue-rotate(-5deg);
        //             }
        //             75% {
        //                 transform: scale(1.002) translateZ(0);
        //                 filter: hue-rotate(3deg);
        //             }
        //         }
        //     `;
        //     document.head.appendChild(style);
        // }

        // Progress container
        this.progressContainer = document.createElement('div');
        this.progressContainer.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            max-width: 80%;
            text-align: center;
        `;

        // Progress text
        this.progressText = document.createElement('div');
        this.progressText.style.cssText = `
            color: #FF6600;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        `;
        this.progressText.textContent = 'Initializing...';

        // Progress bar background
        const progressBg = document.createElement('div');
        progressBg.style.cssText = `
            width: 100%;
            height: 8px;
            background: #333;
            border-radius: 4px;
            overflow: hidden;
        `;

        // Progress bar fill
        this.progressBar = document.createElement('div');
        this.progressBar.style.cssText = `
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, #FF6600, #FF0000);
            border-radius: 4px;
            transition: width 0.3s ease-out;
        `;

        progressBg.appendChild(this.progressBar);
        this.progressContainer.appendChild(this.progressText);
        this.progressContainer.appendChild(progressBg);

        // Controls hint (hidden initially)
        this.controlsHint = document.createElement('div');
        this.controlsHint.style.cssText = `
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: #888;
            font-size: 14px;
            text-align: center;
            opacity: 0;
            transition: opacity 0.5s;
        `;
        this.controlsHint.innerHTML = `
            🎃 <strong>Press ESC to exit</strong>
        `;

        this.container.appendChild(this.canvasContainer);
        this.container.appendChild(this.progressContainer);
        this.container.appendChild(this.controlsHint);

        document.body.appendChild(this.container);

        // Fade in animation
        this.container.style.opacity = '0';
        setTimeout(() => {
            this.container.style.transition = 'opacity 0.5s';
            this.container.style.opacity = '1';
        }, 10);
    }

    updateProgress(text, percentage) {
        if (this.progressText) {
            this.progressText.textContent = text;
        }
        if (this.progressBar) {
            this.progressBar.style.width = percentage + '%';
        }
    }

    hideProgress() {
        if (this.progressContainer) {
            this.progressContainer.style.transition = 'opacity 0.5s';
            this.progressContainer.style.opacity = '0';
            setTimeout(() => {
                if (this.progressContainer) {
                    this.progressContainer.style.display = 'none';
                }
            }, 500);
        }

        // Show controls hint
        if (this.controlsHint) {
            this.controlsHint.style.opacity = '1';
        }
    }

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async captureViewport() {
        try {
            // Temporarily hide the scary mode container
            if (this.container) {
                this.container.style.display = 'none';
            }

            // Capture the entire document element (not just body) at full viewport size
            const canvas = await html2canvas(document.documentElement, {
                allowTaint: true,
                useCORS: true,
                logging: true,  // Enable logging to debug
                width: window.innerWidth,
                height: window.innerHeight,
                x: 0,
                y: 0,
                scrollX: 0,
                scrollY: 0,
                windowWidth: window.innerWidth,
                windowHeight: window.innerHeight,
                backgroundColor: null  // Preserve transparency
            });

            // Show container again
            if (this.container) {
                this.container.style.display = 'flex';
            }

            // Create texture from canvas
            this.viewportTexture = new THREE.CanvasTexture(canvas);
            this.viewportTexture.needsUpdate = true;

            console.log('✅ Viewport captured:', canvas.width, 'x', canvas.height);
            console.log('   Window size:', window.innerWidth, 'x', window.innerHeight);
            console.log('   Texture created:', this.viewportTexture);
            console.log('   Texture image:', this.viewportTexture.image);
            console.log('   Canvas data URL (first 100 chars):', canvas.toDataURL().substring(0, 100));
        } catch (error) {
            throw new Error('Failed to capture viewport: ' + error.message);
        }
    }

    setupThreeJS() {
        try {
            console.log('🎨 Initializing Three.js...');

            // Create scene with transparent background to show captured viewport
            this.scene = new THREE.Scene();
            this.scene.background = null; // Transparent - let the captured viewport show through

            // Create perspective camera for depth effect (skull grows as it approaches)
            const aspect = window.innerWidth / window.innerHeight;
            this.camera = new THREE.PerspectiveCamera(
                75,      // Field of view
                aspect,  // Aspect ratio
                0.1,     // Near clipping plane
                1000     // Far clipping plane
            );
            this.camera.position.set(0, 0, 2);

            console.log('📹 Perspective camera created, aspect:', aspect);

            // Create renderer WITHOUT passing a canvas - let Three.js create it
            console.log('🖼️ Creating WebGL renderer...');
            try {
                this.renderer = new THREE.WebGLRenderer({
                    antialias: true, // Enable for smoother edges
                    alpha: true, // Enable transparency
                    powerPreference: 'default', // Use default instead of high-performance
                    failIfMajorPerformanceCaveat: false
                });
            } catch (rendererError) {
                console.error('❌ THREE.WebGLRenderer failed:', rendererError);
                throw new Error('Failed to create WebGL renderer. Try enabling hardware acceleration in your browser settings.');
            }

            if (!this.renderer) {
                throw new Error('Renderer is null');
            }

            console.log('✅ Renderer created successfully');

            // Get the canvas that Three.js created
            this.canvas = this.renderer.domElement;
            this.canvas.style.cssText = `
                width: 100vw;
                height: 100vh;
                display: block;
                position: fixed;
                top: 0;
                left: 0;
                margin: 0;
                padding: 0;
                object-fit: fill;
            `;

            // Append to our container
            this.canvasContainer.appendChild(this.canvas);

            // Set size and pixel ratio
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5)); // Cap at 1.5x for better compatibility

            console.log('📐 Renderer size set:', window.innerWidth, 'x', window.innerHeight);

            // Handle context loss
            this.canvas.addEventListener('webglcontextlost', (event) => {
                event.preventDefault();
                console.warn('⚠️ WebGL context lost');
                this.showMessage('Graphics context lost. Exiting Scary Mode.', 'error');
                this.deactivate();
            }, false);

            this.canvas.addEventListener('webglcontextrestored', () => {
                console.log('✅ WebGL context restored');
            }, false);

            // Add WebGL error logging
            const gl = this.renderer.getContext();
            const oldGetError = gl.getError.bind(gl);
            gl.getError = function() {
                const error = oldGetError();
                if (error !== gl.NO_ERROR) {
                    console.error('WebGL Error:', error);
                }
                return error;
            };
            console.log('✅ WebGL error logging enabled');

            // Add lighting
            const ambientLight = new THREE.AmbientLight(0x404040, 0.8);
            this.scene.add(ambientLight);

            const pointLight1 = new THREE.PointLight(0xff6600, 1.5);
            pointLight1.position.set(2, 2, 2);
            this.scene.add(pointLight1);

            const pointLight2 = new THREE.PointLight(0xff0000, 1.0);
            pointLight2.position.set(-2, -2, 2);
            this.scene.add(pointLight2);

            console.log('✅ Three.js scene initialized');
            console.log('Renderer info:', this.renderer.info);

            // Handle window resize
            this.resizeHandler = () => this.onWindowResize();
            window.addEventListener('resize', this.resizeHandler);
        } catch (error) {
            console.error('Failed to setup Three.js:', error);
            throw new Error('Failed to initialize 3D graphics: ' + error.message);
        }
    }

    async createExtrusionMesh() {
        // Create the viewport plane with high detail for smooth deformation
        const segments = 256; // Very high detail for smooth elastic effect

        // Calculate plane size to fill viewport with perspective camera
        // Camera is at z=2, plane is at z=0, so distance = 2
        const aspect = window.innerWidth / window.innerHeight;
        const distance = 2; // Camera distance from plane
        const fov = 75; // Field of view in degrees

        // Calculate visible height at the plane's distance from camera
        // Formula: height = 2 * distance * tan(fov/2 * PI/180)
        const vFOV = fov * Math.PI / 180; // Convert to radians
        const planeHeight = 2 * Math.tan(vFOV / 2) * distance;
        const planeWidth = planeHeight * aspect;

        console.log('Plane dimensions:', planeWidth, 'x', planeHeight, 'for aspect', aspect);

        const planeGeometry = new THREE.PlaneGeometry(planeWidth, planeHeight, segments, segments);

        // Create the cube/skull position marker
        // Increased size to match the skull scale (50x) and create more visible deformation
        const cubeSize = 2.5; // Much larger influence radius
        this.cubePosition = new THREE.Vector3(0, 0, -0.5); // BEHIND membrane (membrane at z=0.5)

        console.log('Cube/skull influence size:', cubeSize, 'units');
        console.log('Cube/skull position (FIXED):', this.cubePosition);

        // Add texture and skull-based displacement to shader
        const planeMaterial = new THREE.ShaderMaterial({
            uniforms: {
                viewportTexture: { value: this.viewportTexture },
                time: { value: 0 },
                cubePosition: { value: this.cubePosition },
                cubeSize: { value: cubeSize },
                extrusionDepth: { value: this.extrusionDepth },
                eyeSocketDepth: { value: this.eyeSocketDepth },
                cheekboneProminence: { value: this.cheekboneProminence },
                teethProtrusion: { value: this.teethProtrusion },
                nasalDepth: { value: this.nasalDepth }
            },
            vertexShader: `
                uniform float time;
                uniform vec3 cubePosition;
                uniform float cubeSize;
                uniform float extrusionDepth;
                uniform float eyeSocketDepth;
                uniform float cheekboneProminence;
                uniform float teethProtrusion;
                uniform float nasalDepth;
                varying vec2 vUv;
                varying float vDisplacement;

                void main() {
                    vUv = uv;
                    vec3 pos = position;

                    vec2 vertexPos2D = pos.xy;
                    vec2 skullPos2D = cubePosition.xy;

                    // Calculate distance from skull center
                    float dist2D = length(vertexPos2D - skullPos2D);

                    // Influence radius
                    float influence = cubeSize * extrusionDepth;

                    // Sharp contact area - vertices close to skull "stick" to it
                    // Steeper falloff creates snap-back effect at edges
                    float contactRadius = influence * 1.8;
                    float contactFalloff = smoothstep(contactRadius, contactRadius * 0.3, dist2D);

                    // Calculate how much this vertex should be pushed FORWARD by skull
                    // Skull pushes from behind (z=-0.5), membrane is at z=0.5, distance = 1.0
                    // Vertices above skull features get pushed FORWARD (positive Z) toward camera

                    // Main skull shape - overall bulge (subtle)
                    vec2 skullOffset = vec2(0.0, 0.0);
                    float skullDist = length((vertexPos2D - (skullPos2D + skullOffset)) * vec2(1.0, 1.1));
                    float skullBase = smoothstep(influence * 2.0, 0.0, skullDist);

                    // Forehead prominence (top)
                    vec2 foreheadOffset = vec2(0.0, 0.4);
                    float foreheadDist = length((vertexPos2D - (skullPos2D + foreheadOffset)) * vec2(1.3, 1.0));
                    float foreheadBulge = smoothstep(influence * 1.0, 0.0, foreheadDist);

                    // Cheekbones - key feature! (protrude outward)
                    vec2 leftCheekOffset = vec2(-0.4, 0.05);
                    vec2 rightCheekOffset = vec2(0.4, 0.05);
                    float leftCheekDist = length((vertexPos2D - (skullPos2D + leftCheekOffset)) * vec2(0.8, 1.2));
                    float rightCheekDist = length((vertexPos2D - (skullPos2D + rightCheekOffset)) * vec2(0.8, 1.2));
                    float cheekbones = smoothstep(0.35, 0.0, leftCheekDist) + smoothstep(0.35, 0.0, rightCheekDist);

                    // Eye sockets - DEEP indentations (negative displacement)
                    vec2 leftEyeOffset = vec2(-0.3, 0.15);
                    vec2 rightEyeOffset = vec2(0.3, 0.15);
                    float leftEyeDist = length((vertexPos2D - (skullPos2D + leftEyeOffset)) * vec2(1.0, 1.3));
                    float rightEyeDist = length((vertexPos2D - (skullPos2D + rightEyeOffset)) * vec2(1.0, 1.3));
                    float eyeSockets = smoothstep(0.3, 0.0, leftEyeDist) + smoothstep(0.3, 0.0, rightEyeDist);

                    // Nasal cavity (small indent)
                    vec2 noseOffset = vec2(0.0, 0.0);
                    float noseDist = length((vertexPos2D - (skullPos2D + noseOffset)) * vec2(2.0, 3.0));
                    float nasalIndent = smoothstep(0.15, 0.0, noseDist);

                    // Teeth ridge - upper and lower jaw protrusions
                    // Upper teeth (horizontal ridge)
                    vec2 upperTeethOffset = vec2(0.0, -0.05);
                    float upperTeethDistY = abs(vertexPos2D.y - (skullPos2D.y + upperTeethOffset.y));
                    float upperTeethDistX = abs(vertexPos2D.x - skullPos2D.x);
                    float upperTeethRidge = smoothstep(0.1, 0.0, upperTeethDistY) * smoothstep(0.6, 0.0, upperTeethDistX);

                    // Lower teeth (horizontal ridge)
                    vec2 lowerTeethOffset = vec2(0.0, -0.25);
                    float lowerTeethDistY = abs(vertexPos2D.y - (skullPos2D.y + lowerTeethOffset.y));
                    float lowerTeethDistX = abs(vertexPos2D.x - skullPos2D.x);
                    float lowerTeethRidge = smoothstep(0.08, 0.0, lowerTeethDistY) * smoothstep(0.5, 0.0, lowerTeethDistX);

                    float teethRidge = upperTeethRidge + lowerTeethRidge;

                    // Combine features - each has its own control
                    float displacement = skullBase * 0.3 * extrusionDepth; // Base skull shape
                    displacement += foreheadBulge * 0.15 * extrusionDepth; // Forehead
                    displacement += cheekbones * 0.25 * extrusionDepth * cheekboneProminence; // Cheekbones
                    displacement -= eyeSockets * 0.4 * extrusionDepth * eyeSocketDepth; // Eye sockets
                    displacement -= nasalIndent * 0.2 * extrusionDepth * nasalDepth; // Nose indent - NOW ADJUSTABLE
                    displacement += teethRidge * 0.15 * extrusionDepth * teethProtrusion; // Teeth ridge

                    // Add subtle pulsing
                    float pulse = 0.9 + 0.1 * sin(time * 2.0);
                    displacement *= pulse;

                    pos.z += displacement;

                    vDisplacement = displacement;

                    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
                }
            `,
            fragmentShader: `
                uniform sampler2D viewportTexture;
                uniform float time;
                varying vec2 vUv;
                varying float vDisplacement;

                void main() {
                    vec4 texColor = texture2D(viewportTexture, vUv);

                    // Darken displaced areas for depth
                    float darken = vDisplacement * 0.15;
                    texColor.rgb *= (1.0 - darken);

                    // Extra darkening for negative displacement (eye sockets)
                    if (vDisplacement < 0.0) {
                        texColor.rgb *= (1.0 + vDisplacement * 0.3); // Darker eye sockets
                    }

                    // Add slight color distortion to stretched areas
                    float distortionAmount = vDisplacement * 0.05;
                    texColor.r += distortionAmount * sin(time * 2.0);
                    texColor.b -= distortionAmount * 0.5;

                    // Subtle edge glow on highly displaced areas
                    float glowThreshold = 2.0;
                    if (vDisplacement > glowThreshold) {
                        float glow = (vDisplacement - glowThreshold) * 0.1;
                        texColor.rgb += vec3(0.2, 0.1, 0.15) * glow;
                    }

                    gl_FragColor = texColor;
                }
            `,
            side: THREE.DoubleSide
        });

        console.log('Using shader with texture and skull-based displacement');
        console.log('Skull at:', this.cubePosition, 'Influence size:', cubeSize);


        // Viewport plane material with elastic deformation (saved for later)
        const planeMaterialComplex = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0 },
                extrusionDepth: { value: this.extrusionDepth },
                viewportTexture: { value: this.viewportTexture },
                cubePosition: { value: this.cubePosition },
                cubeSize: { value: cubeSize }
            },
            vertexShader: `
                uniform float time;
                uniform float extrusionDepth;
                uniform vec3 cubePosition;
                uniform float cubeSize;

                varying vec2 vUv;
                varying float vDisplacement;

                void main() {
                    vUv = uv;
                    vec3 pos = position;

                    // DEBUG: Add a simple wave to test if shader is working
                    float testWave = sin(position.x * 3.0 + time) * 0.5;
                    pos.z += testWave;

                    // Calculate distance from vertex to edges (0.0 at edge, 1.0 at center)
                    // UV coordinates go from 0 to 1, so distance from edge is:
                    float edgeDistX = min(uv.x, 1.0 - uv.x) * 2.0; // 0 at edges, 1 at center
                    float edgeDistY = min(uv.y, 1.0 - uv.y) * 2.0;
                    float edgeFactor = min(edgeDistX, edgeDistY); // Use minimum to pin all edges
                    edgeFactor = smoothstep(0.0, 0.3, edgeFactor); // Smooth transition from edge to center

                    // Calculate distance from current vertex to cube center (in 2D)
                    vec2 vertexPos2D = pos.xy;
                    vec2 cubePos2D = cubePosition.xy;
                    float dist = length(vertexPos2D - cubePos2D);

                    // Elastic deformation - the closer to cube, the more displacement
                    // Using a smooth falloff function
                    float influence = cubeSize * extrusionDepth * 3.0; // Increased influence multiplier
                    float falloff = smoothstep(influence * 2.0, 0.0, dist); // Wider influence radius

                    // Skull is at FIXED position z=-0.5, plane is at z=0
                    // proximityFactor is always 1.0 for fixed position (no animation)
                    float proximityFactor = 1.0;

                    // Push vertices forward (positive Z) where skull is pushing
                    // Dramatically increased displacement for membrane bulge effect
                    float displacement = falloff * influence * 15.0 * proximityFactor; // Much larger displacement

                    // Add pulsating effect
                    float pulse = 0.9 + 0.1 * sin(time * 2.0);
                    displacement *= pulse;

                    // Apply edge constraint: vertices near edges cannot move much
                    displacement *= edgeFactor;

                    // Apply Z displacement (pushing through)
                    pos.z += displacement;

                    // Also pull vertices toward cube center (elastic stretch)
                    // But only for vertices not near the edges
                    // Increased stretch for more dramatic membrane tension
                    vec2 direction = normalize(cubePos2D - vertexPos2D);
                    pos.xy += direction * falloff * influence * 1.5 * edgeFactor * proximityFactor;

                    // Add subtle wave animation around the deformation
                    float wave = sin(dist * 20.0 - time * 3.0) * 0.01 * falloff * edgeFactor;
                    pos.z += wave * extrusionDepth;

                    vDisplacement = displacement;

                    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
                }
            `,
            fragmentShader: `
                uniform float time;
                uniform sampler2D viewportTexture;

                varying vec2 vUv;
                varying float vDisplacement;

                void main() {
                    // DEBUG: Simple solid color to verify shader runs
                    gl_FragColor = vec4(1.0, 0.0, 1.0, 1.0); // Bright magenta
                }
            `,
            side: THREE.DoubleSide,  // DoubleSide so we can see it from both angles
            transparent: true,
            wireframe: false
        });

        console.log('Shader material created (not used yet)');

        // Create viewport plane with elastic deformation
        this.viewportPlane = new THREE.Mesh(planeGeometry, planeMaterial);

        console.log('Using material:', planeMaterial.type);
        console.log('Plane geometry vertices:', planeGeometry.attributes.position.count);

        this.viewportPlane.position.z = 0.5; // Membrane positioned in front, skull will push from behind (z=-1.0)

        // Add to scene BEFORE compiling
        this.scene.add(this.viewportPlane);

        console.log('✅ ShaderMaterial created with skull-based displacement');
        console.log('Membrane plane at z=', this.viewportPlane.position.z, ', Skull at z=', this.cubePosition.z);
        console.log('Camera at z=', this.camera.position.z);

        // Create the scary skull that will push through the sheet
        try {
            this.skull = await this.loadSkullModel();
            console.log('✅ Using loaded GLB skull model');
        } catch (error) {
            console.warn('⚠️ Failed to load GLB model, using fallback:', error);
            this.skull = this.createSkullFallback();
        }

        this.skull.position.copy(this.cubePosition);
        this.scene.add(this.skull);

        // Track skull's initial Z position for animation
        this.skullStartZ = this.cubePosition.z;
        this.skullAnimationTime = 0;
        this.skullTargetZ = -0.2; // End position - just behind the plane (which is at z=0) to push through membrane

        // Add point light at skull position for dramatic effect
        this.skullLight = new THREE.PointLight(0xffffff, 5, 20);  // Bright white, high intensity
        this.skullLight.position.copy(this.cubePosition);
        this.scene.add(this.skullLight);

        // Add ambient light to make sure scene is visible
        const ambientLight = new THREE.AmbientLight(0xffffff, 1.0);
        this.scene.add(ambientLight);

        console.log('✅ Skull created at z =', this.cubePosition.z);
        console.log('   skullStartZ =', this.skullStartZ, ', skullTargetZ =', this.skullTargetZ);
    }

    async loadSkullModel() {
        // Load 3D skull model from GLB file
        return new Promise((resolve, reject) => {
            const loader = new THREE.GLTFLoader();
            const modelPath = '/static/models/low-poly-skull/low-poly-skull.glb';

            console.log('🦴 Loading skull model from:', modelPath);

            loader.load(
                modelPath,
                (gltf) => {
                    console.log('✅ Skull model loaded successfully');
                    const skullGroup = gltf.scene;

                    // Scale the model EXTREMELY large since it will be further from camera
                    // Target position is z=-0.2, camera at z=2, so distance is ~2.2 units
                    skullGroup.scale.set(50.0, 50.0, 50.0);

                    // Make skull invisible - we only want to see the membrane deformation
                    skullGroup.traverse((child) => {
                        if (child.isMesh) {
                            child.visible = false; // Hide the mesh
                            console.log('Hidden mesh (deformation only):', child.name, 'vertices:', child.geometry.attributes.position.count);
                        }
                    });

                    // Calculate bounding box to find the visual center of the model
                    const box = new THREE.Box3().setFromObject(skullGroup);
                    const center = box.getCenter(new THREE.Vector3());

                    console.log('Skull bounding box:');
                    console.log('  - Min:', box.min);
                    console.log('  - Max:', box.max);
                    console.log('  - Center:', center);

                    // Store the center offset to apply during animation
                    // This allows us to align the visual center with the viewport center
                    skullGroup.userData.centerOffset = center.clone();

                    // Log model info
                    console.log('Skull model info:');
                    console.log('  - Position:', skullGroup.position);
                    console.log('  - Scale:', skullGroup.scale);
                    console.log('  - Children count:', skullGroup.children.length);

                    // Skull is invisible - only deformation visible
                    skullGroup.visible = false;

                    resolve(skullGroup);
                },
                (progress) => {
                    const percent = (progress.loaded / progress.total) * 100;
                    console.log(`Loading skull: ${percent.toFixed(0)}%`);
                },
                (error) => {
                    console.error('❌ Error loading skull model:', error);
                    reject(error);
                }
            );
        });
    }

    createSkullFallback() {
        // Fallback: Create a detailed skull with concave features (procedural)
        console.log('⚠️ Using fallback procedural skull');
        const skullGroup = new THREE.Group();

        // DEBUG: Bright material for skull bone
        const boneMaterial = new THREE.MeshStandardMaterial({
            color: 0xe8dcc0,  // Bone color
            emissive: 0xff3300,
            emissiveIntensity: 0.8,
            roughness: 0.6,
            metalness: 0.2,
            wireframe: false
        });

        // === CRANIUM (Main skull) ===
        const craniumGeometry = new THREE.SphereGeometry(0.5, 64, 64);
        craniumGeometry.scale(1, 1.15, 1.05); // Elongate and widen slightly
        const cranium = new THREE.Mesh(craniumGeometry, boneMaterial);
        cranium.position.set(0, 0.15, -0.05);
        skullGroup.add(cranium);

        // Forehead prominence
        const foreheadGeometry = new THREE.SphereGeometry(0.35, 32, 32);
        foreheadGeometry.scale(1.2, 0.8, 1);
        const forehead = new THREE.Mesh(foreheadGeometry, boneMaterial);
        forehead.position.set(0, 0.35, 0.15);
        skullGroup.add(forehead);

        // === FACIAL STRUCTURE ===
        // Cheekbones (zygomatic arch) - prominent
        const cheekboneMaterial = boneMaterial.clone();

        const leftCheekGeometry = new THREE.SphereGeometry(0.18, 32, 32);
        leftCheekGeometry.scale(1.3, 0.7, 0.9);
        const leftCheek = new THREE.Mesh(leftCheekGeometry, cheekboneMaterial);
        leftCheek.position.set(-0.28, 0.08, 0.25);
        skullGroup.add(leftCheek);

        const rightCheekGeometry = new THREE.SphereGeometry(0.18, 32, 32);
        rightCheekGeometry.scale(1.3, 0.7, 0.9);
        const rightCheek = new THREE.Mesh(rightCheekGeometry, cheekboneMaterial);
        rightCheek.position.set(0.28, 0.08, 0.25);
        skullGroup.add(rightCheek);

        // Upper jaw (maxilla)
        const maxillaGeometry = new THREE.SphereGeometry(0.35, 32, 32);
        maxillaGeometry.scale(1, 0.65, 0.85);
        const maxilla = new THREE.Mesh(maxillaGeometry, boneMaterial);
        maxilla.position.set(0, -0.1, 0.25);
        skullGroup.add(maxilla);

        // Lower jaw (mandible) - more angular
        const mandibleGeometry = new THREE.SphereGeometry(0.38, 32, 32);
        mandibleGeometry.scale(1.05, 0.5, 0.75);
        const mandible = new THREE.Mesh(mandibleGeometry, boneMaterial);
        mandible.position.set(0, -0.42, 0.08);
        skullGroup.add(mandible);

        // Chin prominence
        const chinGeometry = new THREE.SphereGeometry(0.12, 32, 32);
        chinGeometry.scale(0.8, 1, 0.9);
        const chin = new THREE.Mesh(chinGeometry, boneMaterial);
        chin.position.set(0, -0.5, 0.22);
        skullGroup.add(chin);

        // === EYE SOCKETS - Deep concave features ===
        const eyeSocketMaterial = new THREE.MeshStandardMaterial({
            color: 0x000000,
            emissive: 0x880000,
            emissiveIntensity: 1.5,
            roughness: 1.0
        });

        // Left eye socket - multiple layers for depth
        const leftEyeOuter = new THREE.SphereGeometry(0.14, 32, 32);
        leftEyeOuter.scale(1.1, 1.3, 0.8);
        const leftEyeOuterMesh = new THREE.Mesh(leftEyeOuter, eyeSocketMaterial);
        leftEyeOuterMesh.position.set(-0.22, 0.18, 0.38);
        skullGroup.add(leftEyeOuterMesh);

        const leftEyeInner = new THREE.SphereGeometry(0.11, 32, 32);
        leftEyeInner.scale(1, 1.2, 1.2);
        const leftEyeInnerMesh = new THREE.Mesh(leftEyeInner, eyeSocketMaterial);
        leftEyeInnerMesh.position.set(-0.22, 0.18, 0.32);
        skullGroup.add(leftEyeInnerMesh);

        // Right eye socket - multiple layers for depth
        const rightEyeOuter = new THREE.SphereGeometry(0.14, 32, 32);
        rightEyeOuter.scale(1.1, 1.3, 0.8);
        const rightEyeOuterMesh = new THREE.Mesh(rightEyeOuter, eyeSocketMaterial);
        rightEyeOuterMesh.position.set(0.22, 0.18, 0.38);
        skullGroup.add(rightEyeOuterMesh);

        const rightEyeInner = new THREE.SphereGeometry(0.11, 32, 32);
        rightEyeInner.scale(1, 1.2, 1.2);
        const rightEyeInnerMesh = new THREE.Mesh(rightEyeInner, eyeSocketMaterial);
        rightEyeInnerMesh.position.set(0.22, 0.18, 0.32);
        skullGroup.add(rightEyeInnerMesh);

        // === NASAL CAVITY - Pear-shaped, deep ===
        const nasalCavityMaterial = eyeSocketMaterial.clone();

        // Main nasal opening
        const nasalGeometry = new THREE.SphereGeometry(0.08, 32, 32);
        nasalGeometry.scale(0.75, 1.4, 0.6);
        const nasal = new THREE.Mesh(nasalGeometry, nasalCavityMaterial);
        nasal.position.set(0, 0.02, 0.46);
        skullGroup.add(nasal);

        // Nasal bridge depth
        const nasalBridgeGeometry = new THREE.SphereGeometry(0.05, 32, 32);
        nasalBridgeGeometry.scale(0.8, 1.2, 1);
        const nasalBridge = new THREE.Mesh(nasalBridgeGeometry, nasalCavityMaterial);
        nasalBridge.position.set(0, 0.08, 0.42);
        skullGroup.add(nasalBridge);

        // === TEETH - Individual with gaps for concave effect ===
        const toothMaterial = new THREE.MeshStandardMaterial({
            color: 0xf0ece0,  // Off-white tooth color
            emissive: 0x331100,
            emissiveIntensity: 0.2,
            roughness: 0.4,
            metalness: 0.1
        });

        // Upper teeth (incisors, canines, molars)
        const upperToothPositions = [
            { x: -0.2, size: [0.032, 0.055, 0.035] },  // Left molar
            { x: -0.14, size: [0.03, 0.05, 0.035] },   // Left premolar
            { x: -0.08, size: [0.028, 0.06, 0.04] },   // Left canine (longer)
            { x: -0.04, size: [0.028, 0.05, 0.038] },  // Left incisor
            // Center gap
            { x: 0.04, size: [0.028, 0.05, 0.038] },   // Right incisor
            { x: 0.08, size: [0.028, 0.06, 0.04] },    // Right canine
            { x: 0.14, size: [0.03, 0.05, 0.035] },    // Right premolar
            { x: 0.2, size: [0.032, 0.055, 0.035] }    // Right molar
        ];

        upperToothPositions.forEach(pos => {
            const toothGeo = new THREE.BoxGeometry(...pos.size);
            const tooth = new THREE.Mesh(toothGeo, toothMaterial);
            tooth.position.set(pos.x, -0.18, 0.36);
            tooth.rotation.x = -0.1; // Slight angle
            skullGroup.add(tooth);
        });

        // Lower teeth (slightly smaller, more irregular)
        const lowerToothPositions = [
            { x: -0.16, size: [0.03, 0.045, 0.03] },   // Left molar
            { x: -0.1, size: [0.028, 0.05, 0.032] },   // Left canine
            { x: -0.05, size: [0.026, 0.045, 0.03] },  // Left incisor
            { x: 0.0, size: [0.026, 0.045, 0.03] },    // Center incisor
            { x: 0.05, size: [0.026, 0.045, 0.03] },   // Right incisor
            { x: 0.1, size: [0.028, 0.05, 0.032] },    // Right canine
            { x: 0.16, size: [0.03, 0.045, 0.03] }     // Right molar
        ];

        lowerToothPositions.forEach(pos => {
            const toothGeo = new THREE.BoxGeometry(...pos.size);
            const tooth = new THREE.Mesh(toothGeo, toothMaterial);
            tooth.position.set(pos.x, -0.45, 0.32);
            tooth.rotation.x = 0.05; // Slight angle
            skullGroup.add(tooth);
        });

        // === TEMPORAL BONES (sides of skull) ===
        const temporalMaterial = boneMaterial.clone();

        const leftTemporalGeometry = new THREE.SphereGeometry(0.15, 32, 32);
        leftTemporalGeometry.scale(0.7, 1, 1.2);
        const leftTemporal = new THREE.Mesh(leftTemporalGeometry, temporalMaterial);
        leftTemporal.position.set(-0.42, 0.1, -0.05);
        skullGroup.add(leftTemporal);

        const rightTemporalGeometry = new THREE.SphereGeometry(0.15, 32, 32);
        rightTemporalGeometry.scale(0.7, 1, 1.2);
        const rightTemporal = new THREE.Mesh(rightTemporalGeometry, temporalMaterial);
        rightTemporal.position.set(0.42, 0.1, -0.05);
        skullGroup.add(rightTemporal);

        // Skull is invisible - only membrane deformation visible
        skullGroup.visible = false;

        return skullGroup;
    }

    setupInteractions() {
        // Mouse movement
        this.container.addEventListener('mousemove', (e) => {
            this.mouseX = (e.clientX / window.innerWidth) * 2 - 1;
            this.mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        });
    }

    startAnimation() {
        this.isInitialized = true;
        this.animate();
    }

    animate() {
        if (!this.isActive || !this.isInitialized) return;

        this.animationId = requestAnimationFrame(() => this.animate());

        this.time += 0.016; // ~60 FPS

        // Subtle horizontal movement for the skull (makes bulge move)
        this.cubePosition.x = Math.sin(this.time * 0.3) * 0.5; // Slow side-to-side
        this.cubePosition.y = Math.cos(this.time * 0.4) * 0.3; // Slow up-down
        // Z stays fixed at -1.0

        // Debug logging
        if (Math.floor(this.time) % 2 === 0 && this.time - Math.floor(this.time) < 0.02) {
            console.log('Skull position:', this.cubePosition.x.toFixed(2), this.cubePosition.y.toFixed(2), this.cubePosition.z.toFixed(2),
                       'Extrusion:', this.extrusionDepth.toFixed(2));
        }

        // Update viewport plane shader uniforms (only if using ShaderMaterial with uniforms)
        if (this.viewportPlane && this.viewportPlane.material.uniforms) {
            // Update time if it exists
            if (this.viewportPlane.material.uniforms.time) {
                this.viewportPlane.material.uniforms.time.value = this.time;
            }

            // Update other uniforms if they exist
            if (this.viewportPlane.material.uniforms.extrusionDepth) {
                this.viewportPlane.material.uniforms.extrusionDepth.value = this.extrusionDepth;
            }

            if (this.viewportPlane.material.uniforms.eyeSocketDepth) {
                this.viewportPlane.material.uniforms.eyeSocketDepth.value = this.eyeSocketDepth;
            }

            if (this.viewportPlane.material.uniforms.cheekboneProminence) {
                this.viewportPlane.material.uniforms.cheekboneProminence.value = this.cheekboneProminence;
            }

            if (this.viewportPlane.material.uniforms.teethProtrusion) {
                this.viewportPlane.material.uniforms.teethProtrusion.value = this.teethProtrusion;
            }

            if (this.viewportPlane.material.uniforms.cubePosition) {
                this.viewportPlane.material.uniforms.cubePosition.value = this.cubePosition;
            }

            // Debug: Log uniforms periodically
            if (Math.floor(this.time) % 2 === 0 && this.time - Math.floor(this.time) < 0.02) {
                console.log('Updating shader uniforms, time:', this.time.toFixed(2));
            }
        }

        // Update skull position and rotation
        if (this.skull) {
            this.skull.position.copy(this.cubePosition);

            // Apply offset to align visual center with viewport center (0, 0)
            if (this.skull.userData.centerOffset) {
                this.skull.position.sub(this.skull.userData.centerOffset);

                // Debug log the adjusted position periodically
                if (Math.floor(this.time) % 2 === 0 && this.time - Math.floor(this.time) < 0.02) {
                    console.log('Skull adjusted position:', this.skull.position, 'Offset:', this.skull.userData.centerOffset);
                }
            }

            // Add subtle neck-like movements - yaw (Y-axis) and pitch (X-axis)
            // Using different frequencies for more natural, unsettling motion
            const yawAmount = 0.15; // ~8.5 degrees max rotation left/right
            const pitchAmount = 0.1; // ~5.7 degrees max rotation up/down

            // Yaw: slow side-to-side head turn (like "no")
            const yaw = Math.sin(this.time * 0.8) * yawAmount;

            // Pitch: subtle up/down nod (like examining the viewer)
            // Using different frequency to avoid synchronized motion
            const pitch = Math.sin(this.time * 1.2) * pitchAmount;

            // Roll: very subtle tilt (like curiosity)
            const roll = Math.sin(this.time * 0.6) * 0.05; // ~2.8 degrees

            // Apply rotations
            this.skull.rotation.y = yaw;   // Yaw (side to side)
            this.skull.rotation.x = pitch; // Pitch (up and down)
            this.skull.rotation.z = roll;  // Roll (tilt)
        }

        // Update light position
        if (this.skullLight) {
            this.skullLight.position.copy(this.cubePosition);

            // Pulsating light intensity - gets brighter as skull approaches
            const distanceFactor = Math.abs(this.cubePosition.z - this.skullStartZ);
            const baseLightIntensity = 2 + distanceFactor * 0.5;
            this.skullLight.intensity = baseLightIntensity + Math.sin(this.time * 3.0) * 0.5;
        }

        this.renderer.render(this.scene, this.camera);
    }

    onWindowResize() {
        if (!this.camera || !this.renderer) return;

        // Update perspective camera aspect ratio
        const aspect = window.innerWidth / window.innerHeight;
        this.camera.aspect = aspect;
        this.camera.updateProjectionMatrix();

        this.renderer.setSize(window.innerWidth, window.innerHeight);

        // Recreate the plane with new aspect ratio if it exists
        if (this.viewportPlane) {
            // Remove old plane
            this.scene.remove(this.viewportPlane);
            this.viewportPlane.geometry.dispose();
            this.viewportPlane.material.dispose();

            // Recreate mesh with new dimensions (async, but we don't await in resize)
            this.createExtrusionMesh().catch(err => console.error('Error recreating mesh:', err));
        }
    }

    resetExtrusion() {
        this.teethProtrusion = 1.0;
        this.showMessage('Teeth Protrusion reset to 1.0', 'info');
    }

    deactivate() {
        if (!this.isActive) return;

        console.log('🎃 Deactivating Scary Mode...');
        this.isActive = false;
        this.isInitialized = false;

        // Stop animation
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        // Remove body ripple animation
        document.body.style.animation = '';

        // Remove ripple style
        const rippleStyle = document.getElementById('scary-ripple-style');
        if (rippleStyle) {
            rippleStyle.remove();
        }

        // Remove event listeners
        if (this.resizeHandler) {
            window.removeEventListener('resize', this.resizeHandler);
            this.resizeHandler = null;
        }

        // Clean up Three.js resources
        if (this.viewportPlane) {
            if (this.viewportPlane.geometry) {
                this.viewportPlane.geometry.dispose();
            }
            if (this.viewportPlane.material) {
                if (this.viewportPlane.material.uniforms) {
                    // Dispose of textures in uniforms
                    if (this.viewportPlane.material.uniforms.viewportTexture && this.viewportPlane.material.uniforms.viewportTexture.value) {
                        this.viewportPlane.material.uniforms.viewportTexture.value.dispose();
                    }
                }
                this.viewportPlane.material.dispose();
            }
            if (this.scene) {
                this.scene.remove(this.viewportPlane);
            }
            this.viewportPlane = null;
        }

        if (this.skull) {
            // Dispose of all meshes in the skull group
            this.skull.traverse((child) => {
                if (child.geometry) {
                    child.geometry.dispose();
                }
                if (child.material) {
                    child.material.dispose();
                }
            });
            if (this.scene) {
                this.scene.remove(this.skull);
            }
            this.skull = null;
        }

        if (this.skullLight) {
            if (this.scene) {
                this.scene.remove(this.skullLight);
            }
            this.skullLight = null;
        }

        if (this.viewportTexture) {
            this.viewportTexture.dispose();
            this.viewportTexture = null;
        }

        if (this.renderer) {
            this.renderer.dispose();
            this.renderer.forceContextLoss();
            this.renderer = null;
        }

        if (this.scene) {
            // Clear scene
            while(this.scene.children.length > 0) {
                const child = this.scene.children[0];
                if (child.geometry) child.geometry.dispose();
                if (child.material) child.material.dispose();
                this.scene.remove(child);
            }
            this.scene = null;
        }

        // Remove UI
        if (this.container) {
            this.container.style.transition = 'opacity 0.3s';
            this.container.style.opacity = '0';
            setTimeout(() => {
                if (this.container && this.container.parentNode) {
                    this.container.parentNode.removeChild(this.container);
                }
                this.container = null;
                this.canvas = null;
                this.progressContainer = null;
                this.progressBar = null;
                this.progressText = null;
                this.controlsHint = null;
            }, 300);
        }

        // Reset state
        this.mouseX = 0;
        this.mouseY = 0;
        this.extrusionDepth = 1.0;
        this.time = 0;

        console.log('✅ Scary Mode deactivated and cleaned up');
    }

    showMessage(text, type = 'info') {
        const colors = {
            success: '#10B981',
            error: '#EF4444',
            info: '#FF6600'
        };

        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${colors[type]};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            max-width: 400px;
            word-wrap: break-word;
        `;
        message.textContent = text;

        document.body.appendChild(message);

        // Errors stay longer
        const duration = type === 'error' ? 5000 : 2000;

        setTimeout(() => {
            message.style.transition = 'opacity 0.3s';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, duration);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.scaryMode = new ScaryModeEasterEgg({ autoStart: false });
    });
} else {
    window.scaryMode = new ScaryModeEasterEgg({ autoStart: false });
}
