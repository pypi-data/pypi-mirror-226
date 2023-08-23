import shutil
import json
from typing import NewType
import os

pair = NewType("pair", dict[str, str])
file_path = "./brof_files/file_pairs.json"

def setup_file(path: str):
    
    if os.path.isfile(path):
        return 

    os.mkdir("./brof_files")

    with open(path, "w+") as f:
        f.write('{"pairs": []}')

def add_pair_to_store(src: str, dst: str) -> None:
    pair = {"src": src, "dst": dst}
    
    setup_file(file_path)

    with open(file_path, "r+") as fjs:
        content = json.load(fjs)
        content["pairs"].append(pair)
        fjs.seek(0)
        json.dump(content, fjs, indent=4)

def find_changed() -> list[pair]:
    changed_pairs = []

    setup_file(file_path)

    with open(file_path, "r+") as fjs:
        for pair in json.load(fjs)["pairs"]:
            import difflib

            with open(pair['src']) as src:
                src_cont = src.readlines()

            with open(pair['dst']) as dst:
                dst_cont = dst.readlines()

            if len(list(difflib.unified_diff(src_cont, dst_cont))) != 0:
                changed_pairs.append(pair)

    return changed_pairs

def refresh_pair(pair: pair) -> None:
    shutil.copy(pair['src'], pair['dst'])

def refresh_pairs(pairs: list[pair]) -> None:
    for pair in pairs:
        refresh_pair(pair)
    
def clear_file_pairs_file() -> None:
    setup_file(file_path)

    content = json.load(open(file_path))
    content['pairs'] = []
    open(file_path, "w").write(json.dumps(content, indent=4))

def remove_sub_folders(folder: str, crr_list: list[str]=[]) -> list[str]:
    content = os.listdir(folder)

    for p in content:
        if os.path.isdir(os.path.join(folder, p)):
            crr_list = remove_sub_folders(os.path.join(folder, p), crr_list)
        elif os.path.isfile(os.path.join(folder, p)):
            crr_list.append(os.path.join(folder, p))
        else:
            print('lol')
    return crr_list

def add_folders(f1: str, f2:str) -> None:
    a = []
    content1 = remove_sub_folders(f1, a)
    b = []
    content2 = remove_sub_folders(f2, b)
    print(content1)

    for i in range(0, len(content1)):
        add_pair_to_store(content1[i], content2[i])

def show_pairs() -> None:

    setup_file(file_path)

    with open(file_path, "r") as fjs:
        print(fjs.read())
