from db_functions import run_search_query_tuples


def get_news(db_path):
    sql = """select news.title, news.subtitle, news.content, member.name
    from news
    join member on news.member_id = member.member_id;
    """
    result = run_search_query_tuples(sql, (), db_path, True)

    for row in result:
        for k in row.keys():
            print(k)
            print(row[k])

def get_classes(db_path):
    sql = """select classes.classes_id, classes.title, classes.context, classes.newsdate, member.name
           from classes
           join member on classes.member_id= member.member_id
           order by classes.newsdate desc;
           """

if __name__ == "__main__":
    db_path = 'data/dance_db.sqlite'
    get_classes(db_path)