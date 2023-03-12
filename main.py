import sys
import requests
import random
import time
import threading
from colorama import init
from colorama import Fore
init()

##

cookies = {
    'GuestData': 'UserID=-1069296614',
    '_ga': 'GA1.2.640812422.1644076282',
    '.RBXID': '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzY2Q4ZWViNS04MTgxLTRkYmYtODlhNS1jZDVmYzQyMGI2OWIiLCJzdWIiOjEyNTk5NTA0fQ.T1Tt_W4UacZWCLrkH5LREXggm071K7bCzOdWViYDXQQ',
    'RBXImageCache': 'timg=34326163303531302D626364362D343562652D613538642D35633931336439343262386525322E3132362E33332E323725352F31392F3230323220373A33303A343320504D3D0F2D4416689800450CF7E280018438C43699C1',
    '.RBXIDCHECK': '856d9b8e-d91a-4ee9-91ca-306a9121c93e',
    'RBXEventTrackerV2': 'CreateDate=5/19/2022 2:31:45 PM&rbxid=1037119901&browserid=127184796125',
    'RBXMarketing': 'FirstHomePageVisit=1',
    '.ROBLOSECURITY': 'cookie here',
    '_gid': 'GA1.2.811902199.1656457439',
    'RBXSessionTracker': 'sessionid=cfa50b58-69d9-4293-bbc3-12b81d653d8c',
}

headers = {
    'authority': 'trades.roblox.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=UTF-8',
    'x-csrf-token': requests.post("https://auth.roblox.com/v2/logout", cookies=cookies).headers['X-CSRF-TOKEN'],
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.roblox.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.roblox.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
}

global queue
global old
global uadsend
global total
old = 0
queue = 0
total = 0
session = requests.session()
itemtable = requests.get("https://www.rolimons.com/itemapi/itemdetails").json()['items']
myitems = []
myvalues = []
already = []
already2 = []
blacklisted = []
ids = []
tradequeue = []
trademsgs = []

##

def getSellers():
    preys = []
    chosen = random.randint(1, 2064)

    while chosen in already:
        chosen = random.randint(1, 2064)

    response = session.get(f'https://economy.roblox.com/v1/assets/{ids[chosen]}/resellers', cookies=cookies, headers=headers).text.split("id")

    for userid in response:
        if userid.find("name") and userid.find("userAssetId"):
            id = userid.strip('":').split(",")[0]

            if not "null" in id and id.isnumeric() and not id in preys and not id in already2:
                preys.append(id)
                already.append(chosen)
                already2.append(id)

    return preys


def getValue(item, type):
    demand = itemtable[item][5]

    if demand == 4:
        demand = 1.05
    elif demand == 3:
        demand = 1.025
    elif demand == 2:
        demand = 1.00
    elif demand < 1:
        demand = .95
    else:
        demand = .95


    if itemtable[item][2] != itemtable[item][4]:
        demand += .05


    if itemtable[item][6] != -1:
        demand += .05


    newvalue = itemtable[item][4] * demand
    type.append(newvalue)


def getLimiteds(current):
    preyvalues = []
    preyitems = []
    response = session.get(f"https://inventory.roblox.com/v1/users/{current}/assets/collectibles?assetType=Hat&sortOrder=Asc&limit=100", headers=headers)
    response2 = session.get(f"https://inventory.roblox.com/v1/users/{current}/assets/collectibles?assetType=Face&sortOrder=Asc&limit=100", headers=headers)

    if "userAssetId" in response.text:
        for id in response.json()['data']:
            id = str(id['assetId'])

            if id in itemtable and id not in blacklisted:
                preyitems.append(id)
                getValue(id, preyvalues)


    if "userAssetId" in response2.text:
        for id in response2.json()['data']:
            id = str(id['assetId'])

            if id in itemtable and id not in blacklisted:
                preyitems.append(id)
                getValue(id, preyvalues)


    return preyitems, preyvalues


def getMyitems():
    global uadsend
    myvalues.clear()
    myitems.clear()
    uadsend = session.get(f"https://www.rolimons.com/api/playerassets/1040172374", headers=headers).json()['playerAssets']
    headers['x-csrf-token'] = requests.post("https://auth.roblox.com/v2/logout", cookies=cookies).headers['X-CSRF-TOKEN']

    for item in uadsend:
        if item.isnumeric() and item not in blacklisted:
            myitems.append(item)
            getValue(item, myvalues)


    print(Fore.YELLOW + "Checked your inventory.")


def sendTrade(send, req, msg, current):
    global uadsend
    tempcurrent = current
    send2 = []
    req2 = []
    response = session.get(f"https://www.rolimons.com/api/playerassets/{tempcurrent}", headers=headers).json()['playerAssets']

    for uad in uadsend:
        if uad.isnumeric() and uad in send:
            send2.append(uadsend[uad][0])


    for uad in response:
        if uad.isnumeric() and uad in req:
            req2.append(response[uad][0])


    json_data = {
        'offers': [
            {
                'userId': tempcurrent,
                'userAssetIds': req2,
                'robux': None,
            },

            {
                'userId': 1040172374,
                'userAssetIds': send2,
                'robux': None,
            },
        ],
    }

    tradequeue.append(json_data)
    trademsgs.append(msg)
    sys.exit()


def searchTrade(preyitems, preyvalues, current):
    global queue
    offer = []
    offervalue = 0
    request = []
    requestvalue = 0

    try:
        if len(myitems) < 3:  # downgrade
            max = 0
            offer.append(myitems[0])
            offervalue = myvalues[0] / 4

            for i in range(len(preyitems)):
                difference = lambda list_value: abs(list_value - offervalue)
                closest = min(preyvalues, key=difference)
                overpay = round(((offervalue - closest) / offervalue) * 100, 1)
                index = preyvalues.index(closest)
                item = preyitems[index]

                if -5 < overpay < -2 or max >= 4:
                    break


                if itemtable[item][7] == -1:
                    request.append(item)
                    requestvalue += preyvalues[index]


                del preyitems[index]
                del preyvalues[index]
                max += 1

            overpay = round(((offervalue * 4 - requestvalue) / requestvalue) * 100, 1)

            if len(offer) <= len(request) and -5 < overpay < -2 and requestvalue > 0:
                valex = "[" + str(round(offervalue, 0)) + " -> " + str(round(requestvalue, 0)) + "]"
                msg = "Sent trade -> [" + str(overpay) + "% ↓] [Upgrade] " + valex
                thread = threading.Thread(target=sendTrade, args=(offer, request, msg, current)).start()
                queue += 1
            else:
                print(Fore.WHITE + "[" + str(round(offervalue * 4, 0)) + " -> " + str(round(requestvalue, 0)) + "]")
        else:  # upgrade
            max = 0

            for i in range(len(myitems)):
                if max > 3:
                    break


                offer.append(myitems[i])
                offervalue += myvalues[i]
                max += 1

            difference = lambda list_value: abs(list_value - offervalue)
            closest = min(preyvalues, key=difference)
            overpay = round(((offervalue - closest) / offervalue) * 100, 1)
            item = preyitems[preyvalues.index(closest)]
            request.append(item)

            if len(offer) > len(request) and 0 < overpay < 2.5 and itemtable[item][7] == -1:
                print(Fore.LIGHTWHITE_EX + "[" + str(overpay) + "%] " + "[" + str(len(offer)) + "->" + str(len(request)) + "]")
                print(Fore.YELLOW + current + " -> Added to queue. " + "[" + str(queue) + " in queue.]")

                queue += 1
                valex = "[" + str(round(offervalue, 0)) + " -> " + str(round(closest, 0)) + "]"
                msg = "Sent trade -> [" + str(overpay) + "% ↓] [Upgrade] " + valex
                thread = threading.Thread(target=sendTrade, args=(offer, request, msg, current)).start()
            else:
                print(Fore.WHITE + "[" + str(round(offervalue, 0)) + " -> " + str(round(requestvalue, 0)) + "]")
    except:
        None



def main():
    while True:
        preys = getSellers()

        if queue > 10:
            time.sleep(100)

            getMyitems()


        if len(preys) < 1:
            continue


        for userid in preys:
            preyitems, preyvalues = getLimiteds(userid)

            if len(preyvalues) < 2:
                continue


            searchTrade(preyitems, preyvalues, userid)


with open("ids.txt",) as txt:
    for id in txt.readlines():
        ids.append(id.strip('\n'))


with open("blacklisted.txt") as txt:
    for id in txt.readlines():
        blacklisted.append(id.strip('\n'))


getMyitems()
threading.Thread(target=main).start()


while True:
    t = 0

    while (t < 31):
        t += 1

        time.sleep(1)


    if len(tradequeue) > 0:
        json_data = tradequeue[0]
        msg = trademsgs[0]
        response = session.post('https://trades.roblox.com/v1/trades/send', cookies=cookies, headers=headers, json=json_data)
        queue -= 1
        del tradequeue[0]
        del trademsgs[0]

        if response.status_code == 200:
            total += 1
            print(Fore.GREEN + msg + " [" + str(total) + " sent.]")
        else:
            print(Fore.RED + response.text)

