from dateutil.parser import parse
from datetime import datetime
from regex import B
import requests
import pandas as pd

class TwitCrawling:
    def __init__(self):
        '''
        기본 세팅
        url = twitter 검색용 API
        header = API 접속을 위해 사용되는 헤더값
        data_list = 저장되어 출력에 사용될 리스트
        '''
        self.url = f"https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_collab_control=false&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={keyword}&tweet_search_mode=live&count=10&query_source=typed_query&pc=1&spelling_corrections=1&include_ext_edit_control=false&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2Cvibe"
        self.payload={}
        self.headers = {
          'accept': '*/*',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
          'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
          'cookie': 'personalization_id="v1_Zc0GHJhGIwS2P+O4WPbmXw=="; guest_id=v1%3A159906270243976328; ads_prefs="HBERAAA="; auth_token=413da357c078452776e4e05fdb6669ff4729ce00; twid=u%3D1301187356704169984; ct0=0afe02f4cf489695b7947912150b576dfd2611c338023a8bd8bd1c92b3f0ba6e653e66478ccad76ca179f4c30a9f6b164229014e93267b850b3696094f489dfaeef2591d9fdec20e9787083fbe2a2a7f; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLNRCeB4AToMY3NyZl9p%250AZCIlNTFiZmExZGY5ZDY5YTExOGMyOGY3NTg4NzlhYjczYzM6B2lkIiU2NDY4%250AMjk5ZWUwY2Y5ZmY5YzBhYjZjNWRiZjM2MjQ5Zg%253D%253D--b1e5e044b0f748db1f4b542dd8893b8921f7ae1b; guest_id_marketing=v1%3A159906270243976328; guest_id_ads=v1%3A159906270243976328; lang=ko; _gid=GA1.2.840859223.1659527308; at_check=true; des_opt_in=Y; _gcl_au=1.1.1387820004.1659528867; mbox=session#301cb4c62777489083c6ad3e02f7b0f3#1659530763|PC#301cb4c62777489083c6ad3e02f7b0f3.32_0#1722773703; _ga_34PHSZMC42=GS1.1.1659528867.1.1.1659528905.0; _ga=GA1.2.1341567002.1640257224; external_referer=padhuUp37zjSzNXpb3CVCQ%3D%3D|0|8e8t2xd8A2w%3D; guest_id=v1%3A165953317685962868; guest_id_ads=v1%3A165953317685962868; guest_id_marketing=v1%3A165953317685962868; personalization_id="v1_zni44KUYlF82agxSopwkSw=="',
          'referer': 'https://twitter.com/search?q=%EB%94%94%EB%A7%A5&src=typed_query&f=live',
          'sec-ch-ua': '"Chromium";v="102", " Not A;Brand";v="99"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 Safari/537.36',
          'x-csrf-token': '0afe02f4cf489695b7947912150b576dfd2611c338023a8bd8bd1c92b3f0ba6e653e66478ccad76ca179f4c30a9f6b164229014e93267b850b3696094f489dfaeef2591d9fdec20e9787083fbe2a2a7f',
          'x-twitter-active-user': 'yes',
          'x-twitter-auth-type': 'OAuth2Session',
          'x-twitter-client-language': 'ko'
        }
        self.data_list = []
        
    def date_format_processor(self, date):
        '''
        날짜 가공용
        '''
        change_time = parse(date.replace('|',' ')).strftime("%Y.%m.%d.%H.%M")
        return change_time
    
    def delrn(self, text):
        '''
        텍스트 가공용
        '''
        return text.replace("\t","").replace("\n","").replace("\r","").lstrip().rstrip()
    
    
    def KeywordSearch(self, keyword, limit):
        
        '''
        키워드를 통한 검색
        '''
        
        url = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_collab_control=false&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={keyword}&tweet_search_mode=live&count=10&query_source=typed_query&pc=1&spelling_corrections=1&include_ext_edit_control=false&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2Cvibe'
        count = 0
        old_count = 0
        reurl = url
        
        self.keyword = keyword
        response = requests.get(self.url.format(keyword = keyword), headers=self.headers)
        while True:
            self.keyword = keyword
            response = requests.get(reurl.format(keyword = keyword), headers=self.headers)
            print(response.text)
            '''
            같은 키워드의 신규 데이터 추출시 cursor를 통해서 스크롤 내렸다는 신호를 전달
            '''
            try:
                self.headers.update({'cursor':response.json()['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']})
                reurl = url+'&cursor='+response.json()['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']
            except:
                self.headers.update({'cursor':response.json()['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']})
                reurl = url+'&cursor='+response.json()['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
            
            for key in response.json()['globalObjects']['tweets']:
                try:
                    place = response.json()['globalObjects']['tweets'][key]['place']
                except:
                    place = ''
                try:
                    data_out = {
                    'key' : key,
                    'keyword' : keyword,
                    'user_id' : response.json()['globalObjects']['tweets'][key]['user_id_str'],
                    'user_name' : response.json()['globalObjects']['users'][response.json()['globalObjects']['tweets'][key]['user_id_str']]['name'],
                    'contents' : self.delrn(response.json()['globalObjects']['tweets'][key]['full_text']),
                    'retweet' : response.json()['globalObjects']['tweets'][key]['retweet_count'],
                    'favorite' : response.json()['globalObjects']['tweets'][key]['favorite_count'],
                    'place' : place,
                    'date' : self.date_format_processor(response.json()['globalObjects']['tweets'][key]['created_at']),
                }
                    self.data_list.append(data_out)
                    print(data_out)
                except Exception as e:
                    print(e)
                    continue
            if old_count == len(self.data_list):
                break
            else :
                old_count =len(self.data_list)
            count = count + 1
            print(keyword+' '+str(len(self.data_list))+'개 추출')
            if count == limit:
                break
    
    def AccountSearch(self, keyword, limit):
        '''
        계정을 통한 검색
        '''
        url = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_collab_control=false&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=(from%3A{keyword})&tweet_search_mode=live&count=20&query_source=typed_query&pc=1&spelling_corrections=1&include_ext_edit_control=false&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2Cvibe'
        count = 0
        reurl = url
        old_count = 0
        while True:
            self.keyword = keyword
            response = requests.get(reurl.format(keyword = keyword), headers=self.headers)
            print(response.text)
            try:
                self.headers.update({'cursor':response.json()['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']})
                reurl = url+'&cursor='+response.json()['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']
            except:
                self.headers.update({'cursor':response.json()['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']})
                reurl = url+'&cursor='+response.json()['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
            
            for key in response.json()['globalObjects']['tweets']:
                try:
                    place = response.json()['globalObjects']['tweets'][key]['place']
                except:
                    place = ''
                try:
                    data_out = {
                    'key' : key,
                    'keyword' : keyword,
                    'user_id' : response.json()['globalObjects']['tweets'][key]['user_id_str'],
                    'user_name' : response.json()['globalObjects']['users'][response.json()['globalObjects']['tweets'][key]['user_id_str']]['name'],
                    'contents' : self.delrn(response.json()['globalObjects']['tweets'][key]['full_text']),
                    'retweet' : response.json()['globalObjects']['tweets'][key]['retweet_count'],
                    'favorite' : response.json()['globalObjects']['tweets'][key]['favorite_count'],
                    'place' : place,
                    'date' : self.date_format_processor(response.json()['globalObjects']['tweets'][key]['created_at']),
                }
                    self.data_list.append(data_out)
                except Exception as e:
                    print(e)
                    continue
            if old_count == len(self.data_list):
                break
            else :
                old_count =len(self.data_list)
            count = count + 1
            print(keyword+' 키워드의 트윗 '+str(len(self.data_list))+'개 추출')
            if count == limit:
                break
            
        
    def getCSV(self, keyword):
        '''
        Json형식으로 저장된 데이터를 CSV로 변환하여 출력
        '''
        today = datetime.now().now().strftime("%Y%m%d%H%M")
        pd.DataFrame(self.data_list).to_csv(today+"_"+keyword+".csv", encoding='utf-8-sig')
        print('[ * ] getCSV terminated')


if __name__=="__main__":
    
    '''
    keyword = 검색할 키워드 ex)감자 or계정 검색시 @ManUtd가 아닌 ManUtd로
    date_start = 검색 기준 시작일 ex)2022-08-06 기간 세팅 안할시 date_end와 같이 ''로 기입
    date_end = 검색 기준 종료일 ex)2022-10-10
    type = 검색 타입(1 : 키워드 검색, 2 : 계정 검색)
    limit = 페이지 갯수 제한(수집될 갯수 제한이 아닙니다. 페이지 제한입니다.)
    '''
    
    keyword = 'ManUtd'
    date_start = '2022-04-01' 
    date_end = '2022-05-31'
    type = 2
    limit = 1000
    
    c = TwitCrawling()
    if type == 1:
        if date_start == '':
            c.KeywordSearch(keyword, limit)
        else :
            c.KeywordSearch(keyword+' until:'+str(date_end)+' since:'+str(date_start), limit)
    elif type == 2:
        if date_start == '':
            c.AccountSearch(keyword, limit)
        else :
            c.AccountSearch(keyword+' until:'+str(date_end)+' since:'+str(date_start), limit)  
    c.getCSV(keyword)
  
