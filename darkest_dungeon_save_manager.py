import os
import shutil
import subprocess
import sys
import time

# VALUES TO MODIFY
PROFILE_NUMBER = 0
SAVES_PATH = 'F:\\Games\\Steam\\userdata\\46587789\\262060\\remote\\'
#

SAVE_PATH = SAVES_PATH + 'profile_' + str(PROFILE_NUMBER) + '\\'
BACKUP_PATH = SAVES_PATH + 'manual backup\\'


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def copy_and_overwrite_folder(src, dst, symlinks=False, ignore=None):
    shutil.rmtree(dst)
    copytree(src, dst, symlinks, ignore)


def get_last_save_num():
    folders = []
    folder_numbers = []
    for r, d, f in os.walk(BACKUP_PATH):
        folders.append(d)

    folders = folders[0]
    for folder_name in folders:
        folder_numbers.append(int(folder_name.split(' - ')[0]))
    # folders = list(map(int, folders))
    return max(folder_numbers)


def backup_save(name=''):
    new_save_name = str(get_last_save_num() + 1) + name

    new_save_path = BACKUP_PATH + new_save_name

    if not os.path.exists(new_save_path):
        os.makedirs(new_save_path)

    copytree(SAVE_PATH, new_save_path)

    sys.stdout.write('Saved as: "' + new_save_name + '", ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
        os.path.getmtime(new_save_path))))


def open_save_location_in_explorer():
    subprocess.Popen(r"explorer /select," + SAVE_PATH)


def load_last_save():
    last_save_num = get_last_save_num()
    last_save_path = BACKUP_PATH + str(last_save_num)
    copy_and_overwrite_folder(last_save_path, SAVE_PATH)

    print("Loaded save nr ", last_save_num, ", last modified:",
          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(last_save_path))))


def list_saves():
    folders = []
    for r, d, f in os.walk(BACKUP_PATH):
        folders.append(d)

    folders = folders[0]
    save_names = sorted(folders, key=lambda x: int(x.split(' ')[0]))

    for folder_name in save_names:
        print(folder_name, " - ",
              time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(BACKUP_PATH + folder_name))))


def backup_save_with_name():
    name = input('Enter save name: ')
    backup_save(" - " + name)


# Menu
action = int(input("Darkest Dungeon save manager:\n"
                   "1 - backup save\n"
                   "2 - backup save with name\n"
                   "3 - load last save\n"
                   "4 - list saves\n"
                   "5 - open save location in explorer\n"))
switcher = {
    1: backup_save,
    2: backup_save_with_name,
    3: load_last_save,
    4: list_saves,
    5: open_save_location_in_explorer
}
func = switcher.get(action, lambda: 'Invalid action')
func()
