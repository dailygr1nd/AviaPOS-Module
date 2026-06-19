from abc import ABC
from abc import abstractmethod


class RailOneAdapter(

    ABC

):

    @abstractmethod
    def request_quote(

        self,

        source_account,

        destination_account,

        amount,

        currency

    ):
        pass

    @abstractmethod
    def create_intent(

        self,

        quote_id

    ):
        pass

    @abstractmethod
    def execute(

        self,

        intent_id

    ):
        pass