import urllib2
import json
import os

#download the json file from baidu picture at page pn
#url is the request url
#filename is the name of output file
def download_json(url, filename):
    file = open('%s.json' % filename, 'w')
    response = urllib2.urlopen(url)
    file.write(response.read())
    file.close()

#download pictures in a page
#save_path is where the output will exis
#json_file is the file download by the function download_json
#referer is the referer url asked by header when send request to the aim url
#pic_name and start_num is the way to name the picture files
#e.g. pic_name is cat and start number is 0,then the name will be cat_0.jpg,cat_1.jpg...
def download_a_batch_of_pictures(save_path, json_file, referer, pic_name, start_number):
    file = open(json_file, 'r')
    data = json.load(file)
    file.close()
    if os.path.isdir(save_path):
        pass
    else:
        os.mkdir(save_path)
    for record in data['data']:
        if record.has_key('hoverURL'):
            if not record['hoverURL'].strip():
                continue
            header = {'Referer': referer}
            request = urllib2.Request(record['hoverURL'], headers= header)
            try:
                response = urllib2.urlopen(request)
            except Exception, e:
                print e
                continue
            pic = open('%s/%s_%d.jpg' % (save_path, pic_name, start_number), 'w')
            pic.write(response.read())
            start_number += 1
            pic.close()
            print '%d picture is download' % start_number
    return start_number


def download_input():
    url_dic = {
            'cat': 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E7%8C%AB&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%E7%8C%AB&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&pn=__PAGENUM__&rn=30&gsm=1e&1479994829795=',
           'dog': 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E7%8B%97&cl=2&lm=7&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E7%8B%97&s=&se=&tab=&width=&height=&face=&istype=2&qc=&nc=1&fr=&pn=__PAGENUM__&rn=30&gsm=1e&1480077658598=',
           'human': 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%99%AE%E9%80%9A%E4%BA%BA%E7%89%A9%E7%94%9F%E6%B4%BB%E7%85%A7+%E7%94%B7&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%99%AE%E9%80%9A%E4%BA%BA%E7%89%A9%E7%94%9F%E6%B4%BB%E7%85%A7+%E7%94%B7&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=__PAGENUM__&rn=30&gsm=1e&1480076025915='
           }
    for url_name in url_dic:
        start_number = 0
        for i in range(50):
            print '%d batch of %s is downlaoding' % (i, url_name)
            download_json(url_dic[url_name].replace('__PAGENUM__', '%d' % (i*30)), 'temp')
            start_number = download_a_batch_of_pictures(url_name, 'temp.json', url_dic[url_name], url_name, start_number)

download_input()