# coding=utf-8
'''
思路：
1.	找到用户所喜爱的番剧
2.	分析这些番剧的类别（一个番剧可能有多个标签），进行统计排序
3.	找到数量最多的前三个标签
4.	从数据库中找到同时具有这三个标签的番剧
5.	去掉已经看过的番剧后，从中随机选择一个
6.	将番剧相关信息（name，brief）进行展示
'''
import MySQLdb
from random import choice


def recommand(user_id):
    # 1.数据库连接
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         password="123456",
                         db="recommand",
                         charset="utf8")
    cursor = db.cursor()

    # 判断用户是否存在
    cursor.execute("select id from user where id=%s", [user_id])
    if len(cursor.fetchall()) == 0:
        return {'flag': 0}

    # 2.找到用户所喜爱的番剧
    cursor.execute("select anime_id from user_anime where user_id=%s", [user_id])
    # print(cursor.fetchall())
    love_anime_id_list = [i[0] for i in cursor.fetchall()]
    # print(love_anime_id_list)

    # 3.分析这些番剧的类别（一个番剧可能有多个标签），进行统计排序,找到数量最多的前三个标签
    sql = '''
    select style_id,count(style_id) from
    (select style_id from anime_style where anime_id in
    (select anime_id from user_anime where user_id=%s))
    as a group by 1 order by 2 desc limit 3
    '''
    cursor.execute(sql, [user_id])
    # print(cursor.fetchall())
    top3_style_id = [i[0] for i in cursor.fetchall()]
    # print(top3_style_id)
    if len(top3_style_id) == 3:
        # 4.从数据库中找到同时具有这三个标签的番剧
        sql = "select anime_id from anime_style where style_id in (%s,%s,%s)"
        cursor.execute(sql, top3_style_id)
        # print(cursor.fetchall())
        like_look_anime_id_list = set([i[0] for i in cursor.fetchall()])
        # print(like_look_anime_id_list)

        # 5.去掉已经看过的番剧后，从中随机选择一个
        like_unlook_anime_id_list = list(like_look_anime_id_list.difference(set(love_anime_id_list)))
        random_anime_id = choice(like_unlook_anime_id_list)
    else:
        # 从全部番剧中随机选取一个
        cursor.execute("select id from anime")
        all_anime = [i[0] for i in cursor.fetchall()]
        random_anime_id = choice(all_anime)
        # print(random_anime_id)

    # 6.将番剧相关信息（name，brief）进行展示
    cursor.execute("select name,brief from anime where id=%s", [random_anime_id])
    # print(cursor.fetchone())
    name, brief = cursor.fetchone()
    result = {"user_id": user_id, 'flag': 1, 'name': name, 'brief': brief}
    return result


if __name__ == '__main__':
    result = recommand(1)
    print(result)
