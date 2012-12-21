class ItemPrettyPrinter():
    def __init__(self, fname="d2items.txt"):
        t = ("name", "code", "type", "rang")
        self.items = {}
        for line in open(fname):
            x = dict(zip(t, line.strip().split("|")))
            self.items[x["code"]] = x

    def pp(self, item, fmt="{quality} {name} ilvl = {ilvl}"):
        i = self.items[item.code]
        return fmt.format(
            quality = item.quality,
            etherial = item.etherial,
            identified = item.identified,
            container = item.container,
            name = i["name"],
            code = i["code"],
            type = i["type"],
            rang = i["rang"]
        )
