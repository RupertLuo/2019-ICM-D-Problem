import matplotlib.pyplot as plt
import math
import networkx as nx
from itertools import islice
global INF
INF=10000000
global drate,rrate
drate=0.9
rrate=1.3
nrate=0.5


def wether_connected(G,route):
    for i in range(len(route)-1):
        if (route[i],route[i+1]) in G.edges:
            continue
        else:
            return False
    return True
def insert_sort(alist,G):
    #print(G.nodes)
    n = len(alist)
    for j in range(1, n):
        for i in range(j, 0, -1):
            #print(G.node[alist[i]])
            if G.node[alist[i]]["rank"] < G.node[alist[i-1]]["rank"]:
                alist[i], alist[i - 1] = alist[i - 1], alist[i]
            else:
                break
    return alist
def ini_(G):
    node_list=list(G.nodes)
    node_list=insert_sort(node_list,G)
    return(node_list)
def create_graph(nodelist,edgelist):
    G = nx.Graph()
    G.add_nodes_from(nodelist)
    G.add_edges_from(edgelist)
    return G
def cross_point(each_k_path,sourceA,sourceB,k,l):
    listA=each_k_path[sourceA][k][2]
    listB = each_k_path[sourceB][l][2]
    ret_inter = list(set(listA).intersection(set(listB)))
    if len(ret_inter)==0:
        return None
    elif len(ret_inter)==1:
        return ret_inter[0]
def wether_cross(route1,source2,each_k_path):
        for route2 in each_k_path[source2]:
            if list(set(route2[2][:-1]).intersection(route1[2][:-1]))!=[]:
                return True
        return False
def min_f(route,G,t):
    f_list=[]
    t_start=t
    for i in range(len(route)-1):
        t_end=t_start+G.edges[route[i],route[i+1]]["time"]
        f_list.append(G.edges[route[i],route[i+1]]["time_num"][t_start])
        t_start=t_end
    return min(f_list)
def cheli(T0,G,renshu,source,route_list,all_time):
    all_t=T0+travel_time(route_list.index(source),route_list.index(0),route_list,G)
    if(renshu>0):
        if (renshu <= G.nodes[source]["Current_num"]):  # renew number of people not arranged

            G.nodes[source]["Current_num"] -= renshu
            #print("Time {T0}from{a} evacuate {ft}people,total time:{all_t}".format(T0=T0, a=source, ft=renshu,all_t=all_t))
            #print(route_list)
            all_time.append(all_t)
        else:
            ftt = G.nodes[source]["Current_num"]
            if(ftt>0):
                G.nodes[source]["Current_num"] = 0
                #print("Time {T0}from{a} evacuate {ft}people,total time:{all_t}".format(T0=T0, a=source, ft=ftt,all_t=all_t))
                #print(route_list)
                all_time.append(all_t)

def door_effect(floor,rate,G,if_open):
    if if_open:
        for i in G.edges:
            if G.edges[i[0],i[1]]["floor"]==floor:
                G.edges[i[0],i[1]]["time"]=int(G.edges[i[0],i[1]]["time"]/rate)+1
def edge_update(G,t1,line,f):
    t_start=t1
    for m in range(len(line) - 1):  # renew network capacity
        t_end=t_start+G.edges[line[m], line[m + 1]]["time"]
        for i in  range(t_start,t_end):
            G.edges[line[m], line[m + 1]]["time_num"][i] = \
            G .edges[line[m], line[m + 1]]["time_num"][i] - f
        t_start = t_end
def node_update(G,t1,line,f):
    for m in range(len(line) - 1):
        t1 = t1 + G.edges[line[m], line[m + 1]]["time"]
        G.node[line[m + 1]]["time_num"][t1] = G.node[line[m + 1]]["time_num"][t1] - f
def check_end(sourcelist,G):
    sum=0
    for x in sourcelist:
        sum+=G.node[x]["Current_num"]
    if sum>0:
        return True
    else:
        return False
def travel_time(n1_index,n2_index,line,G):
    sum=0
    for i in range(n1_index,n2_index-1):
        sum+=G.edges[line[i],line[i+1]]["time"]
    return sum
def k_shortest_paths(G, source, target, k, weight=None):
     return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))
def excution(nodelist,edgelist,K,exit_gate,open_door,when_close):
    all_time=[]
    G=create_graph(nodelist,edgelist)#create graph
    nodelist_1 = ini_(G)#initialize graph
    sourcelist=[]
    if nodelist_1 !=None:
        for i in nodelist_1:
            if G.node[i]["Current_num"]!=0:
                sourcelist.append(i)
    each_k_path={}
    for i in sourcelist:
        x_list=list(k_shortest_paths(G,i,exit_gate,K,weight="time"))#求出了所有的源通往出口的路径
        all_list_nd_lenth=[]
        for j in range(len(x_list)):
            sum=0
            f_min=100000
            for p in range(len(x_list[j])-1):
                if G[x_list[j][p]][x_list[j][p+1]]["Max_num"] < f_min:
                    f_min=G[x_list[j][p]][x_list[j][p+1]]["Max_num"]#求出每条路径的最小流
                sum+=G[x_list[j][p]][x_list[j][p+1]]["time"]#计算每条简单路径的长度
            all_list_nd_lenth.append((sum,f_min,x_list[j]))
        all_list_nd_lenth=sorted(all_list_nd_lenth)#取到了源 i 前k个路径
        new_G=create_graph(nodelist,edgelist)
        m=0
        while(m <len(all_list_nd_lenth)):
            for j in range(len(all_list_nd_lenth[m][2])-1):
                x=all_list_nd_lenth[m][2][j]
                x_next=all_list_nd_lenth[m][2][j+1]
                new_G.node[x_next]["Max_num"] = new_G.node[x_next]["Max_num"] - all_list_nd_lenth[m][1]
                new_G.edges[x,x_next]["Max_num"]= new_G.edges[x,x_next]["Max_num"]-all_list_nd_lenth[m][1]
                if new_G.edges[x,x_next]["Max_num"]<=0:
                    new_G.remove_edge(x,x_next)
                if new_G.node[x_next]["Max_num"]<=0:#如果边和点的此时容量小于0就删除边和点
                    for q in range(j):
                        new_G.remove_edge(all_list_nd_lenth[m][2][q],all_list_nd_lenth[m][2][q+1])
            if m!=len(all_list_nd_lenth)-1:
                for n in range(m,len(all_list_nd_lenth)-1):
                    if wether_connected(new_G,all_list_nd_lenth[m+1][2])==False:
                        all_list_nd_lenth.remove(all_list_nd_lenth[m + 1])
            m+=1
        if m<=K:
            each_k_path[i] = all_list_nd_lenth
        else:
            each_k_path[i]=all_list_nd_lenth[:K]
    for i in range(len(open_door)):
        door_effect(i+1,drate,G,open_door[i])
    sum=0
    for i in open_door:
        sum+=i
    for i in range(len(open_door)):

        if sum>0:
            R=min(rrate**sum,2)
            door_effect(i + 1, R, G, 1)
    t=0
    T0 = 0
    while (check_end(sourcelist,G)):
        if t==when_close:
            for i in range(len(open_door)):
                door_effect(i+1, 1/drate, G, open_door[i])#when close
        for a in range(len(sourcelist)):
            for route_a in each_k_path[sourcelist[a]]:
                t = T0
                ft=min_f(route_a[2],G,t)#flow rate of time t
                if_intersect=False #Determines whether there is an intersection with a higher priority point
                for a_ in range(0,a):
                    if wether_cross(route_a,sourcelist[a_],each_k_path)==True:
                        if_intersect=True
                if(if_intersect==False):#if not,renew after evacuate
                    cheli(T0,G,ft,sourcelist[a],route_a[2],all_time)
                    edge_update(G,t,route_a[2],ft)
                    node_update(G,t,route_a[2],ft)
                else:
                    for a_ in range(0, a):
                        for route_a_ in each_k_path[sourcelist[a_]]:
                            '''ft_a_ = min_f(route_a_[2], G, t)
                            ft = min_f(route_a[2],G,t)'''
                            intersect = [i for i in route_a[2][:-1] if i in route_a_[2][:-1]]


                            if intersect!=[]:
                                na = intersect[0]
                                t_astart=travel_time(route_a[2].index(sourcelist[a]),route_a[2].index(na),route_a[2],G)
                                t_a_start=travel_time(route_a_[2].index(sourcelist[a_]),route_a_[2].index(na),route_a_[2],G)
                                t_common=travel_time(route_a_[2].index(na),route_a_[2].index(0),route_a_[2],G)
                                t_aend=t_astart+t_common
                                t_a_end=t_a_start+t_common
                                if t_astart==t_a_start:
                                    fa_=min_f(route_a_[2],G,t)
                                    cheli(t,G,fa_,sourcelist[a_],route_a_[2],all_time)
                                    edge_update(G, t, route_a[2], fa_)
                                    node_update(G, t, route_a[2], fa_)
                                    fa=min_f(route_a[2],G,t)
                                    if fa>0:
                                        cheli(t,G,fa,sourcelist[a],route_a[2],all_time)
                                        edge_update(G, t, route_a[2], fa)
                                        node_update(G, t, route_a[2], fa)
                                elif(t_aend>t_a_start and t_astart<t_a_start or t_a_end > t_astart and t_a_start < t_astart):
                                    fa_ = min_f(route_a_[2], G, t)
                                    cheli(t, G, fa_, sourcelist[a_], route_a_[2],all_time)
                                    edge_update(G, t, route_a_[2][:route_a_[2].index(na)], fa_)
                                    edge_update(G, t + t_a_start, route_a_[2][route_a_[2].index(na):], fa_)
                                    node_update(G, t, route_a_[2], fa_)

                                    fa = min_f(route_a[2], G, t)
                                    cheli(t, G, fa, sourcelist[a], route_a[2],all_time)
                                    edge_update(G, t, route_a[2][:route_a[2].index(na)], fa)
                                    edge_update(G, t+t_astart, route_a[2][route_a[2].index(na):], fa)
                                    node_update(G, t, route_a[2], fa)#  intersect
                                else:
                                    fa_ = min_f(route_a_[2], G, t)
                                    fa = min_f(route_a[2], G, t)
                                    cheli(t, G, fa_, sourcelist[a_], route_a_[2],all_time)
                                    edge_update(G, t, route_a_[2], fa_)
                                    node_update(G, t, route_a_[2], fa_)
                                    cheli(t, G, fa, sourcelist[a], route_a[2],all_time)
                                    edge_update(G, t, route_a[2], fa)
                                    node_update(G, t, route_a[2], fa)
                                     # no intersection

        T0+=1
    return  max(all_time)

def find_best_plan(node,edge,):
    all_opendoor=[[0,0,0,0,0],[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,0,0,0,0],[1,1,0,0,0],[1,0,1,0,0],[1,0,0,1,0],[1,0,0,0,1],\
                              [0,1,1,0,0],[0,1,0,1,0],[0,1,0,0,1],[0,0,1,1,0],[0,0,1,0,1],[0,0,0,1,1],[1,1,1,0,0],[1,1,0,1,0],[1,1,0,0,1],[1,0,1,1,0],\
                              [1,0,1,0,1],[1,0,0,1,1],[0,1,1,1,0],[0,1,1,0,1],[0,1,0,1,1],[0,0,1,1,1],[1,1,1,1,0],[1,1,1,0,1],[1,1,0,1,1],[1,0,1,1,1],\
                              [0,1,1,1,1],[1,1,1,1,1]]
    best_plan=[all_opendoor[0],0,0]
    max_all_time=10000
    for i in range(len(all_opendoor)):
        opendoor=all_opendoor[i]
        for m in range(3):
            when_close=m+1
            for j in range(6):
                k=j+1

                #maintain original data
                nodelist = node
                edgelist = edge
                for x in edgelist:
                    for i in range(100):
                        x[2]["time_num"][i] = x[2]["Max_num"]
                for x in nodelist:
                    for i in range(100):
                        x[1]["time_num"][i] = x[1]["Max_num"]

                try:
                    time=excution(nodelist, edgelist, k, 0, opendoor, when_close)
                except:
                    time=10000
                else:
                    pass
                print("Auxiliary Doors:",opendoor,"      Time to close Auxiliary Doors:" ,when_close, "      Maximum number of paths each source use:",k,"      Totol Time:",time)
                if time<max_all_time:
                    max_all_time=time
                    best_plan = [opendoor, when_close, k]
    return  [best_plan,max_all_time]

nodelist=[(101,{"rank":1,"Max_num":5710,"Current_num":2700,"time_num":{}}),
          (201,{"rank":30,"Max_num":3860,"Current_num":430,"time_num":{}}),
          (202,{"rank":25,"Max_num":3860,"Current_num":430,"time_num":{}}),
          (203,{"rank":9,"Max_num":3860,"Current_num":430,"time_num":{}}),
          (204,{"rank":29,"Max_num":3860,"Current_num":430,"time_num":{}}),
          (205,{"rank":23,"Max_num":3860,"Current_num":430,"time_num":{}}),
          (206,{"rank":4,"Max_num":3860,"Current_num":430,"time_num":{}}),
          (210,{"rank":2,"Max_num":3730,"Current_num":540,"time_num":{}}),
          (211,{"rank":3,"Max_num":7670,"Current_num":900,"time_num":{}}),
          (212,{"rank":8,"Max_num":3930,"Current_num":360,"time_num":{}}),
          (213,{"rank":27,"Max_num":3930,"Current_num":360,"time_num":{}}),
          (214,{"rank":24,"Max_num":3930,"Current_num":360,"time_num":{}}),
          (215,{"rank":26,"Max_num":3930,"Current_num":360,"time_num":{}}),
          (216,{"rank":28,"Max_num":3930,"Current_num":360,"time_num":{}}),
          (401,{"rank":46,"Max_num":9960,"Current_num":680,"time_num":{}}),
          (402,{"rank":44,"Max_num":5410,"Current_num":340,"time_num":{}}),
          (403,{"rank":43,"Max_num":5410,"Current_num":340,"time_num":{}}),
          (404,{"rank":45,"Max_num":5410,"Current_num":340,"time_num":{}}),
          (405,{"rank":34,"Max_num":5410,"Current_num":340,"time_num":{}}),
          (406,{"rank":35,"Max_num":9150,"Current_num":740,"time_num":{}}),
          (407,{"rank":43,"Max_num":3730,"Current_num":400,"time_num":{}}),
          (408,{"rank":36,"Max_num":6220,"Current_num":650,"time_num":{}}),
          (409,{"rank":33,"Max_num":6220,"Current_num":650,"time_num":{}}),
          (410,{"rank":41,"Max_num":3730,"Current_num":400,"time_num":{}}),
          (411,{"rank":32,"Max_num":11730,"Current_num":1020,"time_num":{}}),
          (412, {"rank": 39, "Max_num": 5510, "Current_num": 370, "time_num": {}}),
          (413, {"rank": 38, "Max_num": 5510, "Current_num": 750, "time_num": {}}),
          (414, {"rank": 37, "Max_num": 5510, "Current_num": 750, "time_num": {}}),
          (415, {"rank": 31, "Max_num": 5510, "Current_num": 370, "time_num": {}}),
          (416, {"rank": 36, "Max_num": 12016, "Current_num": 850, "time_num": {}}),
          (301, {"rank": 22, "Max_num": 7730, "Current_num": 280, "time_num": {}}),
          (302, {"rank": 20, "Max_num": 7730, "Current_num": 280, "time_num": {}}),
          (303, {"rank": 18, "Max_num": 7730, "Current_num": 280, "time_num": {}}),
          (304, {"rank": 21, "Max_num": 7730, "Current_num": 280, "time_num": {}}),
          (305, {"rank": 19, "Max_num": 7730, "Current_num": 280, "time_num": {}}),
          (306, {"rank": 14, "Max_num": 11460, "Current_num": 560, "time_num": {}}),
          (307, {"rank": 16, "Max_num": 3730, "Current_num": 280, "time_num": {}}),
          (308, {"rank": 17, "Max_num": 6220, "Current_num": 420, "time_num": {}}),
          (309, {"rank": 15, "Max_num": 6220, "Current_num": 420, "time_num": {}}),
          (310, {"rank": 13, "Max_num": 3730, "Current_num": 280, "time_num": {}}),
          (311, {"rank": 12, "Max_num": 10940, "Current_num": 840, "time_num": {}}),
          (312, {"rank": 10, "Max_num": 4720, "Current_num": 280, "time_num": {}}),
          (313, {"rank": 7, "Max_num": 4720, "Current_num": 280, "time_num": {}}),
          (314, {"rank": 11, "Max_num": 4720, "Current_num": 280, "time_num": {}}),
          (315, {"rank": 6, "Max_num": 4720, "Current_num": 280, "time_num": {}}),
          (316, {"rank": 5, "Max_num": 4720, "Current_num": 280, "time_num": {}}),
          (501, {"rank": 57, "Max_num": 5410, "Current_num": 450, "time_num": {}}),
          (502, {"rank": 50, "Max_num": 5410, "Current_num": 450, "time_num": {}}),
          (503, {"rank": 55, "Max_num": 5410, "Current_num": 450, "time_num": {}}),
          (504, {"rank": 56, "Max_num": 5410, "Current_num": 450, "time_num": {}}),
          (505, {"rank": 54, "Max_num": 5410, "Current_num": 450, "time_num": {}}),
          (506, {"rank": 53, "Max_num": 9150, "Current_num": 900, "time_num": {}}),
          (507, {"rank": 48, "Max_num": 3730, "Current_num": 450, "time_num": {}}),
          (508, {"rank": 52, "Max_num": 6220, "Current_num": 750, "time_num": {}}),
          (509, {"rank": 47, "Max_num": 6220, "Current_num": 750, "time_num": {}}),
          (510, {"rank": 49, "Max_num": 3730, "Current_num": 450, "time_num": {}}),
          (511, {"rank": 51, "Max_num": 6220, "Current_num": 750, "time_num": {}}),
          (0,{"rank":INF,"Max_num":INF,"Current_num":0,"time_num":{}})]
#consider different number of people in the museum
for i in range(len(nodelist)):
    nodelist[i][1]["Current_num"]=nodelist[i][1]["Current_num"]*nrate

edgelist=[(101,0,{"Max_num":3490,"time":5,"time_num":{},"floor":1}),
          (316,0,{"Max_num":3213,"time":9,"time_num":{},"floor":3}),


          (101,210,{"Max_num":500,"time":1,"time_num":{},"floor":2}),
          (201,202,{"Max_num":428,"time":3,"time_num":{},"floor":2}),
          (202,203,{"Max_num":428,"time":3,"time_num":{},"floor":2}),
          (203,206,{"Max_num":428,"time":3,"time_num":{},"floor":2}),
          (206,204,{"Max_num":428,"time":4,"time_num":{},"floor":2}),
          (205,204,{"Max_num":428,"time":3,"time_num":{},"floor":2}),
          (204,201,{"Max_num":428,"time":2,"time_num":{},"floor":2}),
          (202,205,{"Max_num":428,"time":2,"time_num":{},"floor":2}),
          (206,210,{"Max_num":414,"time":3,"time_num":{},"floor":2}),
          (210,211,{"Max_num":414,"time":3,"time_num":{},"floor":2}),
          (214,215,{"Max_num":400,"time":4,"time_num":{},"floor":2}),
          (214,211,{"Max_num":400,"time":4,"time_num":{},"floor":2}),
          (211,212,{"Max_num":400,"time":4,"time_num":{},"floor":2}),
          (213,214,{"Max_num":400,"time":4,"time_num":{},"floor":2}),
          (213,212,{"Max_num":400,"time":4,"time_num":{},"floor":2}),
          (215,216,{"Max_num":400,"time":4,"time_num":{},"floor":2}),
          (216,213,{"Max_num":400,"time":4,"time_num":{},"floor":2}),
          (202,302,{"Max_num":500,"time":1,"time_num":{},"floor":3}),
          (211,311,{"Max_num":500,"time":1,"time_num":{},"floor":3}),
          (215,315,{"Max_num":500,"time":1,"time_num":{},"floor":3}),
          (213,313,{"Max_num":500,"time":1,"time_num":{},"floor":3}),
          (301, 302, {"Max_num": 856, "time": 3, "time_num": {}, "floor": 3}),
          (302, 303, {"Max_num": 856, "time": 3, "time_num": {}, "floor": 3}),
          (303, 306, {"Max_num": 856, "time": 3, "time_num": {}, "floor": 3}),
          (306, 304, {"Max_num": 856, "time": 4, "time_num": {}, "floor": 3}),
          (305, 304, {"Max_num": 856, "time": 3, "time_num": {}, "floor": 3}),
          (304, 301, {"Max_num": 856, "time": 2, "time_num": {}, "floor": 3}),
          (302, 305, {"Max_num": 856, "time": 2, "time_num": {}, "floor": 3}),
          (306, 310, {"Max_num": 414, "time": 3, "time_num": {}, "floor": 3}),
          (310, 311, {"Max_num": 414, "time": 3, "time_num": {}, "floor": 3}),
          (306, 307, {"Max_num": 414, "time": 2, "time_num": {}, "floor": 3}),
          (307, 308,  {"Max_num": 414, "time": 2, "time_num": {}, "floor": 3}),
          (308,309,  {"Max_num":828,"time":4,"time_num":{},"floor":3}),
          (309, 311, {"Max_num": 828, "time": 4, "time_num": {}, "floor": 3}),
          (314,315,{"Max_num":524,"time":4,"time_num":{},"floor":3}),
          (314,311,{"Max_num":524,"time":4,"time_num":{},"floor":3}),
          (311,312,{"Max_num":524,"time":4,"time_num":{},"floor":3}),
          (313,314,{"Max_num":524,"time":4,"time_num":{},"floor":3}),
          (313,312,{"Max_num":524,"time":4,"time_num":{},"floor":3}),
          (315,316,{"Max_num":524,"time":4,"time_num":{},"floor":3}),
          (316,313,{"Max_num":524,"time":4,"time_num":{},"floor":3}),
          (305, 405, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 4}),
          (306, 406, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 4}),
          (308, 408, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 4}),
          (309, 409, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 4}),
          (311, 411, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 4}),
          (315, 415, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 4}),
          (401, 402, {"Max_num": 600, "time": 3, "time_num": {}, "floor": 4}),
          (402, 403, {"Max_num": 600, "time": 3, "time_num": {}, "floor": 4}),
          (403, 406, {"Max_num": 600, "time": 3, "time_num": {}, "floor": 4}),
          (406, 404, {"Max_num": 600, "time": 4, "time_num": {}, "floor": 4}),
          (405, 404, {"Max_num": 600, "time": 3, "time_num": {}, "floor": 4}),
          (404, 401, {"Max_num": 600, "time": 2, "time_num": {}, "floor": 4}),
          (402, 405, {"Max_num": 600, "time": 2, "time_num": {}, "floor": 4}),
          (406, 410, {"Max_num": 414, "time": 3, "time_num": {}, "floor": 4}),
          (410, 411, {"Max_num": 414, "time": 3, "time_num": {}, "floor": 4}),
          (406, 407, {"Max_num": 414, "time": 2, "time_num": {}, "floor": 4}),
          (407, 408,  {"Max_num": 414, "time": 2, "time_num": {}, "floor": 4}),
          (408, 409,  {"Max_num":828,"time":4,"time_num":{},"floor":4}),
          (409, 411, {"Max_num": 828, "time": 4, "time_num": {}, "floor": 4}),
          (414, 415, {"Max_num": 610, "time": 4, "time_num": {}, "floor": 4}),
          (414, 411, {"Max_num": 610, "time": 4, "time_num": {}, "floor": 4}),
          (411, 412, {"Max_num": 610, "time": 4, "time_num": {}, "floor": 4}),
          (413, 414, {"Max_num": 610, "time": 4, "time_num": {}, "floor": 4}),
          (413, 412, {"Max_num": 610, "time": 4, "time_num": {}, "floor": 4}),
          (415, 416, {"Max_num": 610, "time": 4, "time_num": {}, "floor": 4}),
          (416, 413, {"Max_num": 610, "time": 4, "time_num": {}, "floor": 4}),

          (402, 502, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 5}),
          (407, 507, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 5}),
          (409, 509, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 5}),
          (410, 510, {"Max_num": 500, "time": 1, "time_num": {}, "floor": 5}),

          (501, 502, {"Max_num": 600, "time": 3, "time_num": {}, "floor": 5}),
          (502, 503, {"Max_num": 600, "time": 3, "time_num": {}, "floor": 5}),
          (503, 506, {"Max_num": 600, "time": 3, "time_num": {}, "floor": 5}),
          (506, 504, {"Max_num": 600, "time": 4, "time_num": {}, "floor": 5}),
          (505, 504, {"Max_num": 600, "time": 3, "time_num": {}, "floor": 5}),
          (504, 501, {"Max_num": 600, "time": 2, "time_num": {}, "floor": 5}),
          (502, 505, {"Max_num": 600, "time": 2, "time_num": {}, "floor": 5}),
          (506, 510, {"Max_num": 414, "time": 3, "time_num": {}, "floor": 5}),
          (510, 511, {"Max_num": 414, "time": 3, "time_num": {}, "floor": 5}),
          (506, 507, {"Max_num": 414, "time": 2, "time_num": {}, "floor": 5}),
          (507, 508, {"Max_num": 414, "time": 2, "time_num": {}, "floor": 5}),
          (508, 509, {"Max_num": 828, "time": 4, "time_num": {}, "floor": 5}),
          (509, 511, {"Max_num": 828, "time": 4, "time_num": {}, "floor": 5}),]
for x in edgelist:
    for i in range(100):
        x[2]["time_num"][i]=x[2]["Max_num"]
for x in nodelist:
    for i in range(100):
        x[1]["time_num"][i]=x[1]["Max_num"]


[best_plan,max_all_time]=find_best_plan(nodelist,edgelist)
print("Best plan:")
print("Auxiliary Doors:",best_plan[0],"Time to close Auxiliary Doors:", best_plan[1], "Maximum number of paths each source use:",best_plan[2],"Totol Time:",max_all_time)

