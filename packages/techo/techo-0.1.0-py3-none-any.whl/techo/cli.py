import argparse
import techo


def main():
    parser = argparse.ArgumentParser(description="Argument parser example")
    parser.add_argument("-k", "--key", help="API key")
    args, extra_args = parser.parse_known_args()

    if args.key:
        techo.store_api_key(args.key)
        print("Successfully stored API key")
        exit(0)

    if not techo.has_api_key():
        print("Error: no API key set, did you run 'techo -k <api_key>'?")
        exit(1)

    message = ' '.join(extra_args)
    techo.send(message)


if __name__ == '__main__':
    main()
