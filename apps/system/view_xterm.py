import os
from django.shortcuts import render
import socketio
import pty
import select
import subprocess
import struct
import fcntl
import termios
import signal
import eventlet

async_mode = "eventlet"
sio = socketio.Server(async_mode=async_mode)


fd = None
child_pid = None


def index(request):
    context = {'parent_menu': 'system', 'menu': 'terminal', 'page_title': '终端'}
    return render(request, 'system/xterm.html', context)

def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward_pty_output():
    global fd
    max_read_bytes = 1024 * 20
    while True:
        sio.sleep(0.01)
        if fd:
            timeout_sec = 0
            (data_ready, _, _) = select.select([fd], [], [], timeout_sec)
            if data_ready:
                output = os.read(fd, max_read_bytes).decode()
                sio.emit("pty_output", {"output": output})
        else:
            print("process killed")
            return

@sio.event
def resize(sid, message):
    if fd:
        set_winsize(fd, message["rows"], message["cols"])

@sio.event
def pty_input(sid, message):
    if fd:
        os.write(fd, message["input"].encode())

@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)

@sio.event
def connect(sid, environ):
    global fd
    global child_pid

    if child_pid:
        os.write(fd, "\n".encode())
        return

    (child_pid, fd) = pty.fork()

    if child_pid == 0:
        subprocess.run('bash')

    else:
        sio.start_background_task(target=read_and_forward_pty_output)


@sio.event
def disconnect(sid):
    global fd
    global child_pid

    os.kill(child_pid, signal.SIGKILL)
    os.wait()

    fd = None
    child_pid = None
    print('Client disconnected')

