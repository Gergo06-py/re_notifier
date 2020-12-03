# Verzió: beta 0.3

from plyer import notification
import time
import notifier_libraries
import threading
import git
import imp

inp = ""

confirm_exit = False
can_check_commands = False


def get_command(stop, paused):
    global inp, confirm_exit
    while True:
        if stop():
            break
        if not paused():
            confirm_exit = True
            inp = input()
            confirm_exit = False
            time.sleep(0.5)

def check_update(stop, paused):
    global inp, can_check_commands, stop_check_update
    repo = git.Repo(".git")
    update = repo.remotes.origin.fetch()
    if len(update) > 0:
        if str(update[0]) == "origin/time_table":
            notification.notify("Notifier", "Frissítések elérhetőek!")
            print("Frissítések elérhetőek. Szeretnél most frissíteni?")
            while True:
                if stop():
                    break
                if not paused():
                    if inp == "yes" or inp == "y" or inp == "igen" or inp == "i":
                        print("Frissítés...")
                        repo.remotes.origin.pull("time_table")
                        print("Frissítve!")
                        can_check_commands = True
                        imp.reload(notifier_libraries)
                        imp.reload(main)
                    elif inp == "n" or inp == "no" or inp == "nem":
                        can_check_commands = True
                        stop_check_update = True
                    elif inp == "":
                        pass
                    else:
                        print("igen-el vagy nem-el válaszolj")
                inp = ""
                time.sleep(0.5)


stop_get_command = False
pause_get_command = False
stop_check_update = False
pause_check_update = False
get_command = threading.Thread(target=get_command, args=(lambda: stop_get_command, lambda: pause_get_command))
check_update = threading.Thread(target=check_update, args=(lambda: stop_check_update, lambda: pause_check_update))


def check_commands(code, index, this_weeks_classes, current_time):
    global inp, get_command, stop_get_command, confirm_exit, stop_check_update, can_check_commands
    class_start_time = notifier_libraries.time_table[index][0].split(":")
    class_start_time = int(class_start_time[0]) * 60 + int(class_start_time[1])
    class_end_time = notifier_libraries.time_table[index][1].split(":")
    class_end_time = int(class_end_time[0]) * 60 + int(class_end_time[1])
    if stop_check_update:
        check_update.join()

    if can_check_commands:
        if not (
                current_time == class_start_time - 1 or current_time == class_end_time - 1 or current_time == class_start_time or current_time == class_end_time):
            if inp == "!ora":
                if code == "break":
                    notification.notify("Notifier", "Szünet van")
                elif code == "class":
                    notification.notify(
                        "Notifier", this_weeks_classes[index] + " órád van")
            elif inp == "!kilepes" or inp == "!kilep" or inp == "!exit":
                print("kilépés...")
                if confirm_exit:
                    print("nyomd meg az enter gombot a kilépéshez")
                stop_get_command = True
                stop_check_update = True
                get_command.join()
                check_update.join()
                exit(1)
            elif inp == "!help" or inp == "!segitseg" or inp == "!segits" or inp == "!h":
                print("Parancsok:\n!ora\n!kilepes / !kilep / !exit\n!help / !segitseg / !segits / !h\n!kicsengo / "
                    "!kicsenget / !kicsengetes / !oraveg / !oravege / !ki-cs\n!becsengo / !becsenget / !becsengetes / "
                    "!orakezdet / !orakezdete / !be-cs")
            elif inp == "!kicsengo" or inp == "!kicsenget" or inp == "!kicsengetes" or inp == "!oraveg" or inp == "!oravege" or inp == "!ki-cs":
                notification.notify("Notifier",
                                    str(class_end_time // 60) + ":" + str(class_end_time % 60) + "kor csengetnek ki")
            elif inp == "!becsengo" or inp == "!becsenget" or inp == "!becsengetes" or inp == "!orakezdet" or inp == "!orakezdete" or inp == "!be-cs":
                if current_time <= class_start_time:
                    notification.notify("Notifier",
                                        str(class_start_time // 60) + ":" + str(
                                            class_start_time % 60) + " kor csengetnek be")
                else:
                    if index < len(this_weeks_classes):
                        class_start_time = notifier_libraries.time_table[index + 1][0].split(":")
                        class_start_time = int(class_start_time[0]) * 60 + int(class_start_time[1])
                        notification.notify("Notifier", str(class_start_time // 60) + ":" + str(
                            class_start_time % 60) + "kor csengetnek be")
            elif inp == "!ver" or inp == "!version" or inp == "!verzio" or inp == "!v":
                print("Verzió: beta 0.3")
            
            elif inp == "":
                pass
            else:
                print("ismeretlen parancs")
        else:
            if not inp == "":
                print("nem írhatsz be parancsot óra előtt 1 perccel, vagy ha óra kezdete van")
        inp = ""


def main():
    global inp, get_command, stop_get_command, pause_get_command
    print(
        "elindítva!\nA ! prefix-el tudsz beírni parancsokat\nSegítségért írd be hogy !help vagy !segits vagy !segitseg\nEz a verzió még fejlesztés alatt áll. Kérlek saját felelősségre használd.\nVerzió: beta 0.3")
    notification.notify("Notifier", "Elindítva!")

    this_weeks_classes = []
    current_week = int(time.strftime("%w"))
    get_command.start()
    check_update.start()

    if 0 < current_week < 6:
        this_weeks_classes = notifier_libraries.classes[int(
            current_week) - 1]
    else:
        notification.notify("Notifier", "Hétvégén nicsenek óráid")
        print("kilépés...")
        exit(1)

    for index in range(len(this_weeks_classes)):
        class_start_time = notifier_libraries.time_table[index][0].split(":")
        class_start_time = int(class_start_time[0]) * 60 + int(class_start_time[1])
        class_end_time = notifier_libraries.time_table[index][1].split(":")
        class_end_time = int(class_end_time[0]) * 60 + int(class_end_time[1])

        notified = False
        current_time = time.strftime("%H:%M").split(":")
        current_time = int(current_time[0]) * 60 + int(current_time[1])
        while current_time <= class_start_time and not notified and not this_weeks_classes[index] == "":
            current_time = time.strftime("%H:%M").split(":")
            current_time = int(current_time[0]) * 60 + int(current_time[1])
            if current_time == class_start_time:
                notification.notify(
                    "Notifier", "A következő órád " + this_weeks_classes[index])
                current_time = time.strftime("%H:%M").split(":")
                current_time = int(current_time[0]) * 60 + int(current_time[1])
                notified = True
            check_commands("break", index, this_weeks_classes, current_time)
            time.sleep(1)

        notified = False
        current_time = time.strftime("%H:%M").split(":")
        current_time = int(current_time[0]) * 60 + int(current_time[1])
        while current_time <= class_end_time and not notified and not this_weeks_classes[index] == "":
            current_time = time.strftime("%H:%M").split(":")
            current_time = int(current_time[0]) * 60 + int(current_time[1])
            if current_time == class_end_time:
                notification.notify(
                    "Notifier", this_weeks_classes[index] + " óra véget ért")
                current_time = time.strftime("%H:%M").split(":")
                current_time = int(current_time[0]) * 60 + int(current_time[1])
                notified = True
            check_commands("class", index, this_weeks_classes, current_time)
            time.sleep(1)
    notification.notify("Notifier", "Az óráid véget értek")


print("indítás...")
if __name__ == "__main__":
    main()
print("kilépés...")
if confirm_exit:
    print("nyomd meg az enter gombot a kilépéshez")
stop_get_command = True
stop_check_update = True
get_command.join()
check_update.join()
exit(1)
