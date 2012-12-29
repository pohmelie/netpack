from construct import *
from recipe import *


class_codes_list = dict(
    act3_waypoint = 237,
    act4_waypoint = 398,
    stash = 267,
)
rclass_codes_list = dict(map(reversed, class_codes_list.items()))

class ClassCodeAdapter(Adapter):
    def _encode(self, obj, context):
        return class_codes_list.get(obj, obj)

    def _decode(self, obj, context):
        return rclass_codes_list.get(obj, obj)

def ClassCode(name):
    return ClassCodeAdapter(ULInt16(name))
