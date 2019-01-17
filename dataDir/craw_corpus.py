import craw_tb as ct
import time
import pandas as pd

# 训练word2vec的语料爬取，因为感觉只使用之前的评论感觉不够，
# 选取了5个卫衣商品，4个高销量，1个uniqlo

urls = [
	('https://rate.tmall.com/list_detail_rate.htm?itemId=569'
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
	'&_ksTS=1544702118464_1473&callback=jsonp1474' ),

	'https://rate.tmall.com/list_detail_rate.htm?itemId=578773285314&spuId=1080323061&sellerId=3563488801&order=3&currentPage=%d&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%%23E1hvKQv4vahvUvCkvvvvvjiPR2Fy0jEmnLqhsj1VPmPytjtjnL5h6jECR2Ly1jtjdphvmpvWLgHboQCc9syCvvpvvvvv9phvh1vUwFsycnMNzYcIzbzEoz%%2B2o0urvpvpjvvj9L6YvUdTFfwznHVt646CvvyvmHgVO0WvP4TrvpvEvv3xCmWFvRAyRphvCvvvvvmjvpvhvvpvv8wCvvpvvUmmRphvCvvvvvvPvpvhvv2MMTyCvv9vvUmsYTb1iUyCvvOUvvhCa64tvpvIvvvv2hCvvvZvvURNphvWOQvv96CvpC29vvm256CvhUvvvURNphvp9vyCvhQvP8vvC0oXwacvefHl8acvsEefbFZHsEjvwfIOw1mxkbmxdByaUUkU%%2BE7reB69QbmDYCIOaZAQ0f0DW3CQog0HsXZpjjIUDajxALwpvphvC9vhvvCvpUhCvCLNqMhG%%2FldNzYGIzP1wQRJmzYSw546CvvyvmnRm1WpvDmTrvpvEvvAwCVrdvUjudphvV2QUOOVfeQ2EbWeQRkxB3Xz91CKSayLv346CvCvwv8AC%%2BqWv07Vnrsw6Zf5BdphvmpvhEUhCvpvKwUhCvCWpmjUGtHdNzYMnqnAYAZrqv6ruRphvCvvvvvmrvpvEvvkK9dRsvjRY9phvHnMzPbGn7rMNzta7MH1pqQ2Nvasv&needFold=0&_ksTS=1544969155703_1425&callback=jsonp1426',

	'https://rate.tmall.com/list_detail_rate.htm?itemId=559117332872&spuId=882860447&sellerId=3166204872&order=3&currentPage=%d&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%%23E1hvcpvPvBUvUvCkvvvvvjiPR2Fy0jEbR2MWtjnEPmP9tjrnR2zWtjYVPLdv6jtWRphvCvvvvvmrvpvEvvkpvzlYvRvwdphvmQ9OZIC2pQm9t4hA2QhvCvvvMM%%2FtvpvIvvvv2hCvvvZvvURNphvWOQvv96CvpC29vvm256CvhUvvvURNphvWOgyCvvOUvvhCa64ivpvUvvmv%%2BMJxtXyEvpCWvm2Wvva66we9QC4XwHeQiNLUV1rz7YeYiXhpVj%%2BO3w0x9E9XJ9kx6acEn1vDN%%2BLyaNoAdcHUa4AUSBh78BLp1nL9HF%%2BSBiVvQRA1%%2BvhCvvOvCvvvphvtvpvhvvvvv8wCvvpvvUmm3QhvCvvhvvmCvpvRqQkszHHwzYMNU7jwQdgtvpvhvvvvvUhCvCLNtYCwIDdNzYME%%2BM1f6YMpzQsw5p%%3D%%3D&needFold=0&_ksTS=1544969959725_1276&callback=jsonp1277',

	'https://rate.tmall.com/list_detail_rate.htm?itemId=563620564284&spuId=920581799&sellerId=3014907114&order=3&currentPage=%d&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%%23E1hv%%2FpvWvR9vUvCkvvvvvjiPR2FyzjrbPLMZzjthPmP96jlUR2MWgjnbR2syljrPdphvmpvCkO6lvvvEOghCvCRG5VxfIJMwznsaSDdAZTDuk85RiQhvCvvvpZptvpvhvvCvpvGCvvpvvPMMkphvC9hvpy2w18yCvv9vvhhezIzHBbyCvm9vvhCOvvvvIvvvBz9vvUH%%2BvvCj1Qvvv3QvvhagvvvmhvvvBz9vvUH%%2BmphvLvVzR29asCQae3DsBf2XrqpAhjCbFO7t%%2B3mwJ9kx6fItn1vDN%%2BCl5d8rjC6sF4VQR4VzEhhH6BoAdX9anbmxdXKK55BVtjeAdBkKfvyCvpvVvUCvpvvv3QhvCvmvphvtvpvhvvCvpv%%3D%%3D&needFold=0&_ksTS=1544970018943_1148&callback=jsonp1149',

	'https://rate.tmall.com/list_detail_rate.htm?itemId=574865546798&spuId=1023113202&sellerId=196993935&order=3&currentPage=%d&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%%23E1hvQpvLvZyvjQCkvvvvvjiPR2Fyzjrbn25O6j3mPmPZ1jDPPsdUAj1RRFLUtj%%2FCvpvZzMNYMit4zYMNtOPGcH25OYGCzWmrvpvEphbKBEyvpPlmdphvmZChuo1Hvh2wHghCvCWpm8pYhHsNzY%%2FhraAYAZrqv6rudphvmZC2Bm1zvh2BCu6CvvDvpsQyyQCvc7kjvpvhphhvv2yCvvBvpvvvvphvCyCCvvvvvvyCvh1haZyvIqyDCcxPAXZTKFEwOv56D40OamDML%%2B2y5ErTpzBC0bvqrADnOH2%%2BFfmtEpx0LWexRdIAcVvEYWA4e53ZnDeDyBvOJ193Zi7vKphv8hCvvVvvvhvCphvwMvvvptrvpCQmvvChNhCvjPQvvhByphvwMvvvBVoivpvUphvh5a%%2BAtJeEvpvVpyUUmEKO2QhvCPMMvvm5vpvhphvhH86CvvDvpTQg%%2B9CvfmUtvpvhphvvv86CvvDvp9v%%2BVvCvY7Ztvpvhphvvvv%%3D%%3D&needFold=0&_ksTS=1544970135251_1504&callback=jsonp1505',
]

if __name__ == '__main__':
	time_start = time.time()

	collectElement = ['aliMallSeller', 'anony', 'buyCount', 'goldUser',
						'useful', 'pics', 'rateContent']
	comm, pureComm = [], []
	for url in urls:
		comm_t, pureComm_t = ct.getComments(url, range(1, 100), collectElement)
		print('共%d条评论' % len(pureComm_t))
		comm += comm_t
		pureComm += pureComm_t
	file = pd.DataFrame(columns=collectElement+['appendComment'], data=comm)
	file.to_csv('raw_data/corpusAll.csv', index=False)
	file2 = pd.DataFrame(columns=['comment'], data=pureComm)
	file2.to_csv('raw_data/corpus.csv', index=False)

	time_end = time.time()
	print('耗时%f秒' % (time_end - time_start))
