
class FrogLogger:
    """
    Simple logging class for utiltities, to allow users run function to send messages back to UI

    Currently just collects all and dumps at the end, but could be send to UI immediately later
    
    """
    
    def __init__(self):
        self.status = "success"
        self.messages = []

    def write(self, message):
        self.messages.append(message)

    def set_status(self, status):
        self.status = status

    def result(self):
        return {
            "status": self.status,
            "messages": self.messages
        }