from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render
from userDS.parser import user_page_parse, signed_list_parse
from userDS.spojUser import spojUser
from userDS.spojUserMulti import spojUserMulti
import urllib2
from google.appengine.api import urlfetch
def home(request):
	return render(request, 'home.html')

def get_user_info(user_name):
	#html = urllib2.urlopen('http://www.spoj.pl/users/'+user_name).read()
	#result = urlfetch.fetch('http://localhost/nims11')

	result = urlfetch.fetch('http://www.spoj.com/users/'+user_name, deadline=30)
	encoding=result.headers['content-type'].split('charset=')[-1]
	html = result.content.decode('ISO-8859-2')
	html = html.replace('\n','')
	#return html

	user_info = user_page_parse(html, user_name)
	# parsing signed list
	#signed_html = urllib2.urlopen('http://localhost/signedlist').read()

	signed_html = urlfetch.fetch('http://www.spoj.com/status/'+user_name+'/signedlist/', deadline=30).content
	problem_info = signed_list_parse(signed_html, user_info)
	user_info.probPool.calc_stats()
	user_info.get_classical_table()
	return user_info

def single_user(request, user_name):
	user_info = get_user_info(user_name)
	return render(request, 'single.html',{'main': user_info})
	#html = get_user_info(user_name)
	#return HttpResponse(html)

def multi_user(request, user_name1, user_name2):
	user_info1 = get_user_info(user_name1)
	user_info2 = get_user_info(user_name2)

	return render(request, 'multi.html', {'main':spojUserMulti(user_info1, user_info2)})

def about(request):
	return render(request, 'about.html', {})
