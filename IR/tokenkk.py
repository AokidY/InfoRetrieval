def tokenize(text):
    sub_str = ""
    token = []
    for word in text:
        if (word.isalnum() and word.isascii()):
            sub_str += word.lower()
        else:
            if (sub_str != ""):
                token.append(sub_str)
            sub_str = ""
    
    if (sub_str != ""):
        token.append(sub_str)

    return token

# print(tk('hello world! love you So much @'))

def computeWordFrequency(token):
    result = dict()
    for j in token:
        if j not in result:
            result[j] = 1
        else:
            result[j] += 1
    return result


def Print(frequency):
    frequency = sorted(frequency.items(), key=lambda x: (-x[1], x[0]))
    for i, j in frequency:
        print(i + '\t' + str(j))
