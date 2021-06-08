class Lunchparty:
    BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "LunchParty!!....\n\n"
            ),
        },
    }
    def __init__(self, channel):
        self.channel = channel
    def sendMessage(self, message):
        text = f"The result is {message}"
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},

    def getMessagePayload(self):
        return {
            "channel": self.channel,
            "blocks": [
                self.BLOCK,
                *self.sendMessage("ㅎㅇㅇ"),
            ],
        }

