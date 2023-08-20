import io, struct
from dataclasses import dataclass
from typing import List, Optional

from .header import PartCloneException, crc32, Header, reportSize


#######################################################################
#                          Numbers of Bits Set                        #
#######################################################################

BITS_SET = [bin(i).count('1') for i in range(256)]
"""The number of bits set for each byte."""


#########################################################################
#                                Bitmap                                 #
#                                ======                                 #
# https://github.com/Thomas-Tsai/partclone/blob/master/IMAGE_FORMATS.md #
#########################################################################

class Bitmap:
    """
    The partclone bitmap is documented in
    https://github.com/Thomas-Tsai/partclone/blob/master/IMAGE_FORMATS.md

    This class reads the bitmap for a given header and verifies
    the bitmaps's crc32.
    """

    BLOCK_OFFSET_SIZE = 1024
    "Allocate an index for every 128 bytes; a reasonable default for indexing."

    @dataclass
    class BlockOffset:
        file_offset : int
        "offset into image file"
        cksum_offset: int
        ">= 0 and < header.checksumBlocks()"

    def __init__(self, header: Header, file: io.BufferedReader,
                 block_offset_size: int):
        self.header = header
        size = (header.totalBlocks() + 7) // 8
        self.bitmap = file.read(size)
        if len(self.bitmap) != size:
            raise PartCloneException("Unexpected end of file at "
                                   f"{header.READ_SIZE + len(self.bitmap):,}.")
        self.crc32 = struct.unpack(f'{header.endian}L', file.read(4))[0]
        if self.crc32 != (crc := crc32(self.bitmap)):
            raise PartCloneException("Bitmap CRC mismatch: "
                                     f"0x{self.crc32:8x} != 0x{crc:8x}.")
        self.blocks_section = header.READ_SIZE + size + 4
        if block_offset_size % 8 != 0:
            raise PartCloneException(f'Block_offset_size={block_offset_size} '
                                     'must be a multiple of 8.')
        self.block_offset_size = block_offset_size
        self.block_offsets: List[Bitmap.BlockOffset] = []

        if (mod := (header.totalBlocks() % 8)) != 0:
            mask = (1 << mod) - 1
            if (self.bitmap[-1] & mask) != self.bitmap[-1]:
                self.bitmap = self.bitmap[:-1] + bytes([self.bitmap[-1] & mask])

        if (used_blks := sum(BITS_SET[b] for b in self.bitmap if b != 0)) != \
           header.usedBlocks():
            raise PartCloneException(f'{header.usedBlocks():,} blocks in use according to '
                                     f'header but {used_blks:,} found in bitmap.')

    def getHeader(self) -> Header:
        "Return header instance."
        return self.header

    def bitMap(self) -> bytes:
        "Return the bitmap."
        return self.bitmap

    def blocksSectionOffset(self) -> int:
        "Return offset of Blocks section in image file"
        return self.blocks_section

    def blockInUse(self, block_no: int) -> bool:
        "Returns True if block_no is in use, False otherwise"
        assert block_no >= 0 and block_no // 8 < len(self.bitmap)
        return bool(self.bitmap[block_no // 8] & (1 << (block_no & 7)))

    def buildBlockIndex(self):
        """
        Populates index self.block_offsets which is required for
        member function getBlockOffset().
        """
        file_offset = self.blocksSectionOffset()
        block_size = self.getHeader().blockSize()
        checksum_mode = self.getHeader().checksumMode()
        checksum_blocks = self.getHeader().checksumBlocks()
        checksum_size = self.getHeader().checksumSize()
        blocks_chksum = 0
        block_offset = self.BlockOffset(file_offset, 0)
        for idx1 in range(0, len(self.bitmap), self.block_offset_size // 8):
            if file_offset != block_offset.file_offset:
                block_offset = self.BlockOffset(file_offset, blocks_chksum)
            self.block_offsets.append(block_offset)
            idx2 = min(idx1+self.block_offset_size // 8, len(self.bitmap))
            inuse_blocks = sum(BITS_SET[b] for b in self.bitmap[idx1:idx2]
                               if b != 0)
            blocks_chksum += inuse_blocks
            file_offset += block_size * inuse_blocks
            if checksum_mode and checksum_blocks:
                if blocks_chksum >= checksum_blocks:
                    file_offset += checksum_size * (blocks_chksum //
                                                    checksum_blocks)
                    blocks_chksum %= checksum_blocks

    def getBlockOffset(self, block_no: int) -> Optional[int]:
        "Return offset of block in image file or None if block is not in use"

        if not self.blockInUse(block_no):
            return None

        if not self.block_offsets:
            self.buildBlockIndex()

        block_size      = self.getHeader().blockSize()
        checksum_mode   = self.getHeader().checksumMode()
        checksum_blocks = self.getHeader().checksumBlocks()
        checksum_size   = self.getHeader().checksumSize()

        block_offset_idx = block_no // self.block_offset_size
        block_offset     = self.block_offsets[block_offset_idx]

        bm_idx1          = block_offset_idx * (self.block_offset_size // 8)
        bm_idx2          = block_no // 8

        file_offset      = block_offset.file_offset
        blocks_cksum     = block_offset.cksum_offset

        inuse_blocks = sum(BITS_SET[b] for b in
                           self.bitmap[bm_idx1:bm_idx2] if b != 0) + \
                       BITS_SET[self.bitmap[bm_idx2] & ((1 << (block_no%8))-1)]
        blocks_cksum += inuse_blocks
        file_offset += block_size * inuse_blocks
        if checksum_mode and checksum_blocks:
            if blocks_cksum >= checksum_blocks:
                file_offset += checksum_size * (blocks_cksum // checksum_blocks)
        return file_offset

    def __str__(self):
        return 'Partclone Bitmap\n================\n' \
              f'bitmap            {len(self.bitmap):,} bytes ' \
              f'({reportSize(len(self.bitmap))})\n' \
              f'crc32             0x{self.crc32:08x}\n' \
              f'blocks_section    at {self.blocks_section:,} in img file\n' \
              f'block_offset_size {self.block_offset_size}\n' \
              f'block_offsets     {len(self.block_offsets):,} instances'
