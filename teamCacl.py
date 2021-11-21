import time
import math
import collections
import sys
import os
import re
import array

file = open("./results.txt")
lines = list(file.readlines())
teams = {}
for line in lines:
    reg = re.search("([A-Za-z\-']+)\s+([A-Za-z\-']+)\s+([A-Za-z\-']+)\s+([0-9]+)\s+([0-9]+)\s+(.*)", line)
    if reg != None:
        fName=reg.group(1)
        lName=reg.group(2)
        teamName=reg.group(3)
        OAPL=int(reg.group(4))
        TPL=int(reg.group(5))
        fTime=reg.group(6)
        if teamName not in teams.keys():
            teams[teamName] = {}
        teams[teamName][fName +" " + lName+ " "+fTime] = [OAPL, TPL]
individuals = []
nonTeam = []
for team in teams.keys():
    totalRunners = 0
    for runner in teams[team].keys():
        totalRunners += teams[team][runner][1]
    if totalRunners < 15:
        for runner in teams[team]:
            individuals.append(teams[team][runner][0])
        nonTeam.append(team)
individuals.reverse()
for team in teams.keys():
    for runner in teams[team].keys():
        if teams[team][runner][0] not in individuals:
            for ind in individuals:
                if teams[team][runner][0] > ind:
                    teams[team][runner][0]-=1
                    
scoreDict={}
for team in teams.keys():
    teamScore = 0
    for runner in teams[team]:
        if teams[team][runner][1] <= 5:
            teamScore+=teams[team][runner][0]
    scoreDict[team]=teamScore
placingList = []
for i in range(len(scoreDict)-len(nonTeam)):
    placingList.append("a")

for team in scoreDict.keys():
    teamsBeaten=0
    if team not in nonTeam:
        for OtherTeam in scoreDict.keys():
            if OtherTeam not in nonTeam and OtherTeam != team:
                if scoreDict[team] <= scoreDict[OtherTeam]:
                    teamsBeaten+=1
        if placingList[teamsBeaten] == "a":
            placingList[teamsBeaten] = team
        else:
            if teamsBeaten-1 >= 0:
                placingList[teamsBeaten-1] = team


placingList.reverse()

teamsOut={}
for team in placingList:
    for teamName in teams.keys():
        if team==teamName:
            teamsOut[team]=teams[teamName]
            teamsOut[team]["score"]=scoreDict[team]

placingList2=[]
for i in range(len(nonTeam)):
    placingList2.append("a")
for team in scoreDict.keys():
    teamsBeaten=0
    if team in nonTeam:
        for OtherTeam in scoreDict.keys():
            if (OtherTeam in nonTeam) and (OtherTeam != team):
                if scoreDict[team] <= scoreDict[OtherTeam]:
                    teamsBeaten+=1
        if placingList2[teamsBeaten] == "a":
            placingList2[teamsBeaten] = team
        else:
            if teamsBeaten-1 > 0:
                placingList2[teamsBeaten-1] = team
placingList2.reverse()

for notaTeam in nonTeam:
    for teamName in teams.keys():
        if notaTeam==teamName:
            teamsOut[notaTeam]=teams[notaTeam]
            teamsOut[notaTeam]["score"]=scoreDict[notaTeam]

for team in teamsOut.keys():
    file2 = open("results2.txt", 'a+')
    file2.write('\n')
    file2.write(team + "  -  " + str(teamsOut[team]["score"]))
    file2.write('\n\n')
    for runner in teamsOut[team].keys():
        file2.write(runner+" "+str(teamsOut[team][runner])+"\n")
    file2.write('\n')

