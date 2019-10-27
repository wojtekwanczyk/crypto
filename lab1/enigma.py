
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
reflectorDict = {"A": "Y", "Y": "A", "B": "R", "R": "B", "C": "U", "U": "C", "D": "H", "H": "D", "E": "Q", "Q": "E", "F": "S", "S": "F",
                 "G": "L", "L": "G", "I": "P", "P": "I", "J": "X", "X": "J", "K": "N", "N": "K", "M": "O", "O": "M", "T": "Z", "Z": "T", "V": "W", "W": "V"}
ringSettings = "ABC"
ringPositions = "DEF"
plugboard = "BT AS WE PO"


def caesarShift(str, amount):
    res = ""
    for i in range(0, len(str)):
        letter = str[i]
        code = ord(letter)
        if ((code >= 65) and (code <= 90)):
            letter = chr(((code - 65 + amount) % 26) + 65)
        res = res + letter

    return res


def encode(plaintext):
    # ładujemy globalne zmienne
    global reflectorDict, ringSettings, ringPositions, plugboard
    plaintext = plaintext.upper()

    #A = Lewy,  B = Srodkowy,  C=Prawy
    rotorA = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    rotorB = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    rotorC = "BDFHJLCPRTXVZNYEIWGAKMUSQO"

    # ustawiamy zapadki rotorów
    # zapadka rotora A jest nie istotna dla 3 rotorow + reflector
    #rotorANotch = "Q"
    rotorBNotch = "E"
    rotorCNotch = "V"

    # ladujemy ustawienie poczatkowe
    rotorALetter = ringPositions[0]
    rotorBLetter = ringPositions[1]
    rotorCLetter = ringPositions[2]

    # ladujemy ustawienia rotorow (ich offsetu)
    rotorASetting = ringSettings[0]
    offsetASetting = alphabet.index(rotorASetting)
    rotorBSetting = ringSettings[1]
    offsetBSetting = alphabet.index(rotorBSetting)
    rotorCSetting = ringSettings[2]
    offsetCSetting = alphabet.index(rotorCSetting)

    # stosujemy dany ofset dla rotora
    rotorA = caesarShift(rotorA, offsetASetting)
    rotorB = caesarShift(rotorB, offsetBSetting)
    rotorC = caesarShift(rotorC, offsetCSetting)

    # przesuwamy w "kolo" caly alfabet o offset
    if offsetASetting > 0:
        rotorA = rotorA[26-offsetASetting:] + rotorA[0:26-offsetASetting]
    if offsetBSetting > 0:
        rotorB = rotorB[26-offsetBSetting:] + rotorB[0:26-offsetBSetting]
    if offsetCSetting > 0:
        rotorC = rotorC[26-offsetCSetting:] + rotorC[0:26-offsetCSetting]

    ciphertext = ""

    # tworzymy mape dla kazdej litery podpietej w plug boardzie
    plugboardConnections = plugboard.upper().split(" ")
    plugboardDict = {}
    for pair in plugboardConnections:
        if len(pair) == 2:
            plugboardDict[pair[0]] = pair[1]
            plugboardDict[pair[1]] = pair[0]
        else:
            print("Wrong plugboard setting!!!")
            return 1

    # przystepujemy do szyfrowania
    for letter in plaintext:
        encryptedLetter = letter

        if letter in alphabet:
            # obracamy rotory zanim zaszyfrujemy litere
            # pierwszy rotor domyslnie zawsze sie obraca
            rotorCLetter = alphabet[(alphabet.index(rotorCLetter) + 1) % 26]
            # sprawdzamy czy trafilismy na zapadke w rotorze C
            rotorTrigger = (rotorCLetter == rotorCNotch)

            if rotorTrigger:
                # obracamy rotor B
                rotorBLetter = alphabet[(alphabet.index(rotorBLetter) + 1) % 26]
                # sprawdzamy czy trafilismy na zapadke w rotorze C
                rotorTrigger = (rotorBLetter == rotorBNotch)

                if rotorTrigger:
                    # obracamy rotor C
                    rotorALetter = alphabet[(alphabet.index(rotorALetter) + 1) % 26]

            # podmieniamy litery na podstawie plugboarda (za pomoca stworzonych wczesniej map)
            if letter in plugboardDict.keys():
                if plugboardDict[letter] != "":
                    encryptedLetter = plugboardDict[letter]

            # odczytujemy stan aktualnych rotorow
            offsetA = alphabet.index(rotorALetter)
            offsetB = alphabet.index(rotorBLetter)
            offsetC = alphabet.index(rotorCLetter)

            # szyfrujemy litere na rotorze C
            pos = alphabet.index(encryptedLetter)
            let = rotorC[(pos + offsetC) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetC + 26) % 26]

            # szyfrujemy litere na rotorze B
            pos = alphabet.index(encryptedLetter)
            let = rotorB[(pos + offsetB) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetB + 26) % 26]

            # szyfrujemy litere na rotorze A
            pos = alphabet.index(encryptedLetter)
            let = rotorA[(pos + offsetA) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetA + 26) % 26]

            # szyfrujemy litere na reflektorze
            if encryptedLetter in reflectorDict.keys():
                if reflectorDict[encryptedLetter] != "":
                    encryptedLetter = reflectorDict[encryptedLetter]

            # I spowrotem szyfrujemy na kazdym kole

            # rotor 1
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetA) % 26]
            pos = rotorA.index(let)
            encryptedLetter = alphabet[(pos - offsetA + 26) % 26]

            # rotor 2
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetB) % 26]
            pos = rotorB.index(let)
            encryptedLetter = alphabet[(pos - offsetB + 26) % 26]

            # rotor 3
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetC) % 26]
            pos = rotorC.index(let)
            encryptedLetter = alphabet[(pos - offsetC + 26) % 26]

            # Na koniec ponownie poslugujemy sie plugboardem
            if encryptedLetter in plugboardDict.keys():
                if plugboardDict[encryptedLetter] != "":
                    encryptedLetter = plugboardDict[encryptedLetter]

        ciphertext = ciphertext + encryptedLetter

    return ciphertext


plaintext = input("Plaintext:\n")
ciphertext = encode(plaintext)
print("Ciphertext: \n " + ciphertext)
