import bpy

def reset_all_blendshapes():
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

    # Check if object has shape keys
    if obj.data.shape_keys is None:
        print(f"ERROR: Object '{obj.name}' has no shape keys!")
        return

    # Reset all shape keys to 0
    reset_count = 0

    for shape_key in obj.data.shape_keys.key_blocks:
        # Skip the Basis shape key (it doesn't have a value)
        if shape_key.name == "Basis":
            continue

        # Set value to 0
        shape_key.value = 0.0
        print(f"Reset: '{shape_key.name}' → 0.0")
        reset_count += 1

    print("\n" + "="*50)
    print(f"Blendshapes Reset Complete!")
    print(f"Object: '{obj.name}'")
    print(f"Reset: {reset_count} blendshapes to 0%")
    print("="*50)

# Run the script
if __name__ == "__main__":
    reset_all_blendshapes()
                            
