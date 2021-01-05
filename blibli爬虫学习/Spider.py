'''
@author: SvanurH
@create_time: 2020-12-29
@updated_time: 2020-12-30
待实现内容:
    进行数据保存工作，存储到mongodb数据库
    数据处理，数据可视化功能
    
'''

import requests
import json


class SpiderForView:
    def __init__(self):
        self.video_url = 'https://api.bilibili.com/x/web-interface/popular?ps=50&pn={page}'  # blibli网站热门api,定义page参数为页数

    def run(self):
        for i in range(1, 50):  # i为页数
            datas = self.__run_spider(i)
            if not datas:
                yield False
            for k in datas:
                yield k

    def __run_spider(self, i):
        data_video = self.__spider(self.video_url.format(page=i))  # 通过格式化url传递到爬虫中
        if data_video['data']['list']:  # 判断是否爬取成功
            for info in self.__video_data_handle(data_video['data']['list']):
                tags = self.__spider_tags(info['video_info']['aid'])
                info['video_info']['tags'] = tags
                yield info
        else:  # 如果爬取不成功就返回false
            return False

    def __spider(self, url):
        '''
        通过requests爬取API返回的数据
        '''
        res = requests.get(url).json()
        return res

    def __video_data_handle(self, data_video_list):
        '''
        处理热门API爬取的数据
        '''
        for info in data_video_list:
            aid = info['aid']
            bvid = info['bvid']
            title = info['title']
            created_time = info['ctime']
            author = info['owner']['name']  # up名
            author_mid = info['owner']['mid']  # up id
            viewed = info['stat']['view']  # 观看次数
            danmaku = info['stat']['danmaku']  # 弹幕
            reply = info['stat']['reply']  # 评论
            favorite = info['stat']['favorite']  # 收藏
            share = info['stat']['share']  # 分享
            likes = info['stat']['like']  # 点赞

            data_video = {  # 集合到一个字典里，方面后期处理使用
                'video_info': {
                    'title': title,
                    'aid': aid,
                    'bvid': bvid,
                    'created_time': created_time
                },
                'author': {
                    'name': author,
                    'id': author_mid
                },
                'info': {
                    'view': viewed,
                    'danmaku': danmaku,
                    'reply': reply,
                    'favorite': favorite,
                    'share': share,
                    'likes': likes
                }
            }

            yield data_video

    def __spider_tags(self, aid):
        '''
         通过requests爬取blibli网站API，通过视频aid获取视频下的标签
        '''
        tag_api_url = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid=' + str(aid)
        tag_list = self.__spider(tag_api_url)['data']
        tags = []
        for tag in tag_list:
            tags.append(tag['tag_name'])
        return tags


