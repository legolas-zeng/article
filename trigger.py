# -*-coding:utf-8 -*-from celery.tasks import timeoutimport sysdef pm(body):    res = body.get('result')    if body.get('status') == 'PROGRESS':        sys.stdout.write('\r任务进度: {0}%'.format(res.get('p')))        sys.stdout.flush()    else:        print '\r'        print resr = timeout.delay()print r.get(on_message=pm, propagate=False)# def abc():# 	a=add.delay(5, 5)# 	print a# 	print a.id# 	print a.status# 	#print a.get()## abc()