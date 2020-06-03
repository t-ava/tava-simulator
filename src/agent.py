class Agent:
    def __init__(self, balance):
        self.balance = balance
        self.src = None
        self.dest = None
        self.return_place = None
        self.rent_time = None
        self.pred_time = None

    def renting(self, src, dest, rent_time, pred_time, args):
        try:
            assert(self.balance - args.fee > 0)
        except:
            return False

        self.balance -= args.fee
        self.src = src
        self.dest = dest
        self.return_place = None
        self.rent_time = rent_time
        self.pred_time = pred_time

        return args.fee  # fee

    def returning(self, return_time, args):
        use_time = return_time - self.rent_time
        if use_time > args.time:
            try:
                assert(self.balance - (args.additional * use_time) > 0)
            except:
                return False
            self.balance -= (args.additional * use_time)

        self.src = None
        self.return_place = self.dest
        self.dest = None
        self.rent_time = None
        self.pred_time = None
        return (args.additional * use_time)  # fee


if __name__ == "__main__":
    agent = Agent(10 ** 18)
    print(agent.balance)
