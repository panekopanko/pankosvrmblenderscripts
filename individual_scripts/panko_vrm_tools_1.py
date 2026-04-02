bl_info = {
    "name": "Panko's VRM Blendshape Tools",
    "author": "Panko (Addon by Claude)",
    "version": (2, 1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > VRM Tools",
    "description": "Collection of tools for managing ARKit blendshapes, custom expressions, and VRM setup",
    "warning": "",
    "doc_url": "https://github.com/panekopanko/pankosvrmblenderscripts",
    "category": "Rigging",
}

import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty, CollectionProperty, IntProperty

# All 52 ARKit blendshapes
ARKIT_BLENDSHAPES = [
    # Eye blendshapes (14)
    "eyeBlinkLeft", "eyeLookDownLeft", "eyeLookInLeft", "eyeLookOutLeft",
    "eyeLookUpLeft", "eyeSquintLeft", "eyeWideLeft",
    "eyeBlinkRight", "eyeLookDownRight", "eyeLookInRight", "eyeLookOutRight",
    "eyeLookUpRight", "eyeSquintRight", "eyeWideRight",
    # Jaw blendshapes (4)
    "jawForward", "jawLeft", "jawRight", "jawOpen",
    # Mouth blendshapes (23)
    "mouthClose", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight",
    "mouthSmileLeft", "mouthSmileRight", "mouthFrownLeft", "mouthFrownRight",
    "mouthDimpleLeft", "mouthDimpleRight", "mouthStretchLeft", "mouthStretchRight",
    "mouthRollLower", "mouthRollUpper", "mouthShrugLower", "mouthShrugUpper",
    "mouthPressLeft", "mouthPressRight", "mouthLowerDownLeft", "mouthLowerDownRight",
    "mouthUpperUpLeft", "mouthUpperUpRight",
    # Brow blendshapes (5)
    "browDownLeft", "browDownRight", "browInnerUp", "browOuterUpLeft", "browOuterUpRight",
    # Cheek blendshapes (3)
    "cheekPuff", "cheekSquintLeft", "cheekSquintRight",
    # Nose blendshapes (2)
    "noseSneerLeft", "noseSneerRight",
    # Tongue blendshape (1)
    "tongueOut"
]

# ARKit + VRM blendshapes for extended list
ARKIT_VRM_BLENDSHAPES = [
    # VRM Emotions (6)
    "happy", "angry", "sad", "relaxed", "surprised", "neutral",
    # VRM Visemes (5)
    "aa", "ih", "ou", "ee", "oh",
    # VRM Blink (3)
    "blink", "blinkLeft", "blinkRight",
    # VRM Look (4)
    "lookUp", "lookDown", "lookLeft", "lookRight",
] + ARKIT_BLENDSHAPES


# ==================== UTILITY FUNCTIONS ====================
def get_vrm_armature_and_extension():
    """
    Helper function to get VRM armature and extension.
    Returns: (armature_data, armature_obj, vrm_extension) or (None, None, None) if not found
    """
    armature = bpy.data.armatures.get("Armature")
    if not armature:
        return None, None, None

    if not hasattr(armature, "vrm_addon_extension"):
        return None, None, None

    vrm_extension = armature.vrm_addon_extension

    if not hasattr(vrm_extension, "vrm1"):
        return None, None, None

    # Find armature object
    armature_obj = None
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE' and obj.data == armature:
            armature_obj = obj
            break

    return armature, armature_obj, vrm_extension


# ==================== OPERATOR 1: Create ARKit Blendshapes ====================
class PANKO_OT_CreateARKitBlendshapes(Operator):
    """Create all 52 ARKit blendshapes on the selected mesh"""
    bl_idname = "panko.create_arkit_blendshapes"
    bl_label = "Create ARKit Blendshapes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object

        if obj.data.shape_keys is None:
            obj.shape_key_add(name="Basis", from_mix=False)
            self.report({'INFO'}, f"Created Basis shape key on '{obj.name}'")

        created_count = 0
        skipped_count = 0

        for shape_name in ARKIT_BLENDSHAPES:
            if obj.data.shape_keys.key_blocks.get(shape_name):
                skipped_count += 1
            else:
                obj.shape_key_add(name=shape_name, from_mix=False)
                created_count += 1

        self.report({'INFO'}, f"Created {created_count} ARKit blendshapes, skipped {skipped_count}")
        return {'FINISHED'}


# ==================== OPERATOR 2: Create ARKit + VRM Blendshapes ====================
class PANKO_OT_CreateARKitVRMBlendshapes(Operator):
    """Create all ARKit + VRM blendshapes (52 ARKit + VRM presets)"""
    bl_idname = "panko.create_arkit_vrm_blendshapes"
    bl_label = "Create ARKit + VRM Blendshapes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object

        if obj.data.shape_keys is None:
            obj.shape_key_add(name="Basis", from_mix=False)

        created_count = 0
        skipped_count = 0

        for shape_name in ARKIT_VRM_BLENDSHAPES:
            if obj.data.shape_keys.key_blocks.get(shape_name):
                skipped_count += 1
            else:
                obj.shape_key_add(name=shape_name, from_mix=False)
                created_count += 1

        self.report({'INFO'}, f"Created {created_count} blendshapes, skipped {skipped_count}")
        return {'FINISHED'}


# ==================== OPERATOR 3: Add ARKit to VRM Expressions ====================
class PANKO_OT_AddARKitToVRMExpressions(Operator):
    """Add all 52 ARKit blendshapes as VRM 1.0 custom expressions"""
    bl_idname = "panko.add_arkit_to_vrm"
    bl_label = "Add ARKit to VRM Expressions"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        armature, armature_obj, vrm_ext = get_vrm_armature_and_extension()
        if armature is None:
            return False
        # Check if any mesh has shape keys
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.data.shape_keys:
                return True
        return False

    def execute(self, context):
        armature, armature_obj, vrm_extension = get_vrm_armature_and_extension()

        if not armature:
            self.report({'ERROR'}, "VRM armature setup not found!")
            return {'CANCELLED'}

        vrm1 = vrm_extension.vrm1
        expressions = vrm1.expressions

        mesh_obj = None
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.data.shape_keys:
                mesh_obj = obj
                break

        if not mesh_obj:
            self.report({'ERROR'}, "No mesh with shape keys found!")
            return {'CANCELLED'}

        shape_keys = mesh_obj.data.shape_keys.key_blocks

        created_count = 0
        skipped_count = 0

        for arkit_name in ARKIT_BLENDSHAPES:
            if arkit_name not in shape_keys:
                skipped_count += 1
                continue

            existing = None
            for custom in expressions.custom:
                if custom.custom_name == arkit_name:
                    existing = custom
                    break

            if existing:
                skipped_count += 1
            else:
                new_custom = expressions.custom.add()
                new_custom.custom_name = arkit_name

                new_bind = new_custom.morph_target_binds.add()
                new_bind.node.mesh_object_name = mesh_obj.name
                new_bind.index = str(shape_keys.find(arkit_name))
                new_bind.weight = 1.0

                created_count += 1

        self.report({'INFO'}, f"Created {created_count} VRM expressions, skipped {skipped_count}")
        return {'FINISHED'}


# ==================== OPERATOR 4: Assign Blendshapes to Proxies ====================
class PANKO_OT_AssignBlendshapesToProxies(Operator):
    """Assign all ARKit shape keys to their corresponding VRM custom expressions"""
    bl_idname = "panko.assign_blendshapes_proxies"
    bl_label = "Assign Blendshapes to Proxies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        armature, armature_obj, vrm_ext = get_vrm_armature_and_extension()
        if armature is None or armature_obj is None:
            return False
        # Check if any mesh has shape keys
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.data.shape_keys:
                return True
        return False

    def execute(self, context):
        armature, armature_obj, vrm_extension = get_vrm_armature_and_extension()

        if not armature or not armature_obj:
            self.report({'ERROR'}, "VRM armature setup not found!")
            return {'CANCELLED'}

        vrm1 = vrm_extension.vrm1
        expressions = vrm1.expressions

        mesh_obj = None
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.data.shape_keys:
                mesh_obj = obj
                break

        if not mesh_obj:
            self.report({'ERROR'}, "No mesh with shape keys found!")
            return {'CANCELLED'}

        shape_keys = mesh_obj.data.shape_keys.key_blocks

        assigned_count = 0
        skipped_count = 0

        for arkit_name in ARKIT_BLENDSHAPES:
            if arkit_name not in shape_keys:
                skipped_count += 1
                continue

            expression_found = None
            for custom in expressions.custom:
                if custom.custom_name == arkit_name:
                    expression_found = custom
                    break

            if not expression_found:
                skipped_count += 1
                continue

            if len(expression_found.morph_target_binds) > 0:
                existing_bind = expression_found.morph_target_binds[0]
                if existing_bind.index == arkit_name:
                    skipped_count += 1
                    continue

            try:
                bpy.ops.vrm.add_vrm1_expression_morph_target_bind(
                    armature_object_name=armature_obj.name,
                    expression_name=arkit_name
                )

                if len(expression_found.morph_target_binds) > 0:
                    new_bind = expression_found.morph_target_binds[-1]
                    new_bind.node.bpy_object = mesh_obj
                    new_bind.index = arkit_name
                    assigned_count += 1
                else:
                    skipped_count += 1

            except Exception as e:
                skipped_count += 1

        self.report({'INFO'}, f"Assigned {assigned_count} binds, skipped {skipped_count}")
        return {'FINISHED'}


# ==================== OPERATOR 5: Assign Selected Mesh Blendshapes to Proxies ====================
class PANKO_OT_AssignSelectedMeshBlendshapesToProxies(Operator):
    """Assign ARKit shape keys from the active mesh to matching VRM 1.0 custom expressions"""
    bl_idname = "panko.assign_selected_mesh_proxies"
    bl_label = "Assign Selected Mesh to Proxies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        armature, armature_obj, vrm_ext = get_vrm_armature_and_extension()
        if armature is None or armature_obj is None:
            return False
        obj = context.active_object
        return (obj is not None and
                obj.type == 'MESH' and
                obj.data.shape_keys is not None)

    def execute(self, context):
        mesh_obj = context.active_object
        shape_keys = mesh_obj.data.shape_keys.key_blocks

        armature, armature_obj, vrm_ext = get_vrm_armature_and_extension()

        if not armature or not armature_obj:
            self.report({'ERROR'}, "VRM armature setup not found!")
            return {'CANCELLED'}

        expressions = vrm_ext.vrm1.expressions

        assigned = 0
        skipped = 0

        for arkit_name in ARKIT_BLENDSHAPES:
            if arkit_name not in shape_keys:
                skipped += 1
                continue

            expression = next(
                (e for e in expressions.custom if e.custom_name == arkit_name),
                None
            )

            if not expression:
                skipped += 1
                continue

            if any(
                b.node.bpy_object == mesh_obj and b.index == arkit_name
                for b in expression.morph_target_binds
            ):
                skipped += 1
                continue

            try:
                bpy.ops.vrm.add_vrm1_expression_morph_target_bind(
                    armature_object_name=armature_obj.name,
                    expression_name=arkit_name,
                )

                bind = expression.morph_target_binds[-1]
                bind.node.bpy_object = mesh_obj
                bind.index = arkit_name

                assigned += 1

            except Exception:
                skipped += 1

        self.report({'INFO'}, f"Assigned {assigned} from selected mesh, skipped {skipped}")
        return {'FINISHED'}


# ==================== OPERATOR 6: Add Custom Blendshape ====================
class PANKO_OT_AddCustomBlendshape(Operator):
    """Add a single custom blendshape with a custom name"""
    bl_idname = "panko.add_custom_blendshape"
    bl_label = "Add Custom Blendshape"
    bl_options = {'REGISTER', 'UNDO'}

    shape_name: StringProperty(
        name="Shape Name",
        description="Name for the custom blendshape",
        default="custom_expression"
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "shape_name")

    def execute(self, context):
        obj = context.active_object

        if not self.shape_name or self.shape_name.strip() == "":
            self.report({'ERROR'}, "Shape name cannot be empty!")
            return {'CANCELLED'}

        # Clean the name (remove leading/trailing spaces)
        clean_name = self.shape_name.strip()

        # Create Basis if it doesn't exist
        if obj.data.shape_keys is None:
            obj.shape_key_add(name="Basis", from_mix=False)

        # Check if shape key already exists
        if obj.data.shape_keys.key_blocks.get(clean_name):
            self.report({'WARNING'}, f"Shape key '{clean_name}' already exists!")
            return {'CANCELLED'}

        # Create the shape key
        obj.shape_key_add(name=clean_name, from_mix=False)
        self.report({'INFO'}, f"Created custom blendshape: '{clean_name}'")

        return {'FINISHED'}


# ==================== OPERATOR 7: Add Multiple Custom Blendshapes ====================
class PANKO_OT_AddMultipleCustomBlendshapes(Operator):
    """Add multiple custom blendshapes at once (comma-separated names)"""
    bl_idname = "panko.add_multiple_custom_blendshapes"
    bl_label = "Add Multiple Custom Blendshapes"
    bl_options = {'REGISTER', 'UNDO'}

    shape_names: StringProperty(
        name="Shape Names",
        description="Comma-separated list of shape names (e.g. 'smirk, wink, pout')",
        default=""
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Enter comma-separated shape names:")
        layout.prop(self, "shape_names", text="")
        layout.label(text="Example: smirk, wink, pout, angry_brows", icon='INFO')

    def execute(self, context):
        obj = context.active_object

        if not self.shape_names or self.shape_names.strip() == "":
            self.report({'ERROR'}, "Shape names cannot be empty!")
            return {'CANCELLED'}

        # Create Basis if it doesn't exist
        if obj.data.shape_keys is None:
            obj.shape_key_add(name="Basis", from_mix=False)

        # Parse the comma-separated names
        names = [name.strip() for name in self.shape_names.split(',') if name.strip()]

        if not names:
            self.report({'ERROR'}, "No valid shape names provided!")
            return {'CANCELLED'}

        created_count = 0
        skipped_count = 0

        for name in names:
            # Check if shape key already exists
            if obj.data.shape_keys.key_blocks.get(name):
                skipped_count += 1
                continue

            # Create the shape key
            obj.shape_key_add(name=name, from_mix=False)
            created_count += 1

        self.report({'INFO'}, f"Created {created_count} custom blendshapes, skipped {skipped_count}")
        return {'FINISHED'}


# ==================== OPERATOR 8: Add Custom Blendshape to VRM ====================
class PANKO_OT_AddCustomBlendshapeToVRM(Operator):
    """Add a custom blendshape to VRM expressions"""
    bl_idname = "panko.add_custom_blendshape_to_vrm"
    bl_label = "Add Custom Shape to VRM"
    bl_options = {'REGISTER', 'UNDO'}

    shape_name: StringProperty(
        name="Shape Key Name",
        description="Name of the shape key to add to VRM",
        default=""
    )

    @classmethod
    def poll(cls, context):
        armature, armature_obj, vrm_ext = get_vrm_armature_and_extension()
        if armature is None:
            return False
        obj = context.active_object
        return (obj is not None and
                obj.type == 'MESH' and
                obj.data.shape_keys is not None)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        layout.label(text="Select shape key to add to VRM:")

        if obj and obj.data.shape_keys:
            # Show available shape keys
            layout.prop_search(self, "shape_name", obj.data.shape_keys, "key_blocks", text="Shape Key")
        else:
            layout.prop(self, "shape_name")

    def execute(self, context):
        if not self.shape_name or self.shape_name.strip() == "":
            self.report({'ERROR'}, "Shape name cannot be empty!")
            return {'CANCELLED'}

        mesh_obj = context.active_object
        armature, armature_obj, vrm_extension = get_vrm_armature_and_extension()

        if not armature or not armature_obj:
            self.report({'ERROR'}, "VRM armature setup not found!")
            return {'CANCELLED'}

        vrm1 = vrm_extension.vrm1
        expressions = vrm1.expressions
        shape_keys = mesh_obj.data.shape_keys.key_blocks

        # Check if shape key exists
        if self.shape_name not in shape_keys:
            self.report({'ERROR'}, f"Shape key '{self.shape_name}' not found!")
            return {'CANCELLED'}

        # Check if custom expression already exists
        for custom in expressions.custom:
            if custom.custom_name == self.shape_name:
                self.report({'WARNING'}, f"VRM expression '{self.shape_name}' already exists!")
                return {'CANCELLED'}

        # Create new custom expression
        new_custom = expressions.custom.add()
        new_custom.custom_name = self.shape_name

        # Add morph target bind
        new_bind = new_custom.morph_target_binds.add()
        new_bind.node.mesh_object_name = mesh_obj.name
        new_bind.index = str(shape_keys.find(self.shape_name))
        new_bind.weight = 1.0

        # Try to assign binding using VRM operator
        try:
            bpy.ops.vrm.add_vrm1_expression_morph_target_bind(
                armature_object_name=armature_obj.name,
                expression_name=self.shape_name
            )

            if len(new_custom.morph_target_binds) > 0:
                bind = new_custom.morph_target_binds[-1]
                bind.node.bpy_object = mesh_obj
                bind.index = self.shape_name
        except Exception as e:
            pass  # Basic binding already done above

        self.report({'INFO'}, f"Added '{self.shape_name}' to VRM expressions")
        return {'FINISHED'}


# ==================== OPERATOR 9: Reset Blendshapes ====================
class PANKO_OT_ResetBlendshapes(Operator):
    """Reset all shape key values to 0"""
    bl_idname = "panko.reset_blendshapes"
    bl_label = "Reset Blendshapes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and
                obj.type == 'MESH' and
                obj.data.shape_keys is not None)

    def execute(self, context):
        obj = context.active_object

        reset_count = 0

        for shape_key in obj.data.shape_keys.key_blocks:
            if shape_key.name == "Basis":
                continue

            shape_key.value = 0.0
            reset_count += 1

        self.report({'INFO'}, f"Reset {reset_count} blendshapes to 0")
        return {'FINISHED'}


# ==================== UI PANEL ====================
class PANKO_PT_VRMToolsPanel(Panel):
    """Creates a Panel in the 3D Viewport sidebar"""
    bl_label = "Panko's VRM Tools"
    bl_idname = "PANKO_PT_vrm_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VRM Tools'

    def draw(self, context):
        layout = self.layout

        # Header
        box = layout.box()
        box.label(text="Blendshape Creation", icon='SHAPEKEY_DATA')
        box.operator("panko.create_arkit_blendshapes", icon='ADD')
        box.operator("panko.create_arkit_vrm_blendshapes", icon='ADD')

        # Custom Blendshapes Section
        box = layout.box()
        box.label(text="Custom Blendshapes", icon='EDITMODE_HLT')
        box.operator("panko.add_custom_blendshape", icon='SOLO_ON')
        box.operator("panko.add_multiple_custom_blendshapes", icon='PRESET_NEW')

        # VRM Expression Tools
        box = layout.box()
        box.label(text="VRM Expression Setup", icon='ARMATURE_DATA')
        box.operator("panko.add_arkit_to_vrm", icon='EXPORT')
        box.operator("panko.add_custom_blendshape_to_vrm", icon='PLUS')

        # Assignment Tools
        box = layout.box()
        box.label(text="Assign to VRM Proxies", icon='LINKED')
        box.operator("panko.assign_blendshapes_proxies", icon='CONSTRAINT')
        box.operator("panko.assign_selected_mesh_proxies", icon='MESH_DATA')

        # Utilities
        box = layout.box()
        box.label(text="Utilities", icon='TOOL_SETTINGS')
        box.operator("panko.reset_blendshapes", icon='LOOP_BACK')


# ==================== REGISTRATION ====================
classes = (
    PANKO_OT_CreateARKitBlendshapes,
    PANKO_OT_CreateARKitVRMBlendshapes,
    PANKO_OT_AddCustomBlendshape,
    PANKO_OT_AddMultipleCustomBlendshapes,
    PANKO_OT_AddARKitToVRMExpressions,
    PANKO_OT_AddCustomBlendshapeToVRM,
    PANKO_OT_AssignBlendshapesToProxies,
    PANKO_OT_AssignSelectedMeshBlendshapesToProxies,
    PANKO_OT_ResetBlendshapes,
    PANKO_PT_VRMToolsPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
