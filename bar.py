import subprocess, signal, sys
import time
from threading import Thread, Event
from queue import Queue
import copy


def exit_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, exit_handler)
lastSong = subprocess.run(["playerctl", "metadata", "mpris:trackid"],
                          stdout=subprocess.PIPE).stdout
while True:
    song = subprocess.run(["playerctl", "metadata", "mpris:trackid"],
                          stdout=subprocess.PIPE).stdout
    if song != lastSong:
        bar = subprocess.Popen(["lemonbar", "-p"], stdin=subprocess.PIPE, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL, bufsize=1,
                               universal_newlines=True)
        bar.stdin.write("Lol\n")
        time.sleep(4)
        bar.send_signal(signal.SIGTERM)
        lastSong = song


class BarCreatorThread(Thread):
    def __init__(self, queue):
        super().__init__()
        self.q = queue
        self._stopper = Event()
        self.screenHeight = int(subprocess.check_output(["xrandr"]).split(b'\n')[0].split(b',')[1].split()[3])
        self.screenWidth = int(subprocess.check_output(["xrandr"]).split(b'\n')[0].split(b',')[1].split()[1])
        self.popups = 0

    def stop_worker(self):
        self._stopper.set()
        
    def stopped(self):
        return self._stopper.is_set()

    def run():
        defaultCmd = ["dzen2", "-x", "5", "-y", str(self.screenHeight - 35), "-h", "30", "-w", "100", "-bg", "white"] 
        while True:
            if self.stopped:
                break
            if not self.q.empty():
                info = self.q.get()
                cmd = copy.deepcopy(defaultCmd)
                height = cmd[4]
                height = height - (35 * self.popups)


class StatusThread(Thread):
    def __init__(self, worker_id, queue):
        super().__init__()
        self.id = worker_id
        self.q = queue
        self._stopper = Event()

    def stop_worker(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()


class MusicStatusThread(StatusThread):
    def __init__(self, worker_id, timeout=None, queue):
        super().__init__(worker_id, queue)
        if timeout is None:
            self.timeout = 0
        else:
            self.timeout = timeout

        def songChanged(self):
            pass

        def run(self):
            lastSong = subprocess.run(["playerctl", "metadata", "mpris:trackid"], stdout=subprocess.PIPE).stdout
            while True:
                if self.stopped:
                    break
                song = subprocess.run(["playerctl", "metadata", "mpris:trackid"], stdout=subprocess.PIPE).stdout
                if song != lastSong:
                    self.songChanged()
                    bar.send_signal(signal.SIGTERM)
                    lastSong = song
