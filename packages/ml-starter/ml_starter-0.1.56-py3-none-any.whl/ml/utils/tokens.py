"""Defines utility functions for dealing with tokens and token datasets.

This file provides helper methods for reading and writing compressed datasets
of tokens. This compresses the tokens into ``ceil(log2(num_tokens))`` bits per
token, with padding at the end of each line to ensure that each line is a
multiple of 8 bits. This optimizes for making the file size as small as
possible while still being efficient to read from.

Here's an example of how to use the API:

.. highlight:: python
.. code-block:: python

    from ml.utils.tokens import TokenReader, TokenWriter

    num_tokens = 6
    file_path = "/path/to/dataset.bin"

    # Write the tokens to the dataset.
    with TokenWriter(file_path, num_tokens, compressed=True) as writer:
        for _ in range(10):
            writer.write([1, 2, 3, 4, 5])

    # Read the tokens from the dataset.
    reader = TokenReader(file_path)
    num_samples = len(reader)
    for i in range(num_samples):
        print(reader[i])

Additionally, you can use an offsets file to cache the offsets of each line
in the dataset:

.. highlight:: python
.. code-block:: python

    reader = TokenReader(file_path, offsets_path="/path/to/offsets.bin")

You can also read some subset of the tokens in a line using slicing syntax.
This syntax will only read the required tokens from the file, rather than
reading the entire line and then slicing it. Here is an example:

.. highlight:: python
.. code-block:: python

    reader = TokenReader(file_path)
    print(reader[0])  # Prints the first line.
    print(reader[0, 1:3])  # Prints the first line, but only the second and third tokens.
"""

import argparse
import functools
import gzip
import logging
import math
import struct
from pathlib import Path
from types import TracebackType
from typing import BinaryIO, ContextManager, Iterable, Literal, cast, overload

logger = logging.getLogger(__name__)

NumberFormat = Literal["Q", "I", "H", "B"]

MAGIC = b"MLTK"  # Magic number for the token file format.
OFFSET_MAGIC = b"MLTO"  # Magic number for the offsets file format.


def _arr_to_bytes(tokens: Iterable[int], num_tokens: int, offset: int = 0) -> tuple[bytes, int]:
    assert 0 <= offset < 8
    num_bits = (num_tokens - 1).bit_length()
    byte_arr = bytearray()
    cur_token = 0
    cur_bits = 0
    total_len = 0
    for token in tokens:
        total_len += 1
        assert 0 <= token <= num_tokens
        cur_token += token << cur_bits
        cur_bits += num_bits
        if offset > 0:
            cur_token <<= offset
            cur_bits += offset
            offset = 0
        while cur_bits >= 8:
            byte_arr.append(cur_token & 0xFF)
            cur_token >>= 8
            cur_bits -= 8
    if cur_bits:
        byte_arr.append(cur_token)
    return bytes(byte_arr), total_len


def _bytes_to_arr(data: bytes, seq_len: int, num_tokens: int, offset: int = 0) -> list[int]:
    assert 0 <= offset < 8
    num_bits = (num_tokens - 1).bit_length()
    arr: list[int] = []
    cur_token = 0
    cur_bits = 0
    mask = (1 << num_bits) - 1
    for byte in data:
        cur_token += byte << cur_bits
        cur_bits += 8
        if offset != 0:
            cur_token >>= offset
            cur_bits -= offset
            offset = 0
        while cur_bits >= num_bits:
            arr.append(cur_token & mask)
            if len(arr) == seq_len:
                return arr
            cur_token >>= num_bits
            cur_bits -= num_bits
    raise ValueError("Not enough bytes to fill sequence")


class TokenWriter(ContextManager):
    """Helper class for writing a dataset of tokens to a file.

    This class can be used in conjunction with :class:`TokenReader` to write
    and read datasets of tokens. The default numerical formats are chosen to
    work well with typical ranges of token datasets. At the upper end, this
    supports ``2 ^ 32`` tokens, ``2 ^ 32`` tokens per line, and ``2 ^ 64``
    tokens per file.

    Parameters:
        path: The path to the file to write to.
        num_tokens: The number of tokens in the dataset.
        compressed: Whether to compress each line independently using zlib.
        overwrite_if_exists: Whether to overwrite the file if it already exists.
        num_tokens_fmt: The format string for the number of tokens.
        lengths_fmt: The format string for the lengths of each line.
        offset_fmt: The format string for the offsets of each line.
    """

    def __init__(
        self,
        path: str | Path,
        num_tokens: int,
        compressed: bool = False,
        overwrite_if_exists: bool = False,
        *,
        num_tokens_fmt: NumberFormat = "I",
        lengths_fmt: NumberFormat = "I",
        offset_fmt: NumberFormat = "Q",
    ) -> None:
        self._path = Path(path)
        self._fp: gzip.GzipFile | BinaryIO | None = None
        self._offsets: list[int] = []
        self._num_tokens = num_tokens
        self._compressed = compressed
        self._overwrite_if_exists = overwrite_if_exists
        self._num_tokens_fmt = num_tokens_fmt
        self._lengths_fmt = lengths_fmt
        self._offset_fmt = offset_fmt

    def __enter__(self) -> "TokenWriter":
        if self._path.exists():
            if self._overwrite_if_exists:
                logger.warning("Token file already exists and will be overwritten")
            else:
                raise FileExistsError(f"Token file already exists at {self._path}")
        self._fp = gzip.open(self._path, "wb") if self._compressed else open(self._path, "wb")

        # Writes the file header.
        self._fp.write(MAGIC)
        self._fp.write((self._num_tokens_fmt + self._lengths_fmt + self._offset_fmt).encode("ascii"))
        self._fp.write(struct.pack(self._num_tokens_fmt, self._num_tokens))

        return self

    def __exit__(self, _t: type[BaseException] | None, _e: BaseException | None, _tr: TracebackType | None) -> None:
        assert self._fp is not None

        self._fp.close()

    def write(self, tokens: Iterable[int]) -> None:
        assert self._fp is not None, "TokenWriter must be opened with a context manager"

        # Converts the tokens to a binary array.
        byte_data, num_tokens = _arr_to_bytes(tokens, self._num_tokens)

        # Writes the binary data
        self._fp.write(struct.pack(self._lengths_fmt, num_tokens))
        self._fp.write(byte_data)

    def writemany(self, tokens: Iterable[Iterable[int]]) -> None:
        assert self._fp is not None, "TokenWriter must be opened with a context manager"

        for line in tokens:
            self.write(line)

    def flush(self) -> None:
        assert self._fp is not None, "TokenWriter must be opened with a context manager"

        self._fp.flush()


class TokenReader:
    """Helper class for reading a dataset of tokens from a file.

    This class can be used in conjunction with :class:`TokenWriter` to write
    and read datasets of tokens.

    Parameters:
        path: The path to the file to read from.
        offsets_path: The path to the file containing the offsets of each line.
            If this is not provided, the offsets will be read from the token
            file itself. If the file does not exist, it will be created.
        use_offsets_file: Whether to use the offsets file. If this is ``False``,
            the offsets will be read from the token file itself every time that
            the reader is opened. However, if the offsets file already exists,
            then it will always be used, even if this argument is ``False``.
        in_memory: Whether to read the entire file into memory.
    """

    def _get_offsets_path(self, path: Path, offsets_path: str | Path | None) -> Path:
        if offsets_path is not None:
            return Path(offsets_path)
        return path.parent / f"{path.stem}.offsets.{path.suffix}"

    def __init__(
        self,
        path: str | Path,
        offsets_path: str | Path | None = None,
        *,
        use_offsets_file: bool = False,
        in_memory: bool = False,
    ) -> None:
        self._path = Path(path)
        offsets_path = self._get_offsets_path(self._path, offsets_path)
        self._offsets_path = offsets_path if use_offsets_file or offsets_path.exists() else None
        self._in_memory = in_memory

        # Check the magic number against GZIP magic number to determine if
        # the file is compressed.
        with open(self._path, "rb") as f:
            self._compressed = f.read(2) == b"\x1f\x8b"

        with gzip.open(self._path, "rb") if self._compressed else open(self._path, "rb") as f:
            magic = f.read(len(MAGIC))
            if magic != MAGIC:
                raise ValueError("Invalid token file")
            fmt_strings = f.read(3).decode("ascii")
            self._num_tokens_fmt = fmt_strings[0]
            self._lengths_fmt = fmt_strings[1]
            self._offset_fmt = fmt_strings[2]
            self._num_tokens = struct.unpack(self._num_tokens_fmt, f.read(struct.calcsize(self._num_tokens_fmt)))[0]

            self._lengths_fmt_size = struct.calcsize(self._lengths_fmt)

            def read_offsets() -> tuple[list[int], int]:
                offsets: list[int] = []
                while True:
                    offset = f.tell()
                    if (sq_bytes := f.read(self._lengths_fmt_size)) is None or len(sq_bytes) == 0:
                        break
                    offsets.append(offset)
                    seq_len_int = struct.unpack(self._lengths_fmt, sq_bytes)[0]
                    f.seek((seq_len_int * self.bits_per_token + 7) // 8, 1)
                return offsets, f.tell()

            if self._offsets_path is not None:
                if self._offsets_path.exists():
                    with open(self._offsets_path, "rb") as ofr:
                        magic = ofr.read(len(OFFSET_MAGIC))
                        if magic != OFFSET_MAGIC:
                            raise ValueError("Invalid offsets file")
                        offset_num_bytes = struct.calcsize(self._offset_fmt)
                        self._total_length = struct.unpack(self._offset_fmt, ofr.read(offset_num_bytes))[0]
                        num_offsets_bytes = ofr.read(struct.calcsize(self._num_tokens_fmt))
                        num_offsets = struct.unpack(self._num_tokens_fmt, num_offsets_bytes)[0]
                        of_bytes = ofr.read(num_offsets * offset_num_bytes)
                        self._offsets = list(struct.unpack(f"{num_offsets}{self._offset_fmt}", of_bytes))
                else:
                    self._offsets, self._total_length = read_offsets()
                    with open(self._offsets_path, "wb") as ofw:
                        ofw.write(OFFSET_MAGIC)
                        ofw.write(struct.pack(self._offset_fmt, self._total_length))
                        ofw.write(struct.pack(self._num_tokens_fmt, len(self._offsets)))
                        ofw.write(struct.pack(f"{len(self._offsets)}{self._offset_fmt}", *self._offsets))
            else:
                self._offsets, self._total_length = read_offsets()

        self._data: bytes | None = None
        if self._in_memory:
            with gzip.open(self._path, "rb") if self._compressed else open(self._path, "rb") as f:
                self._data = f.read()

    @functools.cached_property
    def bits_per_token(self) -> int:
        return math.ceil(math.log2(self._num_tokens))

    def byte_length(self, index: int) -> int:
        start = self._offsets[index]
        end = self._offsets[index + 1] if (index + 1) < len(self._offsets) else self._total_length
        return end - start

    def length(self, index: int) -> int:
        return ((self.byte_length(index) - self._lengths_fmt_size) * 8) // self.bits_per_token

    @property
    def byte_lengths(self) -> list[int]:
        return [self.byte_length(i) for i in range(len(self._offsets))]

    @property
    def lengths(self) -> list[int]:
        return [self.length(i) for i in range(len(self._offsets))]

    @property
    def offsets(self) -> list[int]:
        return self._offsets

    def __len__(self) -> int:
        return len(self._offsets)

    @overload
    def __getitem__(self, index: int | tuple[int, slice]) -> list[int]:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[list[int]]:
        ...

    def __getitem__(self, index: int | tuple[int, slice] | slice) -> list[int] | list[list[int]]:
        if isinstance(index, int):
            offset = self._offsets[index]
            seq_len = self.length(index)
            start, length = offset + self._lengths_fmt_size, (seq_len * self.bits_per_token + 7) // 8
            if self._data is None:
                with gzip.open(self._path, "rb") if self._compressed else open(self._path, "rb") as f:
                    f.seek(start)
                    byte_data = f.read(length)
            else:
                byte_data = self._data[start : start + length]
            return _bytes_to_arr(byte_data, seq_len, self._num_tokens)

        if isinstance(index, tuple) and len(index) == 2 and isinstance(index[0], int) and isinstance(index[1], slice):
            index, seq_slice = index
            offset = self._offsets[index]
            seq_len = self.length(index)
            offset_start = offset + self._lengths_fmt_size

            def make_positive(n: int) -> int:
                return min(n if n >= 0 else n + seq_len, seq_len)

            # Breaks down the slice into start, stop, and step.
            start = 0 if seq_slice.start is None else make_positive(seq_slice.start)
            stop = seq_len if seq_slice.stop is None else make_positive(seq_slice.stop)
            if stop <= start:
                return cast(list[int], [])

            start_bit = start * self.bits_per_token
            start_byte, start_offset = start_bit // 8, start_bit % 8
            end_byte = (stop * self.bits_per_token + 7) // 8

            if self._data is None:
                with gzip.open(self._path, "rb") if self._compressed else open(self._path, "rb") as f:
                    f.seek(offset_start)
                    f.seek(start_byte, 1)
                    byte_data = f.read(end_byte - start_byte)
            else:
                byte_data = self._data[offset_start + start_byte : offset_start + end_byte]

            arr = _bytes_to_arr(byte_data, stop - start, self._num_tokens, offset=start_offset)
            if seq_slice.step is not None:
                arr = arr[:: seq_slice.step]
            return arr

        if isinstance(index, slice):

            def make_positive(n: int) -> int:
                return min(n if n >= 0 else n + len(self), len(self))

            start = 0 if index.start is None else make_positive(index.start)
            stop = len(self) if index.stop is None else make_positive(index.stop)
            if stop <= start:
                return cast(list[int], [])

            # Non-contiguous reads can just be done using existing logic.
            if index.step is not None and index.step != 1:
                return [self[i] for i in range(start, stop, index.step)]

            offsets = [self._offsets[i] for i in range(start, stop)]
            seq_lens = [self.length(i) for i in range(start, stop)]

            start = offsets[0] + self._lengths_fmt_size
            stop = offsets[-1] + self._lengths_fmt_size + (seq_lens[-1] * self.bits_per_token + 7) // 8
            if self._data is None:
                with gzip.open(self._path, "rb") if self._compressed else open(self._path, "rb") as f:
                    f.seek(start)
                    byte_data = f.read(stop - start)
            else:
                byte_data = self._data[start:stop]
            starts = [offset - offsets[0] for offset in offsets]
            return [
                _bytes_to_arr(byte_data[start:], seq_len, self._num_tokens) for start, seq_len in zip(starts, seq_lens)
            ]

        raise TypeError("Index must be an integer or a tuple of an integer and a slice")


def reshard_token_file(input_file: str | Path, num_shards: int, batch_size: int) -> list[Path]:
    """Reshards an input file into multiple output shards.

    Args:
        input_file: The input file to reshard.
        num_shards: The number of shards to create.
        batch_size: The number of rows to read at a time.

    Returns:
        A list of paths to the output shards.
    """
    assert num_shards >= 1, "Number of shards must be at least 1."

    reader = TokenReader(input_file, use_offsets_file=False)
    reader_len = len(reader)
    output_paths: list[Path] = []

    # Writes the shards.
    for shard_id in range(num_shards):
        shard_size = (reader_len + shard_id) // num_shards
        start = shard_id * shard_size
        stop = (shard_id + 1) * shard_size

        path = reader._path
        output_path = path.parent / f"{path.stem}.{shard_id}.{num_shards}{path.suffix}"
        with TokenWriter(output_path, reader._num_tokens, reader._compressed) as writer:
            batch_start = start
            while batch_start < stop:
                batch_stop = min(batch_start + batch_size, stop)
                writer.writemany(reader[batch_start:batch_stop])
                batch_start = batch_stop
        output_paths.append(output_path)

    return output_paths


def run_reshard_cli() -> None:
    """Defines an interface for resharding token datasets.

    Usage:

    .. code-block:: bash

        python -m ml.utils.tokens <num_shards> <input_file> (<input_file> ...)

    The input files must each be token datasets. This script will create a new
    token dataset for each of the output shards. The output shards will be
    named ``<input_stem>.<shard_num>.<total_shards>.<input_ext>``.
    """
    parser = argparse.ArgumentParser(description="Reshards token datasets")
    parser.add_argument("num_shards", type=int, help="The number of shards to create")
    parser.add_argument("input_files", nargs="+", help="The input files to reshard")
    parser.add_argument("-b", "--batch-size", type=int, default=32, help="The number of rows to read at a time")
    args = parser.parse_args()

    for input_file in args.input_files:
        reshard_token_file(input_file, args.num_shards, args.batch_size)


if __name__ == "__main__":
    run_reshard_cli()
