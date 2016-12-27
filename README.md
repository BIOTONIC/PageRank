# DataMining PageRank Howework
- 这次的作业我用Python完成的，主要参考了这篇文章[PageRank算法简介及Map-Reduce实现](http://www.cnblogs.com/fengfenggirl/p/pagerank-introduction.html)
- 我就结合代码说一下具体实现吧

``` python
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
```
- 一开始我要做的是从relation.txt中读取关系网络，存到dict中。但在后来写完运行的时候，我发现读取部分占用了很大的时间。于是我把读取到的dict转成了json格式，并存储到了本地的json.json文件中了。事实证明这样做的确节省了很多时间：读取40+M的json文件也就耗费几秒钟吧，而直接读取原文件并转成DafaFrame要花费几分钟。

``` python
def load_json():
    json_file = open('relation.json', 'r')
    d_dic = json.load(json_file)
    print('load dict from json success...')
    return d_dic
```
- 这就是从json文件中读取数据并转成dict格式，之后的数据操作我都采用了dict格式，应为在大规模数据查找的时候，dict效率比list更高。

``` python
def initiate_pr(d_dic):
    i_dic = {}
    for key in d_dic.keys():
        for item in d_dic[key]:
            i_dic[item] = 0
    for key in d_dic.keys():
        i_dic[key] = 1 / len(d_dic)
    print('initiate probabilities success...')
    return i_dic
```
- 这一步是初始化每个节点的平均概率，值得一提的是我遍历了d_dic（data_dict）的key和value，确保那些即使关注0个用户（也就是key里没有出现，只在value里出现）的人群也能成为i_dic(initiate_dict)的key。

``` python
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
```
- 这是PageRank的MapReduce的Mapper和Reduce阶段，具体细节可以看上面的链接。

``` python
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
```
- 最后面是我的主函数，先加载json数据，然后初始化init_dic, 之后就循环使用mapper()和reducer()函数，直到前后两次结果一直，那么认为此时收敛，迭代结束。

```
load dict from json success...
initiate probabilities success...
in No.1 iteration...
mapper procedure success...
reduce procedure success...
in No.2 iteration...
mapper procedure success...
reduce procedure success...
in No.3 iteration...
mapper procedure success...
reduce procedure success...
in No.4 iteration...
mapper procedure success...
reduce procedure success...
in No.5 iteration...
mapper procedure success...
reduce procedure success...
in No.6 iteration...
mapper procedure success...
reduce procedure success...
in No.7 iteration...
mapper procedure success...
reduce procedure success...
in No.8 iteration...
mapper procedure success...
reduce procedure success...
page rank finish in 8 iteration...
write result into result.txt success...
```
- 这是我控制台的输出，可以看到8次迭代就收敛了。迭代次数着么少，是因为我之前把权重由float变成了str了，精度上有一定损失，但是迭代次数少了好多（另一个同学的迭代次数大概是一百多）。
- 之后就是转成list，把结果存储到result.txt中，结果在下面，太长了，我就列出前面的吧
```
1192329374  1.426081539562061e-06
1266321801  1.42540594316526e-06
1223762662  1.4241205384022555e-06
1182391231  1.423644570573122e-06
1644395354  1.4231646288784073e-06
1821898647  1.4227095226868863e-06
1197161814  1.4224087023614488e-06
1713926427  1.422390344336367e-06
2115302210  1.4217596504133305e-06
1618051664  1.4214638064824772e-06
1780417033  1.4213685318336237e-06
1193491727  1.421221953723955e-06
1097201945  1.4207977932371488e-06
1638782947  1.4207234148789125e-06
1182389073  1.4206757474951787e-06
1275017594  1.4206647005497293e-06
1615743184  1.4205762576616788e-06
1660612723  1.420570226006897e-06
1362607654  1.4205700174856827e-06
1252373132  1.4203826485050683e-06
1644572034  1.4203727536946893e-06
1757353251  1.4203646180302994e-06
1642482194  1.420289246044347e-06
1813080181  1.420240596833434e-06
```
- 前面几个用户依次是谢娜、姚晨、林心如、潘石屹、冷笑话精选（什么鬼），和其他同学结果还是一致的。
