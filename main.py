import random
from conf_SHA import *
from constants_SHA import *
from work_func import *
import time


def menu_sha():
    case = input('1 - ввод из консоли\n2 - чтение из файла\n>>>\t')
    if case == '1':
        massive = input('Введите текст:\t')

    elif case == '2':
        with open("input.txt", "r") as file:
            massive = file.read()

    massive = text_to_bin(massive)

    choose = input('Выбор свертки\n256 - 1\n512 - 2\n>>>\t')
    if choose == '1':
        final = sha_256(massive)
        with open("output.txt", "a", encoding='utf-8') as file:
            file.write('256: {}\ntime:\t{}\n\n'.format(final, time.asctime()))

    elif choose == '2':
        final = sha_512(massive)
        with open("output.txt", "a", encoding='utf-8') as file:
            file.write('512: {}\ntime:\t{}\n\n'.format(final, time.asctime()))


def menu_pygost():

    case = input('1 - ввод из консоли\n2 - чтение из файла\n>>>\t')
    if case == '1':
        massive = input('Введите текст:\t')

    elif case == '2':
        with open("input.txt", "r") as file:
            massive = file.read()

    massive = hex_bin(reverse(text_to_hex(text_to_bin(massive))))

    choose = input('Выбор свертки\n512 - 1\n256 - 2\n>>>\t')
    if choose == '1':
        final = stribog_256_512(massive, 1)
        with open("output.txt", "a", encoding='utf-8') as file:
            file.write('512: {}\ntime:\t{}\n\n'.format(final, time.asctime()))

        return final

    elif choose == '2':
        final = stribog_256_512(massive, 2)
        with open("output.txt", "a", encoding='utf-8') as file:
            file.write('256: {}\ntime:\t{}\n\n'.format(final, time.asctime()))

        return final


def create_key():
    size = random.randint(1, 64)
    list_key = []
    for i in range(size):
        list_key.append(random.randint(1, 255))

    return list_key


def hmac(message, flag, h_func):
    ipad = int('00110110', 2)
    opad = int('01011100', 2)


    massive = text_to_bin(message)
    if h_func == 'GOST':
        massive = hex_bin(reverse(text_to_hex(massive)))

    key = create_key()
    key_1 = key.copy()
    key_2 = key.copy()

    while len(key_1) != flag:
        key_1.append(0)

    for i in range(len(key_1)):
        key_1[i] = bin(key_1[i] ^ ipad)[2:].zfill(8)

    key_1_bin = ''.join(key_1)

    massive = key_1_bin + massive

    while len(key_2) != flag:
        key_2.append(0)

    for i in range(len(key_2)):
        key_2[i] = bin(key_2[i] ^ opad)[2:].zfill(8)

    key_2_bin = ''.join(key_2)

    if h_func == 'GOST':
        result = stribog_256_512(key_2_bin + hex_bin(stribog_256_512(massive, 1)), 1)
        print(result)
        open('output.txt', 'w', encoding='utf-8').write(result)

    elif h_func == 'SHA':

        if flag == 64:
            result = sha_256(key_2_bin + hex_bin(sha_256(massive)))
            print(result)
            open('output.txt', 'w', encoding='utf-8').write(result)

        elif flag == 128:
            result = sha_512(key_2_bin + hex_bin(sha_512(massive)))
            print(result)
            open('output.txt', 'w', encoding='utf-8').write(result)


def menu():

    case = input('keyboard - 1\nfile - 2\n>>>\t')
    if case == '1':
        s = input('massage:\t')

    elif case == '2':
        s = open('input.txt', 'r', encoding='utf-8').read()

    choose = input('Choose size block:\n1 - 512\n2 - 1024\n>>>\t')
    if choose == '1':
        flag = 64

        hash_func = input('1 - GOST\n2 - SHA\n>>>\t')

        if hash_func == '1':
            h = 'GOST'
            hmac(s, 64, h)

        elif hash_func == '2':
            h = 'SHA'
            hmac(s, 64, h)

    elif choose == '2':
        flag = 128
        h = 'SHA'
        hmac(s, 128, h)


menu()