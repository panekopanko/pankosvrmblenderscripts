import bpy

# ------------------------------------------------------------
# All 52 ARKit blendshapes
# ------------------------------------------------------------

ARKIT_BLENDSHAPES = [
    # Eyes
    "eyeBlinkLeft", "eyeLookDownLeft", "eyeLookInLeft", "eyeLookOutLeft",
    "eyeLookUpLeft", "eyeSquintLeft", "eyeWideLeft",
    "eyeBlinkRight", "eyeLookDownRight", "eyeLookInRight", "eyeLookOutRight",
    "eyeLookUpRight", "eyeSquintRight", "eyeWideRight",

    # Jaw
    "jawForward", "jawLeft", "jawRight", "jawOpen",

    # Mouth
    "mouthClose", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight",
    "mouthSmileLeft", "mouthSmileRight",
    "mouthFrownLeft", "mouthFrownRight",
    "mouthDimpleLeft", "mouthDimpleRight",
    "mouthStretchLeft", "mouthStretchRight",
    "mouthRollLower", "mouthRollUpper",
    "mouthShrugLower", "mouthShrugUpper",
    "mouthPressLeft", "mouthPressRight",
    "mouthLowerDownLeft", "mouthLowerDownRight",
    "mouthUpperUpLeft", "mouthUpperUpRight",

    # Brows
    "browDownLeft", "browDownRight", "browInnerUp",
    "browOuterUpLeft", "browOuterUpRight",

    # Cheeks
    "cheekPuff", "cheekSquintLeft", "cheekSquintRight",

    # Nose
    "noseSneerLeft", "noseSneerRight",

    # Tongue
    "tongueOut",
]


# ------------------------------------------------------------
# Main Function
# ------------------------------------------------------------

def assign_arkit_morph_binds_selected():
    """
    Blender 5.0 compatible

    Assign ARKit shape keys from the ACTIVE mesh
    to matching VRM 1.0 custom expressions.

    Assumes:
    - Active object is a mesh with ARKit shape keys
    - An armature object named "Armature"
    - VRM 1.0 addon installed
    - Custom expressions already created with ARKit names
    """

    # --------------------------------------------------------
    # Validate selected mesh
    # --------------------------------------------------------

    mesh_obj = bpy.context.active_object
    if not mesh_obj or mesh_obj.type != 'MESH':
        print("ERROR: Active object must be a mesh")
        return

    if not mesh_obj.data.shape_keys:
        print(f"ERROR: Mesh '{mesh_obj.name}' has no shape keys")
        return

    shape_keys = mesh_obj.data.shape_keys.key_blocks

    print(f"Using mesh: {mesh_obj.name}")

    # --------------------------------------------------------
    # Find armature object (preferred in Blender 5.0)
    # --------------------------------------------------------

    armature_obj = bpy.data.objects.get("Armature")
    if not armature_obj or armature_obj.type != 'ARMATURE':
        print("ERROR: Armature object named 'Armature' not found")
        return

    armature_data = armature_obj.data

    # --------------------------------------------------------
    # VRM 1.0 validation
    # --------------------------------------------------------

    if not hasattr(armature_data, "vrm_addon_extension"):
        print("ERROR: VRM addon not found on armature")
        return

    vrm_ext = armature_data.vrm_addon_extension

    if not hasattr(vrm_ext, "vrm1"):
        print("ERROR: VRM 1.0 data not found")
        return

    expressions = vrm_ext.vrm1.expressions

    # --------------------------------------------------------
    # Assignment loop
    # --------------------------------------------------------

    assigned = 0
    skipped = 0

    print("\n" + "=" * 60)
    print("Assigning ARKit Shape Keys → VRM 1.0 Expressions")
    print("=" * 60)

    for arkit_name in ARKIT_BLENDSHAPES:

        # Shape key check
        if arkit_name not in shape_keys:
            print(f"SKIP: Missing shape key '{arkit_name}'")
            skipped += 1
            continue

        # Find matching custom expression
        expression = next(
            (e for e in expressions.custom if e.custom_name == arkit_name),
            None
        )

        if not expression:
            print(f"SKIP: Missing custom expression '{arkit_name}'")
            skipped += 1
            continue

        # Prevent duplicate binds
        if any(
            b.node.bpy_object == mesh_obj and b.index == arkit_name
            for b in expression.morph_target_binds
        ):
            print(f"SKIP: Already assigned '{arkit_name}'")
            skipped += 1
            continue

        # ----------------------------------------------------
        # Add bind via VRM operator
        # ----------------------------------------------------

        try:
            bpy.ops.vrm.add_vrm1_expression_morph_target_bind(
                armature_object_name=armature_obj.name,
                expression_name=arkit_name,
            )

            bind = expression.morph_target_binds[-1]
            bind.node.bpy_object = mesh_obj
            bind.index = arkit_name

            print(f"ASSIGNED: {arkit_name}")
            assigned += 1

        except Exception as exc:
            print(f"ERROR: {arkit_name} → {exc}")
            skipped += 1

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("Completed")
    print(f"Mesh: {mesh_obj.name}")
    print(f"Armature: {armature_obj.name}")
    print(f"Assigned: {assigned}")
    print(f"Skipped: {skipped}")
    print(f"Total ARKit shapes: {len(ARKIT_BLENDSHAPES)}")
    print("=" * 60)


# ------------------------------------------------------------
# Run
# ------------------------------------------------------------

if __name__ == "__main__":
    assign_arkit_morph_binds_selected()

