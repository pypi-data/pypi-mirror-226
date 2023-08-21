from .core import number_to_word

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert a number to its Finnish textual representation.")
    parser.add_argument('number', type=int, help='The number to convert. Must be a positive integer.')
    parser.add_argument('--nospaces', action='store_true', help='If set, removes spaces between words.')

    args = parser.parse_args()

    try:
        result = number_to_word(args.number, not args.nospaces)
        print(result)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
