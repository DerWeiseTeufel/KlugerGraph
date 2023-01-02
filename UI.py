from graph_cl import Graph


cmd_create = "CREATE_GRAPH"
cmd_edge = "ADD_EDGE"
cmd_node = "ADD_NODE"
cmd_del_edge = "DELETE_EDGE"
cmd_del_node = "DELETE_NODE"
cmd_print = "PRINT_GRAPH"
cmd_exit = "EXIT"
cmd_fail = "FAILED"
cmd_file = "FROM_FILE"
cmd_ok = "SUCCESS"
cmd_degree = "DEGREE"
cmd_print_all_but = "PRINT_ALL_VERTICES_THAT_ARE_NOT_CONNECTED_WITH"
cmd_lvs = "PRINT_LEAVES"
cmd_graphwoutlvs = "GET_GRAPH_WITHOUT_LEAVES"
cmd_write_file = "WRITE_TXT"
cmd_find_shortest_loop = "FIND_SHORTEST_LOOP"
cmd_mst = "RETURN_MST"
cmd_exists_path = "EXISTS_PATH_IN_RANGE_L"
cmd_shortest_path_btw = "SHOW_SHORTEST_FROM_U1_U2_TO_V"
cmd_N_peref = "FIND_N_PEREFERY"
cmd_find_all_paths = "FIND_ALL_PATHS"
cmd_find_all_paths_b = "FIND_ALL_PATHS_B"
cmd_graphwoutlvs = "GET_GRAPH_WITHOUT_LEAVES"


def Menu():
    print(cmd_create)
    print(cmd_file)
    print(cmd_edge)
    print(cmd_node)
    print(cmd_del_edge)
    print(cmd_del_node)
    print(cmd_degree)
    print(cmd_print)
    print(cmd_lvs)
    print(cmd_exit)
    print(cmd_write_file)
    print(cmd_find_shortest_loop)
    print(cmd_mst)
    print(cmd_exists_path)
    print(cmd_shortest_path_btw)
    print(cmd_N_peref)
    print(cmd_find_all_paths)
    print(cmd_find_all_paths_b)
    print(cmd_graphwoutlvs)

flag = True
while True:

    while flag:
        print("Hello, User, this is Graph, you can line your commands just like they are listed below: ")
        print(cmd_create)
        print(cmd_file)
        decision = input().upper()
        if decision == cmd_create:  # CREATE FROM CONSOLE
            print("HOW MANY LINES?")
            n = int(input().split()[0])
            print("The first lin ein input has to be Weighted/Unweightd Directed/Undirected sequence")
            ngr = Graph.createConsole(n)  # CONSTRUCTOR CALL
            flag = False
        elif decision == cmd_file:  # CREATE FROM FILE
            path = input()
            ngr = Graph.createFromFile(path)
            flag = False
        else:
            print(cmd_fail)
            continue

    decision = input().upper()
    if not decision:
        print(cmd_fail)
        continue
    if decision == "MENU":
        Menu()
    if (decision == cmd_create):
      # CREATE FROM CONSOLE
        print("HOW MANY LINES/VERTICES?")
        n = int(input().split()[0])
        print("The first lin ein input has to be Weighted/Unweightd Directed/Undirected sequence")
        ngr = Graph.createfromconsol(n)  # CONSTRUCTOR CALL
        continue
    elif decision == cmd_print:
        print(ngr.show())
        continue

    elif decision == cmd_edge:
        print("FROM:")
        v = ngr.dtype(input())
        print("TO:")
        v2 = ngr.dtype(input())
        w = 1
        if ngr.Weighted:
            print("WEIGHT:")
            w = int(input())
        ngr.add_edge(v, v2, w)
        continue
    elif decision == cmd_node:
        print("NAME NEW vertex")
        node = input()
        ngr.add_vertex(node)
        continue
    elif decision == cmd_del_edge:
        print("remove from")
        fr_del = input()
        print("to")
        to_del = input()
        ngr.remove_edge(fr_del, to_del)
        continue
    elif decision == cmd_write_file:
        print("Path : ")
        path = input()
        ngr.write_to_txt(path)
        continue
    elif decision == cmd_file:
        path = input()
        ngr = Graph.createFromFile(path)
        continue
    elif decision == cmd_del_node:
        print("WHICH ONE")
        v_to_del = ngr.dtype(input())
        ngr.remove_node(v_to_del)
        continue
    elif decision == cmd_degree:
        print("Which one?")
        vofd = ngr.dtype(input())
        print(ngr.out_degree(vofd))
        continue
    elif decision == cmd_lvs:
        ngr.remove_all_leaves()
        continue
    elif decision == cmd_exit:
        print("Rate my performance:")
        n = int(input())
        break
    elif decision == cmd_find_shortest_loop:
        print(ngr.find_shortest_loop())
    elif decision == cmd_mst:
        print("Enter where to start:")
        v = input()
        ngr.prim(v)
    elif decision == cmd_exists_path:
        print("Enter starting point")
        v = input()
        print("Enter destination")
        d = input()
        print("Enter L")
        l = float(input())
        print(ngr.exists_path(v, d, l))

    elif decision == cmd_shortest_path_btw:
        print("enter U1")
        u1 = input()
        print("enter U2")
        u2 = input()
        print("enter V")
        v = input()
        ngr.show_shortest_(u1,u2,v)
    elif decision == cmd_N_peref:
        print("Enter vertex")
        v = input()
        print("Enter N")
        n = float(input())
        print(ngr.N_peref(v, n))
    elif decision == cmd_find_all_paths:
        print("Enter the starting vertex")
        u = input()
        print("Enter destination vertex")
        v = input()
        res = ngr.find_all_paths(u, v)
        print(res)
    elif decision == cmd_find_all_paths_b:
        print("Enter the starting vertex")
        u = input()
        print("Enter destination vertex")
        v = input()
        res = ngr.find_all_paths_b(u, v)
        print("\n".join([" ".join(way) for way in res]))
    elif decision == cmd_graphwoutlvs:
        ngr = Graph.createGrWoutLeaves(ngr)


