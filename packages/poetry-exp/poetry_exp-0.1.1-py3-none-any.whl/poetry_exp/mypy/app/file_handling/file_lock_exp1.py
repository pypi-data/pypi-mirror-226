from filelock import FileLock
import time

APP_NAME = "app1"


def write(file_name="a.txt"):
    with FileLock(str(file_name) + ".lock"):
        print(f"[{APP_NAME}] Lock acquired for writing to file...")
        time.sleep(30)
        f = open(file_name, "a")
        f.write(f"Wrote by {APP_NAME}")
        f.close()
        print(f"[{APP_NAME}]Closed file")


if __name__ == '__main__':
    write()



