# coding=utf-8
# @author: zwa❤lqp
# @time: 2020/11/22 15:05

# coding=utf-8
import requests,random
import json
import time
import os
import re

INFO = {
    "name": "kuaishou-crawler",
    "author": "oGsLP",
    "repository": "www.github.com/oGsLP/kuaishou-crawler",
    "version": "0.5.0",
    "publishDate": "20-08-06"
}

PROFILE_URL = "https://live.kuaishou.com/profile/"
DATA_URL = "https://live.kuaishou.com/m_graphql"
WORK_URL = "https://m.gifshow.com/fw/photo/"


class Crawler:


    __headers_web = {
        'accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'live.kuaishou.com',
        'Origin': 'https://live.kuaishou.com',
        'Sec - Fetch - Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # User-Agent/Cookie 根据自己的电脑修改
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Cookie':'kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; clientid=3; did=web_8b1ef0506c146c24627a858c9a646ad2; client_key=65890b29; userId=1717892941; WEBLOGGER_INCREAMENT_ID_KEY=1077; WEBLOGGER_HTTP_SEQ_ID=499; didv=1600953928773; sid=9ff1ca2ccca59fd641cf3190; logj=; kpn=GAME_ZONE; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1606749838; userId=1717892941; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1607951257; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAZKHmQ4KA3DbNqjgu6VQcruaQ3v1MGoHLKVkfIBnROpH15Map_tPSegEpCBneETGNpShKsaEeczYXaJc-bSdyUSoSHcWCfl1FM0C4QOC3vJf4dwhx5vo-9n0lK7FFCIRoirgKGHBAevyjXMAHDBR6Qbx-XgOBivHQkgEjKONHOZmpGwOF0kl27mco2o45mt4ih1XoRatD8Rdreh9Bv2cvXwaEoMRdS355EPfvO-WEFcOv_Ls2yIgt_7ygqExH0miHzepgAC3qcJwLqNwhGb3o397Qun6vw8oBTAB; kuaishou.live.web_ph=3fd8c6d06572dfea278d69cdad730dff094d',
        #'Cookie':'',
    }
    __headers_mobile = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
        'Cookie': 'did=web_f3915064ee334c508642888137f27598; didv=1601290877000; sid=9ad11d5739016e866ddaa456; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1606915674; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1608029646'}
        # 'Cookie': ''}

    __crawl_list = []

    __date_cache = ""
    __date_pic_count = 0

    def __init__(self, prod=True):
        self.__intro()
        if prod:
            time.sleep(random.randint(1,10))
        else:
            self.__read_preset()

    def set_did(self, did):
        self.__param_did = did
        self.__headers_web['Cookie'] = 'did=' + did + "; userId="
        # self.__headers_mobile['Cookie'] = 'did=' + did

    def set_mobile_did(self,did):
        self.__headers_mobile['Cookie'] = 'did=' + did

    def crawl(self):
        print("准备开始爬取，共有%d个用户..." % len(self.__crawl_list))
        time.sleep(random.randint(1,10))
        for uid in self.__crawl_list:
            self.__date_cache = ""
            self.__date_count = 0
            self.__crawl_user(uid)
            # self.crawl_like(uid)

    def add_to_list(self, uid):
        self.__crawl_list.append(uid)

    def __crawl_user(self, uid):
        if uid.isdigit():
            uid = self.__switch_id(uid)

        payload = {"operationName": "privateFeedsQuery",
                   "variables": {"principalId": uid, "pcursor": "", "count": 1999},
                   "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}
        res = requests.post(DATA_URL, headers=self.__headers_web, json=payload)
        print("获取的网页：",json.loads(res.content.decode(encoding='utf-8', errors='strict')))
        print(len(json.loads(res.content.decode(encoding='utf-8', errors='strict'))))
        works = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']
        print(works)
        if not os.path.exists("H:\\04-快手素材"):
            os.makedirs("H:\\04-快手素材")

        # 这两行代码将response写入json供分析
        # with open("data/" + uid + ".json", "w") as fp:
        #     fp.write(json.dumps(works, indent=2))

        # 防止该用户在直播，第一个作品默认为直播，导致获取信息为NoneType
        if works[0]['id'] is None:
            works.pop(0)
        name = re.sub(r'[\\/:*?"<>|\r\n]+', "", works[0]['user']['name'])

        dir = "H:\\04-快手素材\\" + name + "(" + uid + ")/"
        # print(len(works))
        if not os.path.exists(dir):
            os.makedirs(dir)

        # if not os.path.exists(dir + ".list"):
        #     print("")

        print("开始爬取用户 " + name + "，保存在目录 " + dir)
        print(" 共有" + str(len(works)) + "个作品")

        for j in range(len(works)):
            self.__crawl_work(dir, works[j], j + 1)
            time.sleep(random.randint(1,10))

        print("用户 " + name + "爬取完成!")
        print()
        time.sleep(random.randint(1,9))

    '''
    快手分为五种类型的作品，在作品里面表现为workType属性
     * 其中两种图集: `vertical`和`multiple`，意味着拼接长图和多图，所有图片的链接在imgUrls里
     * 一种单张图片: `single` 图片链接也在imgUrls里
     * K歌: `ksong` 图片链接一样，不考虑爬取音频...
     * 视频: `video` 需要解析html获得视频链接
    '''

    def __crawl_work(self, dir, work, wdx, like=False):
        # 作品类型
        w_type = work['workType']
        # 标题
        w_caption = re.sub(r"\s+", " ", work['caption'])

        w_name = re.sub(r'[\\/:*?"<>|\r\n]+', "", w_caption)[0:24]
        # 时间
        w_time = time.strftime('%Y-%m-%d', time.localtime(work['timestamp'] / 1000))
        w_index = ""
        if not like:
            if self.__date_cache == w_time:
                self.__date_count = self.__date_count + 1
                if self.__date_count > 0:
                    w_index = "(%d)" % self.__date_count
            else:
                self.__date_cache = w_time
                self.__date_count = 0

        if w_type == 'vertical' or w_type == 'multiple' or w_type == "single" or w_type == 'ksong':
            w_urls = work['imgUrls']
            l = len(w_urls)
            print("  " + str(wdx) + ")图集作品：" + w_caption + "，" + "共有" + str(l) + "张图片")
            for i in range(l):
                p_name = w_time + w_index + "_" + w_name + "_" + str(i + 1) + '.jpg'
                pic = dir + p_name
                if not os.path.exists(pic):
                    r = requests.get(w_urls[i].replace("webp", "jpg"))
                    r.raise_for_status()
                    with open(pic, "wb") as f:
                        f.write(r.content)
                    print("    " + str(i + 1) + "/" + str(l) + " 图片 " + p_name + " 下载成功 √")
                else:
                    print("    " + str(i + 1) + "/" + str(l) + " 图片 " + p_name + " 已存在 √")
        elif w_type == 'video':
            w_url = WORK_URL + work['id'] +"?did="+ self.__param_did
            print("视频请求地址：",w_url)
            res = requests.get(w_url, headers=self.__headers_mobile,)
            html = res.text
            # with open("data/" + work['id'] + ".html", "w") as fp:
            #     fp.write(html)
            # print(html)
            pattern = '"srcNoMark":"(https:.*?).mp4'
            v_url = re.search(pattern, html).group(1)+".mp4"
            print("无水印地址：", v_url)
            # print(v_url)
            # pattern = re.compile(r"playUrl", re.MULTILINE | re.DOTALL)
            # script = soup.find("script", text=pattern)
            # s = pattern.search(script.text).string
            # v_url = s.split('playUrl":"')[1].split('.mp4')[0].encode('utf-8').decode('unicode-escape') + '.mp4'
            try:
                print("  " + str(wdx) + ")视频作品：" + w_caption)
            except:
                print("  这里似乎有点小错误，已跳过")
            v_name = w_time + w_index + "_" + w_name + ".mp4"
            video = dir + v_name

            if v_url:
                if not os.path.exists(video):
                    r = requests.get(v_url)
                    try:
                        r.raise_for_status()
                    except:
                        print("  这里似乎有点小错误，已跳过")
                    with open(video, "wb") as f:
                        f.write(r.content)
                    print("    视频 " + v_name + " 下载成功 √")
                else:
                    print("    视频 " + v_name + " 已存在 √")
            else:
                print("未找到视频")
        else:
            print("错误的类型")

    def crawl_like(self, uid):
        payload = {"operationName": "likedFeedsQuery",
                   "variables": {"principalId": uid, "pcursor": "", "count": 1999},
                   "query": "query likedFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  likedFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}
        res = requests.post(DATA_URL, headers=self.__headers_web, json=payload)
        print("获取的网页：",json.loads(res.content.decode(encoding='utf-8', errors='strict')))
        dta = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['likedFeeds']
        print(dta)
        works = dta['list']
        print("开始爬取用户 " + uid + " 的喜欢作品")
        print(" 共有" + str(len(works)) + "个作品")
        name = re.sub(r'[\\/:*?"<>|\r\n]+', "", works[0]['user']['name'])
        dir = "H:\\04-快手素材\\" + name + "(" + uid + ")/"
        for i in range(len(works)):
            self.__crawl_work(dir, works[i], i + 1, True)

    def __read_preset(self):
        p_path = "preset"
        if not os.path.exists(p_path):
            print("创建预设文件 preset ...")
            open(p_path, "w")
        if not os.path.getsize(p_path):
            print("请在预设文件 preset 中记录需要爬取的用户id，一行一个")
            exit(0)
        with open(p_path, "r") as f:
            for line in f:
                if line[0] != "#":
                    self.__crawl_list.append(line.strip())

    def __switch_id(self, uid):
        payload = {"operationName": "SearchOverviewQuery",
                   "variables": {"keyword": uid, "ussid": None},
                   "query": "query SearchOverviewQuery($keyword: String, $ussid: String) {\n  pcSearchOverview(keyword: $keyword, ussid: $ussid) {\n    list {\n      ... on SearchCategoryList {\n        type\n        list {\n          categoryId\n          categoryAbbr\n          title\n          src\n          __typename\n        }\n        __typename\n      }\n      ... on SearchUserList {\n        type\n        ussid\n        list {\n          id\n          name\n          living\n          avatar\n          sex\n          description\n          counts {\n            fan\n            follow\n            photo\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on SearchLivestreamList {\n        type\n        lssid\n        list {\n          user {\n            id\n            avatar\n            name\n            __typename\n          }\n          poster\n          coverUrl\n          caption\n          id\n          playUrls {\n            quality\n            url\n            __typename\n          }\n          quality\n          gameInfo {\n            category\n            name\n            pubgSurvival\n            type\n            kingHero\n            __typename\n          }\n          hasRedPack\n          liveGuess\n          expTag\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

        res = requests.post(DATA_URL, headers=self.__headers_web, json=payload)
        dt = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']
        print(dt)
        # with open("data/jj_" + uid + ".json", "w") as fp:
        #     fp.write(json.dumps(dt, indent=2))

        return dt['pcSearchOverview']['list'][1]['list'][0]['id']

    def __intro(self):
        print()
        print("|  %s (v%s %s)" % (INFO["name"], INFO["version"], INFO["publishDate"]))
        print("|  本程序由%s提供, %s, 喜欢的话可以给个star >_<" % (INFO["author"], INFO["repository"]))
        print()



def crawl():
    crawler = Crawler()
    # web 端的did
    param_did = "web_8b1ef0506c146c24627a858c9a646ad2"
    crawler.set_did(param_did)

    # mobile 端的did
    mobile_did = "web_f3915064ee334c508642888137f27598"
    crawler.set_mobile_did(mobile_did)


    # uid = "3xh2dvcz3c396gu"
    uidlist=["s934686153"]
    for uid in uidlist:
        crawler.add_to_list(uid)

    crawler.crawl()

    input("请按回车键退出......")


if __name__ == "__main__":
    crawl()