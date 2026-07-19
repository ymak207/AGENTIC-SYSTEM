from routing.intent_classifier import IntentClassifier
from capabilities.capability_router import CapabilityRouter


class IntentRouter:

    def __init__(self):

        self.intent_classifier = IntentClassifier()

        self.capability_router = CapabilityRouter()

    def route(
        self,
        user_input
    ):

        intent = self.intent_classifier.classify(
            user_input
        )

        capabilities = self.capability_router.route(
            intent
        )

        return {

            "capabilities": capabilities

        }