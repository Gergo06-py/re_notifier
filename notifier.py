# Verzió: beta 0.81

from plyer import notification
import time
import notifier_libraries
import threading

inp = ""

confirm_exit = False


def run(stop, paused):
    global inp, confirm_exit
    while True:
        if stop():
            break
        if not paused():
            confirm_exit = True
            inp = input()
            time.sleep(0.5)
        confirm_exit = False


stop_thread = False
pause_thread = True
get_input = threading.Thread(target=run, args=(lambda: stop_thread, lambda: pause_thread))


def check_commands(code, index, this_weeks_classes, current_time):
    global inp, get_input, stop_thread, confirm_exit
    class_start_time = notifier_libraries.time_table[index][0].split(":")
    class_start_time = int(class_start_time[0]) * 60 + int(class_start_time[1])
    class_end_time = notifier_libraries.time_table[index][1].split(":")
    class_end_time = int(class_end_time[0]) * 60 + int(class_end_time[1])

    if not (
            current_time == class_start_time - 1 or current_time == class_end_time - 1 or current_time == class_start_time or current_time == class_end_time):
        if inp == "!ora":
            if code == "break":
                notification.notify("Notifier", "Szünet van")
            elif code == "class":
                notification.notify(
                    "Notifier", this_weeks_classes[index] + " órád van")
        elif inp == "!kilepes" or inp == "!kilep" or inp == "!exit":
            if confirm_exit:
                inp = "."
                print("nyomd meg az enter gombot a kilépéshez")
            while not inp == "":
                pass
            print("kilépés...")
            stop_thread = True
            get_input.join()
            exit(1)
        elif inp == "!help" or inp == "!segitseg" or inp == "!segits" or inp == "!h":
            print("Parancsok:\n!ora\n!kilepes / !kilep / !exit\n!help / !segitseg / !segits / !h\n!kicsengo / "
                  "!kicsenget / !kicsengetes / !oraveg / !oravege / !ki-cs\n!becsengo / !becsenget / !becsengetes / "
                  "!orakezdet / !orakezdete / !be-cs\n!ver / !version / !verzio / !v\nVerzió: beta 0.81")
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
            print("Verzió: beta 0.81")
        
        elif inp == "":
            pass
        else:
            print("ismeretlen parancs")
    else:
        if not inp == "":
            print("nem írhatsz be parancsot óra előtt 1 perccel, vagy ha óra kezdete van")
    inp = ""


def main():
    global inp, get_input, stop_thread, pause_thread
    this_weeks_classes = []
    current_week = int(time.strftime("%w"))
    get_input.start()

    print(
        "elindítva!\nA ! prefix-el tudsz beírni parancsokat\nSegítségért írd be hogy !help vagy !segits vagy !segitseg\nEz a verzió még fejlesztés alatt áll. Kérlek saját felelősségre használd.\nVerzió: beta 0.81")
    notification.notify("Notifier", "Elindítva!")

    if 0 < current_week:
        this_weeks_classes = notifier_libraries.classes[
            current_week - 1]
    else:
        current_week = 7
        this_weeks_classes = notifier_libraries.classes[
            current_week - 1]
        
    pause_thread = False
    had_classes = False

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
                had_class = True
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
    if had_classes:
        notification.notify("Notifier", "Vége az óráidnak")
        print("vége az óráidnak")
    else:
        notification.notify("Notifier", "Ma nincsenek óráid")
        print("ma nincsenek óráid")

    if confirm_exit:
        inp = "."
        print("nyomd meg az enter gombot a kilépéshez")
    while not inp == "":
        pass
    print("kilépés...")
    stop_thread = True
    get_input.join()
    exit(1)
