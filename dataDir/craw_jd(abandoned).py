from bs4 import BeautifulSoup
import requests
import re, json
import pandas as pd
import time

# 参考https://www.cnblogs.com/zz22--/p/9320614.html
# 爬取京东商品评论

# get 
def getHtml(url, data):
	try:
		# print('Requesting...')
		r = requests.get(url, params=data)
		# print('Request stringatisfied!')
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print('爬取失败')

def getComment(html):
	commentList = []
	i = json.dumps(html)
	j = json.loads(i)
	comment = re.findall(r'{"productAttr":.*}', j)
	# print(j)
	# print(comment)
	comm_dict = json.loads(comment[0])
	commentSummary = comm_dict['comments']
	for comment in commentSummary:
		c_content = ''.join(comment['content'].split())
		uLevelColor = ''.join(comment['userLevelColor'].split())
		uLevelId = ''.join(comment['userLevelId'].split())
		uLevelName = ''.join(comment['userLevelName'].split())
		useful = comment['usefulVoteCount']
		useless = comment['uselessVoteCount']
		score = comment['score']
		commentList.append([score, uLevelColor, uLevelId,
			uLevelName, useful, useless, c_content])
	return commentList

def getComments(url, num):
	# Query string parameters
	data = {'callback': 'fetchJSON_comment98vv1610',
			'productId': '100000961842',
			'score': 0,
			'sortType': 5,
			'page': 0,
			'pageSize': 10,
			'isShadowSku': 0,
			'rid': 0,
			'fold': 1
			}
	comments = []
	for i in range(num):
		# data['page'] = i
		# html = getHtml(url, data)
		# comment = getComment(html)		
		try:	# skip failed page
			data['page'] = i
			html = getHtml(url, data)
			comment = getComment(html)
		except:
			print('EXCEPTION in getComments')
			continue
		comments += comment
		print('页数', i)
		time.sleep(2)
	return comments

if __name__ == '__main__':
	time_start = time.time()
	url = 'https://sclub.jd.com/comment/productPageComments.action?'
	comm = getComments(url, 500)
	print('共%d条评论' % len(comm))
	name = ['score', 'userLevelColor', 'userLevelId', 'userLevelName', 
		'usefulVote', 'uselessVote', 'comment']
	file = pd.DataFrame(columns=name, data=comm)
	file.to_csv('WDHardDisk.csv', index=False)
	time_end = time.time()
	print('耗时%f秒' % (time_end - time_start))
