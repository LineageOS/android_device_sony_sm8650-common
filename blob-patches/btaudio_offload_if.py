#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import re

from extract_utils.fixups_blob import (
    BlobFixupCtx,
    File,
)
from extract_utils.tools import (
    llvm_objdump_path,
)
from extract_utils.utils import (
    run_cmd,
)


def blob_fixup(
    ctx: BlobFixupCtx,
    file: File,
    file_path: str,
    *args,
    **kwargs,
):
    disassemble_symbol = '_ZNSt3__16vectorIhNS_9allocatorIhEEE13__vdeallocateEv'

    # b.ne 0x13314; mov w8, #0x1e0
    from_instructions = [
        '54000221',
        '52803c08',
    ]

    # Divide peerDelayUs by 1000 (microseconds to milliseconds)
    to_bytes = bytes.fromhex(
        '09 D1 40 B9 3F 09 00 71 A1 08 00 54 08 89 40 B9 09 7D 80 52 08 09 C9 1A 25 00 00 14 1F 20 03 D5 '
        '09 41 41 B9 3F 09 00 71 A1 07 00 54 08 F9 40 B9 09 7D 80 52 08 09 C9 1A 1D 00 00 14 1F 20 03 D5'
    )

    segments = [
        (int(vaddr, 16), int(off, 16), int(filesz, 16))
        for off, vaddr, filesz in re.findall(
            r'LOAD off\s+(0x[0-9a-f]+) vaddr (0x[0-9a-f]+).*\n'
            r'\s+filesz (0x[0-9a-f]+)',
            run_cmd([llvm_objdump_path, '-p', file_path]),
        )
    ]

    instructions = []

    for line in run_cmd(
        [
            llvm_objdump_path,
            f'--disassemble-symbols={disassemble_symbol}',
            file_path,
        ]
    ).splitlines():
        line = line.split(maxsplit=3)

        if len(line) != 4:
            continue

        offset, instruction, _, _ = line

        instructions = (instructions + [instruction])[-len(from_instructions):]

        if instructions != from_instructions:
            continue

        offset = int(offset[:-1], 16)
        offset = next(
            offset - vaddr + off
            for vaddr, off, filesz in segments
            if vaddr <= offset < vaddr + filesz
        )

        with open(file_path, 'rb+') as f:
            f.seek(offset)
            f.write(to_bytes)

        break
