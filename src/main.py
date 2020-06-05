import arguments


args = arguments.parser()
print("> Setting:", args)


from datetime import datetime, timedelta
import os
import json
import time
import numpy as np
import sys
import random
from mechanisms import incentive_exp, incentive_power, incentive_linear
from environment import Env
from agent import Agent


if __name__ == "__main__":
    """parameters"""
    dt = datetime(2019, 12, 19, 6, 0)
    dt_time = [dt.month, dt.weekday(), dt.hour]
    num_stations, num_divices = 100, 2
    stations_idx = [i for i in range(num_stations)]  # TODO: locational info.

    """log"""
    log_dict = dict()
    log_dict["log_bankrupts"],\
        log_dict["log_incentive"],\
        log_dict["log_fee"],\
        log_dict["log_balance"]\
        = [], [], [], []

    """bandit"""
    env = Env(num_stations, num_divices)
    agents = [Agent(args.balance) for _ in range(args.users)]  # TODO: Pareto dist.
    bankrupts, incentives, fees = [], [], []

    for i in range(args.round):
        """reset"""
        if env.devices.count(0) == num_stations:
            env.reset()
            break

        print("\n>>> Round %05d" % i, " " * 64)

        curr_dt = dt + timedelta(hours=i)
        dt_time = [curr_dt.month, curr_dt.weekday(), curr_dt.hour]

        tmp_fee, tmp_incentive = 0, 0

        """returning"""
        for agent_idx, agent in enumerate(agents):
            if agent_idx in bankrupts or\
                    agent.rent_time is None or\
                    agent.rent_time + agent.pred_time > i or\
                    random.random() < args.missing:
                continue

            print("> [Return] Agent %05d" % agent_idx, " " * 64, end="\r")

            res = agent.returning(i, args)
            if res is False:
                bankrupts.append(agent_idx)
                continue  # The agent's best response is no returning

            tmp_fee += res

            pred = np.array(env.incentive(dt_time, [agent.return_place]))
            idx = stations_idx.index(agent.return_place)

            # give incentive
            earn = 0
            diff = preds[0] - env.devices[idx]
            if diff >= 0:
                if args.mechanism == 0:
                    earn = incentive_linear((diff), args.coef)
                elif args.mechanism == 1:
                    earn = incentive_power((diff), args.coef, args.power)
                elif args.mechanism == 2:
                    earn = incentive_exp((diff), args.coef, args.exp)

            agent.balance += earn
            tmp_incentive += earn

            env.devices[idx] += 1

        """renting"""
        for agent_idx, agent in enumerate(agents):
            if agent_idx in bankrupts or\
                    random.random() > args.active:  # only active users
                continue

            print("> [Rent] Agent %05d" % agent_idx, " " * 64, end="\r")

            RAND_NUM = 10
            dests = []
            for _ in range(RAND_NUM):
                dests.append(stations_idx[np.random.randint(num_stations)])  # TODO: using locational info.

            pred_times = [np.random.randint(12) for _ in range(RAND_NUM)]
            tmp_dts = [curr_dt + timedelta(hours=t) for t in pred_times]
            dt_pred_times = [[t.month, t.weekday(), t.hour] for t in tmp_dts]

            preds = np.array([(env.incentive(dt_pred_times[t], [dests[t]]))[0] for t in range(RAND_NUM)])
            max_idx = preds.argmax()
            dest = dests[max_idx]

            src = None

            nonzero_idx = np.array(env.devices).nonzero()[0].tolist()
            if nonzero_idx == []:
                break
            src = np.random.choice(nonzero_idx)

            res = agent.renting(src, dest, i, pred_times[max_idx], args)
            if res is False:
                bankrupts.append(agent_idx)
                continue

            tmp_fee += res

            idx = stations_idx.index(agent.src)
            env.devices[idx] -= 1

        incentives.append(tmp_incentive)
        fees.append(tmp_fee)

        # print logs
        print("> # of bankrupts      :", len(bankrupts))
        print("> total incentive     :", sum(incentives))
        print("> total fee           :", sum(fees))
        print("> sum of user balances:", sum([agent.balance for agent in agents]))

        log_dict["log_bankrupts"].append(bankrupts)
        log_dict["log_incentive"].append(int(sum(incentives)))
        log_dict["log_fee"].append(sum(fees))
        log_dict["log_balance"].append(int(sum([agent.balance for agent in agents])))

    """save logs"""
    PATH = "./logs"
    try:
        os.mkdir(PATH)  # Create target Directory
    except FileExistsError:
        pass

    with open(PATH + "/log_" + str(int(time.time())) + ''.join(sys.argv[1:]).replace("--", "_").replace("=", "_") + ".json", "w") as f:
        json.dump(log_dict, f)
