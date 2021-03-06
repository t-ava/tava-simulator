from matplotlib import pyplot as plt
import numpy as np
import json
import argparse


def parser():
    parser = argparse.ArgumentParser(description='Name of log file')
    parser.add_argument('--log', metavar='L', type=str, default="",
                        help='name of log file')
    parser.add_argument('--show', action='store_true', default=False,
                        help='show figs')

    args = parser.parse_args()
    return args


args = parser()
print("> Setting:", args)

# target = "log_1591166747.json"
# target = "log_1591169262_mechanism_1.json"
# target = "log_1591170934_mechanism_2.json"
target = args.log
if target == "":
    raise("Input valid log file.")

PATH = "./logs/" + target


if __name__ == "__main__":
    with open(PATH, 'r') as f:
        log_dict = json.load(f)

        """
        print("> # of bankrupts      :", len(bankrupts))
        print("> total incentive     :", sum(incentives))
        print("> total fee           :", sum(fees))
        print("> sum of user balances:", sum([agent.balance for agent in agents]))
        """
        log_bankrupts = log_dict["log_bankrupts"]

        rounds = len(log_bankrupts)

        log_bankrupts = [len(e) for e in log_bankrupts]

        log_total_incentive = log_dict["log_incentive"]
        log_total_fee = log_dict["log_fee"]
        log_balance = log_dict["log_balance"]

        x = np.arange(rounds)

        """log_bankrupts"""
        y = log_bankrupts
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(
            xlabel='Rounds',
            ylabel='Number',
            title='# of bankrupts')
        # ax.grid()
        fig.savefig(PATH[:-5] + "_" + "bankrupts.png")
        if args.show:
            plt.show()

        """log_total_incentive & log_total_fee"""
        y1 = log_total_incentive
        y2 = log_total_fee
        fig, ax = plt.subplots()
        ax.plot(x, y1, label="incentive")
        ax.plot(x, y2, label="fee")
        ax.legend()
        ax.set(
            xlabel='Rounds',
            ylabel='Token',
            title='total incentive & fee')
        # ax.grid()
        fig.savefig(PATH[:-5] + "_" + "incentive_and_fee.png")
        if args.show:
            plt.show()

        """log_balance"""
        y = log_balance
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(
            xlabel='Rounds',
            ylabel='Token',
            title='sum of user balances')
        # ax.grid()
        fig.savefig(PATH[:-5] + "_" + "balance.png")
        if args.show:
            plt.show()
