def atbashCipher(plainText):
  plainText = plainText.lower()
  cipherLetters = []
  
  for letter in plainText:
    match letter:
      case "a":
        cipherLetters.append("z")
      case "b":
        cipherLetters.append("y")
      case "c":
        cipherLetters.append("x")
      case "d":
        cipherLetters.append("w")
      case "e":
        cipherLetters.append("v")
      case "f":
        cipherLetters.append("u")
      case "g":
        cipherLetters.append("t")
      case "h":
        cipherLetters.append("s")
      case "i":
        cipherLetters.append("r")
      case "j":
        cipherLetters.append("q")
      case "k":
        cipherLetters.append("p")
      case "l":
        cipherLetters.append("o")
      case "m":
        cipherLetters.append("n")
      case "n":
        cipherLetters.append("m")
      case "o":
        cipherLetters.append("l")
      case "p":
        cipherLetters.append("k")
      case "q":
        cipherLetters.append("j")
      case "r":
        cipherLetters.append("i")
      case "s":
        cipherLetters.append("h")
      case "t":
        cipherLetters.append("g")
      case "u":
        cipherLetters.append("f")
      case "v":
        cipherLetters.append("e")
      case "w":
        cipherLetters.append("d")
      case "x":
        cipherLetters.append("c")
      case "y":
        cipherLetters.append("b")
      case "z":
        cipherLetters.append("a")
      case " ":
        cipherLetters.append(" ")

  cipherText = "".join(cipherLetters)
  return cipherText