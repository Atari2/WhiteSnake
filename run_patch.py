import glob
import sys
import os
from patchexception import PatchException
from owsprite import OWSprite
from routine import Routine
import asar
import re
from rom import Rom

SPRITE_COUNT = 0x80


def create_routines():
    local_routines = []
    for file in glob.glob('./routines/*.asm'):
        routine_name = re.findall(r'\w+\.asm', file)[-1].replace('.asm', '')
        if not routine_name.startswith('__'):
            local_routines.append(Routine(file))
    return local_routines


def create_sprites():
    local_sprites = []
    try:
        with open('list.txt', 'r') as listfile:
            spritelist = listfile.readlines()
    except IOError:
        print('List file not found.')
        exit(-1)
    for lineno, file in enumerate(spritelist):
        match = re.match(r'([0-9A-F]{2}) +(.*\.asm)', file)
        if not match:
            print(f'Error in list.txt at line {lineno+1}', f'<{file}>')
            exit(-1)
        file = match.group(2)
        file_name = re.findall(r'\w+\.asm', file)[-1].replace('.asm', '')
        if not file_name.startswith('__'):
            local_sprites.append(OWSprite(file))
    return local_sprites


try:
    asar.init(dll_path='./asar.dll')
except OSError:
    print('asar.dll wasn\'t found')
    exit(-1)

if len(sys.argv) == 1:
    romname = input('Insert the name of your rom here:\n')
else:
    romname = sys.argv[1]

rom = Rom(romname)
try:
    rom.autoclean_rom('./global_ow_code/autoclean_routines.asm')
    routines = create_routines()
    sprites = create_sprites()
    m = open('./global_ow_code/routines.asm', 'w')
    with open('./global_ow_code/autoclean_routines.asm', 'w') as f, \
            open('./global_ow_code/_OverworldInitPtr.bin', 'wb') as init_table, \
            open('./global_ow_code/_OverworldMainPtr.bin', 'wb') as main_table:
        for routine in routines:
            routine.patch_routine(rom)
            f.write(routine.create_autoclean())
            m.write(routine.create_macro())
        m.close()
        for sprite in sprites:
            sprite.patch_sprite(rom)
        for i in range(SPRITE_COUNT):
            try:
                init_table.write(sprites[i].init_ptr.to_bytes(3, byteorder='little', signed=False))
                main_table.write(sprites[i].main_ptr.to_bytes(3, byteorder='little', signed=False))
            except IndexError:
                init_table.write((0).to_bytes(3, byteorder='big', signed=False))
                main_table.write((0).to_bytes(3, byteorder='big', signed=False))
    rom.patch_rom('./global_ow_code/ow_main.asm')
    rom.save_rom()
    os.remove('./global_ow_code/_OverworldInitPtr.bin')
    os.remove('./global_ow_code/_OverworldMainPtr.bin')
except PatchException as e:
    print(str(e))
