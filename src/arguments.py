import argparse


def parser():
    parser = argparse.ArgumentParser(description='Hyperparameters')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    """fee"""
    parser.add_argument('--fee', metavar='F', type=int, default=100,
                        help='default rent fee')
    parser.add_argument('--additional', metavar='A', type=int, default=200,
                        help='additional fee per 1h')

    """params"""
    parser.add_argument('--balance', metavar='B', type=int, default=10**6,
                        help='default balance')
    parser.add_argument('--time', metavar='T', type=int, default=1,
                        help='default rent time')

    parser.add_argument('--active', metavar='P', type=float, default=0.05,
                        help='active ratio')
    parser.add_argument('--missing', metavar='M', type=float, default=0.03,
                        help='missing ratio')

    """simulation"""
    parser.add_argument('--users', metavar='U', type=int, default=100,
                        help='number of users')
    parser.add_argument('--round', metavar='R', type=int, default=1000,
                        help='number of rounds (h)')

    """mechanism"""
    parser.add_argument('--mechanism', metavar='S', type=int, default=0,
                        help='incentive system (0: linear, 1: power, 2: exponential)')
    parser.add_argument('--coef', metavar='C', type=int, default=1000,
                        help='incentive coef.')
    parser.add_argument('--power', metavar='X', type=float, default=2.0,
                        help='incentive power')
    parser.add_argument('--exp', metavar='E', type=float, default=2.0,
                        help='incentive exp.')

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parser()
    print(args)
