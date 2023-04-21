#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/4/20 22:05
# @Author  : Benjamin

# 导入包
import json
import random
import math

from sklearn.model_selection import train_test_split
from tqdm import tqdm

class AGRM():

    def __init__(self, fp, data, user_recs, train, test, train_ex, test_ex, long, item_user, user50_test,wait_user, getRecommendation, sorted_user_sim):
        self.fp = fp
        self.data = data
        self.train = train
        self.test = test
        self.train_ex = train_ex
        self.test_ex = test_ex
        self.long = long
        self.item_user = item_user
        self.user50_test = user50_test
        self.wait_user = wait_user
        self.getRecommendation = getRecommendation
        self.sorted_user_sim = sorted_user_sim
        self.user_recs = user_recs

    def run(self,user):
        user_sim = self.sorted_user_sim[user]
        usesimlist = []
        for i in range(0, len(user_sim)):  # 从相似用户中随机挑选20个
            num = user_sim[i]
            use_key = num[0]
            usesimlist.append(use_key)

        # 定义目标函数Lat
        def function1(usergroup):
            recs = getRec(user, self.getRecommendation, usergroup)
            value = 0
            for item, score in recs:
                if item in self.long:
                    value += score * 2
                else:
                    value += score ** 0.5
            return -round(value, 3)

        # 定义目标函数Pop
        def function2(usergroup):
            recs = getRec(user, self.getRecommendation, usergroup)
            pop = 0
            for item, score in recs:
                if item in self.item_user:
                    if item in self.long:
                        pop += math.log(1 + len(self.item_user[item])) ** 0.5
                    else:
                        pop += (math.log(1 + len(self.item_user[item]))) ** 2  # 放大热门物品的流行度

            return round(pop, 3)

        # 查找列表指定元素的索引
        def index_of(a, list):
            for i in range(0, len(list)):
                if list[i] == a:
                    return i
            return -1

        # 函数根据指定的值列表排序
        def sort_by_values(list1, values):
            sorted_list = []
            while (len(sorted_list) != len(list1)):
                # 当结果长度不等于初始长度时，继续循环
                if index_of(min(values), values) in list1:
                    # 标定值中最小值在目标列表中时
                    sorted_list.append(index_of(min(values), values))
                #     将标定值的最小值的索引追加到结果列表后面
                values[index_of(min(values), values)] = math.inf
            #      将标定值的最小值置为无穷小,即删除原来的最小值,移向下一个
            #     infinited
            return sorted_list

        # 函数执行NSGA-II的快速非支配排序,将所有的个体都分层
        def fast_non_dominated_sort(values1, values2):
            S = [[] for i in range(0, len(values1))]
            # 种群中所有个体的sp进行初始化 这里的len(value1)=pop_size
            front = [[]]
            # 分层集合,二维列表中包含第n个层中,有那些个体
            n = [0 for i in range(0, len(values1))]
            rank = [0 for i in range(0, len(values1))]
            # 评级
            for p in range(0, len(values1)):
                S[p] = []
                n[p] = 0
                # 寻找第p个个体和其他个体的支配关系
                # 将第p个个体的sp和np初始化
                for q in range(0, len(values1)):
                    # step2:p > q 即如果p支配q,则
                    if (values1[p] > values1[q] and values2[p] > values2[q]) or (
                            values1[p] >= values1[q] and values2[p] > values2[q]) or (
                            values1[p] > values1[q] and values2[p] >= values2[q]):
                        # 支配判定条件:当且仅当,对于任取i属于{1,2},都有fi(p)>fi(q),符合支配.或者当且仅当对于任意i属于{1,2},有fi(p)>=fi(q),且至少存在一个j使得fj(p)>f(q)  符合弱支配
                        if q not in S[p]:
                            # 同时如果q不属于sp将其添加到sp中
                            S[p].append(q)
                    # 如果q支配p
                    elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
                            values1[q] >= values1[p] and values2[q] > values2[p]) or (
                            values1[q] > values1[p] and values2[q] >= values2[p]):
                        # 则将np+1
                        n[p] = n[p] + 1
                if n[p] == 0:
                    # 找出种群中np=0的个体
                    rank[p] = 0
                    # 将其从pt中移去
                    if p not in front[0]:
                        # 如果p不在第0层中
                        # 将其追加到第0层中
                        front[0].append(p)

            i = 0
            while (front[i] != []):
                # 如果分层集合为不为空，
                Q = []
                for p in front[i]:
                    for q in S[p]:
                        n[q] = n[q] - 1
                        # 则将fk中所有给对应的个体np-1
                        if (n[q] == 0):
                            # 如果nq==0
                            rank[q] = i + 1

                            if q not in Q:
                                Q.append(q)
                i = i + 1
                # 并且k+1
                front.append(Q)

            del front[len(front) - 1]
            # print(front)
            return front
            # 返回将所有个体分层后的结果

        # 计算拥挤距离的函数

        def crowding_distance(values1, values2, front):
            distance = [0 for i in range(0, len(front))]
            # 初始化个体间的拥挤距离
            sorted1 = sort_by_values(front, values1[:])
            sorted2 = sort_by_values(front, values2[:])
            # 基于目标函数1和目标函数2对已经划分好层级的种群排序
            distance[0] = 4444444444444444
            distance[len(front) - 1] = 4444444444444444
            for k in range(1, len(front) - 1):
                distance[k] = distance[k] + (values1[sorted1[k + 1]] - values2[sorted1[k - 1]]) / (
                        max(values1) - min(values1))
            for k in range(1, len(front) - 1):
                distance[k] = distance[k] + (values1[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (
                        max(values2) - min(values2))
            return distance

        # 返回拥挤距离

        # 函数进行交叉
        def crossover(a, b):
            r = random.random()
            List1, List2 = [], []
            length = int(len(a) / 2)
            List1 = a[:length] + b[length:]
            List2 = a[length:] + b[:length]
            if r > 0.5:
                return mutation(List1)
            else:
                return mutation(List2)

        # 函数进行变异操作
        def mutation(solution):
            mutation_prob = random.random()
            List = solution
            if mutation_prob < 1:
                i = random.randint(0, 19)
                user = random.choice(usesimlist)
                if user not in List:
                    List[i] = user
            solution = List
            return solution

        pop_size = 20  # 种群规模
        max_gen = 50
        # 迭代次数
        solution = []
        for i in range(0, pop_size):
            solution.append(usesimlist[i * 20:(i + 1) * 20])  # 20个随机用户作为种群个体

        # 随机生成变量
        gen_no = 0

        while (gen_no < max_gen):
            function1_values = [function1(solution[i]) for i in range(0, pop_size)]
            function2_values = [function2(solution[i]) for i in range(0, pop_size)]
            # 生成两个函数值列表，构成一个种群
            non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])
            crowding_distance_values = []
            # 计算非支配集合中每个个体的拥挤度
            for i in range(0, len(non_dominated_sorted_solution)):
                crowding_distance_values.append(
                    crowding_distance(function1_values[:], function2_values[:], non_dominated_sorted_solution[i][:]))
            solution2 = solution[:]

            # 生成了子代
            while (len(solution2) != 2 * pop_size):
                a1 = random.randint(0, pop_size - 1)
                b1 = random.randint(0, pop_size - 1)
                # 选择
                solution2.append(crossover(solution[a1], solution[b1]))
                # 随机选择，将种群中的个体进行交配，得到子代种群2*pop_size

            function1_values2 = [function1(solution2[i]) for i in range(0, 2 * pop_size)]
            function2_values2 = [function2(solution2[i]) for i in range(0, 2 * pop_size)]
            non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:], function2_values2[:])
            # 将两个目标函数得到的两个种群值value,再进行排序 得到2*pop_size解
            crowding_distance_values2 = []
            for i in range(0, len(non_dominated_sorted_solution2)):
                crowding_distance_values2.append(
                    crowding_distance(function1_values2[:], function2_values2[:], non_dominated_sorted_solution2[i][:]))
            # 计算子代的个体间的距离值
            new_solution = []
            for i in range(0, len(non_dominated_sorted_solution2)):
                non_dominated_sorted_solution2_1 = [
                    index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
                    range(0, len(non_dominated_sorted_solution2[i]))]
                # 排序
                front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
                front = [non_dominated_sorted_solution2[i][front22[j]] for j in
                         range(0, len(non_dominated_sorted_solution2[i]))]
                front.reverse()
                for value in front:
                    new_solution.append(value)
                    if (len(new_solution) == pop_size):
                        break
                if (len(new_solution) == pop_size):
                    break
            solution = [solution2[i] for i in new_solution]
            gen_no = gen_no + 1

        Best_user_group = solution[0]
        getrecs = getRec(user, self.getRecommendation, Best_user_group)
        return getrecs

    # 定义精确率指标计算方式
    def precision(self):
        all, hit = 0, 0
        for user in self.wait_user:
            test_items = set(self.test[user])
            test_items_ex = set(self.test_ex[user])
            last = (test_items_ex | test_items)
            rank = self.user_recs[user]
            for item, score in rank:
                if item in last:
                    hit += 1
            all += len(rank)
        return round(hit / all * 100, 2)

    # 定义覆盖率指标计算方式
    def coverage(self):
        all_item, recom_item = set(), set()
        cnt = 0
        for user in self.wait_user:
            test_items = set(self.train[user])
            for item in test_items:
                all_item.add(item)
            rank = self.user_recs[user]
            for item, score in rank:
                if item in self.long:
                    cnt += 1
                recom_item.add(item)
        return round(len(recom_item) / len(all_item) * 100, 2)

    # 定义新颖度指标计算方式
    def popularity(self):
        # 计算物品的流行度
        item_pop = {}
        for user in self.train:
            for item in self.train[user]:
                if item not in item_pop:
                    item_pop[item] = 0
                item_pop[item] += 1

        num, pop = 0, 0
        for user in self.wait_user:
            rank = self.user_recs[user]
            for item, score in rank:
                # 取对数，防止因长尾问题带来的被流行物品所主导
                if item in item_pop:
                    pop += math.log(1 + item_pop[item])
                else:
                    pop += 0
                num += 1
        return round(pop / num, 6)

# 读取数据集
def loadData(fp):
    data = []
    for l in open(fp):
        data.append(tuple(map(int, l.strip().split('::')[:2])))
    return data

# 处理成字典的形式，user->set(items)
def convert_dict(data):
    data_dict = {}
    for user, item in data:
        if user not in data_dict:
            data_dict[user] = set()
        data_dict[user].add(item)
    data_dict = {k: list(data_dict[k]) for k in data_dict}
    return data_dict

#处理数据集
def splitData(data):
    '''
    :params: data, 加载的所有(user, item)数据条目
    :params: seed, random的种子数，对于不同的k应设置成一样的
    :return: train, test
    '''
    train, test = [], []

    # 将原始数据处理成(user, item)格式
    All = []
    for user, item in data:
        All.append((user, item))

    # 计算user->item索引用来提取1000个用户
    user1000_item = {}
    user_All = convert_dict(All)
    for user in user_All:
        user1000_item[user] = len(user_All[user])

    # user50_test = list(sorted(user1000_item.items(), key=lambda x: x[1],reverse=True))[900:1000]
    user50_test = list(sorted(user1000_item.items(), key=lambda x: x[1],reverse=True))[2400: 2500]
    user50_test = convert_dict(user50_test)
    # user1000_item = list(sorted(user1000_item.items(), key=lambda x: x[1],reverse=True))[:1000]
    user1000_item = list(sorted(user1000_item.items(), key=lambda x: x[1], reverse=True))[1500:2500]
    user1000_item = convert_dict(user1000_item)
    All1000 = []
    for user,item in data:
        if user in user1000_item:
            All1000.append((user,item))

    # 计算item->user的倒排索引
    item_users = {}
    item_count = 0  # 统计物品出现的次数
    count = 0
    for user, item in All1000:
        if item not in item_users:
            item_users[item] = set()
        item_users[item].add(user)
        item_count += len(item_users[item])
        count += 1

    # 按照出现次数，取低于均值的为长尾
    mean = item_count / count
    long_tail = {}
    for item in item_users.keys():
        if (len(item_users[item]) < mean):
            if item not in long_tail:
                long_tail[item] = ""
            long_tail[item] = "Long_tail"
    #
    train, test = train_test_split(All1000, train_size=0.7, random_state=0)

    # 替换函数
    def exc_data(data):
        train_ex = convert_dict(data)  # 定义替换的数据集
        ex_radio = 0.5 # 定义长尾比例（替换比例）
        eex = {}
        for user in train_ex:
            count_hot, count_long = 0, 0
            ex = []
            for item in train_ex[user]:
                if item in long_tail:
                    count_long += 1
                else:
                    count_hot += 1
            if(count_long!=0):
                ex_radio = 0.5+0.5-math.pow(0.5,count_hot*0.5/count_long)
            else:
                ex_radio = 0.5+0.5-math.pow(0.5,count_hot*0.5)
            count_hot, count_long = 0, 0
            for item in train_ex[user]:
                if item in long_tail:  # 如果是热门物品就选择替换
                    ex.append(item)
                else:
                    if (count_hot + count_long) / len(train_ex[user]) <= ex_radio:  # 替换数满足比例时停止替换
                        a = random.sample(long_tail.keys(), 1)
                        if a[0] not in train_ex[user]:
                            ex.append(a[0])
                    else:
                        ex.append(item)

                    count_hot += 1
            eex[user] = ex

        return eex

    train_ex = exc_data(train)
    test_ex = exc_data(test)
    train = convert_dict(train)
    test = convert_dict(test)
    test_ex = dict(sorted(test_ex.items(), key=lambda x: x[0]))
    train_ex = dict(sorted(train_ex.items(), key=lambda x: x[0]))
    test = dict(sorted(test.items(), key=lambda x: x[0]))
    train = dict(sorted(train.items(), key=lambda x: x[0]))

    return train, test, train_ex, test_ex, long_tail, item_users, user50_test

# 3. 基于用户余弦相似度的推荐
def UserCF(train, train_ex, N):
    '''
    :params: train, 训练数据集
    :params: K, 超参数，设置取TopK相似用户数目
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation, 推荐接口函数
    '''
    def make_sim(data):
        # 计算item->user的倒排索引
        item_users = {}
        for user in data:
            for item in data[user]:
                if item not in item_users:
                    item_users[item] = []
                item_users[item].append(user)

        # 计算用户相似度矩阵
        sim = {}
        num = {}
        for item in item_users:
            users = item_users[item]
            for i in range(len(users)):
                u = users[i]
                if u not in num:
                    num[u] = 0
                num[u] += 1
                if u not in sim:
                    sim[u] = {}
                for j in range(len(users)):
                    if j == i: continue
                    v = users[j]
                    if v not in sim[u]:
                        sim[u][v] = 0
                    sim[u][v] += 1 / math.log(1 + len(users))


        for u in sim:
            for v in data:
                if v in sim[u]:
                    sim[u][v] /= math.sqrt(num[u] * num[v])
                else:
                    sim[u][v] = 0
        return sim

    simold = make_sim(train)        #初始相似度 sima
    simex = make_sim(train_ex)      #替换后相似度 simb

    sorted_sim = {}
    for user in train:
        Sim_count = {}
        for v, x in simold[user].items():
            if v in simex[user].keys():
                y = simex[user].get(v)
                degree = math.atan2(y, x) / (math.pi / 180)
                if degree < 90 and degree > 0:  # 判断变化幅度
                    Sim_count[v] = math.sqrt((x ** 2) + (y ** 2))  # 计算相似距离
        sorted_sim[user] = Sim_count

    # 按照相似度排序
    sorted_simuser = {k: list(sorted(v.items(), \
                                      key=lambda x: x[1], reverse=True)) \
                       for k, v in sorted_sim.items()}
    # 按照相似度排序
    sorted_sim = {k: dict(sorted(v.items(), \
                                      key=lambda x: x[1], reverse=True)) \
                       for k, v in sorted_sim.items()}

    # 获取接口函数
    def GetRecommendation(user, sorted_simu):
        items = {}
        seen_items = set(train[user])
        for u in sorted_simu:
            train_items = set(train[u])
            train_items_ex = set(train_ex[u])
            last = (train_items|train_items_ex)
            for item in last:
                # 要去掉用户见过的
                if item not in seen_items:
                    if item not in items:
                        items[item] = 0
                    items[item] += sorted_sim[user][u]

        recs = list(sorted(items.items(), key=lambda x: x[1], reverse=True))[:N]

        return recs

    return GetRecommendation, sorted_simuser

def getRec(user, GetRecommendation, user_sim):  #获取用户推荐列表

    rank = GetRecommendation(user, user_sim)
    return rank

# def run(user):
#     user_sim = sorted_user_sim[user]
#     usesimlist = []
#     for i in range(0, len(user_sim)):  # 从相似用户中随机挑选20个
#         num = user_sim[i]
#         use_key = num[0]
#         usesimlist.append(use_key)
#
#     # 定义目标函数Lat
#     def function1(usergroup):
#         recs = getRec(user, getRecommendation, usergroup)
#         value = 0
#         for item, score in recs:
#             if item in long:
#                 value += score*2
#             else:
#                 value += score**0.5
#         return -round(value, 3)
#
#     # 定义目标函数Pop
#     def function2(usergroup):
#         recs = getRec(user, getRecommendation, usergroup)
#         pop = 0
#         for item, score in recs:
#             if item in item_user:
#                 if item in long:
#                     pop += math.log(1 + len(item_user[item]))**0.5
#                 else:
#                     pop += (math.log(1 + len(item_user[item]))) ** 2  # 放大热门物品的流行度
#
#         return round(pop, 3)
#
#     # 查找列表指定元素的索引
#     def index_of(a, list):
#         for i in range(0, len(list)):
#             if list[i] == a:
#                 return i
#         return -1
#
#     # 函数根据指定的值列表排序
#     def sort_by_values(list1, values):
#         sorted_list = []
#         while (len(sorted_list) != len(list1)):
#             # 当结果长度不等于初始长度时，继续循环
#             if index_of(min(values), values) in list1:
#                 # 标定值中最小值在目标列表中时
#                 sorted_list.append(index_of(min(values), values))
#             #     将标定值的最小值的索引追加到结果列表后面
#             values[index_of(min(values), values)] = math.inf
#         #      将标定值的最小值置为无穷小,即删除原来的最小值,移向下一个
#         #     infinited
#         return sorted_list
#
#     # 函数执行NSGA-II的快速非支配排序,将所有的个体都分层
#     def fast_non_dominated_sort(values1, values2):
#         S = [[] for i in range(0, len(values1))]
#         # 种群中所有个体的sp进行初始化 这里的len(value1)=pop_size
#         front = [[]]
#         # 分层集合,二维列表中包含第n个层中,有那些个体
#         n = [0 for i in range(0, len(values1))]
#         rank = [0 for i in range(0, len(values1))]
#         # 评级
#         for p in range(0, len(values1)):
#             S[p] = []
#             n[p] = 0
#             # 寻找第p个个体和其他个体的支配关系
#             # 将第p个个体的sp和np初始化
#             for q in range(0, len(values1)):
#                 # step2:p > q 即如果p支配q,则
#                 if (values1[p] > values1[q] and values2[p] > values2[q]) or (
#                         values1[p] >= values1[q] and values2[p] > values2[q]) or (
#                         values1[p] > values1[q] and values2[p] >= values2[q]):
#                     # 支配判定条件:当且仅当,对于任取i属于{1,2},都有fi(p)>fi(q),符合支配.或者当且仅当对于任意i属于{1,2},有fi(p)>=fi(q),且至少存在一个j使得fj(p)>f(q)  符合弱支配
#                     if q not in S[p]:
#                         # 同时如果q不属于sp将其添加到sp中
#                         S[p].append(q)
#                 # 如果q支配p
#                 elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
#                         values1[q] >= values1[p] and values2[q] > values2[p]) or (
#                         values1[q] > values1[p] and values2[q] >= values2[p]):
#                     # 则将np+1
#                     n[p] = n[p] + 1
#             if n[p] == 0:
#                 # 找出种群中np=0的个体
#                 rank[p] = 0
#                 # 将其从pt中移去
#                 if p not in front[0]:
#                     # 如果p不在第0层中
#                     # 将其追加到第0层中
#                     front[0].append(p)
#
#         i = 0
#         while (front[i] != []):
#             # 如果分层集合为不为空，
#             Q = []
#             for p in front[i]:
#                 for q in S[p]:
#                     n[q] = n[q] - 1
#                     # 则将fk中所有给对应的个体np-1
#                     if (n[q] == 0):
#                         # 如果nq==0
#                         rank[q] = i + 1
#
#                         if q not in Q:
#                             Q.append(q)
#             i = i + 1
#             # 并且k+1
#             front.append(Q)
#
#         del front[len(front) - 1]
#         # print(front)
#         return front
#         # 返回将所有个体分层后的结果
#
#     # 计算拥挤距离的函数
#
#     def crowding_distance(values1, values2, front):
#         distance = [0 for i in range(0, len(front))]
#         # 初始化个体间的拥挤距离
#         sorted1 = sort_by_values(front, values1[:])
#         sorted2 = sort_by_values(front, values2[:])
#         # 基于目标函数1和目标函数2对已经划分好层级的种群排序
#         distance[0] = 4444444444444444
#         distance[len(front) - 1] = 4444444444444444
#         for k in range(1, len(front) - 1):
#             distance[k] = distance[k] + (values1[sorted1[k + 1]] - values2[sorted1[k - 1]]) / (
#                     max(values1) - min(values1))
#         for k in range(1, len(front) - 1):
#             distance[k] = distance[k] + (values1[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (
#                     max(values2) - min(values2))
#         return distance
#     # 返回拥挤距离
#
#     # 函数进行交叉
#     def crossover(a, b):
#         r = random.random()
#         List1, List2 = [], []
#         length = int(len(a)/2)
#         List1 = a[:length] + b[length:]
#         List2 = a[length:] + b[:length]
#         if r > 0.5:
#             return mutation(List1)
#         else:
#             return mutation(List2)
#
#     # 函数进行变异操作
#     def mutation(solution):
#         mutation_prob = random.random()
#         List = solution
#         if mutation_prob < 1:
#             i = random.randint(0,19)
#             user = random.choice(usesimlist)
#             if user not in List:
#                 List[i] = user
#         solution = List
#         return solution
#
#     pop_size = 20  # 种群规模
#     max_gen = 50
#     # 迭代次数
#     solution = []
#     for i in range(0, pop_size):
#         solution.append(usesimlist[i*20:(i+1)*20])  # 20个随机用户作为种群个体
#
#     # 随机生成变量
#     gen_no = 0
#
#     while (gen_no < max_gen):
#         function1_values = [function1(solution[i]) for i in range(0, pop_size)]
#         function2_values = [function2(solution[i]) for i in range(0, pop_size)]
#         # 生成两个函数值列表，构成一个种群
#         non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])
#         crowding_distance_values = []
#         # 计算非支配集合中每个个体的拥挤度
#         for i in range(0, len(non_dominated_sorted_solution)):
#             crowding_distance_values.append(
#                 crowding_distance(function1_values[:], function2_values[:], non_dominated_sorted_solution[i][:]))
#         solution2 = solution[:]
#
#         # 生成了子代
#         while (len(solution2) != 2 * pop_size):
#             a1 = random.randint(0, pop_size - 1)
#             b1 = random.randint(0, pop_size - 1)
#             # 选择
#             solution2.append(crossover(solution[a1], solution[b1]))
#             # 随机选择，将种群中的个体进行交配，得到子代种群2*pop_size
#
#         function1_values2 = [function1(solution2[i]) for i in range(0, 2 * pop_size)]
#         function2_values2 = [function2(solution2[i]) for i in range(0, 2 * pop_size)]
#         non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:], function2_values2[:])
#         # 将两个目标函数得到的两个种群值value,再进行排序 得到2*pop_size解
#         crowding_distance_values2 = []
#         for i in range(0, len(non_dominated_sorted_solution2)):
#             crowding_distance_values2.append(
#                 crowding_distance(function1_values2[:], function2_values2[:], non_dominated_sorted_solution2[i][:]))
#         # 计算子代的个体间的距离值
#         new_solution = []
#         for i in range(0, len(non_dominated_sorted_solution2)):
#             non_dominated_sorted_solution2_1 = [
#                 index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
#                 range(0, len(non_dominated_sorted_solution2[i]))]
#             # 排序
#             front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
#             front = [non_dominated_sorted_solution2[i][front22[j]] for j in
#                      range(0, len(non_dominated_sorted_solution2[i]))]
#             front.reverse()
#             for value in front:
#                 new_solution.append(value)
#                 if (len(new_solution) == pop_size):
#                     break
#             if (len(new_solution) == pop_size):
#                 break
#         solution = [solution2[i] for i in new_solution]
#         gen_no = gen_no + 1
#
#     Best_user_group = solution[0]
#     getrecs = getRec(user, getRecommendation, Best_user_group)
#     return getrecs

if __name__ == '__main__':
    fp = 'Movielens dataset/ratings.dat'  # 读取文件路径
    data = loadData(fp)
    train, test, train_ex, test_ex, long, item_user, user50_test = splitData(data)
    wait_user = []  # 候选集用户列表
    getRecommendation, sorted_user_sim = UserCF(train, train_ex, 10)
    for user in user50_test:
        wait_user.append(user)

    user_recs = {}
    agrm = AGRM(fp, data, user_recs, train, test, train_ex, test_ex, long, item_user, user50_test,wait_user, getRecommendation, sorted_user_sim)

    for user in tqdm(wait_user):
        user_recs[user] = agrm.run(user)

    resys_list = open("Resys_result_10.json", "w")
    json.dump(user_recs, resys_list)
    resys_list.close()