import bpy


class SimplePanel(bpy.types.Panel):
    bl_label = "让我们开始吧"
    bl_idname = "OBJECT_PT_pmx_to_obj"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMD To OBJ"

    def draw(self, context):
        layout = self.layout
        layout.operator("pmx_to_obj.start", text="打开目录并开始批量转换", icon="GHOST_ENABLED")
        layout.operator("pmx_to_obj.klbq_mtl_fix", text="修复卡拉彼丘模型的材质信息", icon="OPTIONS")
        layout.operator("pmx_to_obj.repeat_hint_fix", text="清理OBJ模型资源重复使用后缀", icon="UNLINKED")
        layout.operator("pmx_to_obj.tga_to_png", text="批量转换指定目录TGA", icon="COLOR")


class hellowe(bpy.types.Panel):
    bl_label = "让我们开始玩吧"
    bl_idname = "OBJECT_PT_tga_to_png"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "TGA To PNG"

    def draw(self, context):
        layout = self.layout
        layout.operator("pmx_to_obj.tga_to_png", text="批量转换指定目录TGA", icon="COLOR")
