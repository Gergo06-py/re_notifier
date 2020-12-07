# Verzió: beta 0.6

import notifier
import git
import os
import shutil

def update():
    try:
        g = git.Git()
        g.clone("https://github.com/Gergo06-py/re_notifier.git", str("../" + os.path.basename(os.getcwd())), branch="main")
    except:
        g = git.Git(str("../" + os.path.basename(os.getcwd())))
        g.pull("https://github.com/Gergo06-py/re_notifier.git", "main")

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
    raw_version_now = open("version_now/version_now.txt")
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