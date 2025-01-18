import os
import re
from clang.cindex import Config, Index, CursorKind


# 设置 Clang 库路径
libclang_path = "/usr/lib/llvm-14/lib/libclang.so"
if not os.path.exists(libclang_path):
    raise RuntimeError(f"libclang not found at {libclang_path}")
Config.set_library_file(libclang_path)

source_root_list = ["../ability_ability_runtime/interfaces/inner_api/ability_manager", 
                    "../ability_ability_runtime/interfaces/inner_api/app_manager",
                    "/home/user/yzb/hw_interface_analyze/interface_test/test_c/ability_ability_runtime/frameworks/simulator/osal",
                    "/home/user/jyw/ohos5/foundation/communication/ipc/interfaces/innerkits/ipc_core/"]
include_dirs = []

    # 查找所有 include 目录及其子目录
for source_root in source_root_list:    
    for root, dirs, _ in os.walk(source_root):
        for dir_name in dirs:
            if dir_name == "include":
                # 遍历该 include 文件夹及其所有子文件夹
                include_path = os.path.join(root, dir_name)
                for root_dir, subdirs, _ in os.walk(include_path):
                    include_dirs.append(root_dir)  # 将所有子文件夹路径添加到 include_dirs 列表

if not include_dirs:
    raise RuntimeError("No include directories found in the source root.")   
# 将所有的 include 目录路径输出到文件
def output_include_dirs(file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for dir_path in include_dirs:
            f.write("-I"+dir_path + "\n")
    print(f"All include directories have been saved to {file_path}")

# 调用函数保存 include 目录到文件
output_include_dirs("include_dirs.txt")