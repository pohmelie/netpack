from connection import Connection
from construct import *


def echo(pack, cname):
    return info(
        str(pack.message, "ascii"),
        "white",
        "open_chat",
        bytes(cname, "ascii")
    )

def info(s, col="silver", ctype="system", cname=b"[sys]"):
    return([
        Container(
            fun = "chat",
            entity_id = 0,
            entity_type = "stash_wp_portal_chest",
            chat_type = ctype,
            color = col,
            char_level = 0,
            message = bytes(s, "ascii"),
            char_name = cname,
            start_fun = 0
        )],
        Connection.SERVER,
        Connection.CLIENT
    )

def check_command(pack):
    return \
        pack.fun == "send_normal_chat" and \
        pack.mode == "normal" and \
        str(pack.message, encoding="ascii")[0] == "\\"
