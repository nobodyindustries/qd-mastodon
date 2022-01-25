import os
import enum


class MastodonEndpoints(str, enum.Enum):
    POST_TOOT = "/api/v1/statuses"
    # For media upload v1 is deprecated
    POST_MEDIA = "/api/v2/media"

    @staticmethod
    def get(endpoint):
        return f"{os.environ['MASTODON_INSTANCE']}{endpoint}"
