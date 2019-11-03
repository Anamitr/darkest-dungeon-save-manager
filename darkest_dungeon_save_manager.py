import os
import re
import shutil
import subprocess
import sys
import time

# VALUES TO MODIFY
PROFILE_NUMBER = '-1'
SAVES_PATH = ''
#

CONFIG_FILE_NAME = 'darkest save.config'

SAVE_PATH = SAVES_PATH + '\\profile_' + str(PROFILE_NUMBER) + '\\'
BACKUP_PATH = SAVES_PATH + '\\manual backup\\'


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


def get_folder_names():
    folders = []
    for r, d, f in os.walk(BACKUP_PATH):
        folders.append(d)
    return folders[0]


def get_last_save_num():
    folder_numbers = []
    folder_names = get_folder_names()

    for folder_name in folder_names:
        try:
            folder_numbers.append(int(folder_name.split(' - ')[0]))
        except ValueError:
            print("Folder name: " + folder_name + " incorrect!")
    return max(folder_numbers)


def backup_save(name=''):
    new_save_name = str(get_last_save_num() + 1) + name

    new_save_path = BACKUP_PATH + new_save_name

    if not os.path.exists(new_save_path):
        os.makedirs(new_save_path)

    copytree(SAVE_PATH, new_save_path)

    sys.stdout.write('Saved as: "' + new_save_name + '", ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
        os.path.getmtime(new_save_path))) + '\n')


def backup_save_with_name():
    name = input('Enter save name: ')
    backup_save(" - " + name)


def get_last_save_name():
    save_names = sorted(get_folder_names(), key=lambda x: int(x.split(' ')[0]))
    return save_names[-1]


def load_save_with_name(name):
    last_save_path = BACKUP_PATH + str(name)
    copy_and_overwrite_folder(last_save_path, SAVE_PATH)
    sys.stdout.write("Loaded save: " + name + ", last modified: " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                  time.localtime(
                                                                                      os.path.getmtime(
                                                                                          last_save_path))) + "\n")


def load_last_save():
    load_save_with_name(get_last_save_name())


def load_save_with_num():
    num = input("Enter number: ")
    save_names = sorted(get_folder_names(), key=lambda x: int(x.split(' ')[0]))
    save_name = [name for name in save_names if name.startswith(num)][0]
    load_save_with_name(save_name)


def get_folder_number(folder_name):
    try:
        return int(folder_name.split(' ')[0])
    except ValueError:
        return -1


def check_if_folder_name_correct(folder_name):
    folder_number = get_folder_number(folder_name)
    if folder_number == -1:
        return False
    else:
        return True


def remove_incorrect_folder_names(folder_names: list):
    for folder_name in folder_names:
        if not check_if_folder_name_correct(folder_name):
            folder_names.remove(folder_name)


def list_saves():
    folders = []
    for r, d, f in os.walk(BACKUP_PATH):
        folders.append(d)

    folders = folders[0]
    remove_incorrect_folder_names(folders)
    save_names = sorted(folders, key=lambda x: get_folder_number(x))

    col_width = max(len(name) for name in save_names) + 2
    for folder_name in save_names:
        sys.stdout.write("".join(folder_name.ljust(col_width)))
        sys.stdout.write(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(BACKUP_PATH + folder_name))) + '\n')
        # print(folder_name, " - \t\t\t\t",
        #       time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(BACKUP_PATH + folder_name))))


def open_save_location_in_explorer():
    subprocess.Popen(r"explorer /select," + SAVE_PATH)


def update_paths():
    global SAVE_PATH, BACKUP_PATH
    SAVE_PATH = SAVES_PATH + '\\profile_' + str(PROFILE_NUMBER) + '\\'
    BACKUP_PATH = SAVES_PATH + '\\manual backup\\'


def update_config():
    global config_file, SAVE_PATH, BACKUP_PATH, PROFILE_NUMBER
    config = 'PROFILE_NUMBER = ' + PROFILE_NUMBER + '\nSAVE_LOCATION = ' + SAVES_PATH
    config_file = open(CONFIG_FILE_NAME, 'w')
    config_file.write(config)
    update_paths()
    config_file.close()


def set_save_location():
    global SAVES_PATH
    SAVES_PATH = input("Enter save path: ")
    update_config()


def choose_profile():
    global PROFILE_NUMBER
    PROFILE_NUMBER = input("Enter profile number (they start from 0): ")
    update_config()


def load_save_location_and_profile_num():
    global config_file, PROFILE_NUMBER, SAVES_PATH
    if os.path.exists(CONFIG_FILE_NAME):
        config_file = open(CONFIG_FILE_NAME, 'r')
        config = config_file.read()

        PROFILE_NUMBER = re.search('PROFILE_NUMBER = (.*)\nSAVE_LOCATION = ', config).group(1)
        SAVES_PATH = config.split("\nSAVE_LOCATION = ")[1]
        update_paths()
        print('Loaded profile =', PROFILE_NUMBER, ' and SAVES PATH = ' + SAVES_PATH)
    else:
        print('You must set save path (exp. F:\\Games\\Steam\\userdata\\46587789\\262060\\remote)')
        set_save_location()
        print('And choose profile')
        choose_profile()


load_save_location_and_profile_num()
# Menu
first_command = True
while True:
    if first_command == False:
        input("Press Enter to continue...\n")
    else:
        first_command = False
    action = int(input("<-- Darkest Dungeon save manager -->\n"
                       "1 - backup save\n"
                       "2 - backup save with name\n"
                       "3 - load last save\n"
                       "4 - load save with num\n"
                       "5 - list saves\n"
                       "6 - open save location in explorer\n"
                       "7 - set save location\n"
                       "8 - choose profile\n"
                       "0 - exit\n"))
    switcher = {
        1: backup_save,
        2: backup_save_with_name,
        3: load_last_save,
        4: load_save_with_num,
        5: list_saves,
        6: open_save_location_in_explorer,
        7: set_save_location,
        8: choose_profile
    }
    func = switcher.get(action, lambda: 'Invalid action')
    func()
    if action == 0:
        break
