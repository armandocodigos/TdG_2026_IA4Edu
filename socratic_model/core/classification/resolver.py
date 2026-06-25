from core.classification.registry import (
    TOPIC_REGISTRY
)


class TopicResolver:

    def resolve(
        self,
        topic_id: str
    ):

        if not topic_id:
            return None

        return TOPIC_REGISTRY.get(
            topic_id
        )
