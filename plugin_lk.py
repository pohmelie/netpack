from time import *
from pluginrecipe import *
from recipe import *
from au3bind import autoit
from construct import *
from connection import Connection


netpack_plugin = True

class Logic():
    name = "lk"
    desc = "Lower Kurast 3ppl chest bot."
    hlp = (
        "\\lk help - this message.",
        "\\lk set sorc mule1 mule2 - sets windows captions for sorc and mules.",
        "\\lk prefix [prefix] - sets gamename prefix to [prefix] (character name if omitted).",
        "\\lk start",
        "\\lk stop"
    )

    (
        GETTING_PLAYER_ID,
        GETTING_PLAYER_COORD,
        WAITING_PLAYER_IN_GAME,
        MAKE_STEP,
        WAITING_MOVEMENT_CONFIRMATION,
        WAIT_TELEKINESIS,
        WAIT_WP_LIST,
        WAIT_LK_LOAD,
        WAIT_TP_BOOK,
        WAIT_TP,
        WAIT_ACT3_LOAD,
        WAIT_TELEKINESIS_ON_END,
        WAIT_WP_LIST_ON_END,
        WAIT_ACT4_LOAD) = tuple(range(14))


    def __init__(self, char_name):
        self.sorc = self.mule1 = self.mule2 = None
        self.act = self.prepare
        self.char_name = char_name
        self.first = True

        self.subact = None
        self.prefix = None
        self.runnum = None

        self.info = InfoGrabber()
        self.au3 = autoit()

        self.subacts = (

        )

    def prepare(self, packets, s, d):
        real = []
        fake = []
        if self.first:
            self.first = False
            fake.append(info("Welcome to 'lk'. Type '\\lk help' for more information."))

        for pack in packets:
            if s == Connection.CLIENT and check_command(pack):
                com = str(pack.message, "ascii").lower().split()
                if com[0] == "\\lk":
                    fake.append(echo(pack, self.char_name))
                    if len(com) == 1:
                        fake.append(info("Type '\\lk help' for more information."))

                    elif com[1] == "help":
                        apply(lambda x: fake.append(info(x)), self.hlp)

                    elif com[1] == "set":
                        if len(com) < 5:
                            fake.append(info("Not enough parametrs.", "red"))
                        else:
                            self.sorc, self.mule1, self.mule2 = tuple(com[2:5])
                            pps = "Captions set to sorc = '{}', mule1 = '{}', mule2 = '{}'."
                            fake.append(info(pps.format(self.sorc, self.mule1, self.mule2)))

                    elif com[1] == "prefix":
                        if len(com) > 2:
                            self.prefix = com[2]
                            fake.append(info("Prefix set to '{}'.".format(self.prefix)))
                        else:
                            self.prefix = None
                            fake.append(info("Prefix cleared."))

                    elif com[1] == "start":
                        if all((self.sorc, self.mule1, self.mule2)):
                            self.prefix = self.prefix or self.sorc[:10]
                            self.runnum = 0
                            self.step = Logic.GETTING_PLAYER_ID
                            self.subact = self.steps
                            self.next_game()
                        else:
                            fake.append(info("There are no captions.", "red"))

                    elif com[1] == "stop":
                        self.subact = None
                        fake.append(info("'lk' stopped."))

                    else:
                        fake.append(info("Unknown '{}'".format(" ".join(com)), "red"))
            else:
                real.append(pack)

        self.info.grab(real, s, d)
        if self.subact:
            real, f = self.subact(real, s, d)
            fake = fake + f
        return real, fake

    def steps(self, packets, s, d):
        real = []
        fake = []
        for pack in packets:
            if self.step == Logic.GETTING_PLAYER_ID:
                real.append(pack)
                if pack.fun == "player_assign" and pack.x == 0 and pack.y == 0:
                    self.id = pack.player_id
                    self.step = Logic.GETTING_PLAYER_COORD

            elif self.step == Logic.GETTING_PLAYER_COORD:
                real.append(pack)
                if pack.fun == "reassign" and pack.entity_id == self.id and pack.entity_type == "player":
                    self.x = pack.x
                    self.y = pack.y
                    self.step = Logic.WAITING_PLAYER_IN_GAME

            elif self.step == Logic.WAITING_PLAYER_IN_GAME:
                real.append(pack)
                if pack.fun == "player_in_game":
                    fake.append(info("'lk' {}, run #{}".format(self.sorc, self.runnum)))
                    self.running_step = 0
                    #here check for stash and npc journey
                    fake.append(c_act_to_object("run_to_a_object", "stash_wp_or_tp", self.act4_wp_id))
                    fake.append(c_select_skill("telekinesis", "right"))
                    self.step = Logic.WAIT_TELEKINESIS

            elif self.step == Logic.MAKE_STEP:
                real.append(pack)
                fake.append(c_run(
                    self.x + self.steps_to_center[self.running_step][0],
                    self.y + self.steps_to_center[self.running_step][1]))
                self.running_step = self.running_step + 1
                self.step = Logic.WAITING_MOVEMENT_CONFIRMATION

            elif self.step == Logic.WAITING_MOVEMENT_CONFIRMATION:
                if pack.fun == "movement_confirmation" and pack.dx == 0 and pack.dy == 0:
                    fake.append(s_reassign("player", self.id, pack.x, pack.y))
                    if self.running_step == len(self.steps_to_center):
                        fake.append(c_select_skill("telekinesis", "right"))
                        self.step = Logic.WAIT_TELEKINESIS
                    else:
                        self.step = Logic.MAKE_STEP
                elif pack.fun != "movement_confirmation":
                    real.append(pack)

            elif self.step == Logic.WAIT_TELEKINESIS:
                real.append(pack)
                if pack.fun == "skill_select" and pack.skill == "telekinesis":
                    fake.append(c_act_to_object("right_skill_on_object", "stash_wp_or_tp", self.act4_wp_id))
                    self.step = Logic.WAIT_WP_LIST

            elif self.step == Logic.WAIT_WP_LIST:
                if pack.fun == "wp_state":
                    fake.append(c_go_to_waypoint("lower_kurast", self.act4_wp_id))
                    self.step = Logic.WAIT_LK_LOAD
                else:
                    real.append(pack)

            elif self.step == Logic.WAIT_LK_LOAD:
                real.append(pack)
                if pack.fun == "enter_game":
                    fake.append(c_select_skill("book_of_townportal", "right"))
                    self.step = Logic.WAIT_TP_BOOK

            elif self.step == Logic.WAIT_TP_BOOK:
                real.append(pack)
                if pack.fun == "skill_select" and pack.skill == "book_of_townportal":
                    fake.append(c_act_to_location("right_skill_on_location", self.x, self.y))
                    self.step = Logic.WAIT_TP

            elif self.step == Logic.WAIT_TP:
                real.append(pack)
                if pack.fun == "tele_state":
                    fake.append(c_act_to_object("interact_with_object", "stash_wp_or_tp", pack.teleport_id))
                    self.step = Logic.WAIT_ACT3_LOAD

            elif self.step == Logic.WAIT_ACT3_LOAD:
                real.append(pack)
                if pack.fun == "reassign" and pack.entity_id == self.id and pack.entity_type == "player":
                    fake.append(c_act_to_object("run_to_a_object", "stash_wp_or_tp", self.act4_wp_id))
                    fake.append(c_select_skill("telekinesis", "right"))
                    self.step = Logic.WAIT_TELEKINESIS_ON_END

            elif self.step == Logic.WAIT_TELEKINESIS_ON_END:
                real.append(pack)
                if pack.fun == "skill_select" and pack.skill == "telekinesis":
                    fake.append(c_act_to_object("right_skill_on_object", "stash_wp_or_tp", self.act3_wp_id))
                    self.step = Logic.WAIT_WP_LIST_ON_END

            elif self.step == Logic.WAIT_WP_LIST_ON_END:
                if pack.fun == "wp_state":
                    fake.append(c_go_to_waypoint("the_pandeminoum_fortress", self.act3_wp_id))
                    self.step = Logic.WAIT_ACT4_LOAD
                else:
                    real.append(pack)

            elif self.step == Logic.WAIT_ACT4_LOAD:
                real.append(pack)
                if pack.fun == "reassign" and pack.entity_id == self.id and pack.entity_type == "player":
                    self.step = Logic.GETTING_PLAYER_ID

        return real, fake

    def next_game(self):
        self.runnum = self.runnum + 1
        Rejoiner(self.sorc, self.prefix + str(self.runnum), self.prefix).start()
