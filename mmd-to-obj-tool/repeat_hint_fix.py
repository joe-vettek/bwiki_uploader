import os
import re

from bpy_extras.io_utils import ImportHelper
import bpy

from .tool.FileHelper import readDir, mycopyfile


def check_last_four_characters(s):
    pattern = r'\.\d{3}$'
    if re.search(pattern, s):
        return True
    else:
        return False


def clean_repeat(filepath):
    with open(filepath, "r", encoding='utf-8') as file:
        mtl_content = file.read().split('\n')
    key_newmtl = 'newmtl'
    key_usemtl = 'usemtl'
    for i, c in enumerate(mtl_content):
        if c.startswith(key_newmtl) or c.startswith(key_usemtl):
            if check_last_four_characters(c):
                mtl_content[i] = mtl_content[i][:-4]

    mtl_content_out_text = "\n".join(mtl_content)
    with open(filepath, "w", encoding='utf-8') as file:
        file.write(mtl_content_out_text)


class Reap_Fix(bpy.types.Operator, ImportHelper):
    bl_idname = "pmx_to_obj.repeat_hint_fix"
    bl_label = "清理重复使用后缀"
    bl_description = "Blender对重复使用的资源会自动追加.00x这样的后缀"

    def execute(self, context):
        print("Selected directory:", self.filepath)
        in_dir = self.filepath
        files = readDir(in_dir, "obj")
        files.extend(readDir(in_dir, "mtl"))
        for mtl in files:
            print(mtl)
            clean_repeat(mtl)
        bpy.ops.wm.path_open(filepath=in_dir)
        return {'FINISHED'}
