import os
os.sys.path.append('..')

from miniCSRanking.wsgi import *
from CSRanking.models import *

def Add_Area():
    f = open("area.csv", "r")
    areas = []
    for line in f:
        areas.append(line.strip().split(","))
    for area in areas:
        Area.objects.get_or_create(name=area[0], direction=area[1])
    print("Add_Area Complete!")

def Add_Conference():
    f = open("conference.csv", "r")
    conf_list = []
    for line in f:
        conf_list.append(line.strip().split(","))
    for conf in conf_list:
        name, abbr= conf[0], conf[1]
        for year in range(2015, 2020):
            Conference.objects.get_or_create(name=name, abbr=abbr, year=year,
                                             DBLP="https://dblp.uni-trier.de/db/conf/%s/%s%d.html" % (abbr.lower(), abbr.lower(), year),
                                             Href="https://www.google.com.hk/search?q=%s%d" % (abbr, year))
    print("Add_Conference Complete!")

def Add_Conference_Area():
    f = open("conference_area.csv", "r")
    conference_areas = []
    for line in f:
        conference_areas.append(line.strip().split(","))
    for conf_area in conference_areas:
        conf_list = Conference.objects.filter(abbr=conf_area[0])
        area = Area.objects.get(name=conf_area[1])
        for conf in conf_list:
            Conference_Area.objects.get_or_create(conf_id=conf, area=area)
    print("Add_Conference_Area Complete!")

def Add_Institution():
    f = open("Institution.csv", "rb")
    institutions = []
    for line in f:
        line = line.decode("utf-8")
        institutions.append(line.strip().split(","))
    print(len(institutions))
    for institution in institutions:
        Institution.objects.get_or_create(name=institution[0], )
    print("Add_Institution Complete!")

def Add_Scholar():
    f = open("csrankings.csv", "rb")
    scholars = []
    for line in f:
        line = line.decode("utf-8")
        scholars.append(line.strip().split(","))
    print(len(scholars))
    #scholars = scholars[0:100]
    cnt = 0
    for scholar in scholars:
        cnt += 1
        if cnt % 1000 == 0: print(cnt)
        affiliation = Institution.objects.filter(name=scholar[1])
        if affiliation.exists():
            Scholar.objects.get_or_create(name=scholar[0], homepage=scholar[2],
                                      affiliation=affiliation[0],
                                      GoogleScholar="https://scholar.google.com/citations?user=%s"%(scholar[3]))
    print("Add_Scholar Complete!")

def Add_Paper():
    f = open("paper.csv", "rb")
    papers = []
    for line in f:
        line = line.decode("utf-8")
        papers.append(line.strip().split("***"))
    print(len(papers))
    #papers = papers[0:100]
    cnt = 0
    for paper in papers:
        cnt += 1
        if cnt % 1000 == 0: print(cnt)
        conf_ids = Conference.objects.filter(abbr=paper[3], year=int(paper[1]))
        for conf_id in conf_ids:
            Paper.objects.get_or_create(title=paper[0], year=int(paper[1]),
                                      href=paper[2],
                                      conf_id=conf_id)
    print("Add_Paper Complete!")

def Add_Paper_Author():
    f = open("paper_author.csv", "rb")
    paper_authors = []
    for line in f:
        line = line.decode("utf-8")
        paper_authors.append(line.strip().split("***"))
    print(len(paper_authors))
    paper_authors = paper_authors[90000:]
    cnt = 0
    for item in paper_authors:
        cnt += 1
        if cnt%1000 == 0: print(cnt)
        authors = Scholar.objects.filter(name=item[1])
        papers = Paper.objects.filter(title=item[0])
        for scholar in authors:
            for paper in papers:
                Scholar_Paper.objects.get_or_create(scholar_name=scholar, paper_title=paper)
    print("Add_Paper_Author Complete!")

def Add_Scholar_Area():
    Scholar_list = Scholar.objects.all()
    cnt = 0
    for scholar in Scholar_list:
        cnt += 1
        if cnt % 1000 == 0: print(cnt)
        scholar_area = set()
        Paper_list = Scholar_Paper.objects.filter(scholar_name=scholar)
        Conference_list = set()
        for paper in Paper_list:
            Conference_list.add(paper.paper_title.conf_id)
        for conf in Conference_list:
            Area_list = Conference_Area.objects.filter(conf_id=conf)
            for area in Area_list:
                scholar_area.add(area.area)
        for area in scholar_area:
            Scholar_Area.objects.get_or_create(scholar_name=scholar, area=area)
    print("Add_Scholar_Area Complete!")

def Add_Institution_homepage():
    f = open("institution_homepage.csv", "rb")
    institutions = []
    for line in f:
        line = line.decode("utf-8")
        institutions.append(line.strip().split(","))
    print(len(institutions))
    cnt = 0
    for ins in institutions:
        cnt += 1
        if cnt % 1000 == 0: print(cnt)
        a = Institution.objects.get(name=ins[0])
        if ins[1][0:8]!="https://" and ins[1][0:7]!="http://":
            ins[1] = "http://" + ins[1]
        a.homepage = ins[1]
        a.save()
        #print(a.name, a.homepage)
    print("Add_Institution_homepage Complete!")

def Add_DBLP():
    f = Scholar.objects.all()
    print(len(f))
    cnt = 0
    for sch in f:
        cnt += 1
        if cnt % 500 ==0: print(cnt)
        name = sch.name.strip().rsplit(' ', 1)
        if len(name) == 1:
            last_name = name[0]
            first_name = ""
        else:
            last_name = name[1]
            first_name = name[0].replace(".", "=").replace(" ", "_")
        if last_name[0] >= "0" and last_name[0] <= "9":
            name = sch.name.strip().rsplit(' ', 2)
            last_name = name[1] + "_" + name[2]
            first_name = name[0].replace(".", "=").replace(" ", "_")
        sch.DBLP = "https://dblp.uni-trier.de/pers/hd/" + last_name[0].lower() + "/" + last_name + ":" + first_name
        sch.save()
    print("Add Scholar DBLP Complete!")

def Add_pub():
    Scholar.objects.all().update(pub_cnt=0)
    Institution.objects.all().update(pub_cnt=0)
    schs = Scholar.objects.all()
    print(len(schs))
    cnt = 0
    for sch in schs:
        cnt += 1
        if cnt % 500 == 0: print(cnt)
        sch.pub_cnt = len(Scholar_Paper.objects.filter(scholar_name=sch))
        sch.save()
        ins = sch.affiliation
        ins.pub_cnt += sch.pub_cnt
        ins.save()
    print("Add Publication Complete!")

if __name__ == "__main__":
    #Add_Area()
    #Add_Conference()
    #Add_Conference_Area()
    #Add_Institution()
    #Add_Scholar()
    #Add_Paper()
    Add_Paper_Author()
    Add_Scholar_Area()
    Add_Institution_homepage()
    Add_DBLP()
    Add_pub()