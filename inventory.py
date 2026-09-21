class Invertory:

    def __init__(self):
        self.slotnum = 12

        self.slots = {}

    def add(self, item, add=1):
        if add <= 0:
            return

        # اگر آیتم از قبل وجود دارد، تعدادش را زیاد کن
        for key, itemy in self.slots.items():
            if itemy[0] == item:
                self.slots[key] = (item, itemy[1] + add)
                return

        # پیدا کردن اولین slot خالی
        for id in range(1, self.slotnum + 1):
            if id not in self.slots:
                self.slots[id] = (item, add)
                return

        return "full"

    def remove(self, item, remove=1):
        # remove <= 0 -> ALL

        k = None

        for key, itemy in self.slots.items():
            if itemy[0] == item:
                k = key
                break

        if k is None:
            return "null item"

        if remove <= 0 or self.slots[k][1] <= remove:
            del self.slots[k]
        else:
            self.slots[k] = (
                item,
                self.slots[k][1] - remove
            )

    def has(self, item, num=1):
        for itemy in self.slots.values():
            if itemy[0] == item and itemy[1] >= num:
                return True

        return False

    def getinvertory(self):
        return self.slots

