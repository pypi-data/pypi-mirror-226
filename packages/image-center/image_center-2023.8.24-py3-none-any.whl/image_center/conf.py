import os
import platform


class _Setting:
    PIC_PATH = ""
    IMAGE_RATE = 0.9
    SCREEN_CACHE = "/tmp/screen.png"
    TMPDIR = "/tmp/tmpdir"
    IMAGE_MATCH_NUMBER = 1
    IMAGE_MATCH_WAIT_TIME = 1

    # RPC config
    SERVER_IP = ""
    PORT = 8889

    if platform.system() == "Linux":
        # 显示服务器
        DISPLAY_SERVER = os.popen(
            "cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1"
        ).read().split("=")[-1].strip("\n")

        class DisplayServer:
            wayland = "wayland"
            x11 = "x11"

        IS_X11 = (DISPLAY_SERVER == DisplayServer.x11)
        IS_WAYLAND = (DISPLAY_SERVER == DisplayServer.wayland)
    elif platform.system() == "Windows":
        ...

setting = _Setting()
