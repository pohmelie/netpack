from construct import *
from d2packetparser_c2s import sid, char_type
from d2packetparser_items import *
from list_skills import Skill
from list_attrs import Attribute
from list_entities import Entity


skills = Skill("skill")
attr_code = Attribute("attribute")
entity_type = Entity("entity_type")

def xy16(pre=""):
    pre = pre and pre + "_"
    return Embed(Struct(None,
            ULInt16(pre + "x"),
            ULInt16(pre + "y")
        )
    )

def etype_eid(pre=""):
    pre = pre and pre + "_"
    return Embed(Struct(None,
            Entity(pre + "entity_type"),
            #ULInt8(pre + "entity_type"),
            sid(pre + "entity_id")
        )
    )

map_add_rem = Struct(None,
    xy16(),
    ULInt8("area_id")
)

s2c_packets = Struct(None,
    Anchor("start_fun"),
    Enum(UBInt8("fun"),
        setup = 0x01,
        load_successful = 0x02,
        seed = 0x03,
        enter_game = 0x04,
        unload_complete = 0x05,
        game_exit = 0x06,
        map_add = 0x07,
        map_rem = 0x08,
        door_assign = 0x09,
        lost_sight = 0x0a,
        handshake = 0x0b,
        show_dmg = 0x0c,
        action_effect = 0x0d,
        object_state = 0x0e,
        entity_move = 0x0f,
        entity_to_entity = 0x10,
        report_kill = 0x11,
        reassign = 0x15,
        pot = 0x18,
        gold_byte = 0x19,
        exp_byte = 0x1a,
        exp_word = 0x1b,
        exp_dword = 0x1c,
        attr_byte = 0x1d,
        attr_word = 0x1e,
        attr_dword = 0x1f,
        player_attr = 0x20,
        update_item_oskill = 0x21,
        skill_book_count = 0x22,
        skill_select = 0x23,
        chat = 0x26,
        npc_interact = 0x27,
        quest_tree = 0x28,
        game_quest_info = 0x29,
        npc_transaction = 0x2a,
        sound = 0x2c,
        update_item_stats = 0x3e,
        use_stackable_item = 0x3f,
        mouse_clear = 0x42,
        relator_1 = 0x47,
        relator_2 = 0x48,
        entity_attack_entity = 0x4c,
        entity_attack_location = 0x4d,
        merc_for_hire = 0x4e,
        stat_merc_list = 0x4f,
        object_assign = 0x51,
        quest_log_info = 0x52,
        game_refresh = 0x53,
        player_assign = 0x59,
        event_notify = 0x5a,
        player_in_game = 0x5b,
        player_quit_game = 0x5c,
        tele_state = 0x60,
        wp_state = 0x63,
        kill_count = 0x65,
        npc_move = 0x67,
        npc_to_target = 0x68,
        npc_state_assign = 0x69,
        npc_action = 0x6b,
        npc_attack = 0x6c,
        npc_stop = 0x6d,
        about_player = 0x75,
        overhead_clear = 0x76,
        trade = 0x77,
        who_trade = 0x78,
        gold_trade = 0x79,
        summon_log = 0x7a,
        bind_skill_to_hotkey = 0x7b,
        use_item = 0x7c,
        party_update = 0x7f,
        merc_owner = 0x81,
        tele_owner = 0x82,
        quest_event = 0x89,
        entity_request_chat = 0x8a,
        party_invite_status = 0x8b,
        player_relationship = 0x8c,
        party_number = 0x8d,
        corpse_assign = 0x8e,
        pong = 0x8f,
        party_pulse = 0x90,
        skill_log = 0x94,
        resources = 0x95,
        walk_verify = 0x96,
        weapon_switch = 0x97,
        skill_triggered = 0x99,
        merc_attr_byte = 0x9e,
        merc_attr_word = 0x9f,
        merc_attr_dword = 0xa0,
        merc_attr_add_byte = 0xa1,
        merc_attr_add_word = 0xa2,
        baal_spawn = 0xa4,
        aura_effect = 0xa7,
        set_state = 0xa8,
        end_state = 0xa9,
        entity_info_add = 0xaa,
        entity_heal = 0xab,
        npc_assign = 0xac,
        warden = 0xae,
        compression = 0xaf,
        game_termination = 0xb0,
        timeout_full = 0xb4,

        #item actions
        world_item_action = 0x9c,
        owner_item_action = 0x9d,

        #unknown, but length
        unknown_0x50 = 0x50,
        unknown_0x5e = 0x5e,
        unknown_0x5f = 0x5f,
        unknown_0x7e = 0x7e,
        unknown_0x91 = 0x91,
        unknown_0xa5 = 0xa5,
        unknown_0xc1 = 0xc1,
        unknown_0xca = 0xca,
        unknown_0xcb = 0xcb,
        unknown_0xcc = 0xcc,

        _default_ = "unknown"
    ),
    Embed(Switch(None, lambda ctx: ctx.fun, {
                "setup":Struct(None,
                    Enum(ULInt8("difficulty"),
                        normal = 0x00,
                        nightmare = 0x01,
                        hell = 0x02
                    ),
                    Const(ULInt8(None), 0x04),
                    Enum(ULInt8("diff_core_flag"),
                        hardcore = 0x08,
                        nightmare = 0x10,
                        hell = 0x20
                    ),
                    Enum(ULInt16("ladder_expo_flag"),
                        lod = 0x10,
                        ladder = 0x20
                    ),
                    Enum(ULInt8("expo"),
                        classic = 0x00,
                        lod = 0x01
                    ),
                    Enum(ULInt16("ladder"),
                        no = 0x00,
                        yes = 0x01
                    )
                ),
                "load_successful":Struct(None, Pass),
                "seed":Struct(None,
                    ULInt8("act"),
                    ULInt32("seed_1"),
                    ULInt16("area_id"),
                    ULInt32("seed_2")
                ),
                "enter_game":Struct(None, Pass),
                "unload_complete":Struct(None, Pass),
                "game_exit":Struct(None, Pass),
                "map_add":map_add_rem,
                "map_rem":map_add_rem,
                "door_assign":Struct(None,
                    etype_eid(),
                    ULInt8("side"),
                    ULInt16("x"),
                    ULInt16("y")
                ),
                "lost_sight":Struct(None, etype_eid()),
                "handshake":Struct(None, etype_eid()),
                "show_dmg":Struct(None,
                    etype_eid(),
                    ULInt8("effect_state"),
                    ULInt8("sfx"),
                    ULInt8("life_percent")
                ),
                "action_effect":Struct(None,
                    etype_eid(),
                    ULInt8("effect_state"),
                    xy16(),
                    ULInt8("life_percent"),
                    ULInt8("graphic_sound_code")
                ),
                "object_state":Struct(None,
                    etype_eid(),
                    Const(ULInt8(None), 0x03),
                    Flag("changeable"),
                    ULInt32("entity_state")
                ),
                "entity_move":Struct(None,
                    etype_eid(),
                    ULInt8("movement_type"),
                    xy16("going_to"),
                    ULInt8("knockback"),
                    xy16("going_from")
                ),
                "entity_to_entity":Struct(None,
                    etype_eid(),
                    ULInt8("movement_type"),
                    etype_eid("going_to"),
                    xy16()
                ),
                "report_kill":Struct(None,
                    etype_eid(),
                    ULInt16("killed_by")
                ),
                "reassign":Struct(None,
                    etype_eid(),
                    xy16(),
                    Flag("reassign")
                ),
                "pot":BitStruct(None,
                    BitField("life", 15),
                    BitField("mana", 15),
                    BitField("stamina", 15),
                    BitField("x", 15),
                    BitField("unknown1", 1),
                    BitField("y", 15),
                    BitField("unknown2", 36),
                ),
                "gold_byte":Struct(None, ULInt8("amount")),
                "exp_byte":Struct(None, ULInt8("amount")),
                "exp_word":Struct(None, ULInt16("amount")),
                "exp_dword":Struct(None, ULInt32("amount")),
                "attr_byte":Struct(None, attr_code, ULInt8("amount")),
                "attr_word":Struct(None, attr_code, ULInt16("amount")),
                "attr_dword":Struct(None, attr_code, ULInt32("amount")),
                "player_attr":Struct(None,
                    ULInt32("player_id"),
                    attr_code,
                    ULInt32("amount")
                ),
                "update_item_oskill":Struct(None,
                    ULInt16("unknown1"),
                    sid("entity_id"),
                    #ULInt16("skill_code"),
                    skills,
                    ULInt8("base_level"),
                    ULInt8("bonus_amount"),
                    ULInt8("unknown2")
                ),
                "skill_book_count":Struct(None,
                    entity_type,
                    #ULInt8("entity_type"),
                    ULInt8("unknown1"),
                    ULInt32("entity_id"),
                    #ULInt16("skill_code"),
                    skills,
                    ULInt8("stats_amount"),
                    ULInt16("unknown2")
                ),
                "skill_select":Struct(None,
                    etype_eid(),
                    Enum(ULInt8("skill_side"),
                        right = 0x00,
                        left = 0x01
                    ),
                    #ULInt16("skill_code"),
                    skills,
                    ULInt32("unknown")
                ),
                "chat":Struct(None,
                    Enum(ULInt16("chat_type"),
                        open_chat = 0x01,
                        recv_whisp = 0x02,
                        system = 0x04,
                        overhead = 0x05,
                        sent_whisp = 0x06,
                    ),
                    etype_eid(),
                    ULInt8("unknown1"),
                    ULInt8("unknown2"),
                    CString("char_name"),
                    CString("message")
                ),
                "npc_interact":Struct(None,
                    etype_eid(),
                    Bytes("unknown", 34)
                ),
                "quest_tree":Struct(None, Bytes("quest_info", 103 - 1)),
                "game_quest_info":Struct(None, Bytes("quest_info", 97 - 1)),
                "npc_transaction":Struct(None,
                    ULInt8("trade_type"),
                    ULInt8("result"),
                    ULInt32("unknown"),
                    sid("npc_id"),
                    ULInt32("gold_in_inventory")
                ),
                "sound":Struct(None, etype_eid(), ULInt16("sound_id")),
                "update_item_stats":Struct(None, Bytes("data", 34 - 1)),
                "use_stackable_item":Struct(None,
                    ULInt8("unknown1"),
                    sid("item_entity_id"),
                    ULInt16("unknown2")
                ),
                "mouse_clear":Struct(None, etype_eid()),
                "relator_1":Struct(None,
                    ULInt16("unknown1"),
                    sid("entity_id"),
                    ULInt32("unknown2")
                ),
                "relator_2":Struct(None,
                    ULInt16("unknown1"),
                    sid("entity_id"),
                    ULInt32("unknown2")
                ),
                "entity_attack_entity":Struct(None,
                    etype_eid("attacker"),
                    #ULInt16("skill_code"),
                    skills,
                    ULInt8("skill_level"),
                    etype_eid("defender"),
                    Const(ULInt16(None), 0x00)
                ),
                "entity_attack_location":Struct(None,
                    etype_eid(),
                    #ULInt16("skill_code"),
                    skills,
                    Const(ULInt16(None), 0x00),
                    ULInt8("skill_level"),
                    xy16(),
                    Const(ULInt16(None), 0x00)
                ),
                "merc_for_hire":Struct(None,
                    ULInt16("merc_id"),
                    ULInt32("unknown")
                ),
                "stat_merc_list":Struct(None, Pass),
                "object_assign":Struct(None,
                    etype_eid(),
                    ULInt16("entity_class_code"),
                    xy16(),
                    ULInt8("state"),
                    ULInt8("interaction"),
                ),
                "quest_log_info":Struct(None, Bytes("data", 42 - 1)),
                "game_refresh":Struct(None,
                    ULInt32("possible_player_slot"),
                    ULInt8("some_boolean"),
                    ULInt32("some_counter")
                ),
                "player_assign":Struct(None,
                    sid("player_id"),
                    char_type,
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name)),
                    xy16()
                ),
                "event_notify":Struct(None,
                    Enum(ULInt8("event"),
                        dropped_due_timeout = 0x00,
                        dropped_due_errors = 0x01,
                        joined_the_game = 0x02,
                        quit_the_game = 0x03,
                        not_in_the_game = 0x04,
                        not_logged_in_the_game = 0x05,
                        was_slain = 0x06,
                        player_relations = 0x07,
                        busy = 0x08,
                        wait_a_short_time = 0x09,
                        item_in_box = 0x0a,
                        not_listenning_you = 0x0d,
                        not_enough_mana = 0x0e,
                        realm_goind_down = 0x0f,
                        wait_before_host = 0x10,
                        soj_sold = 0x11,
                        diablo_walks = 0x12
                    ),
                    Enum(ULInt8("action"),
                        neutral = 0x00,
                        teaming = 0x02,
                        friendly = 0x04,
                        nasty = 0x08,
                        remove = 0x09
                    ),
                    sid("some_number_or_id"),
                    entity_type,
                    #ULInt8("entity_type"),
                    CString("A"),
                    Bytes("_unused1", lambda ctx: 15 - len(ctx.A)),
                    CString("B"),
                    Bytes("_unused2", lambda ctx: 15 - len(ctx.B)),
                ),
                "player_in_game":Struct(None,
                    ULInt16("pack_len"),
                    sid("player_id"),
                    char_type,
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name)),
                    ULInt16("char_level"),
                    ULInt16("party_number"),
                    Padding(lambda ctx: ctx.pack_len - 28)
                ),
                "player_quit_game":Struct(None, sid("player_sid")),
                "tele_state":Struct(None,
                    Enum(ULInt8("state"),
                        unused_town_area = 0x00,
                        unused_area = 0x03,
                        used_town_area = 0x05,
                        used_area = 0x07
                    ),
                    ULInt8("area_id"),
                    sid("teleport_id")
                ),
                "wp_state":Struct(None,
                    sid("wp_id"),
                    Const(ULInt16(None), 0x0102),
                    Bytes("wp_avaliblity", 14)
                ),
                "kill_count":Struct(None,
                    sid("entity_id"),
                    ULInt16("count")
                ),
                "npc_move":Struct(None,
                    sid("npc_id"),
                    ULInt8("movement_type"),
                    xy16(),
                    Bytes("unknown", 6)
                ),
                "npc_to_target":Struct(None,
                    sid("npc_id"),
                    ULInt8("movement_type"),
                    xy16(),
                    etype_eid("target"),
                    Bytes("unknown", 6)
                ),
                "npc_state_assign":Struct(None,
                    sid("npc_id"),
                    ULInt8("npc_state"),
                    xy16(),
                    ULInt8("life_percent"),
                    ULInt8("unknown")
                ),
                "npc_action":Struct(None,
                    sid("npc_id"),
                    ULInt8("action_type"),
                    Const(Bytes(None, 6), b"\x00\x00\x00\x00\x00\x00"),
                    xy16()
                ),
                "npc_attack":Struct(None,
                    sid("npc_id"),
                    #ULInt16("skill_code"),
                    skills,
                    etype_eid("defender"),
                    xy16()
                ),
                "npc_stop":Struct(None,
                    sid("npc_id"),
                    xy16(),
                    ULInt8("life_percent")
                ),
                "about_player":Struct(None,
                    sid("player_id"),
                    ULInt16("party_id"),
                    ULInt16("char_level"),
                    ULInt16("relationship_flag"),
                    Flag("in_your_party"),
                    Const(ULInt8(None), 0)
                ),
                "overhead_clear":Struct(None, etype_eid()),
                "trade":Struct(None, ULInt8("button_action")),
                "who_trade":Struct(None,
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name)),
                    sid("player_id")
                ),
                "gold_trade":Struct(None,
                    Flag("verifyed"),
                    ULInt32("amount")
                ),
                "summon_log":Struct(None,
                    Enum(ULInt8("action"),
                        remove = 0x00,
                        add = 0x01
                    ),
                    ULInt8("skill_number"),
                    ULInt16("summoned_class"),
                    sid("player_id"),
                    sid("summoned_id")
                ),
                "bind_skill_to_hotkey":Struct(None,
                    ULInt8("slot"),
                    ULInt8("skill"),
                    ULInt8("side"),
                    Const(ULInt32(None), 0xffffffff)
                ),
                "use_item":Struct(None,
                    ULInt8("type"),
                    sid("item_id")
                ),
                "party_update":Struct(None,
                    entity_type,
                    #ULInt8("entity_type"),
                    ULInt16("life_percent"),
                    sid("entity_id"),
                    ULInt16("area_id")
                ),
                "merc_owner":Struct(None,
                    Const(ULInt16(None), 0x5207),
                    etype_eid(),
                    sid("merc_id"),
                    ULInt32("unknown1"),
                    ULInt32("unknown2")
                ),
                "tele_owner":Struct(None,
                    sid("player_owner_id"),
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name)),
                    sid("tp_id_your_side"),
                    sid("tp_id_other_side")
                ),
                "quest_event":Struct(None, ULInt8("event_id")),
                "entity_request_chat":Struct(None, etype_eid()),
                "party_invite_status":Struct(None,
                    sid("player_id"),
                    ULInt8("relation_status")
                ),
                "player_relationship":Struct(None,
                    sid("player_id_1"),
                    sid("player_id_2"),
                    ULInt16("relationship_flag")
                ),
                "party_number":Struct(None,
                    sid("player_id"),
                    ULInt16("party_number")
                ),
                "corpse_assign":Struct(None,
                    Enum(ULInt8("event"),
                        remove = 0x00,
                        add = 0x01
                    ),
                    sid("player_id"),
                    sid("corpse_id")
                ),
                "pong":Struct(None, Bytes("server_response", 32)),
                "party_pulse":Struct(None,
                    sid("player_id"),
                    ULInt32("mini_map_x"),
                    ULInt32("mini_map_y")
                ),
                "skill_log":Struct(None,
                    ULInt8("count"),
                    sid("player_id"),
                    Array(lambda ctx: ctx.count, Struct("skill",
                            #ULInt16("skill_code"),
                            skills,
                            ULInt8("skill_level")
                        )
                    )
                ),
                "resources":BitStruct(None,
                    BitField("life", 15),
                    BitField("mana", 15),
                    BitField("stamina", 15),
                    BitField("x", 15),
                    BitField("unknown1", 1),
                    BitField("y", 15),
                    BitField("unknown2", 20),
                ),
                "walk_verify":BitStruct(None,
                    BitField("stamina", 15),
                    BitField("location_x", 15),
                    BitField("unknown1", 1),
                    BitField("location_y", 15),
                    BitField("unknonw2", 18)
                ),
                "weapon_switch":Struct(None, Pass),
                "skill_triggered":Struct(None, Bytes("data", 16 - 1)),
                "merc_attr_byte":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt8("amount")
                ),
                "merc_attr_word":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt16("amount")
                ),
                "merc_attr_dword":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt32("amount")
                ),
                "merc_attr_add_byte":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt8("amount")
                ),
                "merc_attr_add_word":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt16("amount")
                ),
                "baal_spawn":Struct(None, ULInt16("uniq_code_class")),
                "aura_effect":Struct(None, etype_eid(), ULInt8("effect_code")),
                "set_state":Struct(None,
                    etype_eid(),
                    ULInt8("length_of_packet"),
                    ULInt8("state"),
                    Bytes("stats_list", lambda ctx: ctx.length_of_packet - 1 - 7)
                ),
                "end_state":Struct(None, etype_eid(), ULInt8("state")),
                "entity_info_add":Struct(None,
                    etype_eid(),
                    ULInt8("length_of_packet"),
                    Bytes("stats_list", lambda ctx: ctx.length_of_packet - 1 - 6)
                ),
                "entity_heal":Struct(None, etype_eid(), ULInt8("life_percent")),
                "npc_assign":Struct(None,
                    sid("npc_id"),
                    ULInt16("npc_class_code"),
                    xy16(),
                    ULInt8("life_percent"),
                    ULInt8("length_of_packet"),
                    Bytes("stats_list", lambda ctx: ctx.length_of_packet - 1 - 12)
                ),
                "warden":Struct(None,
                    ULInt8("length_of_packet"),
                    Bytes("stats_list", lambda ctx: ctx.length_of_packet - 1 - 1)
                ),
                "compression":Struct(None, Flag("active")),
                "game_termination":Struct(None, Pass),
                "timeout_full":Struct(None, Enum(ULInt32("reason"),
                        bad_char_version = 0x01,
                        bad_char_quest_data = 0x02,
                        bad_char_wp_data = 0x03,
                        bad_char_stats_data = 0x04,
                        bad_char_skill_data = 0x05,
                        unable_to_join = 0x06,
                        bad_char_inventory = 0x07,
                        bad_char_bodies = 0x08,
                        bad_header = 0x09,
                        bad_char_merc = 0x0a,
                        bad_intro = 0x0b,
                        bad_item = 0x0c,
                        bad_char_dead_body_item = 0x0d,
                        generic_bad_file = 0x0e,
                        game_is_full = 0x0f,
                        bad_game_version = 0x10,
                        must_kill_norm_baal = 0x11,
                        must_kill_night_baal = 0x12,
                        soft_cant_to_hard = 0x13,
                        hard_cant_to_soft = 0x14,
                        dead_hard_cant = 0x15,
                        unknown_failure = 0x16,
                        classic_cant_exp = 0x17,
                        exp_cant_classic = 0x18,
                        failed_to_join = 0x19,
                        unable_to_enter_the_game = 0x1a
                    )
                ),

                #item actions
                "world_item_action":Struct(None,
                    d2item_header,
                    Bytes("next", lambda ctx: ctx.length_of_packet - 1 - 7)
                ),
                "owner_item_action":Struct(None,
                    d2item_header,
                    etype_eid("owner"),
                    Bytes("next", lambda ctx: ctx.length_of_packet - 1 - 12)
                ),

                #unknown, but length
                "unknown_0x50":Struct(None, Bytes("data", 15 - 1)),
                "unknown_0x5e":Struct(None, Bytes("data", 38 - 1)),
                "unknown_0x5f":Struct(None, Bytes("data", 5 - 1)),
                "unknown_0x7e":Struct(None, Bytes("data", 5 - 1)),
                "unknown_0x91":Struct(None, Bytes("data", 26 - 1)),
                "unknown_0xa5":Struct(None, Bytes("data", 8 - 1)),
                "unknown_0xc1":Struct(None, Pass),
                "unknown_0xca":Struct(None, Bytes("data", 25 - 1)),
                "unknown_0xcb":Struct(None, Bytes("data", 23 - 1)),
                "unknown_0xcc":Struct(None, Bytes("data", 15 - 1)),
            },
            default = Struct(None,
                Pointer(lambda ctx: ctx.start_fun, HexDumpAdapter(GreedyRange(ULInt8("data")))),
                GreedyRange(ULInt8(None))
            )
        )
    )
)

if __name__ == "__main__":
    data = b'''\x01\x02\x04\x20\x20\x00\x00\x01\x00\x02\x03\x03\x79\x10\x6d\
\x44\x67\x00\xd8\x04\xda\x28\x04\x05\x07\xf0\x03\xf0\x03\x67\x0b\x00\x01\x00\
\x00\x00\x0e\x02\x12\x00\x00\x00\x03\x01\x02\x00\x00\x00\x22\x00\xa0\x01\x00\
\x00\x00\xda\x00\x13\x44\x00\x22\x00\xa0\x01\x00\x00\x00\xdc\x00\x14\x44\x00\
\x26\x04\x00\x02\x00\x00\x00\x00\x01\x00\x5b\x73\x79\x73\x5d\x00\x57\x65\x6c\
\x63\x6f\x6d\x65\x20\x74\x6f\x20\x50\x6c\x61\x79\x47\x72\x6f\x75\x6e\x64\x2e\
\x72\x75\x20\x44\x69\x61\x62\x6c\x6f\x20\x49\x49\x20\x73\x65\x72\x76\x65\x72\
\x2e\x00\x26\x05\x00\x00\x03\x00\x00\x00\x1c\xfc\x00\x79\x6f\x62\x61\x00\x26\
\x06\x00\x02\x00\x00\x00\x00\x00\xe5\x70\x6d\x63\x61\x00\x71\x00\x26\x02\x00\
\x02\x00\x00\x00\x00\x00\x02\x70\x6d\x61\x61\x00\x71\x00\x5b\x24\x00\x03\x00\
\x00\x00\x00\x70\x6d\x63\x61\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x01\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x94\x08\x03\x00\x00\x00\x00\
\x00\x01\x02\x00\x01\x01\x00\x01\xd9\x00\x01\xda\x00\x01\xdb\x00\x01\xdc\x00\
\x01\x03\x00\x01'''
    from recipe import *
    from d2crypt import Decrypter

    s2c = OptionalGreedyRange(s2c_packets)

    #a = rev("f1 2c 06 a1 e2 0a fe f1 7c 6c 1c 86 c1 82 2e 0c a7 a5 91 a5 60 ca 76 36 8d 27 65 33 d1 90 72 15 46 b1 a4 6e 1a 0b 42 18 d6 37 1d 8a 6a c6 42 c1 e8 d2 76 2b 8a e7 63 60 ca 35 8d e3 28 d6 21 c5 d7 e8 55 8d a3 60 c4 36 8d 63 20 d5 ff e0 86 fc c9 58 ba 19 9b 3a 1b ef c0 89 b3 fd d7 bb dc 25 dc 26 5c 26 dc 27 5d 8b 9f b8 68 b8 69 b8 6a bd d9 5d cc 58 76 91 3b a3 77 32 77 33 76 8d 5d 76 9d a3 77 70 e7 7e 12 ee 29 c3 9d f8 4d b8 a7 0f 5d fb cf a4 1d 12 93 87 50 98 7c 2a 01 20 3a bb 6d 9d 40 b8 47 0c 83 48 54 02 40 75 70 36 bf 0b 81 b9 18 3a bf 9b bb 6d b6 d8 c2 fb de f7 f7 77 df bb ee ef 7b e3 81 29 0f de e6 87 26 86 52 38 11 c8 e6 8f 79 a9 a0 e4 1b b0 68 3c 1a b0 68 c1 a3 de e6 8e 68 8e e6 86 06 82 89 a3 de e6 8e c9 dd ff fe 1c 1a 23 8f 66 e6 53 03 51 81 af ff c3 ee b6 b7 90 1d 6f 3b 90 1c 80 90 15 b5 bc ee 40 56 f5 b2 02 40 7d 6d 6f ff fd 6f 5b d6 d6 ff fe 63 7e 31 3f 39 9c 9c b9 1c e5 76 80 f1 bc 50 7c 20 39 d2 28 8a 86 a0 c1 68 14 3a 31 86 15 e7 26 45 73 a3 32 00 92 1e 40 aa 03 a3 47 e6 95 b1 96 7a 22 04 83 63 e3 c8 6e 01 c9 e2 98 56 06 cb 90 80 0c 35 9f 02 a8 03 73 45 f9 a5 6c 65 8c e2 20 48 36 3e 3c 86 e9 62 9a 10 7e 15 45 00 2a 81 41 a1 fe 69 5a 8c 65 aa 11 02 41 b1 f5 ce c0 68 25 14 c6 62 81 98 fe 0f 87 70 2a 46 68 d1 07 34 40 40 23 19 51 a1 08 48 45 c3 eb 81 54 0a 0d 18 e6 95 b1 96 33 08 81 20 d8 f8 f2 1b b0 09 45 31 98 03 91 87 f0 7c 3b 81 64 24 b3 44 3e fc d6 b5 18 ca 29 a0 34 09 05 64 43 c8 59 4e 02 a5 34 c4 00 76 40 08 c4 00 da 3c 87 cc 04 54 80 74 d8 a2 3b 86 23 a0 2c 84 40 34 45 ef cd 6b 63 28 37 32 3b 2f 85 64 23 c8 55 60 7b 12 96 96 9d 30 09 01 26 a1 05 92 d0 0e 50 db 81 64 22 01 a2 3f 7e 6b 5b 19 42 a1 18 ec be 15 90 ae 16 d2 8f 62 52 d2 d3 a6 01 20 24 d4 20 32 5a 01 ca 1b 70 2c 84 49 34 30 f7 e6 b5 b1 94 3b 65 68 3a 0f 10 8f 21 68 21 91 84 31 8c af 19 02 20 09 32 02 ab 45 20 32 31 92 c0 30 e2 40 87 c0 2c 78 14 49 24 f0 06 4a 0d 28 80 a9 19 a3 44 9c d2 40 23 19 51 91 82 12 11 70 fa e0 54 8c d1 a1 8f 34 90 08 c6 54 66 c1 09 08 b8 7d 70 2a 46 68 d0 cb 9a 20 20 23 2a 35 c2 12 11 70 fa e0 54 8c d1 a2 5e 68 80 80 46 32 a3 48 10 90 8b 87 d7 02 a4 66 8d 08 dc d2 40 23 19 51 a0 5a 84 5c 3e b8 15 23 34 68 67 cd 24 02 31 95 19 92 d4 22 e1 f5 c0 a9 19 a3 43 4e 69 20 23 2a 34 c1 09 08 b8 7d 70 f1 a9 02 a8 0e 8d 0d 79 a5 6a 31 96 68 22 04 81 20 fa e1 60 03 82 91 c5 73 31 f0 29 27 07 23 b8 15 40 21 1a 26 e6 95 a8 c6 59 50 44 09 06 c7 c7 90 be 5d 06 7b 30 f2 24 46 f2 c1 28 1c 04 21 f0 0c 9b 13 ca a3 78 69 07 83 b8 15 40 1b 9a 33 cd 2b 63 2c 6b 11 02 41 b1 f5 ce d8 8d 41 50 7b 02 8d 81 54 07 66 8d 73 4a d8 cb 1a 84 40 90 6c 7c 79 4e 9c 9e 01 05 31 50 6a 21 19 12 5b 70 2a 46 68 d1 3f 34 40 40 46 54 75 a8 45 53 eb 81 52 33 46 86 dc d2 40 46 54 6d 2d 42 2a 9f 5c 0b 21 10 cd 0d fd f9 ad 6d 74 06 a4 e0 f4 1c a1 1e 42 99 31 11 a9 70 97 06 a0 e0 04 9a 89 a0 3d 82 81 2c 05 8d c1 7c 34 a2 02 a8 03 73 43 8e 69 5b 19 68 c4 40 90 24 1f 5c ed 3c 63 0a 82 b9 00 d8 15 23 34 68 47 e6 88 08 08 ca 8d 1a d4 22 a9 f5 c0 aa 06 8d 09 1c d2 40 46 59 d8 7e 88 45 3e b8 15 40 d1 a0 6d cd 24 04 65 93 83 f4 41 d1 f5 c0 aa 06 8d 03 7e 69 20 23 2c 39 0f d1 0d 87 d7 02 a8 0d cd 0e 79 a5 6c 65 a0 0e 43 20 08 44 3c 80 82 28 e8 0a a0 12 0d 14 73 4a d4 63 2d 30 88 12 03 c3 e3 c8 5f 60 1d c8 a4 c4 39 24 87 11 c8 71 b8 85 25 00 70 86 90 0d 1b 0a 82 d8 31 10 4f 42 d8 7c 07 48 40 7e 18 45 11 44 29 0a 00 55 03 46 87 5c d2 40 46 58 a4 1f a2 27 9f 5c 0a a0 68 d0 ef 9a 48 08 cb 18 c3 f4 43 d1 f5 c0 aa 06 8d 03 8e 69 20 23 2c b0 1f 9b 8b 67 d7 02 a8 1a 34 0e 79 a4 80 8c b5 c3 f4 43 d1 f5 c0 f1 b0 02 c8 49 4e 1d 7b f3 54 6b 50 0c a5 a4 2b 43 d1 25 10 28 04 25 c3 10 0e 64 47 4e 18 5b 1e c5 c2 50 3b 6d c0 b3 24 73 40 ef a0 0e b9 c4 80 8c a7 13 b0 f4 f9 f5 c0 b3 24 73 42 4f 40 1d 73 89 01 19 4e 17 3b 37 1e 8f ae 05 99 23 9a 07 9d 00 75 ce 24 02 31 94 e1 01 da 21 14 fa e0 59 08 86 68 1e fb f3 5a da e2 9a 70 84 37 83 94 23 c8 42 1e 10 b4 b5 6c 78 06 c0 18 c8 4f 2d 10 e6 02 c9 28 03 8b a1 6c 50 02 a4 66 8d 09 5c d2 40 46 54 66 8b 50 8a a7 d7 02 a8 14 1a 07 dc d2 b6 32 c6 81 10 24 1b 1f 1e 52 a5 06 ad 21 27 0a c3 e0 15 6c 0a a0 3a 34 0f f9 a5 6c 65 8a 82 20 48")
    #b = rev("36 3e 3c 86 e0 1c 83 2b 85 a1 4c 7d 01 84 22 d6 c0 aa 00 dc d0 40 e6 95 b1 96 90 44 09 02 41 f1 e4 37 4f 2d 05 41 5c 0c b6 05 50 06 e6 82 0f 34 ad 8c b3 21 10 24 09 07 d7 3b 62 31 85 41 ec 80 6c 0a a0 0d cd 04 2e 69 5b 19 64 61 10 24 09 07 d7 10 58 96 82 a0 ae 06 5b 02 a8 1a 34 10 f9 a4 80 8c b8 7e 88 45 3e b8 15 40 72 68 00 39 a4 0c c6 5a 40 26 17 02 f8 9c 09 87 70 0e 16 c1 50 c2 0d 08 c7 e0 55 00 76 c1 2f 9a 56 c6 59 00 04 c9 e3 82 25 c4 20 a4 06 06 96 93 82 03 40 46 08 0e 06 12 64 34 19 81 54 07 6c 13 39 a5 6c 65 90 20 4c 9e 38 22 5c 87 2e 10 21 b9 a9 a1 d9 5c 5b 00 8d b8 16 42 22 c4 4f 7e 6a 8d 6c 65 0e d7 29 9b a1 44 04 02 f8 f0 66 34 0c 65 33 48 a6 b8 0a 40 02 90 80 a1 58 94 4e 04 e1 a4 3a 3d 28 89 01 58 50 f1 ae 02 cc 91 cd 04 5e 80 44 e7 12 02 32 9c 4e c3 d3 e7 d7 02 a8 09 2e 23 73 4a d8 cb 03 e3 e0 09 0a c8 47 90 a4 01 12 90 ea 84 b0 08 b4 c4 03 0b c7 61 88 07 91 44 59 98 15 40 a1 81 1f 9a 56 c6 5c 7f 27 8e 08 97 20 0a 61 50 b2 10 01 b0 23 02 43 fb 60 55 03 46 82 47 34 90 11 96 b4 3f 37 64 fa e0 55 01 d1 a0 93 cd 2b 63 2c 53 11 02 40 78 7c 79 0d c0 39 75 50 76 3c 04 21 f8 48 6d c0 aa 06 8d 04 ae 69 20 23 2c 79 0f d1 0f 47 d7 02 a8 04 76 04 be 69 5b 19 60 74 33 87 86 c8 47 90 9c 0d 4d 44 42 4a e1 09 08 42 3b 29 89 43 20 11 21 55 00 73 c3 10 e8 94 5e 16 c1 40 8c 22 14 00 39 68 78 4a 04 9b 02 a8 1a 34 13 39 a4 80 8c b1 8c 08 09 02 4a 15 c0 aa 06 8d 09 bc d2 40 46 59 60 52 12 44 94 2b 81 54 04 a3 41 37 9a 56 c6 58 a4 98 24 15 91 0f 20 0c 06 87 87 68 80 d8 76 53 16 09 84 92 cc 64 16 03 10 a0 03 42 b8 a0 05 90 9c 9a 09 de fc d6 b6 32 96 8d cd 0d 94 a2 1e 41 29 0e 18 c5 00 2c 84 50 42 27 fb f3 54 6b 50 0c a0 18 8e b4 7a 0f 10 8a 44 01 04 81 82 a0 f0 1a c5 51 58 7f 1a 8f b0 03 03 62 98 88 34 14 cf 42 72 d4 c0 f8 b0 32 13 8c 8b e1 58 94 33 04 63 72 39 1d b7 02 cc 91 cd 05 0e 80 4f e7 12 02 32 9c 4e d1 08 a7 d7 02 cc 91 cd 09 dd 00 9f ce 24 04 65 38 5c ed 11 64 fa e0 59 92 39 a0 a3 d0 09 fc e2 40 46 53 84 07 66 e1 d1 f5 c0 b3 24 73 41 4b a0 13 f9 c4 80 8c a7 08 4e cd c7 a3 eb 80 f1 9c 02 c8 4e 98 27 fb f3 54 6b 63 28 1b 48 4b 0f 04 94 45 82 00 9c 28 83 50 d6 7c 0b 32 47 34 14 fa 02 7f 38 90 11 94 e2 76 1e 9f 3e b8 16 64 8e 68 50 e8 09 fc e2 40 46 53 85 ce c3 d3 e7 d7 02 cc 91 cd 05 4e 80 9f ce 24 04 65 38 40 76 1e 9f 3e b8 16 64 8e 68 2a f4 04 fe 71 20 23 29 c2 13 b0 f4 f9 f5 c0 b3 24 73 41 5b a0 27 f3 89 01 19 4e 11 9d 87 a7 cf ae 05 99 23 9a 0a fd 01 3f 9c 48 08 ca 70 90 ec 3d 3e 7d 70 2c 84 47 42 2c 7b f3 54 6b 50 0c a0 19 19 04 5e 15 11 07 20 8c d0 c0 1c 39 99 80 60 03 0b 8d c5 80 f8 1c 04 41 f0 0e 1b 0b 20 04 41 14 42 c0 8a 3d 03 d0 c4 28 01 66 48 e6 82 cf 40 2c 73 89 00 8c 65 38 9d 9b 88 a7 d7 02 cc 91 cd 0a 3d 00 b1 ce 24 04 65 38 5c ed 10 b6 7d 70 0a ba ee db 6d b6 01 4f 84 eb 6d b6 d8 05 40 6a ed b6 db 60 15 83 37 6d b6 db 00 a8 44 8b 6d b6 d8 05 44 d3 b6 db 6d 80 54 66 ee db 6d b6 01 4c 0e ed b6 db 60 15 22 37 6d b6 db 0e af df 6d b6 db 0e af e6 ee db 6d b6 73 39 39 72 39 ca ed 28 3e 10 1c e9 14 45 43 50 60 b4 0a 1d 18 c3 0a f3 93 22 b9 d1 99 00 49 0f 27 21 ea 83 90 f9 41 c8 80 a0 e4 42 50 7e 01 8a 21 c8 86 f2 ca d0 20 2c 0b 6b ff a2 01 48 08 23 ee 89 6a 00 3e 7d d1 2d 40 41 1f 74 40 29 00 1f 3e e8 8b 88 00 f9 f7 44 b5 01 06 7d d1 00 a4 04 11 f7 44 5c 40 41 1f 74 40 29 01 06 7d c0 f1 50 44 5c 40 41 9f 74 f7 e0 ac d8 6c 4c e3 b7 82 37 e5 47 05 66 c3 62 65 a4 70 1e b9 d8 ff ce 3c 10 bb f3 25 62 e8 66 6c e8 80 4a fc 06 0e 01 75 00 17 32 7e 57 02 f7 e0 d0 0b ae fc 09 90 08 9f c6 24 52 01 0b f8 14 45 03 07 4f ca 0c 10 09 5f 80 c1 c0 2e a0 20 14 3f 25 8b 84 76 00 ba 77 e4 d0 2e 6c fc 52 02 e1 eb f1 fc 0b 87 cf c7 f0 2e 20 3f 1f c0 b8 84 fc 7f 58 fc 15 9b 0d 89 96 82 33 0e 04 e0 38 d9 52 65 a4 67 04 2e 61 cc 95 8b a1 99 b3 a5 86 1c 07 1b 2a 4c b4 f1 76 79 26 5e 36 2c 26 5e 46 5d 9e 7e bf 3c 5d 37 24 c0 51 b0 d2 99 79 19 74 dc fd 7e 78 b9 af 1c 20 78 d8 ac 99 79 19 73 5e 7d d7 e0 8d 1f 1f e5 d3 62 e2 65 a6 86 a8 e0 85 d1 f3 25 62 e8 66 6c e9 62 3e 5d 36 2e 26 5a 78 b9 a7 0e e5 d3 61 bd 36 78 b9 9f 16 a0 78 d8 78 4d 9e 2e 46 e4 99 70 d8 79 4c bc 8c b9 1b 9f af cf 17 4b c9 30 36 6c 39 26 5e 46 5d 2f 3f 5f")

    a = rev("f1 2b 06 a1 e2 0a fe f1 7c 6c 1c 86 c1 82 2e 0c a7 a5 91 a5 60 ca 76 36 8d 27 65 33 d1 90 72 15 46 b1 a4 6e 1a 0b 42 18 d6 37 1d 8a 6a c6 42 c1 e8 d2 76 2b 8a e7 63 60 ca 35 8d e3 28 d6 21 c5 d7 e8 55 8d a3 60 c4 36 8d 63 20 d5 ff e0 86 fc c9 58 ba 19 9b 3a 1b ef c0 89 b3 fd d7 bb dc 25 dc 26 5c 26 dc 27 5d 8b 9f b8 68 b8 69 b8 6a bd d9 5d cc 58 76 91 3b a3 77 32 77 33 76 8d 5d 76 9d a3 77 70 e7 7e 12 ee 01 e1 ce fc 26 dc 03 c3 d7 7e f3 e9 07 44 a2 50 e4 0d 0f 88 c2 88 1e 5d b6 ce a0 5c 23 86 41 a4 46 14 40 f2 e0 6d 7e 17 0a a8 c3 ab fa ee db 6d b6 30 be f7 bd fd dd f7 ee fb bb de f8 e0 4a 43 f7 b9 a1 c9 a1 94 8e 04 72 39 a3 de 6a 68 39 06 ec 1a 0f 06 ac 1a 30 68 f7 b9 a3 9a 23 b9 a1 81 a0 a2 68 f7 b9 a3 b2 77 7f ff 87 06 88 e3 d9 b9 94 c0 d4 60 6b ff f0 fb ad ad e4 07 5b ce e4 07 20 24 05 6d 6f 3b 90 15 bd 6c 80 90 1f 5b 5b ff ff 5b d6 f5 b5 bf ff 98 df 8c 4f ce 67 27 2e 47 39 5d a0")

    d = Decrypter()
    def yoba(a):
        print("\n\n\nreal:")
        print(rev(a))
        try:
            print("head before", d.head)
            print("decrypted:")
            rda = d.decrypt(a)
            print(len(rda))
            print("head after", d.head)

            print("\nparsing:")
            for da in rda:
                print()
                print(rev(da))
                try:
                    pda = s2c.parse(da)
                    print(pda)
                except:
                    print("can't parse")
        except:
            print("can't decrypt")

    yoba(a)
    #yoba(b)
    #yoba(a + b)
