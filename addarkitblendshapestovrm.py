import bpy

# All 52 ARKit blendshapes - create them all as custom VRM expressions
# (Easier than trying to map to VRM presets which are read-only)
ARKIT_BLENDSHAPES = [
    # Eye blendshapes (14)
    "eyeBlinkLeft",
    "eyeLookDownLeft",
    "eyeLookInLeft",
    "eyeLookOutLeft",
    "eyeLookUpLeft",
    "eyeSquintLeft",
    "eyeWideLeft",
    "eyeBlinkRight",
    "eyeLookDownRight",
    "eyeLookInRight",
    "eyeLookOutRight",
    "eyeLookUpRight",
    "eyeSquintRight",
    "eyeWideRight",

    # Jaw blendshapes (4)
    "jawForward",
    "jawLeft",
    "jawRight",
    "jawOpen",

    # Mouth blendshapes (23)
    "mouthClose",
    "mouthFunnel",
    "mouthPucker",
    "mouthLeft",
    "mouthRight",
    "mouthSmileLeft",
    "mouthSmileRight",
    "mouthFrownLeft",
    "mouthFrownRight",
    "mouthDimpleLeft",
    "mouthDimpleRight",
    "mouthStretchLeft",
    "mouthStretchRight",
    "mouthRollLower",
    "mouthRollUpper",
    "mouthShrugLower",
    "mouthShrugUpper",
    "mouthPressLeft",
    "mouthPressRight",
    "mouthLowerDownLeft",
    "mouthLowerDownRight",
    "mouthUpperUpLeft",
    "mouthUpperUpRight",

    # Brow blendshapes (5)
    "browDownLeft",
    "browDownRight",
    "browInnerUp",
    "browOuterUpLeft",
    "browOuterUpRight",

    # Cheek blendshapes (3)
    "cheekPuff",
    "cheekSquintLeft",
    "cheekSquintRight",

    # Nose blendshapes (2)
    "noseSneerLeft",
    "noseSneerRight",

    # Tongue blendshape (1)
    "tongueOut"
]

def add_arkit_to_vrm_expressions():
    """
    Add all 52 ARKit blendshapes as VRM 1.0 custom expressions.
    This mimics clicking "Add Custom Expression" in the VRM plugin UI.

    Assumes:
    - An armature named "Armature" exists with VRM extension
    - VRM addon is installed and enabled
    - A mesh with ARKit shape keys exists
    """

    # Get the armature
    armature = bpy.data.armatures.get("Armature")
    if not armature:
        print("ERROR: No armature named 'Armature' found!")
        return

    # Check if VRM addon extension exists
    if not hasattr(armature, "vrm_addon_extension"):
        print("ERROR: VRM addon not found or not enabled on armature!")
        return

    vrm_extension = armature.vrm_addon_extension

    # Check if VRM 1.0 is being used
    if not hasattr(vrm_extension, "vrm1"):
        print("ERROR: VRM 1.0 not found! Make sure you're using VRM 1.0 format.")
        return

    vrm1 = vrm_extension.vrm1
    expressions = vrm1.expressions

    # Find mesh object with shape keys (don't require selection)
    mesh_obj = None
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.data.shape_keys:
            mesh_obj = obj
            break

    if not mesh_obj:
        print("ERROR: No mesh with shape keys found!")
        return

    shape_keys = mesh_obj.data.shape_keys.key_blocks

    # Track statistics
    created_count = 0
    skipped_count = 0

    print("\n" + "="*60)
    print("Adding ARKit Blendshapes as VRM Custom Expressions")
    print("="*60)

    # Add each ARKit blendshape as a custom VRM expression
    for arkit_name in ARKIT_BLENDSHAPES:
        # Check if shape key exists
        if arkit_name not in shape_keys:
            print(f"SKIP: Shape key '{arkit_name}' not found")
            skipped_count += 1
            continue

        # Check if custom expression already exists
        existing = None
        for custom in expressions.custom:
            if custom.custom_name == arkit_name:
                existing = custom
                break

        if existing:
            print(f"SKIP: Custom expression '{arkit_name}' already exists")
            skipped_count += 1
        else:
            # Create new custom expression (like clicking "Add Custom Expression")
            new_custom = expressions.custom.add()
            new_custom.custom_name = arkit_name

            # Add morph target bind (link to the shape key)
            new_bind = new_custom.morph_target_binds.add()
            new_bind.node.mesh_object_name = mesh_obj.name
            new_bind.index = str(shape_keys.find(arkit_name))
            new_bind.weight = 1.0

            print(f"CREATED: '{arkit_name}'")
            created_count += 1

    print("\n" + "="*60)
    print("VRM Expression Setup Complete!")
    print(f"Mesh: '{mesh_obj.name}'")
    print(f"Custom expressions created: {created_count}")
    print(f"Skipped (already exists or not found): {skipped_count}")
    print(f"Total ARKit shapes: {len(ARKIT_BLENDSHAPES)}")
    print("="*60)

# Run the script
if __name__ == "__main__":
    add_arkit_to_vrm_expressions()
