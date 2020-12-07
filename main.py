# Verzió: beta 0.6

import notifier
import git
import os
import shutil

def update():
    try:
        g = git.Git()
        g.clone("https://github.com/Gergo06-py/re_notifier.git", "update", branch="main")
    except:
        g = git.Git("update")
        g.pull("https://github.com/Gergo06-py/re_notifier.git", "main")

    file_names = os.listdir("update")
    for file_name in file_names:
        shutil.move(os.path.join("update", file_name), "")


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

    if version_num_now < version_num:
        print("új verzió elérhető:", end="")
        for line in version:
            print(" " + line, end="")
        print("\nfrissítés...")
        update()
    elif version_num_now == version_num:
        print("nincsen frissítés!")
    elif version_num_now > version_num:
        print("a te verzió számod nagyobb mint ami a szerveren van.\nszeretnéd lebutítani a mostani verziót?")
        inp = input()
        if inp == "yes" or inp == "y" or inp == "":
            update()
    
    notifier.main()

if __name__ == "__main__":
    main()