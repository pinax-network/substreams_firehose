"""
SPDX-License-Identifier: MIT

This modules holds the custom exception defined for the application.
"""

class BlockStreamException(Exception):
    """
    Thrown by a task when failing to process a block.

    The information will be used to start another task for the remaining blocks to be processed.

    Attributes:
        start:
            The block stream's starting block.
        end:
            The block stream's ending block.
        failed:
            The block that failed processing.
    """
    def __init__(self, start: int, end: int, failed: int) -> None:
        self.start = start
        self.end = end
        self.failed = failed

    def __str__(self) -> str:
        return (f'Block streaming failed for block #{self.failed} in range [{self.start}, {self.end}]'
                f' ({self.end - self.failed} blocks remaining)')
