"""
numtofi.core Submodule

Constants:
- one_to_ten: List containing numbers 1-10 in Finnish.
- powers_of_ten: Dictionary defining large numbers, such as hundred, thousand, million, etc., in Finnish.

Main Function:
- number_to_text(n, spaces=True):
  - Description: Converts a number into its Finnish textual representation.
  - Parameters:
    - n (int): The number to convert. Must be a positive integer less than 10^18.
    - spaces (bool): If False, removes spaces between words. Default is True.
  - Returns: The textual representation of the number in Finnish.
  - Errors: If the given number is not a positive integer or it's greater than or equal to 10^18, the function raises a ValueError.

Usage Example:

from numtofi import number_to_text, number_to_text_length

# Convert a number to Finnish with spaces
number = 12345
textual_representation = number_to_text(number)
print(textual_representation)  # Expected output: "kaksitoistatuhatta kolmesataaneljäkymmentäviisi"

# Convert a number to Finnish without spaces
textual_representation_no_spaces = number_to_text(number, spaces=False)
print(textual_representation_no_spaces)  # Expected output: "kaksitoistatuhattakolmesataaneljäkymmentäviisi"

# Find the length of the number's textual representation
textual_representation_length = number_to_text_length(number)
print(textual_representation_length)  # Expected output: "47"

# Handling errors
try:
    large_number = 10**18
    number_to_text(large_number)
except ValueError as e:
    print(f"Error: {e}")  # Expected output: "Error: Number must be a positive integer less than 10^18."

"""

MIN_SUPPORT = 0
MAX_SUPPORT = 10**18

# The first nine numbers 1-9 (yksi to yhdeksän) that will repeat in all written numbers.
one_to_ten = [
    # The first index is left for zero but written as empty string to the end of the numbers in certain cases.
    '', 'yksi', 'kaksi', 'kolme', 'neljä', 'viisi', 'kuusi', 'seitsemän', 'kahdeksan', 'yhdeksän', 'kymmenen'
]

powers_of_ten = {
    100: 'sata',
    1000: 'tuhat',
    # https://fi.wikipedia.org/wiki/Suurten_lukujen_nimet
    1000000: 'miljoona',
    1000000000: 'miljardi',
    1000000000000: 'biljoona',
    1000000000000000: 'triljoona'
}

def number_to_text(n, spaces=True):
    """Calculate the number of letters in the Finnish textual representation of a number using further optimized approach.
    Parameters:
    - n (int): The number to convert. Must be a positive integer less than 10^18.
    - spaces (bool): Whether to include spaces in the count.
    Returns:
    - int: The number of letters in the textual representation of the number in Finnish.
    """

    # Check that the given number is a positive integer less than quintillion.
    if not isinstance(n, int) or n < MIN_SUPPORT or n >= MAX_SUPPORT:
        raise ValueError("Number must be a positive integer less than 10^18.")

    # Handle zero
    if n == 0:
        return "nolla"

    # Initialize the result
    result = ""

    # Use a stack to keep track of numbers to process
    stack = [n]

    def _prefix(x):
        # Ones
        if x < 11:
            prefix = one_to_ten[x]
        # Teens
        elif x < 20:
            prefix = one_to_ten[x-10]+'toista'
        # Tens
        elif x < 100:
            prefix = one_to_ten[x//10]+'kymmentä'+one_to_ten[x%10]
        # Hundreds
        else:
            # First hundred
            if x < 200:
                prefix = 'sata'
                n = (x-100)
            # 200-900
            else:
                prefix = one_to_ten[x//100]+'sataa'
                n = x % 100
            # Rest of the hundred
            prefix += _prefix(n)
        return prefix

    while stack:
        current_n = stack.pop()
        # Numbers under thousand
        if current_n < 1000:
            result += _prefix(current_n)
        else:
            max_power = max(power for power in powers_of_ten if power <= current_n)
            max_power_n = current_n // max_power
            next_number = current_n % max_power

            if max_power_n == 1:
                result += powers_of_ten[max_power]
                stack.append(next_number)
            else:
                prefix = _prefix(max_power_n)
                if max_power == 1000:
                    separator = " " if spaces else ""
                    affix = "ta"
                else:
                    separator = " " if spaces and (max_power % 1000) == 0 else ""
                    affix = "a"
                    if spaces and next_number == 0 and current_n > 999999:
                        prefix += " "

                if next_number == 0:
                    separator = ""

                result += prefix + powers_of_ten[max_power] + affix + separator
                stack.append(next_number)

    return result

def number_to_text_rec(n, spaces=True):
    """
    Convert a number into its Finnish textual representation. Recrusive version.
    See for format recommendations:
    - https://www.kielikello.fi/-/luvut-ja-tekstin-hahmotettavuus
    - http://users.jyu.fi/~pamakine/kieli/suomi/numeraalit/numerot.html

    Parameters:
    - n (int): The number to convert. Must be a positive integer less than 10^18.
    - spaces (bool): If False, removes spaces between words. Default is True.

    Returns:
    - str: The textual representation of the number in Finnish.
    """

    # Check that the given number is a positive integer less than quintillion.
    if not isinstance(n, int) or n < MIN_SUPPORT or n >= MAX_SUPPORT:
        raise ValueError("Number must be a positive integer less than 10^18.")

    # Handle zero
    if n == 0:
        return "nolla"

    # Main recursive function
    def _number_to_text(n):
        # "Zero" does not appear in number words.
        # Numbers from 1 to 9 are base for all numbers in the finnish base 10 number systems.
        if n < 11:
            return one_to_ten[n]
        # Numbers up to nineteen have special words.
        elif n < 20:
            return one_to_ten[n-10] + "toista"
        # Optimize for the easy cases between twenty and ninety-nine.
        elif n < 100:
            return one_to_ten[n // 10] + "kymmentä" + (one_to_ten[n % 10] if n % 10 != 0 else "")
        else:
            # Determine the maximum power of ten for which the number qualifies.
            max_power = max(power for power in powers_of_ten if power <= n)

            # First power numbers don't need repetition e.g., "sata, tuhat, miljoona..."
            if n // max_power == 1:
                # No spaces.
                return (powers_of_ten[max_power] + _number_to_text(n % max_power)).strip()

            prefix = _number_to_text(n // max_power)
            next_number = _number_to_text(n % max_power)
            # Special case: "tuhat" becomes "tuhatta"
            if max_power == 1000:
                separator = " " if spaces else ""
                affix = "ta"
            # Suffix "-a" is added to numbers like "sata" -> "sataa", "miljoona" -> "miljoonaa",...
            else:
                # Add a space after every power of a thousand.
                separator = " " if spaces and (max_power % 1000) == 0 else ""
                affix = "a"
                # one more special case for plain millions, billions etc.
                # "viisi miljoonaa" and "viisimiljoonaa viisi" are preferred formats
                if spaces and next_number == "" and n > 999999:
                    prefix += " "
            return (prefix + powers_of_ten[max_power] + affix + separator + next_number).strip()

    return _number_to_text(n)

# Pre-calculated lengths
TA_LENGTH = len("ta")
A_LENGTH = len("a")
NOLLA_LENGTH = len("nolla")

# Lengths for number from 0 to 999.
one_to_ten_lengths = {n: len(number_to_text(n)) for n in range(1, 1000)}
one_to_ten_lengths[0] = 0

# Length of powers of ten.
powers_of_ten_lengths = {key: len(value) for key, value in powers_of_ten.items()}

def number_to_text_length(n, spaces=True):
    """
    Calculate the number of letters in the Finnish textual representation of a number
    using optimized approach with while loop instead of recursion.

    Parameters:
    - n (int): The number to convert. Must be a positive integer less than 10^18.
    - spaces (bool): Whether to include spaces in the count.

    Returns:
    - int: The number of letters in the textual representation of the number in Finnish.
    """

    # Check that the given number is a positive integer less than quintillion.
    if not isinstance(n, int) or n < MIN_SUPPORT or n >= MAX_SUPPORT:
        raise ValueError("Number must be a positive integer less than 10^18.")

    # Handle zero
    if n == 0:
        return NOLLA_LENGTH

    # Initialize the result
    result = 0

    # Use a stack to keep track of numbers to process
    stack = [n]

    while stack:
        current_n = stack.pop()

        # Number from 0 to 999 have already been calculated to the dictionary
        # since they repeat in all scales
        if current_n < 1000:
            result += one_to_ten_lengths[current_n]
        else:
            max_power = max(power for power in powers_of_ten_lengths if power <= current_n)
            max_power_n = current_n // max_power
            max_power_m = current_n % max_power

            if max_power_n == 1:
                result += powers_of_ten_lengths[max_power]
                stack.append(max_power_m)
            else:
                prefix = one_to_ten_lengths[max_power_n]
                next_number = max_power_m
                if max_power == 1000:
                    separator = 1 if spaces else 0
                    affix = TA_LENGTH
                else:
                    separator = 1 if spaces and (max_power % 1000) == 0 else 0
                    affix = A_LENGTH
                    if spaces and next_number == 0 and current_n > 999999:
                        prefix += 1
                if next_number == 0:
                    separator = 0

                result += prefix + powers_of_ten_lengths[max_power] + affix + separator
                stack.append(next_number)

    return result
