from filelock import FileLock
import time

APP_NAME = "app2"


def write(file_name="a.txt"):
    with open(file_name, "a") as f:
        print(f"[{APP_NAME}] writing to file...")
        f.write(f"Wrote by {APP_NAME}")
        f.close()
        print(f"[{APP_NAME}]Closed file")


if __name__ == '__main__':
    write()



