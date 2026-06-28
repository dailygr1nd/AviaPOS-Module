from typing import Protocol

from core.commands.command import (
    Command
)


class CommandHandler(
    Protocol
):

    def handle(
        self,
        command: Command
    ):

        ...