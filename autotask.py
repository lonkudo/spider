import time
import datetime
import subprocess
import os
import sys

def get_venv_python():
    venv_path = sys.prefix
    if os.name == 'nt':  # Windows
        return os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        return os.path.join(venv_path, 'bin', 'python')

def wait_for_midnight_and_run():
    has_run = False

    while True:
        now = datetime.datetime.now()
        if now.hour == 23 and now.minute == 44 and not has_run:
            print("[INFO] 00:00 hit — running yepay_spider.py off")
            python_path = get_venv_python()

            process = subprocess.Popen(
                [python_path, 'yepay_spider.py', 'off'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                print(line, end='')

            process.wait()
            has_run = True

        # Reset flag after 00:01
        if now.hour == 0 and now.minute > 1:
            has_run = False

        time.sleep(5)



if __name__ == "__main__":
    wait_for_midnight_and_run()