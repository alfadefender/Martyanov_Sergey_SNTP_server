LOCAL_SNTP_SERVER = 'localhost'
GOOGLE_SNTP_SERVER = 'time.google.com'

def to_binary(num):
    string = ""

    while num:
        string += str(num % 2)
        num //= 2

    return "0" * (8 - len(string)) + string[::-1]

def to_hex_list(num):
    temp = hex(num)[2:]
    temp = "0" * (8 - len(temp)) + temp
    result = []
    for i in range(0, len(temp), 2):
        cur = int(temp[i] + temp[i + 1], 16)
        result += [cur]

    return result