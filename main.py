# Verzió: beta 0.5

from plyer import notification
import git
import notifier
from distutils.dir_util import copy_tree
import shutil


def main():
    notification.notify("Notifier", "Frissítések keresése...")
    print("frissítések keresése...")
    g = git.Git()
    g.clone("https://github.com/Gergo06-py/re_notifier.git", "version", branch="version")
    
    raw_version = open("version/version.txt")
    raw_version_now = open("version_now/version_now.txt")
    version = [line.strip() for line in raw_version]
    version_now = [line.strip() for line in raw_version_now]
    raw_version.close()
    raw_version_now.close()
    shutil.rmtree("version")

    if len(version) > 0 and len(version_now) > 0:
        if version[0][0:4] == "beta":
            if float(version[0][5:len(version[0])]) > float(version_now[0][6:len(version_now[0])]):
                g.clone("https://github.com/Gergo06-py/re_notifier.git", "update", branch="main")
                copy_tree("update", "..\\re_notifier")
                shutil.rmtree("update")
                print("frissítve!")
                notification.notify("Notifier", "Frissítve!")
            else:
                print("nincsen frissítés")
                notification.notify("Notifier", "Nincsen frissítés")
        else:
            if float(version[0][0:len(version[0])]) > float(version_now[0][0:len(version_now[0])]):
                g.clone("https://github.com/Gergo06-py/re_notifier.git", "update", branch="main")
                copy_tree("update", "..\\re_notifier")
                shutil.rmtree("update")
                print("frissítve!")
                notification.notify("Notifier", "Frissítve!")
            else:
                print("nincsen frissítés")
                notification.notify("Notifier", "Nincsen frissítés")

    notifier.main()

if __name__ == "__main__":
    main()