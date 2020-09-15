import os
import asar
from patchexception import PatchException
from pointer import Pointer

SPRITE_COUNT = 0x80


def get_pointer(data, address, size, bank):
    address = (data[address]) | (data[address + 1] << 8) | ((data[address + 2] << 16) * (size - 2))
    return address | (bank << 16)


class Rom:
    def __init__(self, name):
        self.name = name
        with open(name, 'rb') as r:
            self.fulldata = r.read()
        self.data = self.fulldata[512:]

    def patch_rom(self, patchname):
        (success, new_data) = asar.patch(patchname, self.data)
        if success:
            self.data = new_data
            print(f'Patch {patchname} was applied correctly')
        else:
            print(asar.getprints())
            raise PatchException(f'Couldn\'t patch {patchname}' + "\n".join(str(error) for error in  asar.geterrors()))

    @staticmethod
    def pc_to_snes(address):
        address -= 0x200
        return (((address << 1) & 0x7F0000) | (address & 0x7FFF)) | 0x8000

    @staticmethod
    def snes_to_pc(address):
        return ((address & 0x7F0000) >> 1 | (address & 0x7FFF)) + 0x200

    def save_rom(self):
        with open(self.name, 'wb') as w:
            w.write(self.fulldata[:512] + self.data)

    def pointer_snes(self, address: int, size: int = 3, bank: int = 0x00) -> Pointer:
        return Pointer.from_snes(get_pointer(self.fulldata, self.snes_to_pc(address), size, bank))

    def pointer_pc(self, address: int, size: int = 3, bank: int = 0x00):
        return Pointer.from_snes(get_pointer(self.fulldata, address, size, bank))

    def autoclean_rom(self, autoclean_routines):
        (success, new_data) = asar.patch(autoclean_routines, self.data)
        if success:
            self.data = new_data
        else:
            raise PatchException('Failed to autoclean routines')
        autoclean_patch = open('autoclean_sprites.asm', 'w')
        ow_tables = self.pointer_snes(0x04F675).addr()
        for i in range(SPRITE_COUNT):
            pointer_main = self.pointer_snes(ow_tables + 3 * i)
            pointer_init = self.pointer_snes((ow_tables + SPRITE_COUNT*3) + 3 * i)
            if not pointer_main.is_empty() and not pointer_main.addr() == 0x00:
                autoclean_patch.write(f'autoclean ${pointer_main.addr():06X}\n')
            if not pointer_init.is_empty() and not pointer_main.addr() == 0x00:
                autoclean_patch.write(f'autoclean ${pointer_init.addr():06X}\n')
        autoclean_patch.close()
        (success, new_data) = asar.patch('autoclean_sprites.asm', self.data)
        if success:
            self.data = new_data
            print('Old sprites cleaned correctly')
        else:
            raise PatchException('Failed to autoclean sprite pointers')
        os.remove('autoclean_sprites.asm')
