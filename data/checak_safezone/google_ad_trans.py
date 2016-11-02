# 구글에서 취득한 영문 주소를 국문 주소로 변환 하기 위한 코드입니다.
# 개발 : https://github.com/MaseKor

import requests
from bs4 import BeautifulSoup

url = 'https://www.google.co.kr/search?q='


def trans_ad(ad_en):
    """
    영문주소를 입력하면 구글에 검색한뒤 bs4로 주소만 크롤해줍니다.
    :param ad_en: 영문 주소
    :return: 튜플 ( 성공여부, 결과 메시지) ; 크롤 실패시: 0, 성공시:1, 주소 오류시: 2
    """
    sourcecode = requests.get(url + ad_en)
    try:
        plaintext = sourcecode.text
        soup = BeautifulSoup(plaintext, "html.parser")
        ad_ko = soup.find_all('b')[1].contents[0]

        # 변환된 주소 결과의 단어가 3개가 안될경우( 일번적으로 주소는 3개이상의 단어로 구성됨)
        if len(ad_ko.split()) < 3:
            return (2, "변환된 값이 주소가 아닌거 같습니다. {}".format(ad_ko))

    except Exception as e:
        return (0, "크롤링중 오류가 발생 했습니다.")
    return (1, ad_ko)
