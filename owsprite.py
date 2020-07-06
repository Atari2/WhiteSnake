class OWSprite:
    incsrc = 'incsrc global_ow_code/defines.asm\nincsrc global_ow_code/macros.asm\nincsrc ' \
             'global_ow_code/macro_pointers.asm\nfreecode cleaned\n'

    def __init__(self, name):
        self.other = ''
        self.init = ''
        self.main = ''
        self.init_ptr = None
        self.main_ptr = None
        self.name = name.replace(".asm", "")[name.rfind("sprites") + len("sprites") + 1:]
        with open(name, 'r') as f:
            lines = f.readlines()
        handler = 0
        for line in lines:
            if line.startswith('init:'):
                self.initline = f'print "$",pc," ;{self.name}_init"\n{self.name}_init:\nPHK : PLB\nJSL $07F7D2\n'
                handler = 1
            elif line.startswith('main:'):
                self.mainline = f'print "$",pc," ;{self.name}_main"\n{self.name}_main:\nPHK : PLB\n'
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
