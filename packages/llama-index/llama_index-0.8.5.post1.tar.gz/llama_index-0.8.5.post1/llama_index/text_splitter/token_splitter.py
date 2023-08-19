"""Token splitter."""
import logging
from typing import Callable, List, Optional

from llama_index.callbacks.base import CallbackManager
from llama_index.callbacks.schema import CBEventType, EventPayload
from llama_index.constants import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE
from llama_index.text_splitter.types import MetadataAwareTextSplitter
from llama_index.text_splitter.utils import split_by_char, split_by_sep
from llama_index.utils import globals_helper

_logger = logging.getLogger(__name__)

# NOTE: this is the number of tokens we reserve for metadata formatting
DEFAULT_METADATA_FORMAT_LEN = 2


class TokenTextSplitter(MetadataAwareTextSplitter):
    """Implementation of splitting text that looks at word tokens."""

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
        tokenizer: Optional[Callable] = None,
        callback_manager: Optional[CallbackManager] = None,
        separator: str = " ",
        backup_separators: Optional[List[str]] = ["\n"],
    ):
        """Initialize with parameters."""
        if chunk_overlap > chunk_size:
            raise ValueError(
                f"Got a larger chunk overlap ({chunk_overlap}) than chunk size "
                f"({chunk_size}), should be smaller."
            )
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self.tokenizer = tokenizer or globals_helper.tokenizer
        self.callback_manager = callback_manager or CallbackManager([])

        all_seps = [separator] + (backup_separators or [])
        self._split_fns = [split_by_sep(sep) for sep in all_seps] + [split_by_char()]

    def split_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]:
        """Split text into chunks, reserving space required for metadata str."""
        metadata_len = len(self.tokenizer(metadata_str)) + DEFAULT_METADATA_FORMAT_LEN
        effective_chunk_size = self._chunk_size - metadata_len
        return self._split_text(text, chunk_size=effective_chunk_size)

    def split_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        return self._split_text(text, chunk_size=self._chunk_size)

    def _split_text(self, text: str, chunk_size: int) -> List[str]:
        """Split text into chunks up to chunk_size."""
        if text == "":
            return []

        with self.callback_manager.event(
            CBEventType.CHUNKING, payload={EventPayload.CHUNKS: [text]}
        ) as event:
            splits = self._split(text, chunk_size)
            chunks = self._merge(splits, chunk_size)

            event.on_end(
                payload={EventPayload.CHUNKS: chunks},
            )

        return chunks

    def _split(self, text: str, chunk_size: int) -> List[str]:
        """Break text into splits that are smaller than chunk size.

        The order of splitting is:
        1. split by separator
        2. split by backup separators (if any)
        3. split by characters

        NOTE: the splits contain the separators.
        """
        if len(self.tokenizer(text)) <= chunk_size:
            return [text]

        for split_fn in self._split_fns:
            splits = split_fn(text)
            if len(splits) > 1:
                break

        new_splits = []
        for split in splits:
            split_len = len(self.tokenizer(split))
            if split_len <= chunk_size:
                new_splits.append(split)
            else:
                # recursively split
                new_splits.extend(self._split(split, chunk_size=chunk_size))
        return new_splits

    def _merge(self, splits: List[str], chunk_size: int) -> List[str]:
        """Merge splits into chunks.

        The high-level idea is to keep adding splits to a chunk until we
        exceed the chunk size, then we start a new chunk with overlap.

        When we start a new chunk, we pop off the first element of the previous
        chunk until the total length is less than the chunk size.
        """
        chunks: List[str] = []

        cur_chunk: List[str] = []
        cur_len = 0
        for split in splits:
            split_len = len(self.tokenizer(split))
            if split_len > chunk_size:
                _logger.warning(
                    f"Got a split of size {split_len}, ",
                    f"larger than chunk size {chunk_size}.",
                )

            # if we exceed the chunk size after adding the new split, then
            # we need to end the current chunk and start a new one
            if cur_len + split_len > chunk_size:
                # end the previous chunk
                chunk = "".join(cur_chunk).strip()
                if chunk:
                    chunks.append(chunk)

                # start a new chunk with overlap
                # keep popping off the first element of the previous chunk until:
                #   1. the current chunk length is less than chunk overlap
                #   2. the total length is less than chunk size
                while cur_len > self._chunk_overlap or cur_len + split_len > chunk_size:
                    # pop off the first element
                    first_chunk = cur_chunk.pop(0)
                    cur_len -= len(self.tokenizer(first_chunk))

            cur_chunk.append(split)
            cur_len += split_len

        # handle the last chunk
        chunk = "".join(cur_chunk).strip()
        if chunk:
            chunks.append(chunk)

        return chunks
