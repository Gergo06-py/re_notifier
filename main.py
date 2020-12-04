# Verzió: beta 0.5

from plyer import notification
import git
import notifier
from distutils.dir_util import copy_tree
import shutil


def main():
    notification.notify("Notifier", "Frissítések keresése...")
    print("frissítések keresése...")
    git.Git().clone("https://github.com/Gergo06-py/re_notifier.git", "version", branch="version")
    
    raw_version = open("version/version.txt")
    raw_version_now = open("version_now/version_now.txt")
    version = [line.strip() for line in raw_version]
    version_now = [line.strip() for line in raw_version_now]

    if len(version) > 0 and len(version_now) > 0:
        if version[0][0:5] == "beta":
            if int(version[0][6:len(version[0])]) > version_now:
                git.Git().clone("https://github.com/Gergo06-py/re_notifier.git", "update", branch="main")
                copy_tree("update", "..\\re_notifier")
                shutil.rmtree("update")
                shutil.rmtree("version")
                print("frissítve!")
                notification.notify("Notifier", "Frissítve!")
            else:
                print("nincsen frissítés")
                notification.notify("Notifier", "Nincsen frissítés")
        else:
            if int(version[0][0:len(version[0])]) > version_now:
                git.Git().clone("https://github.com/Gergo06-py/re_notifier.git", "update", branch="main")
                copy_tree("update", "..\\re_notifier")
                shutil.rmtree("update")
                shutil.rmtree("version")
                print("frissítve!")
                notification.notify("Notifier", "Frissítve!")
            else:
                print("nincsen frissítés")
                notification.notify("Notifier", "Nincsen frissítés")
        
    notifier.main()

if __name__ == "__main__":
    main()