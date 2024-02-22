bl_info = {
    "name": "MMD格式批量转OBJ",
    "author": "剑走诗湖",
    "version": (0, 7, 0),
    "blender": (2, 80, 0),
    "description": "选择指定目录，对此目录下的PMX文件进行批量扫描，并导出为OBJ+MTL格式，注意需要开启OBJ插件和CATS插件。",
    "category": "Import-Export"
}

import bpy

from .helloword import SimplePanel, hellowe
from .klbq_mtl_fix import OP_MTL_FIX
from .mmd_to_obj import SelectDirectoryOperator
from .tga_to_png import Tga_To_Png
from .repeat_hint_fix import Reap_Fix


def register():
    bpy.utils.register_class(SelectDirectoryOperator)
    bpy.utils.register_class(SimplePanel)
    bpy.utils.register_class(hellowe)
    bpy.utils.register_class(OP_MTL_FIX)
    bpy.utils.register_class(Tga_To_Png)
    bpy.utils.register_class(Reap_Fix)


def unregister():
    bpy.utils.unregister_class(SelectDirectoryOperator)
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(hellowe)
    bpy.utils.unregister_class(OP_MTL_FIX)
    bpy.utils.unregister_class(Tga_To_Png)
    bpy.utils.unregister_class(Reap_Fix)


if __name__ == "__main__":
    unregister()
    register()
