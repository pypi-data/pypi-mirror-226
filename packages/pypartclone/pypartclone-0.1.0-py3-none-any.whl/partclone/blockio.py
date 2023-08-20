import io, math

from .header import PartCloneException
from .bitmap import Bitmap


#########################################################################
# This class is called with read requests of disk data. It breaks these #
# requests down into reads of full blocks from the image file.          #
#########################################################################

class BlockIO:

    """
    This class fulfills read requests of disk data. It breaks these requests
    down into reads of full blocks from the image file.
    """

    def __init__(self, image_file: io.BufferedReader, bitmap: Bitmap):
        self.image_file   = image_file
        self.bitmap       = bitmap
        self.block_size   = bitmap.getHeader().blockSize()
        self.total_blocks = (bitmap.getHeader().totalSize() +
                             self.block_size - 1) // self.block_size
        self.total_size   = self.block_size * self.total_blocks
        self.empty_block  = bytes(self.block_size)

    def read_data(self, offset: int, size: int) -> bytes:
        "Read size bytes at offset."
        if offset + size > self.total_size:
            size = max(0, self.total_size - offset)
        output = bytes()
        if size > 0:
            min_block = offset // self.block_size
            max_block = (offset + size - 1) // self.block_size
            for block_no in range(min_block, max_block + 1):
                idx1 = offset % self.block_size if block_no == min_block else 0
                idx2 = ((offset + size - 1) % self.block_size) + 1 \
                           if block_no == max_block else self.block_size

                image_file_offset = self.bitmap.getBlockOffset(block_no)
                if image_file_offset is None:
                    block = self.empty_block
                else:
                    self.image_file.seek(image_file_offset)
                    block = self.image_file.read(self.block_size)
                    if len(block) != self.block_size:
                        PartCloneException(f'Failed to read full block '
                                           'at {image_file_offset:,}.')

                # Append (a subrange of) block to output.
                output += block[idx1:idx2]
        return output

    def getTotalSize(self) -> int:
        "Return the total (used and unused blocks) size in bytes."
        return self.total_size
