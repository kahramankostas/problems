#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
from itertools import product


i=input()
i=i.split()
N,M,T,P,D=map(int, i)
#print(N,M,P,T,D)
edges=[]

for j in range(M):
    temp=[]
    i=input()
    i=i.split()
    l0, l1, l2, l3 = map(int, i)
    edges.append([l0,l1, l2, l3] )
targets=[]
for j in range(T):
    temp=[]
    i=input()
    i=i.split()
    l0, l1 = map(int, i)
    targets.append([l0,l1] )



kanallar={}
M=10
P=4
for i in range(P):
    kanallar[i]=[]
    for ii in range(M):
        kanallar[i].append(ii)


ids=defaultdict()
for i in edges:
    try:ids[i[1],i[2]].append(i[0])
    except:ids[i[1],i[2]]=[i[0]]


global paths
eklenen=[]

def add_edge(graph, u, v):
    graph[u].append(v)
    graph[v].append(u)  # Çift yönlü kenar ekle

def print_all_paths_util(graph, u, d, visited, path):
    visited[u] = True
    path.append(u)
    if u == d:
        # Rota tamamlandığında 'paths' listesine ekle
        paths.append(list(path))
    else:
        for i in graph[u]:
            if not visited[i]:
                print_all_paths_util(graph, i, d, visited, path)

    path.pop()
    visited[u] = False

def print_all_paths(graph, s, d):
    visited = [False] * len(graph)
    path = []
    print_all_paths_util(graph, s, d, visited, path)
V = 128 # Düğüm sayısı
graph = defaultdict(list)


for i in edges:
    add_edge(graph, i[1], i[2] )


rotas=defaultdict()
for i in targets:
    paths = []
    print_all_paths(graph, i[0], i[1])
    unique_paths=[]
    for p in paths:
        if p not in unique_paths:
            unique_paths.append(p)
    unique_paths.sort(key=len)
    rotas[i[0],i[1]]=unique_paths



def findway(way):
    input_list=[]
    for i  in range(len(way)-1):
        s = tuple(sorted([way[i], way[i + 1]]))
        input_list.append(ids[s])

    result = []
    for combination in product(*input_list):
        # Her bir kombinasyonun eleman sayısını kontrol et
        # Tek bir eleman varsa, direkt olarak sonuç listesine ekle
        if all(isinstance(item, int) for item in combination):
            result.append([item for item in combination])
        else:
            # Birden fazla eleman varsa, birleştirerek sonuç listesine ekle
            result.append([item for sublist in combination for item in sublist])

    return result
    


def kenar_ekle(result):
    kayip=[]
    for iii in result:
        for jj in kanallar:
            for j in iii:
                if j not in kanallar[jj]:
                    kayip.append(j)
    hist = {}
    for x in kayip:
        hist[x] = hist.get(x, 0) + 1
    for i in hist:
        if hist[i]>P:
            for j in kanallar:
                kanallar[j].append(len(edges))    
            ids[edges[i][1],edges[i][2]].append(len(edges))
            eklenen.append([edges[i][1],edges[i][2]])
            edges.append([len(edges),edges[i][1],edges[i][2],edges[i][3]])
     
            


final_rota = []
final_kanal = []
i = 0
while i < len(targets):
    buldum = False
    ii_index = 0
    while ii_index < len(rotas[targets[i][0], targets[i][1]]):
        ii = rotas[targets[i][0], targets[i][1]][ii_index]
        result = findway(ii)
        iii_index = 0

        while iii_index < len(result):
            iii = result[iii_index]
            jj_index = 0
            flag = True

            while jj_index < len(kanallar):
                jj = kanallar[jj_index]
                channel_flag = True

                for j in iii:
                    if j not in jj:
                        channel_flag = False

                if channel_flag:
                    final_kanal.append(jj_index)
                    final_rota.append(iii)
                    for j in iii:
                        jj.remove(j)
                    break

                jj_index += 1

            if channel_flag:
                break

            iii_index += 1

        if channel_flag:
            break

        ii_index += 1

    if not channel_flag:
        kenar_ekle(result)
        i-=1


    i += 1


    
print(len(eklenen))
for i in eklenen:
    print(i[0],i[1])
    
for i in range(len(final_kanal)):
    dep=[]
    for ii in final_rota[i]:
        if edges[ii][1] not in dep:
            dep.append(edges[ii][1])
        if edges[ii][2] not in dep:
            dep.append(edges[ii][2])
    dep=dep[1:-1]
    
    
    line=f"{final_kanal[i]} {len(final_rota[i])} {len(dep)}"
    
    knr_str=( " ".join( str(k) for k in final_rota[i]) )
    
    dep=( " ".join( str(k) for k in dep ) )
    

    line=f"{line} {knr_str} {dep}"
    
    
    print(line)