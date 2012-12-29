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

def c_act_to_location(fname, lx, ly):
    return ([
        Container(
            fun = fname,
            x = lx,
            y = ly,
            start_fun = 0
        )],
        Connection.CLIENT,
        Connection.SERVER
    )

def c_act_to_object(fname, otype, oid):
    return ([
        Container(
            fun = fname,
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

class InfoGrabber():
    act = act4_wp_id = act3_wp_id = stash_id = area_id = x = y = tp_count =\
    hp = mp = stamina = lskill = rskill = id = None

    def grab(self, packets, s, d):
        for pack in packets:
            if pack.fun == "object_assign":
                if pack.entity_class_code == "act4_waypoint":
                    self.act4_wp_id = pack.entity_id
                elif pack.entity_class_code == "act3_waypoint":
                    self.act3_wp_id = pack.entity_id
                elif pack.entity_class_code == "stash":
                    self.stash_id = pack.entity_id

            elif pack.fun == "seed":
                self.area_id = pack.area_id
                self.act = pack.act + 1

            elif pack.fun == "reassign" and pack.entity_id == self.id and pack.entity_type == "player":
                self.x = pack.x
                self.y = pack.y

            elif pack.fun == "skill_book_count" and pack.skill == "book_of_townportal" \
                and pack.entity_type == "player" and pack.entity_id == self.id:
                self.tp_count = pack.stats_amount

            elif pack.fun == "stats_confirmation":
                self.hp = pack.hp
                self.mp = pack.mp
                self.x = pack.x
                self.y = pack.y
                self.stamina = pack.stamina

            elif pack.fun == "movement_confirmation":
                self.stamina = pack.stamina
                if pack.dx == 0 and pack.dy == 0:
                    self.x = pack.x
                    self.y = pack.y

            elif pack.fun == "skill_select" and pack.entity_id == self.id and pack.entity_type == "player":
                if pack.skill_side == "right":
                    self.rskill = pack.skill
                else:
                    self.lskill = pack.skill

            elif pack.fun == "player_assign" and pack.x == 0 and pack.y == 0:
                self.id = pack.player_id

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

