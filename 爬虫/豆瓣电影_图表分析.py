# coding=utf-8import pygalimport MySQLdbdef get_data():    db=MySQLdb.connect(host='localhost',user='root',passwd='suyu.123',db='movie',charset='utf8')    cursor = db.cursor()    cursor.execute('select grade,count(2) from movie_info group by grade;')    datas=cursor.fetchall()    count=[]    print(type(datas))    for data in datas:        count.append(int(data[1]))        #grade=data[0]        #count=data[1]    return countdef main():    a=range(81,97)    grade = []    for b in range(81,97):        c=b/10.0        grade.append(c)    chart_count=get_data()    #for chart_count in chart_data:    movie_chart=pygal.Line()    movie_chart.title='movie chart'    movie_chart.x_labels=map(str, grade)    movie_chart.add('count',chart_count)    movie_chart.render_to_file(r'C:\Users\legolas\Desktop\movie_chart.svg')if __name__ == '__main__':    main()