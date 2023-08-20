import io, os, struct
from typing import Optional


#######################################################################
#                              Exception                              #
#######################################################################

class PartCloneException(Exception):
    def __init__(self, s: str):
        super().__init__(s)


#######################################################################
#                              Checksums                              #
#                              =========                              #
# https://github.com/Thomas-Tsai/partclone/blob/master/src/checksum.c #
#######################################################################

def crc(byte: int) -> int:
    "Computes the crc_table cached values."
    crc = byte
    for j in range(8):
        crc = (crc >> 1) ^ 0xedb88320 if crc & 1 else crc >> 1
    return crc

CRC32_TABLE = [crc(i) for i in range(256)]

del crc # delete crc function to prevent it from being called instead of crc32

CRC32_SEED = 0xffffffff

def crc32(buffer: bytes, seed = CRC32_SEED) -> int:
    "Compute partclone crc32 for a given buffer."
    crc = seed
    for b in buffer:
        crc = (crc >> 8) ^ CRC32_TABLE[(crc ^ b) & 0xff]
    return crc


#########################################################################
#                                Header                                 #
#                                ======                                 #
# https://github.com/Thomas-Tsai/partclone/blob/master/IMAGE_FORMATS.md #
#########################################################################

class Header:
    """
    The partclone header is documented in
    https://github.com/Thomas-Tsai/partclone/blob/master/IMAGE_FORMATS.md

    This class reads the header of a partclone image, checks for
    the supported version (version 2) and compares the header's crc32.
    """

    READ_SIZE = 110

    CHECKSUM_MODE = { 0: 'NONE', 32: 'CRC32' }
    BITMAP_MODE   = { 0: 'NONE', 1: 'BIT', 8: 'BYTE' }

    PARTCLONE = b'partclone-image'
    PARTIMAGE = b'PaRtImAgE-VoLuMe'
    NTFSCLONE = b'ntfsclone-image'

    GZIP  = 0x8b1f
    BZIP2 = 0x5a42
    ZSTD  = 0xb528
    XZ    = 0x37fd
    LZMA  = 0x005d
    LZ4   = 0x2204

    def __init__(self, file: io.BufferedReader):
        buffer = file.read(self.READ_SIZE)
        if buffer[:15] != self.PARTCLONE:
            # Not a partclone image, maybe from another image backup tool...
            if buffer[:16] == self.PARTIMAGE:
                raise PartCloneException("This utility is for partclone images;"
                                  f" '{file.name}' was written with partimage.")
            if buffer[1:16] == self.NTFSCLONE:
                raise PartCloneException("This utility is for partclone images;"
                                  f" '{file.name}' was written with ntfsclone.")
            # ... or possibly a compressed image file.
            first_word = struct.unpack('<H', buffer[:2])[0]
            if first_word == self.GZIP:
                raise PartCloneException(gzip_image_msg(file.name, 'gz'))
            if first_word == self.BZIP2:
                raise PartCloneException(gzip_image_msg(file.name, 'bz2'))
            if first_word == self.ZSTD:
                raise PartCloneException(gzip_image_msg(file.name, 'zstd'))
            if first_word == self.XZ:
                raise PartCloneException(gzip_image_msg(file.name, 'xz'))
            if first_word == self.LZMA:
                raise PartCloneException(gzip_image_msg(file.name, 'lzma'))
            if first_word == self.LZ4:
                raise PartCloneException(gzip_image_msg(file.name, 'lz4'))
            # Unknown file format.
            raise PartCloneException(f"'{file.name}' is not a partclone image. "
                                     f"Command 'file {file.name}' can help "
                                     "figure out what kind of file this is.")
        self.partclone_version = str(buffer[16:30], 'utf-8')
        if (pos := self.partclone_version.find('\0')) != -1:
            self.partclone_version = self.partclone_version[:pos]
        self.img_version = str(buffer[30:34], 'utf-8')
        if self.img_version != '0002':
            raise PartCloneException(f"Version {self.img_version} not "
                                     "supported; only version 2 is supported.")
        self.endian = struct.unpack('<H', buffer[34:36])[0]
        if self.endian not in [0xc0de, 0xdec0]:
            raise PartCloneException("Unexpected endianness "
                                     f"{self.endian:04x}.")
        self.endian = '<' if self.endian == 0xc0de else '>'
        self.fs_type = str(buffer[36:52], 'utf-8')
        if (pos := self.fs_type.find('\0')) != -1:
            self.fs_type = self.fs_type[:pos]
        self.fs_total_size, self.fs_total_blocks, self.fs_used_blocks, \
            self.fs_used_bitmap, self.fs_block_size, feature_selection, \
            self.image_version, self.cpu_bits, self.checksum_mode, \
            self.checksum_size, self.checksum_blocks, self.checksum_reseed, \
            self.bitmap_mode, self.crc32 = \
                struct.unpack(f'{self.endian}4Q2L4HL2BL', buffer[52:110])
        if self.checksum_mode not in [0, 32]:
            raise PartCloneException("Unsupported checksum mode "
                                     f"{self.checksum_mode}; modes 0 and 32 "
                                     "are supported.")
        if self.crc32 != (crc := crc32(buffer[:106])):
            raise PartCloneException(f"Header CRC mismatch: "
                                     f"0x{self.crc32:8x} != 0x{crc:8x}.")

    def fsType(self) -> str:
        """Return file system type, e.g. NTFS or BTRFS."""
        return self.fs_type

    def blockSize(self) -> int:
        "Return file system's block size."
        return self.fs_block_size

    def totalSize(self) -> int:
        "Return file system's total size in bytes."
        return self.fs_total_size

    def totalBlocks(self) -> int:
        "Return file system's total size in blocks."
        return self.fs_total_blocks

    def usedBlocks(self) -> int:
        "Return file system's number of blocks in use."
        return max(self.fs_used_bitmap, self.fs_used_blocks)

    def checksumMode(self) -> int:
        "Return checksum mode, 0 (no checksum) or 32 (crc32)."
        return self.checksum_mode

    def checksumSize(self) -> int:
        "Return checksum size (usually 4 bytes)."
        return self.checksum_size

    def checksumBlocks(self) -> int:
        "Return number of blocks preceeding a checksum."
        return self.checksum_blocks

    def checksumReseed(self) -> bool:
        "Reseed crc32 for next checksum or not."
        return bool(self.checksum_reseed)

    def getEndian(self) -> str:
        "Return '<' or '>' for struct.unpack."
        return self.endian

    def mntType(self) -> str:
        "Return file-system type for the mount command."
        return 'exfat' if self.fsType() == 'EXFAT' else \
               'vfat' if 'FAT' in self.fsType() else self.fsType().lower()

    def fsckCmd(self) -> str:
        "Return fsck command to check this filesystem."
        return 'ntfsfix --no-action' if self.fsType() == 'NTFS' else \
               'btrfsck --check --readonly'  if self.fsType() == 'BTRFS' else \
               'fsck.exfat -n' if self.fsType() == 'EXFAT' else \
               'fsck.fat -n' if 'FAT' in self.fsType() else \
               'xfs_repair -f -n' if self.fsType() == 'XFS' else \
               f'fsck.{self.fsType().lower()} -n'

    def __str__(self) -> str:
        return 'Partclone Header\n================\n' \
               f'partclone version {self.partclone_version}\n' \
               f'fs type           {self.fs_type}\n' \
               f'fs total size     {self.fs_total_size:,} ' \
               f'({reportSize(self.fs_total_size)})\n' \
               f'fs total blocks   {self.fs_total_blocks:,}\n' \
               f'fs used blocks    {self.fs_used_blocks:,} ' \
               f'({reportSize(self.fs_used_blocks * self.fs_block_size)})' \
               '\tused block count based on super-block\n' \
               f'fs_used_bitmap    {self.fs_used_bitmap:,} ' \
               f'({reportSize(self.fs_used_bitmap * self.fs_block_size)})' \
               '\tused block count based on bitmap\n' \
               f'fs block size     {self.fs_block_size}\n' \
               f'image version     {self.image_version}\n' \
               f'cpu bits          {self.cpu_bits}\n' \
               f"checksum mode     {self.CHECKSUM_MODE.get(self.checksum_mode)}\n" \
               f'checksum size     {self.checksum_size}\n' \
               f'checksum blocks   {self.checksum_blocks}\n' \
               f'checksum reseed   {self.checksumReseed()}\n' \
               f"bitmap mode       {self.BITMAP_MODE.get(self.bitmap_mode)}\n" \
               f'crc32             0x{self.crc32:08x}'


def gzip_image_msg(filename: str, compression: str):
    """
    Forms the error message for compressed images encountered when reading
    header.
    """

    # Suggest an output file name that does not already exist.
    out_name = os.path.split(filename)[1].replace('.'+compression, '')
    if out_name == filename or not out_name.endswith('.img') or \
       os.path.exists(out_name):
        if os.path.exists(out_name + '.img'):
            i = 1
            while os.path.exists(out_name + f'_{i}.img'):
                i += 1
            out_name = out_name + f'_{i}.img'
        else:
            out_name += '.img'

    if compression == 'gz':
        msg = "File '{n1}' is gzip-compressed; run 'gunzip < {n1} > {n2}' " \
              "and try again with '{n2}'."
    elif compression == 'bz2':
        msg = "File '{n1}' is bzip2-compressed; run 'bunzip2 < {n1} > {n2}' " \
              "and try again with '{n2}'."
    else:
        msg = "File '{n1}' is {c}-compressed; run 'zstd -d " \
              "--format={c} -o {n2} {n1}' and try again with '{n2}'."

    return msg.format(msg, n1=filename, n2=out_name, c=compression)


def reportSize(size: int) -> str:
    "Report size in appropriate unit (B, KB, MB, GB, TB, PB, EB, ZB)."
    units = [ 'B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB' ]
    for k in range(len(units)-1, -1, -1):
        if k == 0:
            return f'{size} {units[k]}'
        sz_unit = 1 << (k * 10)
        if size >= sz_unit:
            return f'{size/sz_unit:.1f} {units[k]}'
    assert False
