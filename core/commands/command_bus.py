from core.commands.command import (
    Command
)


class CommandHandlerNotFound(
    Exception
):

    pass


class CommandBus:

    def __init__(self):

        self.handlers = {}

    def register(

        self,

        command_type,

        handler

    ):

        self.handlers[
            command_type
        ] = handler

    def dispatch(
        self,
        command: Command
    ):

        command_type = type(
            command
        )

        handler = self.handlers.get(
            command_type
        )

        if not handler:

            raise CommandHandlerNotFound(

                f"No handler registered for command: "

                f"{command_type.__name__}"

            )

        return handler.handle(
            command
        )