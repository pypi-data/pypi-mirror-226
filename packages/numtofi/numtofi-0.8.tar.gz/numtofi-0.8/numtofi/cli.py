from .core import number_to_text, number_to_text_length

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert a number to its Finnish textual representation.")
    parser.add_argument('number', type=int, help='The number to convert. Must be a positive integer.')
    parser.add_argument('--nospaces', action='store_true', help='If set, removes spaces between words.')
    parser.add_argument('--length', action='store_true', help='If set, return only the character length of the textual representation.')

    args = parser.parse_args()

    try:
        if args.length:
            result = number_to_text_length(args.number, not args.nospaces)
        else:
            result = number_to_text(args.number, not args.nospaces)
        print(result)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
