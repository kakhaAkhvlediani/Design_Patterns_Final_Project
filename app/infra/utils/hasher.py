import hashlib
import pickle


class DefaultHashFunction:
    def use_my_hash(self, *args: object) -> str:
        encoded_password: bytes = pickle.dumps(args)
        hashed_password: str = hashlib.sha256(encoded_password).hexdigest()

        return hashed_password

    def __call__(self, *args: object) -> str:
        return self.use_my_hash(args)
