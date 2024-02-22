from .tool.FileHelper import readDir, getFileNameFromPath, unzip_file
import os
from bpy_extras.io_utils import ImportHelper
import bpy


def pmx_to_obj(p_in, p_out):
    # 遍历所有的对象
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    # imported_object = bpy.ops.import_scene.obj(filepath=obj_filePath)
    imported_object = bpy.ops.mmd_tools.import_model(filepath=p_in)
    # obj_object = bpy.context.selected_objects[0]
    # bpy.context.selected_objects
    print('Imported pmx name: ', imported_object)
    bpy.ops.cats_armature.fix()
    bpy.ops.export_scene.obj(filepath=p_out)


class SelectDirectoryOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "pmx_to_obj.start"
    bl_label = "选择和开始转换"
    out_dir: bpy.props.StringProperty(
        name='导出文件夹名字',
        description="默认为output，也可以自行设置",
        default="output",
    )
    unzip: bpy.props.BoolProperty(
        name='解压ZIP压缩包',
        description="会将ZIP压缩包解压到初始目录下",
        default=False,
    )

    def execute(self, context):
        print("Selected directory:", self.filepath)
        in_dir = self.filepath
        out_dir = os.path.join(os.path.dirname(os.path.dirname(in_dir)), self.out_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if self.unzip:
            zips=readDir(in_dir, "zip")
            for z in zips:
                newpath = os.path.splitext(z)[0]
                unzip_file(z,newpath)
        pmxfiles = readDir(in_dir, "pmx")
        for pmx in pmxfiles:
            newpath = os.path.join(out_dir, "{}.obj".format(getFileNameFromPath(pmx)))
            print(newpath)
            pmx_to_obj(pmx, newpath)
        bpy.ops.wm.path_open(filepath=out_dir)
        return {'FINISHED'}

    # bpy.ops.object.select_directory('INVOKE_DEFAULT')
