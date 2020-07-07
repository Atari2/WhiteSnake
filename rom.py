import os
import asar
from patchexception import PatchException


class Rom:
    def __init__(self, name):
        self.name = name
        with open(name, 'rb') as r:
            self.fulldata = r.read()
        self.data = self.fulldata[512:]

    def patch_rom(self, patchname):
        pass

    def save_rom(self):
        with open(self.name, 'wb') as w:
            w.write(self.fulldata[:512] + self.data)

    def autoclean_rom(self):
        try:
            os.listdir('./global_ow_code').index('autoclean_pointers.asm')
            (success, rom_data) = asar.patch('./global_ow_code/autoclean_pointers.asm', self.data)
            if success:
                self.data = rom_data
                print('Pointers were autocleaned')
            else:
                raise PatchException(f'Errors were found while cleaning the old pointers {asar.geterrors()}')
        except ValueError:
            print('No pointers to autoclean were found')