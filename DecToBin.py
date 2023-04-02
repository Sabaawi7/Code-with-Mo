def DecToBin(n):
    BinNum = []
    if n >= 1:
        BinNum.append((n % 2))
        DecToBin(int(n / 2))
    print(BinNum)


DecToBin(20)
