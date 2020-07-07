from patchexception import PatchException
import os
from rom import Rom
import re


class OWSprite:
    incsrc = 'incsrc global_ow_code/defines.asm\nincsrc global_ow_code/macros.asm\nincsrc ' \
             'global_ow_code/macro_pointers.asm\nfreecode cleaned\n'

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
            if line.startswith('init:'):
                self.initline = f'print "$",pc\n{self.name}_init:\nPHK : PLB\nJSL $07F7D2\n'
                handler = 1
            elif line.startswith('main:'):
                self.mainline = f'print "$",pc\n{self.name}_main:\nPHK : PLB\n'
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
        self.init_ptr = init_ptr
        self.main_ptr = main_ptr

    def init_macro(self):
        return f'macro {self.name}_init()\n\tPHB : JSL {self.init_ptr} : PLB\nendmacro\n'

    def main_macro(self):
        return f'macro {self.name}_main()\n\tPHB : JSL {self.main_ptr} : PLB\nendmacro\n'

    def patch_sprite(self, rom: Rom):
        import asar
        with open(f'tmp_{self.name}.asm', 'w') as f:
            f.write(str(self))
        (success, rom_data) = asar.patch(f'tmp_{self.name}.asm', rom.data)
        if success:
            rom.data = rom_data
            ptrs = asar.getprints()
            self.init_ptr = ptrs[0]
            self.main_ptr = ptrs[1]
            print(f'Sprite {self.name} was applied correctly')
        else:
            print(asar.geterrors())
            raise PatchException(f'Sprite {self.name} encountered an error while patching')
        os.remove(f'tmp_{self.name}.asm')

    def create_autoclean(self):
        return f'autoclean {self.init_ptr}\nautoclean {self.main_ptr}\n'
