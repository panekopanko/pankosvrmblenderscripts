import bpy

# All 52 ARKit blendshapes in correct naming convention+ VRMS
arkit_blendshapes = [
    # Emotions (6)
    "happy",
    "angry",
    "sad",
    "relaxed",
    "surprised",
    "neutral",

    # Visemes (5)
    "aa",
    "ih",
    "ou",
    "ee",
    "oh",

    # Blink (3)
    "blink",
    "blinkLeft",
    "blinkRight",

    # Look (4)
    "lookUp",
    "lookDown",
    "lookLeft",
    "lookRight"

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

    # Mouth blendshapes (24)
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

def create_arkit_blendshapes():
    # Get the active object
    obj = bpy.context.active_object

    # Check if an object is selected
    if obj is None:
        print("ERROR: No object selected!")
        return

    # Check if the selected object is a mesh
    if obj.type != 'MESH':
        print(f"ERROR: Selected object '{obj.name}' is not a mesh!")
        return

    # Create basis shape key if it doesn't exist
    if obj.data.shape_keys is None:
        obj.shape_key_add(name="Basis", from_mix=False)
        print(f"Created Basis shape key on '{obj.name}'")

    # Create all ARKit blendshapes
    created_count = 0
    skipped_count = 0

    for shape_name in arkit_blendshapes:
        # Check if shape key already exists
        if obj.data.shape_keys.key_blocks.get(shape_name):
            print(f"Skipped: '{shape_name}' already exists")
            skipped_count += 1
        else:
            obj.shape_key_add(name=shape_name, from_mix=False)
            print(f"Created: '{shape_name}'")
            created_count += 1

    print("\n" + "="*50)
    print(f"ARKit Blendshapes Creation Complete!")
    print(f"Object: '{obj.name}'")
    print(f"Created: {created_count} shape keys")
    print(f"Skipped: {skipped_count} (already existed)")
    print(f"Total ARKit blendshapes: {len(arkit_blendshapes)}")
    print("="*50)

# Run the script
if __name__ == "__main__":
    create_arkit_blendshapes()
