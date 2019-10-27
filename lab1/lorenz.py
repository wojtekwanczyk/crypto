import baudot
import random

initial_config = 'ndvfjlagfkasdfawejhioahsrgjvfnfjlfgjlnvdfz'
random.seed(initial_config)
plaintext = "to jest tajny text"
plaintext = plaintext.upper()
ciphertext = ""


# define wheel sizes and their positions
k_wheels_size = [41, 31, 29, 26, 23]
k_pos = [0 ,0, 0, 0, 0]

s_wheels_size = [43, 47, 51, 53, 59]
s_pos = [0 ,0, 0, 0, 0]

m_wheels_size = [32, 45]
m_pos = [0 ,0]

# get initial state for all the wheels
def get_init_state(wheel_sizes):
    res = []
    for wh in wheel_sizes:
        wheel_config = []
        for i in range(0, wh):
            wheel_config.append(random.randint(0, 1))
        res.append(wheel_config)
    return res


k_wheels = get_init_state(k_wheels_size)
s_wheels = get_init_state(s_wheels_size)
m_wheels = get_init_state(m_wheels_size)

rotate_s = False
rotate_m2 = False
for letter in plaintext:

    # zawsze obracamy kola K
    for i, state in enumerate(k_pos):
        k_pos[i] = k_pos[i] + 1 % k_wheels_size[i]

    # zawsze obracamy m1
    m_pos[0] = m_pos[0] + 1 % m_wheels_size[0]

    # czy obracamy m2?
    m1_state = m_wheels[0][m_pos[0]]
    rotate_m2 = (m1_state == 1)
    if rotate_m2:
        m_pos[1] = m_pos[1] + 1 % m_wheels_size[1]
    
    # czy obracamy koła S?
    m2_state = m_wheels[1][m_pos[1]]
    rotate_s = (m1_state ^ m2_state)

    # jesli tak, to przechodzimy do czynu
    if rotate_s:
        for i, state in enumerate(s_pos):
            s_pos[i] = s_pos[i] + 1 % s_wheels_size[i]
    

    # szyfrujemy literke

    # najpierw konwertujemy na baudot
    baudot_letter = baudot.from_char[letter]

    # XOR z rotorami K
    letter_after_k = ""
    for i, bit in enumerate(baudot_letter):
        bit = int(bit)
        letter_after_k += str(bit ^ k_wheels[i][k_pos[i]])
    
    # XOR z rotorami S
    letter_after_s = ""
    for i, bit in enumerate(letter_after_k):
        bit = int(bit)
        letter_after_s += str(bit ^ s_wheels[i][s_pos[i]])

    # Convert letter and append it to ciphertext
    ciphered_letter = baudot.to_char[letter_after_s]
    ciphertext += ciphered_letter
    # print((letter, ciphered_letter))


print(ciphertext)
