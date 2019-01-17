from bs4 import BeautifulSoup
import requests
import re, json
import pandas as pd
import time
import random

# 爬取淘宝商品评论
# 参考 https://www.cnblogs.com/zz22--/p/9320614.html, 
# https://www.cnblogs.com/ruyingsuixing/p/9101051.html

# get 
def getResponse(url, data):
	try:
		# print('Requesting...')
		r = requests.get(url, params=data)
		# print('Request stringatisfied!')
		r.raise_for_status()
		# r.encoding = r.apparent_encoding
		return r.text
	except:
		print('爬取失败')

def getComment(response, collectElement):
	commentList, pureComment = [], []
	comment = re.findall(r'{".*}', response)	# A list

	comm_dict = json.loads(comment[0])						# json to dict
	commentSummary = comm_dict['rateDetail']['rateList']
	for comment in commentSummary:
		elements = []
		# other element
		for ele in collectElement:
			elements.append(comment[ele])
		# element 'appendComment'
		if comment['appendComment'] == None:
			elements.append(None)
		else:
			pureComment.append([comment['appendComment']['content']])
			elements.append(comment['appendComment']['content'])
		pureComment.append([comment['rateContent']])
		commentList.append(elements)
	return commentList, pureComment

# interval example: range(1, 3) = [1, 2]
def getComments(url, interval, collectElement):
	# Query string parameters
	data = {
		'currentPage': 0,
		'_ksTS': '',
		'callback': ''
	}
	comments, pureComm = [], []
	try:
		for i in interval:
			t = str(time.time()).split('.')
			data['currentPage'] = i
			data['_ksTS'] = '%s_%s' % (t[0], t[1])
			data['callback'] = 'jsonp%s' % (int(t[1])+1)

			try:	# skip failed page
				response = getResponse((url % i), data)
				comment, pureC = getComment(response, collectElement)
			except:
				print('EXCEPTION in getComments')
				continue
			
			comments += comment
			pureComm += pureC
			print('页数', i)
			time.sleep(random.random())

	except:
		file = pd.DataFrame(columns=collectElement+['appendComment'], data=comments)
		file.to_csv('raw_data/taobao_t.csv', index=False)
		file2 = pd.DataFrame(columns=['comment'], data=pureComm)
		file2.to_csv('raw_data/taobaoPure_t.csv', index=False)
		raise KeyboardInterrupt
	return comments, pureComm

if __name__ == '__main__':
	time_start = time.time()

	url = (	'https://rate.tmall.com/list_detail_rate.htm?itemId=569'
			'117247360&spuId=966657630&sellerId=3826760664&order=3&'
			'currentPage=%d&append=0&content=1&tagId=&posi=&picture='
			'&groupId=&ua=098%%23E1hvPvvXvXOvUvCkvvvvvjiPR2FwQjDERLS'
			'htjD2PmPwljY8PLFhtjDRRF5wtjnb9phv2n1w1V0DzYswzCZM7u6Cv'
			'vDvpuwOhvCvM80CvpvLSnsZ7TzSznswdar4GDRi4Ikisu6CvvDvpQW'
			'p%%2BvCv7VRjvpvhphhvv8wCvvBvpvpZ2QhvCvvvMMGCvpvVphhvvvv'
			'vmphvLh2%%2BEQmFVC69bpPCSL9Z4ZZDNr1l5dUf83lVD76Od361Ecq'
			'vaXTpEctz8dmD5dUf816kgRvfejibwyRQ0fJ6EvBQ2N79R3OSvjEVG'
			'wmtvpvIphvvOvvvpvHvpCsGvvC2e6CvjvUvvhBGphvwMvvvBVBvpCs'
			'GvvChX8yCvv3vpvoa6s74wIyCvvXmp99Uet9tvpvhphvvv86CvvDvp'
			'QwpJvCvmxervpvEphRMCEGvp2DfdphvmZCh9p9qvhvYD46CvvDvpwy'
			'hqpCvsoOtvpvhphvvv86CvvDvBEghnpCv0fJrvpvEphWpRbGvpUbVR'
			'phvChCvvvmrvpvEphBYFnpvpEGNdphvhyD8et9LvhmDqgAY%%2BX4AR'
			'hQAZghCvvswMmnq1rMwznAtwxItvpvhphvvvv%%3D%%3D&needFold=0'
			'&_ksTS=1544702118464_1473&callback=jsonp1474' )

	collectElement = ['aliMallSeller', 'anony', 'buyCount', 'goldUser',
						'useful', 'pics', 'rateContent']
	comm, pureComm = getComments(url, range(99, 100), collectElement)
	print('共%d条评论' % len(pureComm))
	file = pd.DataFrame(columns=collectElement+['appendComment'], data=comm)
	file.to_csv('raw_data/taobao500.csv', index=False)
	file2 = pd.DataFrame(columns=['comment'], data=pureComm)
	file2.to_csv('raw_data/taobaoPure500.csv', index=False)

	pure1 = pd.DataFrame(columns=['comment'], data=pureComm[0:200])
	pure1.to_csv('raw_data/taobaoPart1.csv', index=False)
	pure2 = pd.DataFrame(columns=['comment'], data=pureComm[200:400])
	pure2.to_csv('raw_data/taobaoPart2.csv', index=False)
	pure3 = pd.DataFrame(columns=['comment'], data=pureComm[400:600])
	pure3.to_csv('raw_data/taobaoPart3.csv', index=False)
	pure4 = pd.DataFrame(columns=['comment'], data=pureComm[600:800])
	pure4.to_csv('raw_data/taobaoPart4.csv', index=False)
	pure5 = pd.DataFrame(columns=['comment'], data=pureComm[800:1000])
	pure5.to_csv('raw_data/taobaoPart5.csv', index=False)

	time_end = time.time()
	print('耗时%f秒' % (time_end - time_start))
