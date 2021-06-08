from slack import WebClient
from lunchparty import Lunchparty
import json
import os
import random
token=""
slack_web_client = WebClient(token=token)
filterList = ["sean.you"]

def getDefaultFilterList():
    return ["sean.you"]

def initFilterList():
    filterList = getDefaultFilterList()

def sendMessageToChannel(channel :str = "#lunchpartytest"):
    # 채널 세부정보 -> 더보기 -> 앱추가
    lunchBot = Lunchparty(channel)
    message = lunchBot.getMessagePayload()
    slack_web_client.api_call(api_method='chat.postMessage', json = message)

def getAllChanellList():
    cursor = None
    dict = {}
    count = 0
    end = False
    while not end:
        params = {}
        limit = 500
        params["limit"] = limit
        params["types"] = "private_channel"
        if cursor:
            params['cursor'] = cursor
        res = slack_web_client.api_call(
            api_method="conversations.list",
            params=params
        )

        for usergroup in res["channels"]:
            if usergroup['id'] not in dict:
                dict[usergroup['id']] = True
                count += 1
                print(usergroup['name'], usergroup['id'])
            else:
                end = True
                break
        if len(res['channels']) <= limit:
            end = True
        cursor = res.data['response_metadata']['next_cursor']
    print(count)

def getUsersInfoByIds(user_ids = ["U01G3KT8KML"]):
    ret = []
    for user_id in user_ids:
        params = {"user":user_id}
        res = slack_web_client.api_call(api_method='users.info', params = params)
        ret.append(res.data)
    return ret


def filterAndExtractName(usersInfoData):
    n = len(usersInfoData)
    # filterList = ["sean.you",
    #               "flo.kim",
    #               "hector.kang",
    #               "tony.s",
    #               "rocket.m",
    #               "lapin.hong",
    #               "pia.no",
    #               "hubert.bear",
    #               "harry.hoon",
    #               ]

    for i, userInfoData in enumerate(usersInfoData[::-1]):
        # print(-1 - i, userInfo)
        if userInfoData['user']['is_bot'] or userInfoData['user']['name'] in filterList:
            usersInfoData.pop(n - i - 1)
    return list(map(lambda x: x['user']['name'], usersInfoData))

def getAllMemberOfChannel(channelId = "C0219J2E9GB"):
    #default lunchpartytest C0219J2E9GB
    # 택시개발파트 C0129126URK
    # U01G3KT8KML, U0212JBCWBG
    #default 100명
    params = {"token":token, "channel":channelId}
    res = slack_web_client.api_call(api_method="conversations.members",
                                    params = params)
    ret = list(map(lambda x : x['members'], res))[0]
    return ret
    # print(len(res['members']))
    # print(res)

def makeParty(allMembers : list):
    #리얼 유저만 들어온다고 가정
    limit = 4
    n = len(allMembers)
    partyCount = (n + limit - 1) // limit
    parties = [[]for _ in range(partyCount)]
    allMembers.sort(key = lambda x : random.randint(1,100))
    for i, member in enumerate(allMembers):
        parties[i % partyCount].append(member)
    return parties

def sendParty(channel : "lunchpartytest", partyMembers, partyNumber:int):
    params = {'channel':channel}
    textBuilder = []

    textBuilder.append(partyNumber.__str__())
    textBuilder.append(" 파티 : ")
    for member in partyMembers:
        textBuilder.append(member)
        textBuilder.append("  ")
    text = "".join(textBuilder).rstrip()
    params["text"] = text

    slack_web_client.api_call(
        api_method='chat.postMessage',
        params = params
    )

def getConversationHistory(channel):
    params = {'channel': channel}
    res = slack_web_client.api_call(
        api_method='conversations.history',
        params=params
    )
    print(res)


def deleteChat(channel : "lunchpartytest", ts : str):
    res = slack_web_client.chat_delete(
        channel=channel,
        ts=ts
    )

    print(res)

def sendJoinParty(channel : "lunchpartytest"):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "곧 점심시간입니다. (deafult : 같이먹어요)"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "같이먹어요"
                    },
                    "style": "primary",
                    "value": "join"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",

                        "text": "따점"
                    },
                    "style": "danger",
                    "value": "absent"
                }
            ]
        }
    ]

    params = {'channel':channel, "blocks":blocks}

    slack_web_client.api_call(
        api_method='chat.postMessage',
        params=params
    )

def join(name : str):
    if name in filterList:
        filterList.remove(name)

def absent(name : str):
    if name not in filterList:
        filterList.append(name)

def getParty():
    return filterList


def getDummyParty():
    dummyParty = [["sean.you",
                  "flo.kim",
                  "hector.kang",
                  "tony.s"],[
                  "rocket.m",
                  "lapin.hong",
                  "pia.no",
                  "hubert.bear",
                  "harry.hoon",
                  ]]
    return dummyParty

def test():
    #택시 백엔드 아이디 알려면 얘가 거기 들어가야
    #택시백엔드 G015Q3N2RQS
    #lunchpartyprivate C022QR3VCQ0


    targetChannelId = "C022QR3VCQ0"
    channelName = "lunchpartyprivate"
    # channelMembers = getAllMemberOfChannel(targetChannelId)
    # infos = getUsersInfoByIds(channelMembers)
    # filteredInfos = filterAndExtractName(infos)
    # partyList = makeParty(filteredInfos)
    partyList = getDummyParty()

    for i, party in enumerate(partyList, 1):
        sendParty(channelName, party, i)

# getConversationHistory("lunchpartytest")

if __name__ == '__main__':
    # getConversationHistory("G015Q3N2RQS")
    # deleteChat("C0219J2E9GB",'1621110113.001900')
    # filterList = getDefaultFilterList()
    # sendJoinParty("lunchpartyprivate")
    test()
    # getAllChanellList()

#TODO pia.no @ 알림? filter 어떻게 구현할지? 메서지 버튼 + 디비 사용? 인메모리?
# 11시 20분쯤 참가 하는 메세지? 12시에 파티 결정 메세지
# slack app interactivity에 메세지받을 url 넣기
# post mapping server 구현(그런데 슬랙에서 이걸 볼 수 있어야 댐;;)
# 버튼 메세지 구현은 더이상 손 안봐도 될 것 같음. 그냥 저 액션 모두가 전송 되는듯
