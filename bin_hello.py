#!/usr/bin/env python

import os
import sys

# 00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............
# 00000010: 0200 3e00 0100 0000 7800 4000 0000 0000  ..>.....x.@.....
# 00000020: 4000 0000 0000 0000 0000 0000 0000 0000  @...............
# 00000030: 0000 0000 4000 3800 0100 0000 0000 0000  ....@.8.........
# 00000040: 0100 0000 0500 0000 0000 0000 0000 0000  ................
# 00000050: 0000 4000 0000 0000 0000 4000 0000 0000  ..@.......@.....
# 00000060: ad00 0000 0000 0000 ad00 0000 0000 0000  ................
# 00000070: 0000 2000 0000 0000 b801 0000 00bf 0100  .. .............
# 00000080: 0000 48be 9f00 4000 0000 0000 ba0e 0000  ..H...@.........
# 00000090: 000f 05b8 3c00 0000 bf00 0000 000f 0548  ....<..........H
# 000000a0: 656c 6c6f 2c20 776f 726c 6421 0a         ello, world!.

def program_instructions(message):
    message_bytes = bytes(message, 'ascii')

    # The raw bytes of the instructions of the program. We use strings
    # for placeholder values computed later.
    prog = [
        0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00, # ELF magic number
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # ELF reserved
        
        0x02, 0x00, # e_type: Executable file
        0x3e, 0x00, # e_machine: AMD64
        0x01, 0x00, 0x00, 0x00, # e_version: 1
        0x78, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, # e_entry (program entry address)
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x38, 0x00,
        0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x01, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00,
        'prog_length', 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # p_filesz, the file size (173)
        'prog_length', 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # p_memsz, the file size (173)
        0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, # p_align
        # end ELF header

        0xb8, 0x01, 0x00, 0x00, 0x00, # mov $1 %eax
        0xbf, 0x01, 0x00, 0x00, 0x00, # mov $1 %edi
        0x48, 0xbe, 0x9f, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, # mov $0 %rsi

        # mov len(message) %edx
        0xba, len(message_bytes), 0x00, 0x00, 0x00,

        0x0f, 0x05, # syscall
        0xb8, 0x3c, 0x00, 0x00, 0x00, # mov $1 %eax
        0xbf, 0x00, 0x00, 0x00, 0x00, # mov $0 %edi

        0x0f, 0x05, # syscall
    ] + list(message_bytes)

    prog_length = len(prog)

    # Set the program length now we know it.
    prog = [
        prog_length if b == 'prog_length' else b
        for b in prog
    ]
    
    return prog


def main(filename):
    with open(filename) as f:
        message = f.read()
    instructions = program_instructions(message)

    with open('hello', 'wb') as f:
        f.write(bytes(instructions))

    os.chmod('hello', 0o744)

    print("Wrote hello ELF")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <path>".format(sys.argv[0]))
        sys.exit(1)
    
    main(sys.argv[1])
