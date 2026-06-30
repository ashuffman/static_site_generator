import os
import shutil

def copy_static_to_public(src_dir: str, dst_dir: str): # accepts path-like object strings
    # make sure that both paths are actually paths
    if not os.path.exists(src_dir):
        raise Exception("Error: Invalid source directory file path")
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    
    # log the current path to the console
    print(f"currently copying {src_dir}")

    # empty the destination directory
    empty_dir(dst_dir)

    # call recursive copy funtion
    _copy_recursive(src_dir, dst_dir)
    return

def dir_list_to_paths(dir: str) -> list[str]:
    # accepts a directory file path, return a list of the file paths of its contents
    dir_items = os.listdir(dir)
    dir_item_paths =[]
    for item in dir_items:
        dir_item_paths.append(os.path.join(dir, item))
    return dir_item_paths

def empty_dir(dir:str) -> None:
    # accepts a directory path and deletes the content of that directory while preserving the directory
    trees = dir_list_to_paths(dir)
    for tree in trees:
        if os.path.isfile(tree):
            os.remove(tree)
        else:
            shutil.rmtree(tree)
    return

def _copy_recursive(src_dir: str, dst_dir: str):
    # make a list of the file paths of src_dir's contents
    src_dir_items = dir_list_to_paths(src_dir)
    # call the function recursively on the contents of src_dir
    for item in src_dir_items:  
        # create a copy of src_dir in the dst_dir
        if os.path.isfile(item):
            shutil.copy(item, dst_dir)
        else:
            new_dst_dir = os.path.join(dst_dir, os.path.basename(item))
            os.mkdir(new_dst_dir) 
            _copy_recursive(item, new_dst_dir)
    return