import io, struct
from typing import Callable, Optional

from .header import PartCloneException, crc32, CRC32_SEED, Header
from .bitmap import Bitmap

from tqdm import tqdm # install with "pip install tqdm"; on Ubuntu install with "sudo apt install python3-tqdm"


#########################################################################
#                                Blocks                                 #
#                                ======                                 #
# https://github.com/Thomas-Tsai/partclone/blob/master/IMAGE_FORMATS.md #
#########################################################################

def BlocksReader(bitmap: Bitmap, file: io.BufferedReader,
                 progress_bar: bool = True, verify_crc: bool = False,
                 fn: Optional[Callable[[int,bytes],None]] = None) -> None:
    """
    Reads all used blocks and verifies all checksums. If fn is not None
    it will be called for each block.
    """
    with tqdm(total=bitmap.getHeader().usedBlocks(), unit=' used blocks',
              unit_scale=True, disable=not progress_bar) as progress:
        endian = bitmap.getHeader().getEndian()
        block_size = bitmap.getHeader().blockSize()
        checksum_mode = bitmap.getHeader().checksumMode()
        checksum_blocks = bitmap.getHeader().checksumBlocks()
        checksum_size = bitmap.getHeader().checksumSize()
        checksum_reseed = bitmap.getHeader().checksumReseed()
        seed = CRC32_SEED
        block_no = blocks_read = prev_blocks_read = 0
        for byte in bitmap.bitMap():
            if block_no % 4096 == 0:
                if blocks_read > prev_blocks_read:
                    progress.update(blocks_read - prev_blocks_read)
                    prev_blocks_read = blocks_read
            if byte == 0:
                block_no += 8
                continue
            for bit in range(8):
                if byte & (1 << bit):
                    block = file.read(block_size)
                    if len(block) != block_size:
                        raise PartCloneException('Unexpected end of file at '
                                                 f'{file.tell():,}.')
                    blocks_read += 1
                    if checksum_mode == 32:
                        seed = crc32(block, seed) if verify_crc else -1
                        if checksum_blocks and \
                           blocks_read % checksum_blocks == 0:
                            crc = struct.unpack(f'{endian}L',
                                                file.read(checksum_size))[0]
                            if seed != -1 and crc != seed:
                                msg = 'Blocks CRC mismatch at file offset '\
                                      f'{file.tell()-checksum_size:,}: '\
                                      f'0x{crc:8x} != 0x{seed:8x}.'
                                raise PartCloneException(msg)
                            if checksum_reseed:
                                seed = CRC32_SEED
                    if fn is not None:
                        fn(block_no * block_size, block)
                block_no += 1
        if blocks_read > prev_blocks_read:
            progress.update(blocks_read - prev_blocks_read)

    # Final CRC check
    if checksum_mode:
        if checksum_blocks and blocks_read % checksum_blocks != 0:
            crc = struct.unpack(f'{endian}L', file.read(checksum_size))[0]
            if seed != -1 and crc != seed:
                msg = 'Blocks CRC mismatch at file offset '\
                      f'{file.tell()-checksum_size:,}: '\
                      f'0x{crc:8x} != 0x{seed:8x}.'
                raise PartCloneException(msg)

    # End-of-file expected.
    block = file.read(block_size)
    if len(block) != 0:
        info = '1 byte' if len(block) == 1 else \
                   'at least 1 block' if len(block) == block_size else \
                       f'{len(block)} bytes'
        print(f"Warning '{file.name}': {info} of unexpected data after "
              "end of backup.")
