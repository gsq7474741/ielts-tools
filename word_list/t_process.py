import os

if __name__ == '__main__':
    # for i in range(9):
    i = 12
    i -= 1
    prefix = 'c5t'
    buffer_list = []
    word_list = []

    r, c = 2, 4
    offset_length = r * c

    with open(f'{prefix}{i + 1}.csv', 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            else:
                buffer_list.append(line.strip())
        buffer_list = buffer_list[2:]
        for j in range((len(buffer_list) - 2) // offset_length + 1):
            for k in range(c):
                word_list.append({'word': buffer_list[j * offset_length + k],
                                  'chinese': buffer_list[j * offset_length + k + c * 1], })
    d = 3
    with open(f'{prefix}/{prefix}{i + 1}.merge.csv', 'w', encoding='utf-8') as f:
        f.write('word,chinese,alias\n')
        for word in word_list:
            f.write(f'{word["word"]},{word["chinese"]}\n')
        d = 3
