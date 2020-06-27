import subprocess
import glob
import os
from contextlib import suppress
import sys


def create_spr_macro(addr, name):
    s = f'macro {name}()\n\tPHB : JSL {addr} : PLB\nendmacro\n'
    return s


def create_macro(addr, name):
    s = f'macro {name}()\n\tJSL {addr}\nendmacro\n'
    return s


def create_shared_patch():
    with open('shared_patch.asm', 'w') as f:
        f.write('incsrc global_ow_code/defines.asm\n')
        f.write('incsrc global_ow_code/macros.asm\n')
        f.write('freecode cleaned\n')
        for file in glob.glob('./routines/*.asm'):
            with open(file, 'r') as r:
                lines = r.readlines()
            f.write(f'print "$",pc," ;{file.replace(".asm", "")[file.rfind("routines") + len("routines") + 1:]}"\n')
            f.writelines(lines)
            f.write("\n\n")


def create_shared_sprites():
    for file in glob.glob('./sprites/*.asm'):
        with open(file, 'r') as r:
            lines = r.readlines()
        lines.insert(0, 'incsrc global_ow_code/defines.asm\n')
        lines.insert(0, 'incsrc global_ow_code/macros.asm\n')
        lines.insert(0, 'incsrc global_ow_code/macro_pointers.asm\n')
        lines.insert(0, 'freecode cleaned\n')
        sprite_name = file.replace(".asm", "")[file.rfind("sprites") + len("sprites") + 1:]
        lines[lines.index('init:\n')] = f'print "$",pc," ;{sprite_name}_init"\n{sprite_name}_init:\n'
        lines[lines.index('main:\n')] = f'print "$",pc," ;{sprite_name}_main"\n{sprite_name}_main:\n'
        with open(file, 'w') as r:
            r.writelines(lines)


def get_spr_pointers(romname):
    with open('spr_pointers.asm', 'w'):
        pass
    for file in glob.glob('./sprites/*.asm'):
        with open('spr_pointers.asm', 'a') as f, open('err_log.txt', 'w') as t:
            process = subprocess.Popen(['asar.exe', file, romname], stderr=t, stdout=f,
                                       universal_newlines=True)
            process.communicate()
        with open('err_log.txt', 'r') as t:
            remove_err_log = True if not t.readlines() else False

        if remove_err_log:
            os.remove('err_log.txt')
        else:
            exit(-1)


def clean_old_pointers(romname):
    try:
        os.listdir('./global_ow_code').index('autoclean_pointers.asm')
        process = subprocess.Popen(['asar.exe', './global_ow_code/autoclean_pointers.asm', romname],
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        (stdout, stderr) = process.communicate()
        if stderr == b'':
            print('Pointers were autocleaned', stdout.decode(encoding='utf-8'))
        else:
            print('Errors were found while cleaning the old pointers', stderr.decode(encoding='utf-8'))
    except ValueError:
        print('No pointers to autoclean were found')
    try:
        os.listdir('./global_ow_code').index('autoclean_spr_pointers.asm')
        process = subprocess.Popen(['asar.exe', './global_ow_code/autoclean_pointers.asm', romname],
                                   stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = process.communicate()
        if stderr == b'':
            print('Sprite pointers were autocleaned', stdout.decode(encoding='utf-8'))
        else:
            print('Errors were found while cleaning the old pointers', stderr.decode(encoding='utf-8'))
    except ValueError:
        print('No sprite pointers to autoclean were found')


def apply_shared_patch(romname):
    with open('pointers.asm', 'w') as f, open('err_log.txt', 'w') as t:
        process = subprocess.Popen(['asar.exe', 'shared_patch.asm', romname], stderr=t, stdout=f,
                                   universal_newlines=True)
        process.communicate()

    with open('err_log.txt', 'r') as t:
        remove_err_log = True if not t.readlines() else False

    if remove_err_log:
        os.remove('err_log.txt')
    else:
        exit(-1)


def create_autoclean(autoclean_file, macro_file, pointers, is_sprites):
    with open(autoclean_file, 'w') as f, \
            open(macro_file, 'w') as m, \
            open(pointers, 'r') as r:
        lines = r.readlines()
        for line in lines:
            f.write('autoclean ' + line + '\n')
            if is_sprites:
                m.write(create_spr_macro(line.split(' ')[0].strip('\n'), line.split(' ')[1].strip('\n').replace(";", "")))
            else:
                m.write(create_macro(line.split(' ')[0].strip('\n'), line.split(' ')[1].strip('\n').replace(";", "")))


def prepare_uberasm_file():
    add_incsrc = 'incsrc global_ow_code/macro_spr_pointers.asm\n' \
                 'incsrc global_ow_code/defines.asm\n' \
                 'incsrc global_ow_code/macros.asm\n' \
                 'incsrc global_ow_code/macro_pointers.asm\n'
    with open('global_uberasm_code.asm', 'w') as p:
        filenames = os.listdir('sprites')
        p.write(add_incsrc)
        p.write('init:\n')
        p.write('LDX #$FF\n')
        for file in filenames:
            if file.endswith('.asm'):
                p.write('INX\n')
                p.write('%' + file.replace('.asm', '') + '_init()\n')
        p.write('RTL\n')
        p.write('main:\n')
        p.write('%dec_timers()\nLDX #$FF\n')
        for file in filenames:
            if file.endswith('.asm'):
                p.write('INX\n')
                p.write('%' + file.replace('.asm', '') + '_main()\n')
        p.write('RTL\n')


def add_asm_to_sprites():
    from shutil import copyfile
    for file in glob.glob('sprites/*.asm'):
        os.remove(file)
    for file in glob.glob('sprites/originals/*.asm'):
        copyfile(file, file.replace('sprites/originals\\', 'sprites/'))
    for file in glob.glob('sprites/*.asm'):
        with open(file, 'r') as p:
            lines = p.readlines()
        with suppress(ValueError):
            lines.remove('PHK : PLB\n')
            lines.remove('JSL $07F7D2\n')
            lines.remove('PHK : PLB\n')
        lines.insert(lines.index('init:\n') + 1, 'PHK : PLB\nJSL $07F7D2\n')
        lines.insert(lines.index('main:\n') + 1, 'PHK : PLB\n')
        with open(file, 'w') as p:
            p.writelines(lines)


def remove_temp_files():
    os.remove('pointers.asm')
    os.remove('shared_patch.asm')
    os.remove('spr_pointers.asm')


if len(sys.argv) == 1:
    rom = input('Insert the name of your rom here:\n')
else:
    rom = sys.argv[1]
clean_old_pointers(rom)
create_shared_patch()
apply_shared_patch(rom)
create_autoclean('./global_ow_code/autoclean_pointers.asm',
                 './global_ow_code/macro_pointers.asm',
                 'pointers.asm', False)
add_asm_to_sprites()
create_shared_sprites()
get_spr_pointers(rom)
create_autoclean('./global_ow_code/autoclean_spr_pointers.asm',
                 './global_ow_code/macro_spr_pointers.asm',
                 'spr_pointers.asm', True)
prepare_uberasm_file()
remove_temp_files()
