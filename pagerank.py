import pandas as pd
import json


# tutorial  http://www.cnblogs.com/fengfenggirl/p/pagerank-introduction.html
# author    lovejoy
# time      2016/12/27 16:12:00
def transfer_data(file_name):
    df = pd.read_csv(file_name, sep='\t', encoding='utf-8', header=None)
    dic = {}
    for index, row in df.iterrows():
        dic.setdefault(str(row[0]), []).append(str(row[1]))
    json_data = json.dumps(dic)
    json_file = open('relation.json', 'w')
    json_file.write(json_data)
    json_file.close()
    print('transfer dict to json success...')


def load_json():
    json_file = open('relation.json', 'r')
    d_dic = json.load(json_file)
    print('load dict from json success...')
    return d_dic


def initiate_pr(d_dic):
    i_dic = {}
    for key in d_dic.keys():
        for item in d_dic[key]:
            i_dic[item] = 0
    for key in d_dic.keys():
        i_dic[key] = 1 / len(d_dic)
    print('initiate probabilities success...')
    return i_dic


def mapper(d_dic, a_dic):
    m_dic = {}
    for key in a_dic.keys():
        m_dic[key] = 0
    for key in d_dic.keys():
        l = len(d_dic[key])
        for item in d_dic[key]:
            m_dic[item] += a_dic[key] / l
    print('mapper procedure success...')
    return m_dic


def reducer(m_dic, i_dic, a_dic):
    r_dic = {}
    for key in a_dic.keys():
        r_dic[key] = 0
    for key in m_dic.keys():
        r_dic[key] = a_dic[key] * m_dic[key] + (1 - a_dic[key]) * i_dic[key]
    print('reduce procedure success...')
    return r_dic


if __name__ == '__main__':
    data_dic = load_json()
    init_dic = initiate_pr(data_dic)
    actual_dic = init_dic
    count = 1
    print('in No.' + str(count) + ' iteration...')
    map_dic = mapper(data_dic, actual_dic)
    new_actual_dic = reducer(map_dic, init_dic, actual_dic)

    while new_actual_dic != actual_dic:
        count += 1
        print('in No.' + str(count) + ' iteration...')
        actual_dic = new_actual_dic
        map_dic = mapper(data_dic, actual_dic)
        new_actual_dic = reducer(map_dic, init_dic, actual_dic)
    print('page rank finish in ' + str(count) + ' iteration...')

    result_list = []
    for key in actual_dic.keys():
        result_list.append([key, actual_dic[key]])
    result_list.sort(key=lambda a: -a[1])

    result_file = open('result.txt', 'w')
    for item in result_list:
        result_file.write(str(item[0]) + '\t' + str(item[1]) + '\n')
    result_file.close()
    print('write result into result.txt success...')
