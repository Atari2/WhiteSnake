import glob
import os
import sys
from patchexception import PatchException
from owsprite import OWSprite
from routine import Routine
import asar
import re
from rom import Rom


def create_routines():
    local_routines = []
    for file in glob.glob('./routines/*.asm'):
        routine_name = re.findall(r'\w+\.asm', file)[-1].replace('.asm', '')
        if not routine_name.startswith('__'):
            local_routines.append(Routine(file))
    return local_routines


def create_sprites():
    local_sprites = []
    for file in glob.glob('./sprites/**/*.asm', recursive=True):
        file_name = re.findall(r'\w+\.asm', file)[-1].replace('.asm', '')
        if not file_name.startswith('__'):
            local_sprites.append(OWSprite(file))
    return local_sprites


def prepare_uberasm_file():
    add_incsrc = 'incsrc global_ow_code/macro_spr_pointers.asm\nincsrc global_ow_code/macro_pointers.asm\n'
    with open('global_uberasm_code.asm', 'w') as p:
        filenames = [re.findall(r'\w+\.asm', file)[-1].replace('.asm', '')
                     for file in glob.glob('./sprites/**/*.asm', recursive=True)]
        p.write(add_incsrc)
        p.write('init:\n')
        p.write('LDX #$FF\n')
        for file in filenames:
            p.write('INX\n')
            p.write('%' + file + '_init()\n')
        p.write('RTL\n')
        p.write('main:\n')
        p.write('%dec_timers()\nLDX #$FF\n')
        for file in filenames:
            p.write('INX\n')
            p.write('%' + file + '_main()\n')
        p.write('RTL\n')


try:
    asar.init(dll_path='./asar.dll')
except OSError:
    print('asar.dll wasn\'t found')

if len(sys.argv) == 1:
    romname = input('Insert the name of your rom here:\n')
else:
    romname = sys.argv[1]

rom = Rom(romname)
rom.autoclean_rom()
routines = create_routines()
sprites = create_sprites()
try:
    m = open('./global_ow_code/macro_pointers.asm', 'w')
    s = open('./global_ow_code/macro_spr_pointers.asm', 'w')
    with open('./global_ow_code/autoclean_pointers.asm', 'w') as f:
        for routine in routines:
            routine.patch_routine(rom)
            f.write(routine.create_autoclean())
            m.write(routine.create_macro())
        m.close()
        for sprite in sprites:
            sprite.patch_sprite(rom)
            f.write(sprite.create_autoclean())
            s.write(sprite.init_macro())
            s.write(sprite.main_macro())
        s.close()
    rom.save_rom()
    prepare_uberasm_file()
except PatchException as e:
    print(str(e))
