import uuid


class DefaultUniqueValueGenerators:
    wallet_prefix: str = ""
    api_key_prefix: str = ""

    def generate_wallet_address(self) -> str:
        return self.wallet_prefix + str(uuid.uuid4())

    def generate_api_key(self) -> str:
        return self.api_key_prefix + str(uuid.uuid4())
