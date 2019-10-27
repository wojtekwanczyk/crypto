# wersja bez litery Q
import re


alphabet = "abcdefghijklmnoprstuvwxyz"

key = "szyfr"
plaintext = "to jest tajna wiadomosc"
plaintext = plaintext.replace(' ', '')
ciphertext = ""


letter_place = dict()
place_letter = {}
# usuwamy litery klucza z alfabetu
alphabet_without_key = re.sub('[' + key + ']', '', alphabet)
# konkatenacja klucza z alfabetem
key_alphabet = key + alphabet_without_key

# tworzymy dwie pomocnicze mapy: 
# litera -> wspolrzedne w tablicy
# wspolrzedne w tablicy -> litera
for i in range(0, 5):
    for j in range(0, 5):
        letter = key_alphabet[5 * i + j]
        letter_place[letter] = (i, j)
        place_letter[(i, j)] = letter

# czesc szyfrujaca, iterujemy po dwojkach liter
# i podmieniamy je zgodnie z algorytmem, ktory jest
# opisany za pomoca 3 kolejnych mozliwosci ponizej
for a_letter, b_letter in zip(plaintext[::2], plaintext[1::2]):
    a_row, a_col = letter_place[a_letter]
    b_row, b_col = letter_place[b_letter]
    if a_row == b_row:
        a_col = (a_col + 1) % 5
        b_col = (b_col + 1) % 5
    elif a_col == b_col:
        a_row = (a_row + 1) % 5
        b_row = (b_row + 1) % 5
    else:
        tmp = a_col
        a_col = b_col
        b_col = tmp
    
    ciphertext += place_letter[(a_row, a_col)]
    ciphertext += place_letter[(b_row, b_col)]

print(ciphertext)

    







