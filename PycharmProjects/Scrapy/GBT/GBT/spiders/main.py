import requests
import re
import csv


def main():
    headers = {
        'Referer': 'http://ck.ysepan.com/f_ht/ajcx/000ht.html?bbh=1166',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36'
    }
    req = requests.get("http://ck.ysepan.com/f_ht/ajcx/ml.aspx?cz=ml_dq&_dlmc=gbtgame&_dlmm=", headers=headers)
    req_str = str(req.text.strip())
    id_list = re.findall(find_id, req_str)
    wenjianjia_list = re.findall(find_wenjianjia, req_str)
    # 表头
    header = ['wenjianjia', 'BT_URL', 'youxi_name']
    with open('../../person.csv', 'w', encoding='utf-8') as file_obj:
        # 1:创建writer对象
        writer = csv.writer(file_obj)
        # 2:写表头
        writer.writerow(header)
        # 3:遍历列表，将每一行的数据写入csv
        for i in range(len(id_list)):
            zi_req = requests.get(
                f'http://ck.ysepan.com/f_ht/ajcx/wj.aspx?cz=dq&jsq=0&mlbh={id_list[i]}&wjpx=1&_dlmc=gbtgame&_dlmm=',
                headers=headers)
            zi_req_str = str(zi_req.text.strip())
            zi_BT_URL_list = re.findall(find_zi_BT_URL, zi_req_str)
            zi_youxi_name_list = []
            for j in range(len(zi_BT_URL_list)):
                youxi_name = zi_BT_URL_list[j].split('/')[-1]
                zi_youxi_name_list.append(youxi_name)
                writer.writerow((wenjianjia_list[i], zi_BT_URL_list[j], youxi_name))


if __name__ == '__main__':
    find_id = 'id="ml_(.*?)"'
    find_wenjianjia = 'href="javascript:;">【(.*?)】</a>'
    find_zi_BT_URL = 'href="(.*?)"'
    main()
