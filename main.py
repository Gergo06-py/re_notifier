from plyer import notification
import git
import notifier


def main():
    repo = git.Repo(".git")
    current = repo.head.commit
    print("frissítések keresése...")
    repo.remotes.origin.pull("time_table")
    if current == repo.head.commit:
        print("nincsen új frissítés")
    else:
        notification.notify("Notifier", "Program frissítve!")
        print("program frissítve!")
    notifier.main()

if __name__ == "__main__":
    main()