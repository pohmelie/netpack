from construct import *


position = Struct(None, ULInt16("x"), ULInt16("y"))

action_to_a_object = Struct(None,
    Enum(ULInt32("object_type"),
        another_player = 0x00,
        town_folk_or_monster = 0x01,
        stash_wp_or_tp = 0x02,
        item = 0x04,
        doorway = 0x05
    ),
    ULInt32("object_id")
)

chat = Struct(None,
    Enum(ULInt8("mode"),
        overhead = 0x00,
        normal = 0x01,
        whisper = 0x02
    ),
    Padding(1),
    Embed(Switch(None, lambda ctx: ctx.mode, {
                "overhead":Struct(None, CString("message"), Padding(2)),
                "normal":Struct(None, CString("message"), Padding(2)),
                "whisper":Struct(None,
                    CString("message"),
                    CString("char_name"),
                    Padding(1)
                )
            }
        )
    )
)

object_id = Struct(None, ULInt32("object_id"))

c2s_packets = Struct("c2s packets",
    Enum(UBInt8("fun"),
        walk = 0x01,
        walk_to_a_object = 0x02,
        run = 0x03,
        run_to_a_object = 0x04,
        left_skill_on_location = 0x05,
        left_skill_on_object = 0x06,
        shift_left_skill_on_object = 0x07,
        left_skill_on_location_repeat = 0x08,
        left_skill_on_object_repeat = 0x09,
        shift_left_skill_on_object_repeat = 0x0a,
        unknown_0b = 0x0b,
        right_skill_on_location = 0x0c,
        right_skill_on_object = 0x0d,
        shift_right_skill_on_object = 0x0e,
        right_skill_on_location_repeat = 0x0f,
        right_skill_on_object_repeat = 0x10,
        shift_right_skill_on_object_repeat = 0x11,
        unknown_12 = 0x12,
        interact_with_object = 0x13,
        send_overhead_chat = 0x14,
        send_normal_chat = 0x15,
        pick_up_object_from_ground = 0x16,
        drop_object_from_cursor_to_the_ground = 0x17,
        place_object_in_a_location = 0x18,
        pick_up_object_from_storage = 0x19,
        put_on_a_body_item = 0x1a,
    ),
    Embed(Switch("", lambda ctx: ctx.fun, {
                "walk":position,
                "walk_to_a_object":action_to_a_object,
                "run":position,
                "run_to_a_object":action_to_a_object,
                "left_skill_on_location":position,
                "left_skill_on_object":action_to_a_object,
                "shift_left_skill_on_object":action_to_a_object,
                "left_skill_on_location_repeat":position,
                "left_skill_on_object_repeat":action_to_a_object,
                "shift_left_skill_on_object_repeat":action_to_a_object,
                "unknown_0b":Pass,
                "right_skill_on_location":position,
                "right_skill_on_object":action_to_a_object,
                "shift_right_skill_on_object":action_to_a_object,
                "right_skill_on_location_repeat":position,
                "right_skill_on_object_repeat":action_to_a_object,
                "shift_right_skill_on_object_repeat":action_to_a_object,
                "unknown_12":Pass,
                "interact_with_object":action_to_a_object,
                "send_overhead_chat":chat,
                "send_normal_chat":chat,
                "pick_up_object_from_ground":Struct(None,
                    Const(ULInt32("request_id"), 0x04),
                    ULInt32("object_id"),
                    Enum(ULInt32("object_direction"),
                        to_inventory = 0x00,
                        to_cursor = 0x01
                    )
                ),
                "drop_object_from_cursor_to_the_ground":object_id,
                "place_object_in_a_location":Struct(None,
                    ULInt32("object_id"),
                    ULInt32("x"),
                    ULInt32("y"),
                    Enum(ULInt32("object_direction"),
                        inventory = 0x00,
                        cube_or_trade = 0x02,
                        stash = 0x04
                    )
                ),
                "pick_up_object_from_storage":object_id,
                "put_on_a_body_item":Struct(None,
                    ULInt32("object_id"),
                    Enum(ULInt16("body_location"),
                        hat = 0x01,
                        amulet = 0x02,
                        body_armor = 0x03,
                        left_side_weapon = 0x04,
                        right_side_weapon = 0x05,
                        left_side_ring = 0x06,
                        right_side_ring = 0x07,
                        belt = 0x08,
                        boots = 0x09,
                        gloves = 0x0a
                    ),
                    Padding(2)
                )
            }
        )
    )
)

if __name__ == "__main__":
    data = b'''\x01\x87\x58\x63\x1a\x02\x02\x00\x00\x00\x18\x00\x00\x00\x06\x01\
\x00\x00\x00\x1e\x00\x00\x00\x0b\x15\x01\x00\x79\x6f\x62\x61\x00\x00\x00\x14\
\x00\x00\x79\x6f\x62\x61\x00\x00\x00\x16\x04\x00\x00\x00\x2e\x00\x00\x00\x00\
\x00\x00\x00\x1a\x2c\x00\x00\x00\x04\x00\x00\x00'''
    x = GreedyRange(c2s_packets).parse(data)
    print(x)

