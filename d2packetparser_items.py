from construct import *
from d2packetparser_c2s import sid


d2item_header = Embed(Struct(None,
        Enum(ULInt8("action"),
            lying_on_ground_just_dropped = 0x00,
            picked_up_from_ground_to_cursor = 0x01,
            dropped_by_player = 0x02,
            lying_on_ground = 0x03,
            moved_in_cube_inventory = 0x04,
            put_onto_cursor = 0x05,
            item_on_cursor_was_equipped = 0x06,
            removed_from_equipment_slot = 0x08,
            swap_cursor_slot = 0x09,
            merge_items = 0x0a,
            added_to_shop = 0x0b,
            removed_from_shop = 0x0c,
            swap_cursor_inventory = 0x0d,
            put_into_belt = 0x0e,
            removed_from_belt = 0x0f,
            swap_cursor_belt = 0x10,
            cursor_item_when_entering = 0x12,
            item_is_socketed_into_another = 0x13,
            item_just_inserted_into_another = 0x15,
            equipment_swap = 0x17
        ),
        ULInt8("length_of_packet"),
        Enum(ULInt8("category"),
            helm = 0x00,
            armor = 0x01,
            weapon = 0x05,
            bow = 0x06,
            shield = 0x07,
            other = 0x10
        ),
        sid("item_id"),
    )
)


if __name__ == "__main__":
    pass
