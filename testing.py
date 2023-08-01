from db_functions import run_search_query_tuples
db_path = 'data/dance_db.sqlite'

sql = """select classes.classes_id, classes.classes_title, classes.content, classes.image, member.name
        from classes
        join member on classes.member_id= member.member_id;
        """
result = run_search_query_tuples(sql, (), db_path, True)
for row in result:
    for k in row.keys():
        print(k)
        print(row[k])
