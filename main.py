import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print(os.getenv('DEEPSEEK_API_KEY'))

client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "Act as a senior Blender Python API expert"},
        {"role": "user", "content":''' 
            Act as a senior Blender Python API expert.  
            I will describe a 3D model I want. Your task is to write a complete, ready‑to‑run Python script that:
            1. Creates that model inside Blender (using bpy).
            2. Exports the finished model to a file on disk so I can use it later (e.g., in another 3D application or for printing).

            Requirements:
            - The script must work in Blender 3.0 or newer.
            - Use only native bpy and mathutils – no external add‑ons.
            - Generate mesh data procedurally (e.g., using bmesh or built‑in primitives + modifiers).
            - The final object should be named clearly, located at world origin, and have simple diffuse materials (optional but nice).
            - After creating the model, **export it to a file**.
            - Use a clear, absolute path that I can easily change. Write a comment: `# CHANGE THIS PATH TO YOUR DESIRED LOCATION`
            - Preferred export format: `OBJ` (or `STL` if the model is solid/watertight, or `.blend` if you prefer).
            - The exported file should contain only the generated model (clear default cube if necessary).
            - Print "Model generated successfully" and also print the full export path.

A stylized but anatomically proportional 3D model of an adult human (male, average build) in a neutral standing pose (A-pose: arms slightly away from torso, legs shoulder-width apart). The model should be constructed from primitive mesh shapes (cubes, cylinders, spheres) combined into a single object or a collection. Use simple diffuse materials with skin color, dark blue pants, and a light grey shirt.

Detailed specifications:

- **Total height**: 5.8 units (from sole of feet to top of head).
- **Origin**: at ground plane (Y = 0) – feet rest on Y=0.

**Body parts (approximate dimensions, positions relative to origin):**

1. **Torso (main body)**:
   - Shape: rectangular box.
   - Width: 1.2 units (side to side, X axis), Depth: 0.8 units (front to back, Z axis), Height: 1.8 units.
   - Position: centered at X=0, Z=0, bottom at Y=0.8 (above legs), top at Y=2.6.
   - Material: light grey (shirt).

2. **Head**:
   - Shape: slightly elongated sphere (or uv sphere scaled).
   - Radius: 0.45 units, scaled Y (vertical) to 0.55, X and Z to 0.45.
   - Position: center at X=0, Z=0, Y=2.85 (on top of neck).
   - Material: skin color (light peach/tan).

3. **Neck**:
   - Shape: cylinder.
   - Radius: 0.25 units, Height: 0.3 units.
   - Position: centered at X=0, Z=0, Y=2.65 (between torso and head).
   - Material: skin color.

4. **Legs (two)**:
   - Upper legs (thighs): cylinders or tapered cubes. Width 0.4, depth 0.4, height 0.9.
     - Left leg: center at X = -0.4, Z = 0, Y range from 0.4 to 1.3.
     - Right leg: center at X = +0.4, Z = 0, Y range from 0.4 to 1.3.
   - Lower legs (calves): cylinders width 0.35, depth 0.35, height 0.9.
     - Left: X = -0.4, Y from 0.0 to 0.4 (connect to upper leg at Y=0.4? Actually upper leg ends at Y=0.4, then lower leg goes from Y=0.0 to 0.4 – better to make continuous: upper leg Y=0.5 to 1.3, lower leg Y=0.0 to 0.5 with slight overlap).
     - Simplified: combine into one leg mesh? Or two cylinders per leg.
   - Feet: flattened cubes (width 0.5, depth 0.7, height 0.2) at Y=0.0.
     - Left foot: X = -0.4, Z = 0.15 (slightly forward), Y = 0.0.
     - Right foot: X = +0.4, Z = 0.15.
   - Material for legs and feet: dark blue (pants) – but feet can be same skin color or shoes (dark brown). For simplicity, use dark blue for legs and dark brown for feet.

5. **Arms**:
   - Upper arms (biceps): cylinders radius 0.2, height 1.0.
     - Left: X = -0.8, Z = 0.0, Y from 2.0 to 3.0 (shoulder at Y≈2.8, elbow at Y≈1.8? Wait: torso top at Y=2.6, shoulder at Y≈2.7). Adjust: Y range 2.2 to 3.2 (shoulder at 3.2, elbow at 2.2).
     - Right: X = +0.8, Z = 0.0, Y from 2.2 to 3.2.
   - Forearms: cylinders radius 0.16, height 0.9.
     - Left: X = -0.8, Z = 0.0, Y from 1.3 to 2.2 (elbow to wrist).
     - Right: X = +0.8, Z = 0.0, Y from 1.3 to 2.2.
   - Hands: small cubes or spheres (width 0.3, depth 0.2, height 0.3).
     - Left: X = -0.8, Z = 0.05, Y = 1.2.
     - Right: X = +0.8, Z = 0.05, Y = 1.2.
   - Material: skin color for arms and hands.

6. **Shoulders (optional)** – small spheres at shoulder joints to smooth transition: radius 0.22 at X=±0.75, Y≈3.15, Z=0.0.

**Pose details**:
- Arms rotated slightly away from body (A-pose): upper arms angle about 15-20 degrees outward. This means the elbow should be shifted outward in X and slightly backward in Z. For simplicity, keep arms straight but move upper arm center to X=±0.85, forearm center to X=±0.85.
- Legs slightly apart: feet centers at X=±0.4, knee joints at same X, no rotation.

**Additional features**:
- Eyes: two small spheres (radius 0.07) on head front: X = ±0.15, Y = 2.98, Z = 0.45 (forward). Material: white with black pupil (separate small sphere).
- Simple hair: a half-sphere or cube on top of head (radius 0.5, height 0.2) – dark brown material.
- Ears: small half-spheres on sides of head: X = ±0.48, Y = 2.85, Z = 0.0.

**Grouping and naming**:
- All parts should be separate mesh objects but joined into a single collection named "Human".
- Each major part (head, torso, left_arm, right_arm, left_leg, right_leg, etc.) should have a descriptive name.
- Use simple diffuse materials without textures. Colors: skin = (0.85, 0.65, 0.55), shirt = (0.7, 0.7, 0.7), pants = (0.1, 0.2, 0.5), shoes = (0.4, 0.2, 0.1), hair = (0.3, 0.2, 0.1), eyes white = (1,1,1), pupil = (0,0,0).

**Constraints**:
- Use only native Blender primitives and bmesh operations (no external add-ons).
- The final model must be manifold (watertight) where possible – except eyes and hair which can be separate overlapping meshes.
- All coordinates are in Blender's default coordinate system: X = right, Y = up, Z = forward (or use Y-up and Z-forward? In Blender, Z is up by default. I need to be consistent: standard Blender uses Z up, Y forward. Let's adjust: In my description I used Y as up, Z as forward. That conflicts. Better to rewrite using Blender's native: Z up, Y forward.)

            Write only the Python script, no explanations before or after.
        ''' },
    ],
    stream=False
)

print(response.choices[0].message.content)
