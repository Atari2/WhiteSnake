RTL_BANK = 0x01
RTL_HIGH = 0x80
RTL_LOW = 0x21


class Pointer:
    lowbyte = RTL_LOW
    highbyte = RTL_HIGH
    bankbyte = RTL_BANK

    def __init__(self):
        pass

    @classmethod
    def from_snes(cls, snes: int):
        pointer = Pointer()
        pointer.lowbyte = snes & 0xFF
        pointer.highbyte = (snes >> 8) & 0xFF
        pointer.bankbyte = (snes >> 16) & 0xFF
        return pointer

    def is_empty(self):
        return self.lowbyte == RTL_LOW and self.highbyte == RTL_HIGH and self.bankbyte == RTL_BANK

    def addr(self):
        return (self.bankbyte << 16) + (self.highbyte << 8) + self.lowbyte


