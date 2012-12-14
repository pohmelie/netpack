from construct import *
from recipe import *


attrs_list = dict(
    strength = 0,
    dexterity = 1,
    mana = 2,
    life = 3,
    level = 12,
    experience = 13,
    stash_gold = 15,
    next_level_exp = 30,
    resist_fire = 39,
    resist_cold = 41,
    resist_lightning = 43,
    resist_poision = 45,
)
rattrs_list = dict(map(reversed, attrs_list.items()))

class AttributeAdapter(Adapter):
    def _encode(self, obj, context):
        return attrs_list.get(obj, obj)

    def _decode(self, obj, context):
        return rattrs_list.get(obj, obj)

def Attribute(name):
    return AttributeAdapter(ULInt8(name))
