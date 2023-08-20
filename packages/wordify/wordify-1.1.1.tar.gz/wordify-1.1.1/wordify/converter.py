class Converter:
    """
    A class for converting numerical values into their English word representation.
    """

    _position_names = [
        "", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion",
        "septillion", "octillion", "nonillion", "decillion", "un-decillion", "duo-decillion",
        "tre-decillion", "quattuor-decillion", "quin-decillion", "sex-decillion", "septen-decillion",
        "octo-decillion", "novem-decillion", "vigintillion", "un-vigintillion", "duo-vigintillion",
        "tres-vigintillion", "quattuor-vigintillion", "quin-vigintillion", "ses-vigintillion",
        "septen-vigintillion", "octo-vigintillion", "novem-vigintillion", "trigintillion",
        "un-trigintillion", "duo-trigintillion", "tres-trigintillion", "quattour-trigintillion",
        "quin-trigintillion", "ses-trigintillion", "septen-trigintillion", "otcto-trigintillion",
        "novem-trigintillion", "quadragintillion", "un-quadragintillion", "duo-quadragintillion",
        "tre-quadragintillion", "quattuor-quadragintillion", "quin-quadragintillion",
        "sex-quadragintillion", "septen-quadragintillion", "octo-quadragintillion",
        "novem-quadragintillion", "quinquagintillion", "un-quinquagintillion", "duo-quinquagintillion",
        "tre-quinquagintillion", "quattuor-quinquagintillion", "quin-quinquagintillion",
        "sex-quinquagintillion", "septen-quinquagintillion", "octo-quinquagintillion",
        "novem-quinquagintillion", "sexagintillion", "un-sexagintillion", "duo-sexagintillion",
        "tre-sexagintillion", "quattuor-sexagintillion", "quin-sexagintillion", "sex-sexagintillion",
        "septen-sexagintillion", "octo-sexagintillion", "novem-sexagintillion", "septuagintillion",
        "un-septuagintillion", "duo-septuagintillion", "tre-septuagintillion",
        "quattuor-septuagintillion", "quin-septuagintillion", "sex-septuagintillion",
        "septen-septuagintillion", "octo-septuagintillion", "novem-septuagintillion", "octogintillion",
        "un-octogintillion", "duo-octogintillion", "tre-octogintillion", "quattuor-octogintillion",
        "quin-octogintillion", "sex-octogintillion", "septen-octogintillion", "octo-octogintillion",
        "novem-octogintillion", "nonagintillion", "un-nonagintillion", "duo-nonagintillion",
        "tre-nonagintillion", "quattuor-nonagintillion", "quin-nonagintillion", "sex-nonagintillion",
        "septen-nonagintillion", "octo-nonagintillion", "novem-nonagintillion", "centillion"
    ]

    _names = {
        '9': 'nine', '8': 'eight', '7': 'seven', '6': 'six', '5': 'five',
        '4': 'four', '3': 'three', '2': 'two', '1': 'one', '0': '',
        '19': 'nineteen', '18': 'eighteen', '17': 'seventeen', '16': 'sixteen',
        '15': 'fifteen', '14': 'fourteen', '13': 'thirteen', '12': 'twelve',
        '11': 'eleven', '10': 'ten',
        '90': 'ninety', '80': 'eighty', '70': 'seventy', '60': 'sixty', '50': 'fifty',
        '40': 'forty', '30': 'thirty', '20': 'twenty', '0': '',
    }

    def __init__(self, number=0):
        """
        Initializes the OptimizedConverter instance with a given number.
        :param number: The numerical value to be converted.
        """
        if not isinstance(number, int) and not isinstance(number, str):
            raise ValueError("Invalid input. Number must be an integer or a string.")
        self.original_number = str(number)
        self.padded_number = self._pad_number()
        self._position = 0

    def _pad_number(self):
        """
        Pads the original number with leading zeros to ensure groups of three digits.
        :return: The padded number.
        """
        if not self.original_number.isdigit():
            raise ValueError("Invalid input. Number must contain only digits.")
        padding = (3 - len(self.original_number) % 3) % 3
        return '0' * padding + self.original_number

    def _convert_group_to_word(self, group):
        """
        Converts a three-digit group into its English word representation.
        :param group: The three-digit group.
        :return: The English word representation of the group.
        """
        res = ""
        if group[0] != '0':
            res += f"{self._names[group[0]]} hundred "
        if group[1] != '0':
            if group[1] != '1':
                res += f"{self._names[group[1]+'0']} {self._names[group[2]]} "
            else:
                res += f"{self._names[group[1]+group[2]]} "
        else:
            res += f"{self._names[group[2]]} "
        res += f"{self._position_names[self._position]} and "
        self._position += 1
        return res

    def set_number(self, number):
        """
        Sets a new numerical value for conversion.
        :param new_number: The new numerical value.
        """
        if not isinstance(number, int) and not isinstance(number, str):
            raise ValueError("Invalid input. Number must be an integer or a string.")
        self.original_number = str(number)
        self.padded_number = self._pad_number()
        self._position = 0

    def convert(self):
        """
        Converts the numerical value into its English word representation.
        :return: The English word representation of the numerical value.
        """
        result = ""
        for i in range(len(self.padded_number) - 3, -1, -3):
            group = self.padded_number[i:i + 3]
            result = self._convert_group_to_word(group) + result
        return result[:-6]
