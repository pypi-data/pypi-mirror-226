import os
import argparse
import shutil
import torch
import warnings

init_path = torch.__file__
backup_file = torch.__file__ + ".backup"

def modify_init_file():
    if not os.path.exists(backup_file):
        shutil.copyfile(init_path, backup_file)
    with open(backup_file, "r") as f:
        source_code = f.read()
    source_code +="""
try:
    from cuda2mlu import torch_proxy
except Exception as e:
    import warnings
    warnings.simplefilter("always")
    warnings.warn("Failed to execute cuda2mlu, " + str(e))
"""
    with open(init_path, "w") as f:
        f.write(source_code)

def recover_init_file():
    if os.path.exists(backup_file):
        shutil.copyfile(backup_file, init_path)
    else:
        warnings.warn(f"no backup file found in {backup_file}")

def str_to_bool(string:str):
    if string in ["0","off","f","F","false","False"]:
        return False
    else:
        return True

parser = argparse.ArgumentParser()
parser.add_argument("mode", nargs = "?" ,const=True, type = str_to_bool, default=True)

def cmd():
    args = parser.parse_args()
    if args.mode:
        print(f"modify {init_path}")
        modify_init_file()
    else:
        print(f"recover {init_path}")
        recover_init_file()

if __name__ == "__main__":
    cmd()

