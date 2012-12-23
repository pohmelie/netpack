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

    def __init__(self, char_name):
        self.sorc = self.mule1 = self.mule2 = None
        self.runs = 0
        self.act = self.prepare
        self.char_name = char_name
        self.first = True

        self.subact = None
        self.prefix = None
        self.runnum = None

        self.id = None

        self.run_to_center_step = None
        self.steps_to_center = (
            (14, -12),
            (14, -37),
            (14, -63),
            (27, -76),
            (30, -96),
            (33, -109)
        )

        self.au3 = autoit()

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
                            self.subact = self.waiting_game_enter
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

        if self.subact:
            real, f = self.subact(real, s, d)
            fake = fake + f
        return real, fake

    def waiting_game_enter(self, packets, s, d):
        fake = []
        if s == Connection.SERVER:
            for pack in packets:
                if pack.fun == "player_assign" and pack.x == 0 and pack.y == 0:
                    self.id = pack.player_id
                elif pack.fun == "reassign" and pack.entity_id == self.id:
                    self.x = pack.x
                    self.y = pack.y
                elif pack.fun == "player_in_game":
                    fake.append(info("'lk' {}, run #{}".format(self.sorc, self.runnum)))
                    fake.append(info("({}, {})".format(self.x, self.y)))
                    self.run_to_center_step = None
                    self.subact = self.run_to_center
        return packets, fake

    def gen_run(self):
        return send_run(
            self.x + self.steps_to_center[self.run_to_center_step][0],
            self.y + self.steps_to_center[self.run_to_center_step][1]
        )

    def run_to_center(self, packets, s, d):
        fake = []
        if self.run_to_center_step == None:
            self.run_to_center_step = 0
            fake.append(self.gen_run())
            fake.append(info("step #{}".format(self.run_to_center_step)))
        elif s == Connection.SERVER:
            for pack in packets:

                if pack.fun == "movement_confirmation":
                    fake.append(info(
                            "x = {}, y = {}, dx = {}, dy = {}, stamina = {}".format(
                                pack.x, pack.y, pack.dx, pack.dy, pack.stamina
                            )
                        )
                    )

                if pack.fun == "movement_confirmation" and abs(pack.dx) < 10 and abs(pack.dy) < 10:
                    self.run_to_center_step = self.run_to_center_step + 1
                    if self.run_to_center_step == len(self.steps_to_center):
                        fake.append(info("on center, bro!"))
                        self.subact = self.waiting_game_enter
                        self.next_game()
                        break
                    fake.append(self.gen_run())
                    fake.append(info("step #{}".format(self.run_to_center_step)))
                    break
            packets = list(filter(lambda x: x.fun != "movement_confirmation", packets))
        return packets, fake

    def next_game(self):
        self.runnum = self.runnum + 1
        Rejoiner(self.sorc, self.prefix + str(self.runnum), self.prefix).start()
