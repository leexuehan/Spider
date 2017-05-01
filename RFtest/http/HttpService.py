class HttpService(object):
    def post(self, url, body):
        print("send request, url:" + url + ",body:" + body)
        return 200
