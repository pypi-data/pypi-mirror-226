import pathlib
import subprocess

import psutil
import requests
import threading

from nms_app.models import SetupProjectDetails


def download_file_from_url(urls, location, ref, filenames=list()):
    for i, url in enumerate(urls):
        file_name = filenames[i] if filenames else pathlib.Path(url).name
        with open(location + file_name, 'wb') as out_file:
            content = requests.get(url, stream=True).content
            out_file.write(content)
            print("Done")
    SetupProjectDetails.objects.filter(spd_ref_id=ref).update(spd_download_status=False)


def background_processing(func, param):
    t2 = threading.Thread(target=func, args=param)
    t2.demon = True
    t2.start()


def run_command(command):
    try:
        # Use subprocess.run() to run the command.
        # Setting `shell=True` allows you to run the command with shell features like wildcard expansion.
        # If you're using Python 3.7 or above, you can use capture_output=True to capture the command's output.
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        # If the command executed successfully, the return code will be 0.
        if result.returncode == 0:
            print("Command executed successfully.")
            # If you want to get the output of the command, you can access `result.stdout`.
            print("Command output:")
            print(result.stdout)
        else:
            print(f"Command execution failed with return code: {result.returncode}.")
            # If you want to get the error output of the command, you can access `result.stderr`.
            print("Error output:")
            print(result.stderr)
    except Exception as e:
        print(f"Error occurred: {e}")


def kill_processes_by_cmdline(keyword):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if keyword in " ".join(proc.info['cmdline']):
                pid = proc.info['pid']
                process = psutil.Process(pid)
                process.terminate()
                print(f"Process '{proc.info['name']}' (PID: {pid}) terminated.")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # The process might have terminated before we get its info
            # or we may not have permission to access the process details
            pass