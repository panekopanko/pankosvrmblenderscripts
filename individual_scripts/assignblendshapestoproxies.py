import bpy

# All 52 ARKit blendshapes
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

def assign_arkit_morph_binds():
    """
    Assigns all ARKit shape keys to their corresponding VRM custom expressions.
    Uses the VRM operator to add morph target binds, then sets the shape key index.

    Assumes:
    - Armature named "Armature" with VRM extension
    - Custom expressions already created with matching ARKit names
    - Mesh with ARKit shape keys exists
    """

    # Get the armature
    armature = bpy.data.armatures.get("Armature")
    if not armature:
        print("ERROR: No armature named 'Armature' found!")
        return

    # Check VRM extension
    if not hasattr(armature, "vrm_addon_extension"):
        print("ERROR: VRM addon not found on armature!")
        return

    vrm_extension = armature.vrm_addon_extension

    if not hasattr(vrm_extension, "vrm1"):
        print("ERROR: VRM 1.0 not found!")
        return

    vrm1 = vrm_extension.vrm1
    expressions = vrm1.expressions

    # Find mesh with shape keys
    mesh_obj = None
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.data.shape_keys:
            mesh_obj = obj
            break

    if not mesh_obj:
        print("ERROR: No mesh with shape keys found!")
        return

    shape_keys = mesh_obj.data.shape_keys.key_blocks

    # Find the armature object (not just the armature data)
    armature_obj = None
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE' and obj.data == armature:
            armature_obj = obj
            break

    if not armature_obj:
        print("ERROR: No armature object found!")
        return

    # Track statistics
    assigned_count = 0
    skipped_count = 0

    print("\n" + "="*60)
    print("Assigning ARKit Shape Keys to VRM Expression Binds")
    print("="*60)

    # Process each ARKit blendshape
    for arkit_name in ARKIT_BLENDSHAPES:
        # Check if shape key exists
        if arkit_name not in shape_keys:
            print(f"SKIP: Shape key '{arkit_name}' not found")
            skipped_count += 1
            continue

        # Find matching custom expression
        expression_found = None
        for custom in expressions.custom:
            if custom.custom_name == arkit_name:
                expression_found = custom
                break

        if not expression_found:
            print(f"SKIP: Custom expression '{arkit_name}' not found")
            skipped_count += 1
            continue

        # Check if bind already exists
        if len(expression_found.morph_target_binds) > 0:
            # Check if it's already assigned to this shape key
            existing_bind = expression_found.morph_target_binds[0]
            if existing_bind.index == arkit_name:
                print(f"SKIP: '{arkit_name}' already assigned")
                skipped_count += 1
                continue

        # Add morph target bind using VRM operator
        try:
            bpy.ops.vrm.add_vrm1_expression_morph_target_bind(
                armature_object_name=armature_obj.name,
                expression_name=arkit_name
            )

            # Get the newly added bind (should be the last one)
            if len(expression_found.morph_target_binds) > 0:
                new_bind = expression_found.morph_target_binds[-1]

                # Set the mesh object and shape key index
                new_bind.node.bpy_object = mesh_obj
                new_bind.index = arkit_name

                print(f"ASSIGNED: '{arkit_name}' -> shape key '{arkit_name}'")
                assigned_count += 1
            else:
                print(f"ERROR: Failed to create bind for '{arkit_name}'")
                skipped_count += 1

        except Exception as e:
            print(f"ERROR: Failed to assign '{arkit_name}': {e}")
            skipped_count += 1

    print("\n" + "="*60)
    print("Morph Target Bind Assignment Complete!")
    print(f"Mesh: '{mesh_obj.name}'")
    print(f"Armature: '{armature_obj.name}'")
    print(f"Shape keys assigned: {assigned_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total ARKit shapes: {len(ARKIT_BLENDSHAPES)}")
    print("="*60)

# Run the script
if __name__ == "__main__":
    assign_arkit_morph_binds()
                              
