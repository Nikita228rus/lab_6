from pygost.gost34112012 import GOST34112012


class GOST34112012512(GOST34112012):
    def __init__(self, data=b''):
        super(GOST34112012512, self).__init__(data, digest_size=64)


def new(data=b''):
    return GOST34112012512(data)

s = '322'.encode('utf-8')
print(GOST34112012512.hexdigest(s))