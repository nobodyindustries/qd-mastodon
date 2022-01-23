import os
import enum


class MastodonEndpoints(str, enum.Enum):
    POST_TOOT = "/api/v1/statuses"

    @staticmethod
    def get(endpoint):
        return f"{os.environ['MASTODON_INSTANCE']}{endpoint}"
