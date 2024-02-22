import os

from bpy_extras.io_utils import ImportHelper
import bpy

from .tool.FileHelper import readDir, mycopyfile

klbq_file_path = "https://wiki.biligame.com/klbq/Special:FilePath/"


def fix_mtl(filepath, pic_dir, copy_pic=True):
    copy_path = os.path.dirname(filepath)
    with open(filepath, "r", encoding='utf-8') as file:
        mtl_content = file.read().split('\n')
    key_map_Kd = 'map_Kd'
    for i, c in enumerate(mtl_content):
        if c.startswith(key_map_Kd):
            pic_path = c[len(key_map_Kd) + 1:]
            pic_name = os.path.basename(pic_path)
            if copy_pic:
                dst_path = os.path.join(copy_path, pic_name)
                # 如何没有重复名字的字
                if not os.path.exists(dst_path):
                    mycopyfile(pic_path, dst_path)
                else:
                    print(filepath, pic_name, "发现命名重复，取消复制")

            mtl_content[i] = key_map_Kd + " " + pic_dir + pic_name

    mtl_content_out_text = "\n".join(mtl_content)
    with open(filepath, "w", encoding='utf-8') as file:
        file.write(mtl_content_out_text)


class OP_MTL_FIX(bpy.types.Operator, ImportHelper):
    bl_idname = "pmx_to_obj.klbq_mtl_fix"
    bl_label = "修复卡拉彼丘材质信息"
    copy_pic: bpy.props.BoolProperty(
        name='是否复制图片',
        description="选择则会自动将图片复制到目录下",
        default=True,
    )
    pic_dir: bpy.props.StringProperty(
        name='设置图片地址前缀',
        description="",
        default=klbq_file_path,
    )

    def execute(self, context):
        print("Selected directory:", self.filepath)
        in_dir = self.filepath
        mtlfiles = readDir(in_dir, "mtl")
        for mtl in mtlfiles:
            print(mtl)
            fix_mtl(mtl, self.pic_dir, self.copy_pic)
        bpy.ops.wm.path_open(filepath=in_dir)
        return {'FINISHED'}
