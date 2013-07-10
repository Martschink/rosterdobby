#!/usr/bin/env python
# -*- coding: utf-8 -*-



def tempTable(stuff, name):
    tableName = "/home/tree/rosterdobby/{NAME}.csv".format(NAME=name)
    cfile = open(tableName, "wb")
    writer = csv.writer(cfile)
    for row in stuff:
        writer.writerow(row)
    cfile.close()


def srapeBatters():
    sack=[]
    IP=0
    for startIndex in range(0,2150, 50):
        print season, startIndex
        if startIndex == 0:
            FAurl="http://games.espn.go.com/flb/freeagency?leagueId=55354&teamId=13&seasonId={season}"
        else:
            FAurl="http://games.espn.go.com/flb/freeagency?leagueId=55354&teamId=13&seasonId={season}&startIndex="+str(startIndex)

        page = mech.open(FAurl.format(season=str(season))).read()
        playersheet=page.split("playerId=")
        for p in playersheet[3:-1]:
            #AB="fred"
            try:
                AB=p.split("<td class=\"playertableStat \">")[1].split("</td>")[0].split("/")[-1]
            except:
                AB="error"
            playerID=int(p.split(" team")[0].strip("\""))
            name=p.split("</a>")[0].split(">")[-1]
            if AB =="--" or AB=="error":
                AB=0
            #print playerID, name, AB, IP
            sack.append((season, playerID, name, int(AB), int(IP)))
    #tempTable(sack,"minors")
    return sack



def srapePitchers():
    bucket=[]
    AB=0
    for startIndex in range(0,2150, 50):
        if startIndex == 0:
            FAurl="http://games.espn.go.com/flb/freeagency?leagueId=55354&teamId=13&seasonId={season}&slotCategoryGroup=2"
        else:
            FAurl="http://games.espn.go.com/flb/freeagency?leagueId=55354&teamId=13&seasonId={season}&slotCategoryGroup=2&startIndex="+str(startIndex)
        page = mech.open(FAurl.format(season=str(season))).read()
        playersheet=page.split("playerId=")
        #playersheet=page.split("playerid=")
        #print "split!"
        #print len(playersheet)
        for p in playersheet[3:-1]:
            name=p.split("</a>")[0].split(">")[-1]
            playerID=int(p.split(" team")[0].strip("\""))
            try:
                IP = p.split("<td class=\"playertableStat \">")[1].split("</td>")[0]
            except:
                IP="error"
            #playerID=int(p.split(" league")[0].strip("\""))
            print name, str(playerID), str(IP)

            #("<td class=\"playertableStat \">")[1].split("</td>")[0].split(“/”)[1]
            #IP = p.split("<td class=\"playertableStat \">")[1].split("</td>")[0]
            if IP =="--" or IP=="error":
                IP=0

            bucket.append((season, playerID, name, int(AB), int(IP)))
    #tempTable(bucket,"minors")
    return bucket


def sumTotals(bag, players2012):
    sack=[]
    IDs=set([b[1] for b in players2012])
    IDs=list(IDs)
    for i in IDs:
        g = zip(*[b for b in bag if b[1]==i])
        ab = sum(g[3])
        ip = sum(g[4])
        name = g[2][0]
        sack.append((i, name, ab, ip))
    tempTable(sack,"minorT")


from mechanize import Browser; import os, csv, datetime, cookielib, urllib2; mech = Browser()
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#cj = cookielib.LWPCookieJar()

#mech.set_cookiejar(cj)


def main():
    global season
    bag=[]
    pitchers2012=[]
    batters2012=[]
    season="2012"
    batters2012 = srapeBatters()
    bag += batters2012
    #pitchers2012 = srapePitchers()
    #bag += pitchers2012
    players2012 = batters2012 + pitchers2012
    
    season = "2011"
    bag += srapeBatters()
    #bag += srapePitchers()

    season = "2010"
    bag += srapeBatters()
    #bag += srapePitchers()

    tempTable(bag,"minors")
    sumTotals(bag, players2012)
    return bag

    "&slotCategoryGroup=2"



if __name__ == '__main__':
    main()


