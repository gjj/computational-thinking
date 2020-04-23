# G2_T11
# Goi Jia Jian, Nicolas Wijaya

# project 2 Q2

# replace the content of this function with your own algorithm
# inputs:
#   p: min target no. of points team must collect. p>0
#   v: 1 (non-cycle) or 2 (cycle)
#   flags: 2D list [[flagID, value, x, y], [flagID, value, x, y]....]
# returns:
#   A list of n lists. Each "inner list" represents a route. There must be n routes in your answer
# from pandas import *
# from sklearn.cluster import KMeans
import copy

def get_routes(p, v, flags, n):
    route0 = []
    # If n = 1, the VRP is effectively reduced to TSP, so we'll run our p2q1 algorithm
    if n == 1:
        return [get_route(p, v, flags)]
    if p <= 800:
        # We also use q1 solution for smaller values of p, with a threshold set by us (same as p2q1 testcases)
        # Will use it later to compare
        route0 = [get_route(p, v, flags)] + [[] for i in range(n-1)]

    count_flags = len(flags)
    f = {flags[i][0]: [float(flags[i][2]), float(flags[i][3]), int(flags[i][1])] for i in range(count_flags)}
    f1 = copy.deepcopy(f)
    
    # Part 1
    # Find out the paths of our greedy approach
    route1 = greedy_multiple(f1, f, p, v, n, 1)    

    # Part 2
    # Improve each of the results above using the 2-opt method
    optimised1 = try2opt_multiple(route1, v, f, n)

    result1 = get_route_dist_multiple(optimised1, f, v, n)
    best_dist, best_route = result1

    if route0:
        result0 = get_route_dist_multiple(route0, f, v, n)
        best_dist, best_route = min(result0, result1)

    return best_route

def try2opt_multiple(routes, v, f, n):
    result = [[] for i in range(n)]
    for i in range(n):
        result[i] = try2opt(routes[i], v, f)[1]
    return result

def get_route_dist_multiple(your_routes, flags_dict, v, n):
    dist = sum([get_route_dist(your_routes[i], flags_dict, v) for i in range(n)])
    return (dist, your_routes)

def greedy_multiple(f, flags, p, v, n, mode):
    result = [[] for i in range(n)]  # Generate empty array for each player
    points = 0
    current = [[0, 0] for i in range(n)]

    while p > points:
        # Every player will take turns to take one step each, but we cap at 2 players
        # See report for our reasoning
        for i in range(2):
            local_best = {
                'flag': '',
                'weight_max': 0,
                'point': 0,
                'coord': [0, 0]
            }

            # Mode 1
            # Greedily grab the next best using max(points per distance travelled)
            for id, [x, y, point] in f.items():
                if mode == 1:
                    dist = get_distance(current[i], [x, y])
                    weight = point / dist

                    if weight > local_best['weight_max']:
                        local_best['weight_max'] = weight
                        local_best['point'] = point
                        local_best['flag'] = id
                        local_best['coord'] = [x, y]
            
            # Store the flag into each player's current route, then update current
            result[i].append(local_best['flag'])
            del f[local_best['flag']]
            points += int(local_best['point'])
            current[i] = local_best['coord']
    return result

def get_route(p, v, flags):
    n = len(flags)

    f = {flags[i][0]: [float(flags[i][2]), float(
        flags[i][3]), int(flags[i][1])] for i in range(n)}
    f1 = copy.deepcopy(f)
    f2 = copy.deepcopy(f)

    # Part 1
    # Find out the paths of our two algorithms (same objective, but different measuring system)
    route1 = greedy(p, f1, f, 1)
    route2 = greedy(p, f2, f, 2)

    # Part 2
    # Improve each of the results above using the 2-opt method
    optimised1 = try2opt(route1, v, f)
    optimised2 = try2opt(route2, v, f)

    # Part 3
    # If best path from above gives more points than required,
    # check to see if by removing some points, whether it can be shorter
    result1 = trim(optimised1[1], p, v, f)
    result2 = trim(optimised2[1], p, v, f)

    # Part 4
    # Pick the best 2-opt optimised + trimmed route i.e. lowest distance of the above
    best_dist, best_route = min(result1, result2)
    
    return best_route

def greedy(p, f, flags, mode):
    points = 0
    current = [0, 0]
    result = []

    while p > points:
        local_best = {
            'flag': '',
            'weight_max': 0,
            'weight_min': 10000,
            'dist': 10000,
            'distance_from_sp': 10000,
            'point': 0,
            'coord': [0, 0]
        }

        for id, [x, y, point] in f.items():
            if mode == 1:
                # mode = 1: Greedy search with objective max(point per unit distance travelled) method,
                # ignoring distance from SP, using Euclidean distance squared
                dist = get_distance_squared(current, [x, y])
                weight = point / dist

                if weight > local_best['weight_max']:
                    local_best['weight_max'] = weight
                    local_best['point'] = point
                    local_best['flag'] = id
                    local_best['coord'] = [x, y]

            elif mode == 2:
                # mode = 2: Greedy search with objective max(point per unit distance travelled) method,
                # ignoring distance from SP, using Euclidean distance
                dist = get_distance(current, [x, y])
                weight = point / dist

                if weight > local_best['weight_max']:
                    local_best['weight_max'] = weight
                    local_best['point'] = point
                    local_best['flag'] = id
                    local_best['coord'] = [x, y]

        result.append(local_best['flag'])
        del f[local_best['flag']]
        points += int(local_best['point'])
        current = local_best['coord']

    return result

def try2opt(route, v, flags):
    local_best = {
        'dist': get_route_dist(route, flags, v),
        'route': route
    }

    n = len(route)

    # 2-opt: Attempting to swap
    for i in range(0, n):
        for j in range(i+1, n):
            new_route = swap2opt(local_best['route'], i, j)
            new_dist = get_route_dist(new_route, flags, v)

            # If there exists a shorter path after the swap, keep the 2-opt swap
            # in hopes of searching for another best combination
            if new_dist < local_best['dist']:
                local_best['dist'] = new_dist
                local_best['route'] = new_route  # Copy the list

    return (local_best['dist'], local_best['route'])


def swap2opt(route, i, j):
    new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]  # left + right reversed + remaining
    return new_route

def trim(route, p, v, f):
    points = 0
    dist = get_route_dist(route, f, v) # Find distance of the best route

    # Find total points of this route
    for id in route:
        points += f[id][2]

    diff = points - p

    # Only run if diff > 0 i.e. the best route returns 502 points, but we only need 500
    if diff > 0:
        local_best = {
            'dist': dist,
            'route': route
        }

        # Prepare a sorted dict of points where it's equal to, or less than diff
        points = sorted({(f[id][2], id) for id in route if f[id][2] <= diff}, reverse=True)

        # For every (points, id) pair, check if after deleting it, will it give a lower distance?
        for to_delete in points:
            new_route = [item for item in route if item != to_delete[1]]
            new_dist = get_route_dist(new_route, f, v)

            # If it does give a lower distance, we keep it
            if new_dist < local_best['dist']:
                local_best['dist'] = new_dist
                local_best['route'] = new_route

        dist = local_best['dist']
        route = local_best['route']

    return (dist, route)

# Calculate Euclidean distance between two points e.g. (0, 0) and (-5.7, 8.8)
def get_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

# Calculate Euclidean distance squared
def get_distance_squared(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# Calculate total distance of a given path
def get_route_dist(your_route, flags_dict, v):
    dist = 0

    start_node = [0, 0]  # starting point SP (0, 0)
    last_node = start_node

    for flagID in your_route:
        curr_node = flags_dict[flagID]
        dist_to_curr_node = get_distance(last_node, curr_node)
        dist += dist_to_curr_node
        last_node = curr_node

    # If game mode v = 2, means have to cycle back to SP
    if v == 2:
        dist += get_distance(last_node, start_node)

    return dist

    # f2 = copy.deepcopy(f)

    # # Part 1: Reduce the search range, pick only points that are close to starting point
    # filtered_f = get_points(p, f2, flags, 1)

    # filtered_flags = [[id, f[id][2], f[id][0], f[id][1]] for id in filtered_f]
    # # print(filtered_flags)

    # data = pandas.DataFrame(filtered_flags, columns=['f', 'p', 'x', 'y'])
    # model = KMeans(n_clusters=2, init='k-means++', random_state=264)
    # model.fit(data[['x', 'y']])

    # clusters = []
    # for i in range(model.n_clusters):
    #     cluster = data[model.labels_ == i].index.tolist()
    #     cluster_flags = [filtered_flags[id][0] for id in cluster]

    #     optimised = try2opt(cluster_flags, v, f)
    #     clusters.append(optimised[1])

    #     # get_route_dist_print(optimised[1], f, v)
    # return clusters + [[], []]

    # print(clusters)
    # return [get_route(p, v, flags)]

    # print("name,desc,lat,long")
    # for id in f:
    #     print("%s,%d,%f,%f" % (id, int(f[id][2]), float(f[id][0]), float(f[id][1])))
    # print("name,desc,lat,long")
    # for id in cluster:
    #     print("%s,%d,%f,%f" % (id, int(f[id][2]), float(f[id][0]), float(f[id][1])))
    # get_route_dist_print(route, f, v)

    # data = pandas.DataFrame(flags, columns=['f', 'p', 'x', 'y'])

    # size = len(flags)
    # model = KMeans(n_clusters=n, init='k-means++', random_state=0)
    # model.fit(data[['x', 'y']])

    # # Process the clusters, find the flag IDs
    # clusters = []
    # for i in range(model.n_clusters):
    #     cluster = data[model.labels_ == i].index.tolist()

    #     cluster_flags = [flags[id][0] for id in cluster]
    #     clusters.append(cluster_flags)

    #     # print("name,desc,lat,long")
    #     # for id in cluster:
    #     #     print("%s,%d,%f,%f" % (flags[id][0], int(flags[id][1]), float(flags[id][2]), float(flags[id][3])))
    #     # get_route_dist_print(route, f, v)

    # result = []

    # # Initial ranking, find whichever's centroid is closest from SP
    # centroids = []
    # for id, centroid in enumerate(model.cluster_centers_):
    #     dist_from_sp = get_distance([0, 0], [centroid[0], centroid[1]])
    #     centroids.append({'dist': dist_from_sp, 'id': id, 'visited': False})
    # centroids = sorted(centroids, key=lambda k: k['dist'])
    # print(centroids)

    # # Start off from first
    # current = [0, 0]
    # for centroid in centroids:
    #     if 'visited' not in data:
    #         cluster_flags = clusters[centroid['id']]
    #         current = model.cluster_centers_[centroid['id']]

    # print(centroids)
    