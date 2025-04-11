from datetime import datetime, timedelta


class RateLimiter:
    def __init__(self, count = 10, period = 360):
        self.users = set()
        self.count = {}
        self.last_access = {}
        self.period = period
        self.limit = count


    def access(self, user):
        if user not in self.users:
            self.users.add(user)
            self.count[user] = 1       # Change self.counts[user] to self.count[user]
            self.last_access[user] = datetime.now()
            return True
        now = datetime.now()
        delta = now - self.last_access[user]
        count = max(self.count[user] - delta.seconds * self.limit / self.period, 0)  # Change self.counts[user] here as well
        if count < self.limit:
            return True
        return False


        