import asar
from rom import Rom
from patchexception import PatchException
import os
import re


class Routine:
    incsrc = 'incsrc global_ow_code/defines.asm\nincsrc global_ow_code/macros.asm\nfreecode cleaned\n'

    def __init__(self, file):
        self.path = file
        self.ptr = None
        self.name = re.findall(r'\w+\.asm', file)[-1].replace('.asm', '')
        with open(self.path, 'r') as r:
            self.routine = f'print "$",pc\n{r.read()}\n\n'

    def __str__(self):
        return self.incsrc + self.routine

    def create_macro(self):
        return f'macro {self.name}()\n\tJSL {self.ptr}\nendmacro\n'

    def create_autoclean(self):
        return f'autoclean {self.ptr}\n'

    def patch_routine(self, rom: Rom):
        with open(f'tmp_{self.name}.asm', 'w') as f:
            f.write(str(self))
        (success, rom_data) = asar.patch(f'tmp_{self.name}.asm', rom.data)
        if success:
            rom.data = rom_data
            ptrs = asar.getprints()
            self.ptr = ptrs[0]
            print(f'Routine {self.name} was applied correctly')
        else:
            print(asar.geterrors())
            raise PatchException(f'Routine {self.name} encountered an error while patching')
        os.remove(f'tmp_{self.name}.asm')
