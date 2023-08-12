import os

if __name__ == '__main__':
    left_list = []
    right_list = []

    flag = True
    with open('c5p1.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if flag:
                left_list.append(line.strip())
                flag = False
            else:
                right_list.append(line.strip())
                flag = True
    # last_top = -100
    # for w in res['words_result']:
    #     if abs(w['location']['top'] - last_top) < 20:
    #         right_list.append(w)
    #     else:
    #         left_list.append(w)
    #     last_top = w['location']['top']

    merge_list = left_list + right_list

    print(f'merge_list:{merge_list}')

    with open(f'word_list/{word_list_name}.txt', 'a', encoding='utf-8') as f:
        for w in res['words_result']:
            f.write(w['words'] + '\n')

    d = 3
