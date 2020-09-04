import re
import json
import os
import requests
import multiprocessing

prefix = './'


def get_html(url, path, filename, save=True):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    cookie = 'lc-main-av=en_US; ubid-main-av=130-0340907-8115719; ubid-main=133-4731179-5965508; session-id=147-5019742-2461603; lc-main=en_US; at-main=Atza|IwEBILGFRveGRupYambyAf5Jdha2vuavEDh3dHEpseK3MRFegk4RcPa4w8kZ6K21N7UL0gS8KIMO5JyJV81LpU3Pz8CccV9zqtZNixI5azGiFFr2pRbS7Cjc11zLmqJa5SAAPyn7ueFsx1kb3BSXiIva1XPIx6ZhnMZ9pgT0dznDTWAlnrIKao9GYyCf3yGfV84hpLxF85vRdNj2LNiZjhNcYyb_pY3GaCp498COUazQVJacq9tsj5OP8_-3p8cyzrhpRHNEl8E4bCWv-ioBesuAUQp4ILKsjIfv8Y2OTpllRAUlMM49wY-WzlNmFzeuivAbuJPfvoXl4AOk_HMrJ7hjrguk_lMjRPppE5xA8f4Wc7HN13tj-x3gTiO_MCpmWM05ikvVnz8zKPr1iAGRZMqBMxFrNUJ3uy6Djc7lOGCam0lNl2Pl_JPoY8LmO9Uv5SF0ujA; sess-at-main="LKU8JN5R0JTHSaByrNdZGlzD5opqLA6Pegeav0Tz1Js="; sst-main=Sst1|PQF-w6JlglKP7Dt8A7U8Z63WC62K56j1xwWQoFLs7KSXPctqWfSk3p6pQ8xsviTO0A1GTGXU3rf6vYV6LmlZ6k6qund77tTb2_ixVfMpJ1T3lpHGhA0JFlD4N89exSYKiMYHnvN8j2VtNwvozheQ0TAboIdgDhGMBJVBpNiqmsnoh-OkLBQMfwa5dU6HPNZz-hs3EnZyv99rzAaxcVUHSxT0gTDja3WQEojNUFR1FOTI6FZ8S3R2nLpFJjcQZ7IxqymnOURUNmDkRT63G3wjHIV4PGuj-h6BiFg6ypxmB8MvuhEB3y3l7fOdsMtfzWF4q0912Mu_AAdRSuIQPcnY2D-NMw; aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjB9; aws-target-static-id=1590025021413-481398; aws-target-data=%7B%22support%22%3A%221%22%7D; s_fid=5317CD9703AA65F8-397C3E69E3ABE466; aws-ubid-main=360-8624470-7607633; regStatus=registering; aws-business-metrics-last-visit=1590165632252; session-id-time=2082787201l; i18n-prefs=CNY; s_vn=1621561021530%26vn%3D3; aws-target-visitor-id=1590025021416-605122.35_0; s_dslv=1597944694537; s_nr=1597944694543-New; sp-cdn="L5Z9:RU"; session-token=AVg/nMVf0s98rL3wVPiHsHsjfuwGCjDw4G5AZFXVC7gSeWCG4pN6d05tCESTXtsA/mRJNTSoTMAdq+tlzEw29C0dGnt3Zld5cYr9Ma29ESkGVCYj3Dj15GFofoW6Agxq+80/Lg/XAaoZRwQpvz0f4okbDB1UkjwLlbvhvJBDpCCeCda5H+xgmWtvQI2hmh4P; csm-hit=tb:s-CGN84PJQTRYXHKESSKW6|1599122418872&t:1599122419429&adb:adblk_no'
    proxies = {'http': '127.0.0.1:1080'}
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}
    while True:
        try:
            get_source = requests.get(url, headers=headers, cookies=cookie_dict, proxies=proxies)
        except:
            print('[RETRY]', url)
        else:
            break
    text = get_source.text

    if save:
        with open(path + filename, 'w', encoding='utf-8') as f:
            f.write(text)
        f.close()

    return text


def save_page(url, path, recurrent):
    text = get_html(url, path, '/main.html')
    for i in range(2, 2 + recurrent):
        p = re.compile('<li class="a-normal"><a href="(.*?)">' + str(i) + '</a></li>')
        for next in re.finditer(p, text):
            url = 'https://www.amazon.com' + next[1]
            print(path + '/' + str(i) + '.html')
        text = get_html(url, path, '/' + str(i) + '.html')


def save_item(url, path, recurrent):
    for i in range(recurrent):
        text = get_html(url, path, '/' + str(i) + '.html', save=False)
        p = re.compile('<a class="a-link-normal a-text-normal" href="(.*?)">', re.S)
        for index, item in enumerate(re.finditer(p, text)):
            item_url = 'https://www.amazon.com' + item[1]
            print(path + '/' + str(i) + '_' + str(index) + '.html')
            item_page = get_html(item_url, path, '/' + str(i) + '_' + str(index) + '.html')

        p = re.compile('a-last"><a href="(.*?)">Next', re.S)
        url = ''
        for next_page in re.finditer(p, text):
            url = 'https://www.amazon.com' + next_page[1]
            print(url)
        if url == '':
            break


def get_category(recurrent=5):
    with open(prefix + 'content.txt', 'r') as f:
        html = f.read()
    f.close()
    pattern = re.compile('" data-menu-id="(.*?)" data-parent-menu-id="1">.*?'
                         '<li><div class="hmenu-item hmenu-title">(.*?)</div></li>'
                         '(.*?)<li class="hmenu-separator"></li>', re.S)
    category = dict()
    for item in re.finditer(pattern, html):
        category[item[2]] = dict()
        process_pool = []

        if not os.path.exists(prefix + item[2]):
            os.mkdir(prefix + item[2])
        pat = re.compile('<li><a href="(.*?)" class="hmenu-item">(.*?)</a></li>', re.S)

        for subitem in re.finditer(pat, item[3]):
            category[item[2]][subitem[2]] = subitem[1]
            if not os.path.exists(prefix + item[2] + '/' + subitem[2]):
                os.mkdir(prefix + item[2] + '/' + subitem[2])
                print(item[2] + '/' + subitem[2])
                url = 'https://www.amazon.com' + subitem[1]
                p = multiprocessing.Process(
                    target=save_item,
                    args=(url, prefix + item[2] + '/' + subitem[2], recurrent,)
                )
                p.start()
                process_pool.append(p)

        for p in process_pool:
            p.join()

    category = json.dumps(category)
    with open(prefix + 'content.json', 'w') as f:
        f.write(category)
    f.close()


if __name__ == '__main__':
    get_category()
