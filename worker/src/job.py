import time

def wait(time_s: int):
    time.sleep(time_s)
    return f"Waited {time_s} seconds!"

def health():
    return "Ok"