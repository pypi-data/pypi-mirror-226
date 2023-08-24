from cloudstorageio.continue_token.continue_token import ContinueToken


class S3ContinueToken(ContinueToken):
    def __init__(self, token: str):
        self.token = token

    def get(self):
        return self.token
