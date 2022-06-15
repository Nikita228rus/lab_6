from constants_SHA import *


def text_to_bin(text):
    return ''.join(format(x, '08b') for x in bytearray(text, 'utf-8'))


def logic_and(a, b):
    result = ''
    for i in range(len(a)):
        result += str(int(a[i]) & int(b[i]))
    return result


def logic_not(a):
    result = ''
    for i in range(len(a)):
        if int(a[i]) == 1:
            result += '0'
        elif int(a[i]) == 0:
            result += '1'
    return result


def x_change(k, a: str) -> str:
    out_list = []

    for i in range(len(k)):
        out_list.append(str(pow(int(k[i]) + int(a[i]), 1, 2)))

    return "".join(out_list)


def right_rows(row, x):
    for i in range(x):
        row = row[-1] + row[:len(row)-1]
    return row


def right(row, x):
    for i in range(x):
        row = '0' + row[:len(row)-1]
    return row


def Ch(x, y, z):
    return x_change(logic_and(x, y), logic_and(logic_not(x), z))


def Maj(x, y, z):
    return x_change(x_change(logic_and(x, y), logic_and(x, z)), logic_and(y, z))


def sig_0_256(x):
    return x_change(x_change(right_rows(x, 2), right_rows(x, 13)), right_rows(x, 22))


def sig_1_256(x):
    return x_change(x_change(right_rows(x, 6), right_rows(x, 11)), right_rows(x, 25))


def sigma_0_256(x):
    return x_change(x_change(right_rows(x, 7), right_rows(x, 18)), right(x, 3))


def sigma_1_256(x):
    return x_change(x_change(right_rows(x, 17), right_rows(x, 19)), right(x, 10))


def sig_0_512(x):
    return x_change(x_change(right_rows(x, 28), right_rows(x, 34)), right_rows(x, 39))


def sig_1_512(x):
    return x_change(x_change(right_rows(x, 14), right_rows(x, 18)), right_rows(x, 41))


def sigma_0_512(x):
    return x_change(x_change(right_rows(x, 1), right_rows(x, 8)), right(x, 7))


def sigma_1_512(x):
    return x_change(x_change(right_rows(x, 19), right_rows(x, 61)), right(x, 6))


def sha_256(M):

    l = len(M)
    M += "1" + ("0" * ((448 - l - 1) % 512)) + bin(l)[2:].zfill(64)

    M_l = [M[x:x + 512] for x in range(0, len(M), 512)]

    result = h_c_bin

    for j in range(len(M_l)):

        W = [(M_l[j][x:x + 32]) for x in range(0, 512, 32)]
        while len(W) != 64:
            W = W + ['00000000000000000000000000000000']

        for i in range(16, 64):
            s0 = sigma_0_256(W[i - 15])
            s1 = sigma_1_256(W[i - 2])
            W[i] = bin(pow(int(W[i - 16], 2) + int(s0, 2) + int(W[i - 7], 2) + int(s1, 2), 1, pow(2, 32)))[2:].zfill(32)

        a = result[0]
        b = result[1]
        c = result[2]
        d = result[3]
        e = result[4]
        f = result[5]
        g = result[6]
        h = result[7]

        for t in range(64):
            T1 = pow(int(h, 2) + int(sig_1_256(e), 2) + int(Ch(e, f, g), 2) + int(k_c_bin[t], 2) + int(W[t], 2), 1, pow(2, 32))
            T2 = pow(int(sig_0_256(a), 2) + int(Maj(a, b, c), 2), 1, pow(2, 32))
            h = g
            g = f
            f = e
            e = bin(pow(int(d, 2) + T1, 1, pow(2, 32)))[2:].zfill(32)
            d = c
            c = b
            b = a
            a = bin(pow(T1 + T2, 1, pow(2, 32)))[2:].zfill(32)

        result[0] = bin(pow(int(result[0], 2) + int(a, 2), 1, pow(2, 32)))[2:].zfill(32)
        result[1] = bin(pow(int(result[1], 2) + int(b, 2), 1, pow(2, 32)))[2:].zfill(32)
        result[2] = bin(pow(int(result[2], 2) + int(c, 2), 1, pow(2, 32)))[2:].zfill(32)
        result[3] = bin(pow(int(result[3], 2) + int(d, 2), 1, pow(2, 32)))[2:].zfill(32)
        result[4] = bin(pow(int(result[4], 2) + int(e, 2), 1, pow(2, 32)))[2:].zfill(32)
        result[5] = bin(pow(int(result[5], 2) + int(f, 2), 1, pow(2, 32)))[2:].zfill(32)
        result[6] = bin(pow(int(result[6], 2) + int(g, 2), 1, pow(2, 32)))[2:].zfill(32)
        result[7] = bin(pow(int(result[7], 2) + int(h, 2), 1, pow(2, 32)))[2:].zfill(32)

    for i in range(len(result)):
        result[i] = hex(int(result[i], 2))[2:]
        result[i] = '0' * (8 - len(result[i])) + result[i]

    return ''.join(result)


def sha_512(M):
    l = len(M)
    M += "1" + ("0" * ((896 - l - 1) % 1024)) + bin(l)[2:].zfill(128)

    M_l = [M[x:x + 1024] for x in range(0, len(M), 1024)]

    result = h_c_512

    for j in range(len(M_l)):

        W = [(M_l[j][x:x + 64]) for x in range(0, 1024, 64)]
        while len(W) != 80:
            W = W + ['0' * 64]

        for i in range(16, 80):
            s0 = sigma_0_512(W[i - 15])
            s1 = sigma_1_512(W[i - 2])
            W[i] = bin(pow(int(W[i - 16], 2) + int(s0, 2) + int(W[i - 7], 2) + int(s1, 2), 1, pow(2, 64)))[2:].zfill(64)

        a = result[0]
        b = result[1]
        c = result[2]
        d = result[3]
        e = result[4]
        f = result[5]
        g = result[6]
        h = result[7]

        for t in range(80):
            T1 = pow(int(h, 2) + int(sig_1_512(e), 2) + int(Ch(e, f, g), 2) + int(k_c_512_bin[t], 2) + int(W[t], 2), 1, pow(2, 64))
            T2 = pow(int(sig_0_512(a), 2) + int(Maj(a, b, c), 2), 1, pow(2, 64))
            h = g
            g = f
            f = e
            e = bin(pow(int(d, 2) + T1, 1, pow(2, 64)))[2:].zfill(64)
            d = c
            c = b
            b = a
            a = bin(pow(T1 + T2, 1, pow(2, 64)))[2:].zfill(64)

        result[0] = bin(pow(int(result[0], 2) + int(a, 2), 1, pow(2, 64)))[2:].zfill(64)
        result[1] = bin(pow(int(result[1], 2) + int(b, 2), 1, pow(2, 64)))[2:].zfill(64)
        result[2] = bin(pow(int(result[2], 2) + int(c, 2), 1, pow(2, 64)))[2:].zfill(64)
        result[3] = bin(pow(int(result[3], 2) + int(d, 2), 1, pow(2, 64)))[2:].zfill(64)
        result[4] = bin(pow(int(result[4], 2) + int(e, 2), 1, pow(2, 64)))[2:].zfill(64)
        result[5] = bin(pow(int(result[5], 2) + int(f, 2), 1, pow(2, 64)))[2:].zfill(64)
        result[6] = bin(pow(int(result[6], 2) + int(g, 2), 1, pow(2, 64)))[2:].zfill(64)
        result[7] = bin(pow(int(result[7], 2) + int(h, 2), 1, pow(2, 64)))[2:].zfill(64)

    for i in range(len(result)):
        result[i] = hex(int(result[i], 2))[2:]
        result[i] = '0' * (8 - len(result[i])) + result[i]

    return ''.join(result)
