import logging
import random
import sys
import time
from argparse import ArgumentParser

import requests

logger = logging.getLogger(__name__)

with open("inputs.txt", "r", encoding="utf-8") as inputs_file:
    inputs = [line.strip() for line in inputs_file]


def benchmark(*urls):
    for isvc in urls:
        times = []
        count_s = count_f = 0
        with requests.Session() as s:
            for _ in range(1000):
                start = time.time()
                res = s.get(f"{isvc}/predict/{random.choice(inputs)}")
                if res.status_code == 200:
                    times.append(time.time() - start)
                    logger.info(
                        f"Good status code from {isvc}: {res.status_code}"
                    )
                    count_s += 1
                else:
                    logger.warning(
                        f"Bad status code from {isvc}: {res.status_code}"
                    )
                    count_f += 1

        print(f"Average Latency for {isvc}: {sum(times)/len(times)}")
        print(f"Successes for {isvc}: {count_s}")
        print(f"Failures for {isvc}: {count_f}")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", help="InferenceService URL", required=True)
    parser.set_defaults(log_level=logging.WARNING)
    parser.add_argument(
        "--verbose",
        "-v",
        help="Show more logs",
        dest="log_level",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "--quiet",
        "-q",
        help="Show fewer logs",
        dest="log_level",
        action="store_const",
        const=logging.ERROR,
    )

    return parser.parse_args()


def setup_logger(level):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.propagate = False
    logger.setLevel(level)


def main():
    args = parse_args()
    setup_logger(args.log_level)
    benchmark(args.url)


if __name__ == "__main__":
    main()