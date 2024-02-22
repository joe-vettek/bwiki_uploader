import os

import bpy
from bpy_extras.io_utils import ImportHelper

from .tool.FileHelper import readDir, getFileNameFromPath


def tga_to_png(p_in, p_out):
    for image in bpy.data.images:
        if not image.users:
            bpy.data.images.remove(image)

    img = bpy.data.images.load(p_in)
    # bpy.ops.image.open(filepath=p_in)
    # img = bpy.context.space_data.image
    print('Imported tga name: ', img.name)
    img.file_format = 'PNG'

    # 修改颜色管理设置
    color_management = bpy.context.scene.view_settings
    color_management.view_transform = 'Standard'
    color_management.look = 'None'
    color_management.exposure = 0.0
    color_management.gamma = 1.0

    img.save_render(p_out, scene=bpy.context.scene)


def fix_mtl(filepath):
    with open(filepath, "r", encoding='utf-8') as file:
        mtl_content = file.read().split('\n')
    key_map_Kd = 'map_Kd'
    for i, c in enumerate(mtl_content):
        if c.startswith(key_map_Kd):
            if c.endswith('tga') or c.endswith('TGA'):
                mtl_content[i] = mtl_content[i][:-3] + "png"
    mtl_content_out_text = "\n".join(mtl_content)
    with open(filepath, "w", encoding='utf-8') as file:
        file.write(mtl_content_out_text)


class Tga_To_Png(bpy.types.Operator, ImportHelper):
    bl_idname = "pmx_to_obj.tga_to_png"
    bl_label = "选择和开始转换"
    copy_pic: bpy.props.BoolProperty(
        name='是否清理旧图片',
        description="选择则会删除旧图片",
        default=False,
    )
    fixmtl: bpy.props.BoolProperty(
        name='是否更新同级目录下的mtl文件',
        description="选择则会将mtl材质索引更新",
        default=True,
    )

    def execute(self, context):
        print("Selected directory:", self.filepath)
        in_dir = self.filepath
        tgafiles = readDir(in_dir, "tga")
        for tga in tgafiles:
            newpath = os.path.join(in_dir, "{}.png".format(getFileNameFromPath(tga)))
            tga_to_png(tga, newpath)
            print(newpath)
            if self.copy_pic:
                os.remove(tga)
        if self.fixmtl:
            mtlfiles = readDir(in_dir, "mtl")
            for mtl in mtlfiles:
                print(mtl)
                fix_mtl(mtl)
        bpy.ops.wm.path_open(filepath=in_dir)
        return {'FINISHED'}
