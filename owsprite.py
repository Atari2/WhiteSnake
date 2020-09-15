from patchexception import PatchException
import os
from rom import Rom
import re


class OWSprite:
    incsrc = 'incsrc "./global_ow_code/defines.asm"\nincsrc "./global_ow_code/routines.asm"\nfreecode cleaned\n'

    def __init__(self, file):
        self.other = ''
        self.init = ''
        self.main = ''
        self.init_ptr = None
        self.main_ptr = None
        self.name = re.findall(r'\w+\.asm', file)[-1].replace('.asm', '')
        self.path = file
        with open(file, 'r') as f:
            lines = f.readlines()
        handler = 0
        for line in lines:
            if line.startswith('print "INIT", pc'):
                self.initline = line
                handler = 1
            elif line.startswith('print "MAIN", pc'):
                self.mainline = line
                handler = 2
            else:
                if handler == 0:
                    self.other += line
                elif handler == 1:
                    self.init += line
                elif handler == 2:
                    self.main += line

    def __str__(self):
        return self.other + self.incsrc + self.initline + self.init + self.mainline + self.main

    def set_ptrs(self, init_ptr, main_ptr):
        self.init_ptr = int(init_ptr, 16)
        self.main_ptr = int(main_ptr, 16)

    def patch_sprite(self, rom: Rom):
        import asar
        with open(f'tmp_{self.name}.asm', 'w') as f:
            f.write(str(self))
        (success, rom_data) = asar.patch(f'tmp_{self.name}.asm', rom.data)
        if success:
            rom.data = rom_data
            ptrs = asar.getprints()
            self.set_ptrs(ptrs[0][-6:], ptrs[1][-6:])
            print(f'Sprite {self.name} was applied correctly')
        else:
            print(asar.geterrors())
            raise PatchException(f'Sprite {self.name} encountered an error while patching')
        os.remove(f'tmp_{self.name}.asm')

