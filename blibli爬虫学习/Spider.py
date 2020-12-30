import requests
import json


class SpiderForView:
    def __init__(self):
        self.video_url = 'https://api.bilibili.com/x/web-interface/popular?ps=50&pn={page}'

    def run(self):
        for i in range(1, 2):
            self.__run_spider(i)

    def __run_spider(self, i):
        data_video = self.__spider(self.video_url.format(page=i))
        if data_video['data']['list']:
            for info in self.__video_data_handle(data_video['data']['list']):
                tags = self.__spider_tags(info['video_info']['aid'])
                info['video_info']['tags'] = tags
                yield info

    def __spider(self, url):
        res = requests.get(url).json()
        return res

    def __video_data_handle(self, data_video_list):
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

            data_video = {
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
        tag_api_url = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid=' + str(aid)
        tag_list = self.__spider(tag_api_url)['data']
        tags = []
        for tag in tag_list:
            tags.append(tag)
        return tags

    def __storage(self):
        pass

a = SpiderForView()
a.run()

'''待实现内容，获取每个视频的标签，并加入到视频当中'''
