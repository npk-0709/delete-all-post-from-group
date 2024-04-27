"""
   * Author: NGUYEN PHU KHUONG (K.AUTO) 
   * Email: dev.phukhuong0709@hotmail.com
   * Github: npk-0709
   * Zalo: 0363561629
"""



import requests
from bs4 import BeautifulSoup
import time



cookie = input('Mời Nhập Cookie: ').strip()
uid_group = input('Mời Nhập Uid Group: ').strip()
delay = float(input('Mời Nhập Thời Gian Delay Giữa 2 Lần Xóa: ').strip())

class Main:
    def __init__(self, cookie: str, uid_group: str) -> None:
        self.count_del = 1
        self.uid_group = uid_group
        self.http = requests.Session()
        self.http.headers = {
            "Cache-Control": 'max-age=0',
            "Accept": "*/*",
            "Connection": "keep-alive",
            "cookie": cookie,
            "Sec-Ch-Prefers-Color-Scheme": "dark",
            "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "Sec-Ch-Ua-Full-Version-List": "\"Chromium\";v=\"124.0.6367.61\", \"Microsoft Edge\";v=\"124.0.2478.51\", \"Not-A.Brand\";v=\"99.0.0.0\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Model": "",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Viewport-Width": "1912"
        }

    def get_post(self):
        try:
            res = self.http.get(
                url=f'https://mbasic.facebook.com/groups/{self.uid_group}'
            )
        except:
            try:
                res = self.http.get(
                    url=f'https://mbasic.facebook.com/groups/{self.uid_group}'
                )
            except:
                return []
        if 'mbasic_logout_button' in res.text:
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.select('a:contains("Toàn bộ tin")')
            datas = []
            for link in links:
                uid_post = link["href"].split('/permalink/')[1].split('/')[0]
                datas.append({
                    'uid': uid_post,
                    'url': link['href']
                })
            return datas
        print('Tài Khoản Đã Toang , Vui Lòng Thử Acc Khác Nhé [#1]')
        return []

    def del_post(self, data: dict):
        uid = data['uid']
        print('Đang xóa bài viết UID=', uid)
        url = data['url']
        res = self.http.get(
            url=url
        )
        if 'mbasic_logout_button' in res.text:
            soup = BeautifulSoup(res.text, 'html.parser')
            try:
                delete_links = soup.find_all(
                    'a', href=lambda href: href and '/delete.php?' in href)[0]
                res_del = self.http.get(
                    url='https://mbasic.facebook.com'+delete_links['href'])
                if 'mbasic_logout_button' in res_del.text:
                    soup = BeautifulSoup(res_del.text, 'html.parser')
                    action = soup.find_all('form', method='post')[0]['action']
                    fb_dtsg = soup.find('input', {'name': 'fb_dtsg'})['value']
                    jazoest = soup.find('input', {'name': 'jazoest'})['value']
                    payloads = {
                        'fb_dtsg': fb_dtsg,
                        'jazoest': jazoest
                    }
                    exe = self.http.post(
                        url='https://mbasic.facebook.com'+action,
                        data=payloads
                    )
                    print(f'[{str(self.count_del)}]Đã xóa hoàn tất ->', uid)
                    with open('result.txt', '+a', encoding='utf-8') as f:
                        f.write(f'{self.uid_group}|{uid}\n')
                    self.count_del += 1
                    return True
                else:
                    print('Tài Khoản Đã Toang , Vui Lòng Thử Acc Khác Nhé[#3]')
                    return None
            except:
                return True
        else:
            print('Tài Khoản Đã Toang , Vui Lòng Thử Acc Khác Nhé[#2]')
            return None

    def run(self):
        for x in range(999999):
            datas = self.get_post()
            if datas == []:
                break
            print('Tìm thấy [', len(datas), '] Bài viết')
            for data in datas:
                exes = self.del_post(data)
                if exes == None:
                    break
                time.sleep(delay)
            if exes == None:
                break



Main(cookie, uid_group).run()
