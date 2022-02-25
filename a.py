from sys import stdin, stdout
from operator import itemgetter


c = {}
p = {}

n, m = map(int, stdin.readline().strip().split())
for i in range(n):
    nom, sk = stdin.readline().strip().split()
    c[nom] = {}
    for j in range(int(sk)):
        skill, level = stdin.readline().strip().split()
        level = int(level)
        c[nom][skill] = level
    c[nom]["occ"] = False

for k in range(m):
    name, days, points, bbd, contrib = stdin.readline().strip().split()
    if not (bbd < days):
        sk = {}
        p[name] = (name, days, bbd, sk)
        for l in range(int(contrib)):
            skill, level = stdin.readline().strip().split()
            if skill in p[name][3].keys():
                if type(p[name][3][skill]) == list:
                    p[name][3][skill].append(skill)
                else:
                    p[name][3][skill] = [p[name][3][skill], level]
            else:
                p[name][3][skill] = level
    else:
        for l in range(int(contrib)):
            skill, level = stdin.readline().strip().split()


days = 0
working_projects = []
num_projects = 0
res = ""
stop = False
while len(p.keys()) and not stop:
    stop = True
    for name in p.keys():
        if p[name] != 0:
            project = p[name]
            pendent_contribs = {}
            finished = True
            contrib_order = []
            for skill, level in project[3].items():
                if type(level) == int:
                    finded = False
                    for contrib, c_skills in c.items():
                        if c_skills["occ"] == False and skill in c_skills.keys() and contrib not in contrib_order:
                            c_skill_level = c_skills[skill] 
                            if int(level) > c_skill_level:
                                continue
                            else:
                                pendent_contribs[contrib] = skill
                                contrib.append(contrib_order)
                                finded = True
                                break
                    if not finded:
                        finished = False
                        break
                else:
                    for lev in level:
                        finded = False
                        for contrib, c_skills in c.items():
                            if c_skills["occ"] == False and skill in c_skills.keys() and contrib not in contrib_order:
                                c_skill_level = c_skills[skill] 
                                if int(lev) > c_skill_level:
                                    continue
                                else:
                                    pendent_contribs[contrib] = skill
                                    contrib_order.append(contrib)
                                    finded = True
                                    break
                        if not finded:
                            finished = False
                            break

            if finished:
                res += project[0] + "\n"
                num_projects += 1
                for contrib in contrib_order:
                    res += contrib + " "
                    c[contrib]["occ"] = True
                    if c[contrib][pendent_contribs[contrib]] == project[3][pendent_contribs[contrib]]:
                        c[contrib][pendent_contribs[contrib]] += 1
                working_project = [int(project[1]), pendent_contribs]
                working_projects.append(working_project)
                p[project[0]] = 0
                res += "\n"
                
                if stop:
                    stop = False

    if len(working_projects) > 0:
        stop = False
        working_projects = (sorted(working_projects, key=itemgetter(0)))
        advanced_days = int(working_projects[0][0])
        liberated_contribs = working_projects[0][1]
        del working_projects[0]
        for i in range(len(working_projects)):
            working_projects[i][0] -= advanced_days
        days += advanced_days
        for liberated_contrib in liberated_contribs:
            c[liberated_contrib]["occ"] = False

stdout.write(str(num_projects) + "\n")
stdout.write(res)
