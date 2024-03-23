bl_info = {
    "name": "Move Strips Up and Down",
    "version": (1, 0, 0),
    "author": "GameDirection",
    "blender": (4, 0, 0),
    "category": "Sequencer",
    "description": "Move selected strips up and down channels in the VSE."
}

import bpy

def move_strip(strip, direction):
    """Move a strip up or down to the next available channel."""
    sequences = bpy.context.sequences
    max_channel = max(s.channel for s in sequences) if sequences else 1
    if direction == 'UP':
        target_channel = strip.channel + 1
        while any(s.channel == target_channel and s.frame_final_start < strip.frame_final_end and s.frame_final_end > strip.frame_start for s in sequences):
            target_channel += 1
        strip.channel = min(target_channel, max_channel)
    elif direction == 'DOWN':
        target_channel = strip.channel - 1
        while any(s.channel == target_channel and s.frame_final_start < strip.frame_final_end and s.frame_final_end > strip.frame_start for s in sequences):
            target_channel -= 1
        strip.channel = max(target_channel, 1)

class MoveStripsOperator(bpy.types.Operator):
    """Move selected strips up or down."""
    bl_idname = "sequencer.move_strips_operator"
    bl_label = "Move Selected Strips"
    direction: bpy.props.StringProperty()

    def execute(self, context):
        sequences = context.scene.sequence_editor.sequences_all
        for strip in sequences:
            if strip.select:
                move_strip(strip, self.direction)
        return {'FINISHED'}

def draw_func(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator(MoveStripsOperator.bl_idname, icon='TRIA_UP', text="").direction = 'UP'
    row.operator(MoveStripsOperator.bl_idname, icon='TRIA_DOWN', text="").direction = 'DOWN'

def register():
    bpy.utils.register_class(MoveStripsOperator)
    bpy.types.SEQUENCER_HT_header.append(draw_func)  # Adjusted for Blender 4.0.0, targeting the header for button placement.

def unregister():
    bpy.utils.unregister_class(MoveStripsOperator)
    bpy.types.SEQUENCER_HT_header.remove(draw_func)

if __name__ == "__main__":
    register()