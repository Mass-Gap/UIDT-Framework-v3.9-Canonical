import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';

const VacuumGrid = ({ kappa, torsionEnabled }) => {
  const meshRef = useRef();
  
  // Create a grid geometry
  const geometry = useMemo(() => new THREE.PlaneGeometry(20, 20, 64, 64), []);
  
  // Custom shader material to represent the UIDT geometric scalar field
  const material = useMemo(() => new THREE.ShaderMaterial({
    uniforms: {
      uTime: { value: 0 },
      uKappa: { value: kappa },
      uTorsion: { value: torsionEnabled ? 1.0 : 0.0 },
      uColorSafe: { value: new THREE.Color(0x00ff88) },
      uColorTension: { value: new THREE.Color(0xff4444) }
    },
    vertexShader: `
      uniform float uTime;
      uniform float uKappa;
      uniform float uTorsion;
      varying vec2 vUv;
      varying float vElevation;

      // Simplex noise function placeholder (using sin/cos for performance)
      float noise(vec2 p) {
        return sin(p.x * 1.5 + uTime * 0.5) * cos(p.y * 1.5 + uTime * 0.3);
      }

      void main() {
        vUv = uv;
        vec3 pos = position;
        
        // Base metric expansion
        float elevation = noise(pos.xy * 0.5) * 0.5;
        
        // Torsion effects (Σ_T) -> higher frequency distortions based on bare coupling κ
        if (uTorsion > 0.5) {
          elevation += sin(pos.x * 8.0 * uKappa + uTime) * cos(pos.y * 8.0 * uKappa + uTime) * 0.2;
        }

        vElevation = elevation;
        pos.z += elevation;
        
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `,
    fragmentShader: `
      uniform float uKappa;
      uniform vec3 uColorSafe;
      uniform vec3 uColorTension;
      varying vec2 vUv;
      varying float vElevation;

      void main() {
        // Tension grows as kappa deviates from 0.5
        float deviation = abs(uKappa - 0.5) * 5.0; 
        vec3 color = mix(uColorSafe, uColorTension, clamp(deviation, 0.0, 1.0));
        
        // Add grid lines
        float grid = max(
          step(0.98, fract(vUv.x * 30.0)),
          step(0.98, fract(vUv.y * 30.0))
        );
        
        // Dim the base, highlight the grid based on elevation
        vec3 finalColor = color * (0.2 + 0.8 * grid) + vec3(vElevation * 0.5);
        gl_FragColor = vec4(finalColor, 0.8 + vElevation * 0.2);
      }
    `,
    wireframe: false,
    transparent: true,
    side: THREE.DoubleSide
  }), [kappa, torsionEnabled]);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.material.uniforms.uTime.value = state.clock.elapsedTime;
      meshRef.current.material.uniforms.uKappa.value = kappa;
      meshRef.current.material.uniforms.uTorsion.value = torsionEnabled ? 1.0 : 0.0;
    }
  });

  return (
    <mesh ref={meshRef} geometry={geometry} material={material} rotation={[-Math.PI / 2, 0, 0]} />
  );
};

const TorsionManifold = () => {
  const [kappa, setKappa] = useState(0.500);
  const [torsionEnabled, setTorsionEnabled] = useState(true);

  return (
    <div className="manifold-container" style={{ width: '100%', height: '500px', position: 'relative', border: '1px solid var(--border-color)', borderRadius: '8px', overflow: 'hidden' }}>
      
      {/* HUD Overlay */}
      <div style={{ position: 'absolute', top: '1rem', left: '1rem', zIndex: 10, background: 'rgba(0,0,0,0.7)', padding: '1rem', borderRadius: '4px', border: '1px solid var(--border-color)', backdropFilter: 'blur(4px)' }}>
        <h3 style={{ margin: '0 0 1rem 0', fontSize: '1rem' }}>Vacuum Geometry [D]</h3>
        
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
            Bare Coupling (κ): {kappa.toFixed(3)}
          </label>
          <input 
            type="range" 
            min="0.300" max="0.700" step="0.001" 
            value={kappa} 
            onChange={(e) => setKappa(parseFloat(e.target.value))}
            style={{ width: '100%' }}
          />
          {Math.abs(kappa - 0.5) > 0.02 && (
             <span style={{ fontSize: '0.75rem', color: 'var(--danger)', display: 'block', marginTop: '0.25rem' }}>Warning: Non-canonical. Fixed point violates 5κ² = 3λs.</span>
          )}
        </div>

        <div>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: 'var(--text-secondary)', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={torsionEnabled}
              onChange={(e) => setTorsionEnabled(e.target.checked)}
            />
            Lattice Torsion (Σ_T)
          </label>
        </div>
      </div>

      <Canvas camera={{ position: [0, 5, 10], fov: 45 }}>
        <color attach="background" args={['#050505']} />
        <fog attach="fog" args={['#050505', 5, 20]} />
        <ambientLight intensity={0.2} />
        <Stars radius={50} depth={50} count={2000} factor={4} saturation={0} fade speed={1} />
        <VacuumGrid kappa={kappa} torsionEnabled={torsionEnabled} />
        <OrbitControls enablePan={false} maxPolarAngle={Math.PI / 2 - 0.1} />
      </Canvas>
    </div>
  );
};

export default TorsionManifold;
