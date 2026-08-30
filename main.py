from collector import TGJUDataCollector
import argparse 

def get_arguments():
    parser = argparse.ArgumentParser(description="Collect Data")
    parser.add_argument("--start-date", help="start date for collecting gold price history from tgu", default="", type=str)
    parser.add_argument("--end-date", help="end date for collecting gold price history from tgu", default="", type=str)
    parser.add_argument("--timeout", help="timeout for sending request", default=3, type=int)
    parser.add_argument("--max-retries", help="number of maximum retrying to get response when getting error", default=5, type=int)
    parser.add_argument("--try-delay", help="delay between tries for getting response (seconds)", default=1.0, type=float)
    return parser.parse_args()

def main(args):
    data_collector = TGJUDataCollector(timeout=args.timeout, max_retries=args.max_retries, try_delay=args.try_delay)
    data = data_collector.collect(start_date = args.start_date, end_date = args.end_date)
    print(data)


if __name__ == "__main__":
    args = get_arguments()
    main(args)