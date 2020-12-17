# Verzió: beta 0.81

import notifier
import git
import os
import shutil

def update():
    try:
        print("p1")
        g = git.Git()
        g.clone("https://github.com/Gergo06-py/re_notifier.git", "update", branch="main")
    
        source_dir = os.path.abspath(os.getcwd()) + "\\update"
        target_dir = os.path.abspath(os.getcwd())
        file_names = os.listdir(source_dir)
        for file_name in file_names:
            shutil.move(os.path.join(source_dir, file_name), target_dir)
    except:
        print("p2")
        g = git.Git("update")
        g.pull("https://github.com/Gergo06-py/re_notifier.git", "main")
        source_dir = os.path.abspath(os.getcwd()) + "\\update"
        target_dir = os.path.abspath(os.getcwd())
        file_names = os.listdir(source_dir)
        for file_name in file_names:
            shutil.move(os.path.join(source_dir, file_name), os.path.join(target_dir, file_name))

    shutil.rmtree("update")
    
    
def main():
    print("verzió ellenőrzése...")
    try:
        g = git.Git()
        g.clone("https://github.com/Gergo06-py/re_notifier.git", "version", branch="version")
    except:
        g = git.Git("version")
        g.pull("https://github.com/Gergo06-py/re_notifier.git", "version")
    
    raw_version = open("version/version.txt")
    version = [line.strip().split(" ") for line in raw_version][0]
    raw_version_now = open("version_now.txt")
    version_now = [line.strip().split(" ") for line in raw_version_now][0]
    version_num = float(version[len(version) - 1])
    version_num_now = float(version_now[len(version_now) - 1])
    raw_version.close()
    raw_version_now.close()

    if version_num_now < version_num:
        print("új verzió elérhető:", end="")
        for line in version:
            print(" " + line, end="")
        print("\nszeretnél frissíteni?")
        ok = False
        while not ok:
            inp = input()
            if inp == "yes" or inp == "igen" or inp == "y" or inp == "i" or inp == "":
                ok = True
                print("frissítés...")
                update()
                print("frissítve!")
            elif inp == "no" or inp == "nem" or inp == "n":
                ok = True
            else:
                print("helytelen bemenet")
    elif version_num_now == version_num:
        print("nincsen frissítés!")
    elif version_num_now > version_num:
        print("a te verzió számod nagyobb mint ami a szerveren van.\nszeretnéd lebutítani a mostani verziót?")
        ok = False
        while not ok:
            inp = input()
            if inp == "yes" or inp == "igen" or inp == "y" or inp == "i" or inp == "":
                ok = True
                print("frissítés...")
                update()
                print("frissítve!")
            elif inp == "no" or inp == "nem" or inp == "n":
                ok = True
            else:
                print("helytelen bemenet")
    
    notifier.main()

if __name__ == "__main__":
    main()
