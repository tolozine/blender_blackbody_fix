import bpy

bl_info = {
    "name": "Blackbody Fixer 4.2",
    "author": "tolozine",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "Node Editor > Right-Click Menu",
    "description": "Blender 4.2专用黑体节点修复工具",
    "category": "Node"
}

class NODE_OT_fix_blackbody(bpy.types.Operator):
    bl_idname = "node.fix_blackbody_42"
    bl_label = "Fix Blackbody (4.2)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'NODE_EDITOR'

    def execute(self, context):
        count = 0
        
        for obj in context.visible_objects:
            if obj.type == 'LIGHT':
                self.fix_light(obj.data)
            elif obj.type == 'MESH' and obj.data.materials:
                for mat in obj.data.materials:
                    self.fix_material(mat)
        
        self.report({'INFO'}, f"Fixed {count} nodes")
        return {'FINISHED'}

    def fix_light(self, light):
        if not light.use_nodes:
            return
        
        for node in light.node_tree.nodes:
            if node.bl_idname == 'ShaderNodeBlackbody':
                self.fix_blackbody_node(node)

    def fix_material(self, mat):
        if not mat.use_nodes:
            return
        
        for node in mat.node_tree.nodes:
            if node.bl_idname == 'ShaderNodeBlackbody':
                self.fix_blackbody_node(node)

    def fix_blackbody_node(self, node):
        try:
            # 4.2专属属性访问
            if hasattr(node, "temperature"):
                temp = node.temperature
            else:
                temp = 6500.0
            
            # 创建新节点
            new_node = node.id_data.nodes.new('ShaderNodeBlackbody')
            new_node.location = node.location
            new_node.temperature = temp

            # 转移链接
            for link in node.outputs[0].links:
                node.id_data.links.new(new_node.outputs[0], link.to_socket)
            
            # 删除旧节点
            node.id_data.nodes.remove(node)
            print(f"Fixed: {node.name} -> {temp}K")
            count += 1

        except Exception as e:
            print(f"Error fixing node: {str(e)}")

def menu_func(self, context):
    self.layout.operator(NODE_OT_fix_blackbody.bl_idname)

def register():
    bpy.utils.register_class(NODE_OT_fix_blackbody)
    bpy.types.NODE_MT_node.append(menu_func)
    print("Blackbody Fixer 4.2 registered")

def unregister():
    bpy.utils.unregister_class(NODE_OT_fix_blackbody)
    bpy.types.NODE_MT_node.remove(menu_func)
    print("Blackbody Fixer 4.2 unregistered")

if __name__ == "__main__":
    register()