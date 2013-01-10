from construct import *
from recipe import *


def _factory(fname, default_fields=None, idn=None):
    lst = None
    class _Adapter(Adapter):
        def _encode(self, obj, ctx):
            return obj._id

        def _decode(self, obj, ctx):
            nonlocal lst
            lst = lst or read_d2_file(fname, default_fields, idn)
            return lst[obj]
    return _Adapter

D2Attribute = _factory("txt\\exp\\ItemStatCost.txt", ("Stat", "ValShift"), "ID")(ULInt8(name))
D2Object = lambda name: _factory("txt\\exp\\objects.txt", ("Name", "description_-_not_loaded"), "Id")(ULInt16(name))
D2Skill = lambda name: _factory("txt\\exp\\skills.txt", ("skill", "charclass"), "Id")(ULInt16(name))
D2Monstat = lambda name: _factory("txt\\exp\\monstats.txt", ("namco", "Type"), "PopulateId")(ULInt16(name))
D2Montype = lambda name: _facotry("txt\\exp\\MonType.txt")
