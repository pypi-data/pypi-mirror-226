def _stringToNumbers(string):
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  numberList = []
  for letter in string.lower():
    if letter == " ":
      number = 1000
    else:
      number = alphabet.find(letter)
    numberList.append(number)
  return numberList

def _numbersToString(numbers):
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  letterList = []
  for number in numbers:
    if number == 1000:
      letter = " "
    else:
      letter = alphabet[int(number)]
    letterList.append(letter)
  return "".join(letterList)

def _stringToAscii(string):
  asciiNumbers = []
  for letter in string:
    number = ord(letter)
    asciiNumbers.append(number)
  return asciiNumbers

def _asciiToString(asciiNumbers):
  letterList = []
  for number in asciiNumbers:
    letter = chr(number)
    letterList.append(letter)
  return "".join(letterList)