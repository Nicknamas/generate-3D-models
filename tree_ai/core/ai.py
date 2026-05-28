from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv('AI_API_URL')
)

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                 }
            ],
            temperature=0.7,
            max_tokens=10000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {e}"


def get_creating_script(prompt, save_filepath="../obj.blend") -> str | None:
    prompt_with_instructions = f"""
YOUR ROLE
You are a Senior Technical Artist and an expert in Blender 5.x/6.0 automation. Your sole task is to analyze the provided detailed 3D model description and write a clean, optimized, production-ready Python script using the `bpy` module.

INPUT DATA FOR ANALYSIS & GENERATION:
================================================================================
{prompt}
================================================================================

STEP 1. ANALYZE AND DECOMPOSE
Before writing any code, perform a full decomposition of the asset:
1. Dimensions & Coordinates: Extract positions (location), scales (scale), and rotations (rotation) for each individual block/primitive.
2. Shapes & Primitives: Map each part to one of three safe primitive types: 'CUBE', 'SPHERE', or 'CYLINDER'.
3. Color Palette: Extract explicit RGB colors (three float numbers from 0.0 to 1.0) for each part based on the description.

STEP 2. CODING ARCHITECTURE & REQUISITES (STRICT RULES)
- Suppress Warnings: To prevent OS-specific warnings on headless Linux systems, include `os.environ["OCIO"] = ""` right after importing libraries.
- Scene Cleanup: The scene must be fully cleared at the very beginning of the script using `bpy.ops.object.delete(use_global=True)`.
- Material Generation: Use a clean node clearing approach without using deprecated `mat.use_nodes = True` flags.
- Component Linkage: All generated meshes must be programmatically unlinked from the base scene collection and linked to a single dedicated master collection.
- Mesh Consolidation: At the end of the mesh generation phase, ALL created sub-objects inside the custom collection must be selected, joined into a single mesh using `bpy.ops.object.join()`, and have their origin point centered to geometry bounds.
- File Exporting: The final consolidated model MUST be exported as a standard wave-front OBJ file to the exact path specified in the `EXPORT_FILEPATH` variable using `bpy.ops.wm.obj_export()`.

STEP 3. SCRIPT TEMPLATE & STRUCTURE
Generate the output code strictly adhering to the structure and syntax of the following reference template:

```python
import os
import sys
import math
import bpy

# Suppress OpenColorIO mismatch warning outputs on Linux headless environments
os.environ["OCIO"] = "" 

# 1. SCENE INITIALIZATION & CLEANUP
if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=True)

# ==============================================================================
# 2. MATERIALS GENERATION SYSTEM
# ==============================================================================
def create_material(name, color_rgb):
    #Creates a modern node-based material with an explicit RGB color tuple.
    mat = bpy.data.materials.new(name=name)
    nodes = mat.node_tree.nodes
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*color_rgb, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.8

    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

# RGB Palette Configuration (Define logical colors matching the description)
# [Example: BASE_COLOR = (0.85, 0.65, 0.55)]
# Generate all necessary material variables here...

# ==============================================================================
# 3. COLLECTION & PRIMITIVE BUILDER SETUP
# ==============================================================================
# Create a unique master collection for sorting the mesh parts
master_collection = bpy.data.collections.new("Generated_Model_Collection")
bpy.context.scene.collection.children.link(master_collection)

def create_mesh(name, location, scale, rotation, mesh_type='CUBE', material=None):
    if mesh_type == 'CUBE':
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    elif mesh_type == 'SPHERE':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=location)
    elif mesh_type == 'CYLINDER':
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1, depth=1, location=location)

    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    if rotation:
        obj.rotation_euler = rotation
    if material:
        obj.data.materials.append(material)

    # Cleanly unlink from base scene and link to our master collection
    if obj.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(obj)
    master_collection.objects.link(obj)
    return obj

# ==============================================================================
# 4. PROCEDURAL COMPONENT GENERATION (BODY PARTS & BLOCKS)
# ==============================================================================
# Strictly use the create_mesh function to instantiate parts.
# Ensure logical anchor coordinates, scales, and assigned materials.
# Example:
# main_torso = create_mesh("Torso", (0, 0, 1.4), (0.6, 0.4, 0.9), (0,0,0), 'CUBE', shirt_mat)

# ==============================================================================
# 5. CONSOLIDATION, ORIGIN BINDING & FILE EXPORT
# ==============================================================================
# Select all objects inside the collection for joining
for obj in master_collection.objects:
    obj.select_set(True)

# Define reference root target and join into a single asset
bpy.context.view_layer.objects.active = master_collection.objects[0]
bpy.ops.object.join()
active_model = bpy.context.view_layer.objects.active
active_model.name = "Final_Joined_Model"

# Center the origin point to bounds
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# Absolute Target Filepath for Exporting
EXPORT_FILEPATH = r"{save_filepath}"
os.makedirs(os.path.dirname(EXPORT_FILEPATH) or ".", exist_ok=True)

# Ensure only the final model is selected for a clean export pipeline
bpy.ops.object.select_all(action='DESELECT')
active_model.select_set(True)
bpy.context.view_layer.objects.active = active_model

# Standard universal object export
try:
    bpy.ops.wm.obj_export(filepath=EXPORT_FILEPATH)
    print(f"Model successfully generated and saved to: {{EXPORT_FILEPATH}}")
except Exception as e:
    print(f"Critical error during OBJ export: {{e}}")
    sys.exit(1)
```

STEP 4. DOUBLE CHECK CRITICAL MISTAKES
Before outputting the script, perform a final strict validation check:
- Do not add any extra conversational text outside the python code block.
- NEVER use any primitive creators other than the ones wrapped inside `create_mesh` ('CUBE', 'SPHERE', 'CYLINDER').
- All dictionary allocations and inline print structures must use double curly braces `{{` and `}}` to stay compliant with parent f-string parsing frameworks.

Provide ONLY the executable Python script wrapped inside a single ```python code block.
    """
    return ask_ai(prompt_with_instructions)


def get_detailed_prompt_by_ai(prompt) -> str:
    detailed_prompt = f""" 
        You are an expert 3D Artist and Technical Director. Your task is to transform a basic user request into a highly detailed, comprehensive, and professional prompt for a 3D generative AI or a 3D modeling briefing.

        Base User Request to expand: "{prompt}"

        Analyze the base request and generate a complete 3D asset description strictly following this structured template. Do not skip any sections. Add rich, logical details appropriate for the object type.

        1. APPEARANCE & VISUAL STYLE (The core focus)
        1.1 Pose & Orientation: Describe the exact stance, pose, or layout (e.g., standing, dynamic pose, lying down, limbs raised, head tilted, symmetrically aligned).
        1.2 Proportions & Anatomy: Specify the scale relationships. Are the proportions realistic, stylized, cartoonish, or exaggerated? (e.g., oversized mechanical arms, enlarged head, elongated sleek body).
        1.3 Surface, Materials & Textures: Detail the tactile and visual properties of every surface. Define the roughness, shininess, and material types (e.g., matte scratched metal, smooth polished obsidian, weathered grainy wood, soft emissive glowing plastics, rusted iron).
        1.4 Environment & Base: Describe the immediate surroundings or what the model is resting on (e.g., stands on a mossy cobblestone pedestal, integrated into a sci-fi metallic grid, presented on a clean studio backdrop).

        2. STRUCTURE & TECHNICAL SPECIFICATIONS
        2.1 Primary Forms & Primitives: Break down the model into its foundational geometric shapes (e.g., dominated by sharp cubic frames, organic rounded curves, interlocking cylindrical joints).
        2.2 Object Composition: Define whether it is a single mesh or a composite model. State the exact or estimated number of sub-objects/parts (e.g., "The model is composite, consisting of 6 to 10 separate logical parts, including wheels, chassis, and weapon turrets").
        2.3 Topology & Poly-Count Style: Explicitly specify the geometric complexity required: Low-Poly (performance optimized) / Medium-Poly / High-Poly (maximum detail). Mention standard styling (e.g., clean topology, smooth edge bevels, hard-surface definition).

        3. EXAMPLES FOR FORMATTING REFERENCE
        3.1 Bad Output Example: "A table."
        3.2 Good Output Example: "A long rustic wooden dining table with four sleek metallic legs. The tabletop has an organic, live-edge design with rounded corners and a smooth satin finish. The legs are made of brushed dark steel, tapering slightly toward the ground. The model is a composite asset consisting of 5 separate meshes (1 tabletop, 4 legs). Medium-Poly topology with clean holding loops on the edges."

        Generate the output for the Base User Request now, following the structure above in clear, descriptive English.
    """
    response = ask_ai(detailed_prompt)

    if response is None:
        return "Car"

    return response
