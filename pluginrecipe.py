from connection import Connection
from threading import Thread
from time import sleep
from au3bind import autoit
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

def c_run(nx, ny):
    return([
        Container(
            start_fun = 0,
            fun = "run",
            x = nx,
            y = ny
        )],
        Connection.CLIENT,
        Connection.SERVER
    )

def s_reassign(etype, eid, nx, ny):
    return ([
        Container(
            start_fun = 0,
            fun = "reassign",
            reassign = True,
            x = nx,
            y = ny,
            entity_type = etype,
            entity_id = eid
        )],
        Connection.SERVER,
        Connection.CLIENT
    )

def c_select_skill(sskill, side):
    return ([
        Container(
            start_fun = 0,
            fun = "select_skill",
            skill_side = side,
            skill = sskill,
            unknown = 0xffffffff
        )],
        Connection.CLIENT,
        Connection.SERVER
    )

def c_act_right_skill(otype, oid):
    return ([
        Container(
            fun = "right_skill_on_object",
            object_type = otype,
            object_id = oid,
            start_fun = 0
        )],
        Connection.CLIENT,
        Connection.SERVER
    )

def c_go_to_waypoint(area, wid):
    return ([
        Container(
            fun = "waypoint_interaction",
            area_id = area,
            waypoint_id = wid,
            start_fun = 0
        )],
        Connection.CLIENT,
        Connection.SERVER
    )

class Rejoiner(Thread):
    def __init__(self, caption, gamename, gamepass):
        Thread.__init__(self)

        self.caption = caption
        self.gamename = gamename
        self.gamepass = gamepass

    def run(self):
        self.au3 = autoit()
        sleep(0.25)
        self.au3.AU3_ControlSend(self.caption, "", "", "{ESCAPE}")
        sleep(0.1)
        self.au3.AU3_ControlClick(self.caption, "", "", "left", 1, 400, 260)
        sleep(3)
        self.au3.AU3_ControlClick(self.caption, "", "", "left", 1, 590, 460)
        sleep(1)
        self.au3.AU3_ControlSend(self.caption, "", "", self.gamename + "{TAB}" + self.gamepass + "{ENTER}")

