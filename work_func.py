from constant import *


def text_bin(s: str) -> str:
    return "".join(f"{ord(i):08b}" for i in s)


def text_to_bin(text):
    return ''.join(format(x, '08b') for x in bytearray(text, 'utf-8'))


def bin_hex(s: str) -> str:
    s1 = ""
    for i in [s[x:x + 8] for x in range(0, len(s), 8)]:
        s1 += hex(int(i, 2))[2:].zfill(2)
    return s1


def hex_bin(hex_s: str) -> str:
    mp = [hex_s[i:i + 2] for i in range(0, len(hex_s), 2)]
    bin_s = ""
    for i in mp:
        mp_bin = bin(int(i, 16))[2:]
        while len(mp_bin) % 8 != 0:
            mp_bin = "0" + mp_bin
        bin_s += mp_bin

    return bin_s


def x_change(k, a: str) -> str: #XOR
    out_list = []

    for i in range(len(k)):
        out_list.append(str(pow(int(k[i]) + int(a[i]), 1, 2)))

    return "".join(out_list)


def S(I: str) -> list: #подстановка по индексу
    I_list = []

    for i in range(512):

        if i % 8 == 0:
            c = int(I[i:i + 8], 2)
            var = pi_bin[c]
            I_list.append(var)

        I_str = "".join(I_list)
    return I_list


def P(I: list) -> str:
    I_list = [0] * 64
    for i in range(64):
        I_list[i] = I[tau[i]]

    return "".join(I_list)


def L(I: str) -> str:
    b = []
    for i in range(512):
        if i % 64 == 0:
            c = I[i:i + 64]
            b.append(c)
    return b


def l(b: list):
    B_list = []
    B_str = ""

    for i in range(8):
        B = "0" * 64

        for j in range(64):
            if int(b[i][j]) == 1:
                B_str = hex_bin(matrix_A[j])

            elif int(b[i][j]) == 0:
                B_str = "0" * 64

            B = x_change(B, B_str)
        B_list.append(B)

    return "".join(B_list)


def E(K, m):
    state = x_change(K, m)
    for i in range(len(C)):
        state = l(L(P(S(state))))
        K = KeySchedule(K, i)
        state = x_change(state, K)
    return state


def KeySchedule(K, i):
    K = l(L(P(S(x_change(K, hex_bin(C[i]))))))
    return K


def g_change(N, m, h: str) -> str:
    K = l(L(P(S(x_change(h, N)))))
    t = E(K, m)
    t = x_change(h, t)
    G = x_change(t, m)
    return G


def stribog_256_512(M, flag) -> str:
    m = M
    N = "0" * 512
    Sig = "0" * 512

    if flag == 1:
        IV = "0" * 512
        h = IV

    elif flag == 2:

        IV = "00000001" * 64
        h = IV

    while len(M) >= 512:
        m = M[len(M) - 512:]
        h = g_change(N, m, h)
        N = format(pow(int(N, 2) + 512, 1, pow(2, 512)), "0b")
        while len(N) != 512:
            N = "0" + N

        Sig = format(pow(int(Sig, 2) + int(m, 2), 1, pow(2, 512)), "0b")
        while len(Sig) != 512:
            Sig = "0" + Sig

        M = M[:len(M) - 512]

    if len(M) < 512:
        m = M
        m = "1" + m
        while len(m) != 512:
            m = "0" + m

        h = g_change(N, m, h)

        N = format(pow(int(N, 2) + len(M), 1, pow(2, 512)), "0b")
        while len(N) != 512:
            N = "0" + N

        Sig = format(pow(int(Sig, 2) + int(m, 2), 1, pow(2, 512)), "0b")
        while len(Sig) != 512:
            Sig = "0" + Sig

        Nol = "0" * 512
        h = g_change(Nol, N, h)
        h = g_change(Nol, Sig, h)

        if flag == 1:
            return reverse(bin_hex(h))
        elif flag == 2:
            h = h[:256]
            return reverse(bin_hex(h))


def test_stribog_gost():
    m1 = '323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130'
    m1 = hex_bin(m1)
    m2 = 'fbe2e5f0eee3c820fbeafaebef20fffbf0e1e0f0f520e0ed20e8ece0ebe5f0f2f120fff0eeec20f120faf2fee5e2202ce8f6f3ede220e8e6eee1e8f0f2d1202ce8f0f2e5e220e5d1'
    m2 = hex_bin(m2)
    test1_1 = '486f64c1917879417fef082b3381a4e211c324f074654c38823a7b76f830ad00fa1fbae42b1285c0352f227524bc9ab16254288dd6863dccd5b9f54a1ad0541b'
    test1_2 = '00557be5e584fd52a449b16b0251d05d27f94ab76cbaa6da890b59d8ef1e159d'
    test2_1 = '28fbc9bada033b1460642bdcddb90c3fb3e56c497ccd0f62b8a2ad4935e85f037613966de4ee00531ae60f3b5a47f8dae06915d5f2f194996fcabf2622e6881e'
    test2_2 = '508f7e553c06501d749a66fc28c6cac0b005746d97537fa85d9e40904efed29d'
    print(stribog_256_512(m1, 1) == test1_1, stribog_256_512(m1, 2) == test1_2, stribog_256_512(m2, 1) == test2_1, stribog_256_512(m2, 2) == test2_2, sep='\n')


from pygost.gost34112012 import GOST34112012
def test_pygost(message):
    class GOST34112012512(GOST34112012):
        def __init__(self, data=b''):
            super(GOST34112012512, self).__init__(data, digest_size=64)

    def new(data=b''):
        return GOST34112012512(data)

    m = new(message)
    print(GOST34112012512.hexdigest(m))


def text_to_hex(text):
    result = ''
    for i in range(len(text)):
        if i % 4 == 0:
            result += hex(int(text[i:i+4], 2))[2:]

    return result


def reverse(text):
    temp_len = []
    result = ''
    for i in range(len(text)):
        if i % 2 == 0:
            temp_len.append(text[i:i+2])

    for i in range(len(temp_len)):
        result += temp_len[-1 - i]
    return result
