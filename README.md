# CT Project 2

COR-IS1702 Computational Thinking AY19/20 Term 2 Project 2

## p2q1 Flag Game: Single Player 👩‍💻

Seems to be a variant of TSP: prize collecting TSP. Our solver uses the greedy approach with objective to `max(points per distance travelled)` to construct an initial route, then use 2-opt to improve the initial route and thereafter, uses a trim function if the route returns more points than required.

We found that in some cases, using the [Euclidean squared distance method](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#euclidean-distance-squared) return a much shorter route. No idea why, but thanks to [@xinweiiiii](https://github.com/xinweiiiii) for pointing it out.

So we decided to run the same greedy algorithm twice, both with the same objective but different distance calculating method (first being the Euclidean distance using Mok’s method in `utility.py`, and second being the one that does not square root).

Total complexity of our solver is ![n3](https://render.githubusercontent.com/render/math?math=O(n^3))
, where `n` is the number of flags – the worst case happens when `p = sum(flag points)` as the all flags will be part of the best route.

## p2q2 Flag Game: Multi Player 👫

Again, seems to be the prize collecting VRP problem. We adopted a similar greedy + 2-opt approach for question 2, and we created `greedy_multiple`, `try2opt_multiple` and `get_route_dist_multiple` wrapper functions that loop through `m` (number of players) and call our question 1’s functions. We also have two decisions here:

- When `n = 1`, immediately return our question 1’s `get_route()` results
- When `p <= 800` (a threshold set by us), we run our `get_route()` in single player mode for comparison with our multiplayer algorithm later – complexity for `get_route()` is `O(n^3)`

For the greedy approach, it was modified to allow up to two players to take one greedy step at a time using the same objective, except that we only used the Euclidean distance method (i.e. the one with square root).

Total complexity is still ![n3](https://render.githubusercontent.com/render/math?math=O(n^3)) as it largely follows our question 1 logic, where `n` is the number of flags. We also do not account for `m` as we analysed the results of sending out `2` players vs. `m` players – sending out only 2 players is almost always the better option for our algorithm design.

PS. We tried k-means clustering but we gave up because it was challenging to find the number of clusters to form. We felt that using both `n` or `p/n` didn't really make sense as in most cases, our paths became longer than our one-man-show method. Hence, we concluded it may not be worth it to force out `n` routes for `n` players.


## To Run
p2q1.py
```
py p2q1_main.py
```

p2q2.py
```
py p2q2_main.py
```

## Results
It works pretty okay when ranked relatively against 160+ other algorithms (ranked 2 of 161 overall), even though ours wasn't exactly very efficient and it probably won't scale compared to those who used k-means clustering for p2q2. Our algorithm will run really, really slow (~10s-ish) especially on clustered datasets when p is high.

| Team ID | Score (/9) | Penalty for failed cases | Quality score (/6) | Performance score (/3) | No. of failed cases | Overall Rank T | Overall Rank Q | Rank0 Q | Rank1 Q | Rank2 Q | Rank3 Q | Rank4 Q | Rank5 Q | Rank6 Q | Rank7 Q | Rank8 Q | Rank9 Q | Rank10 Q | Rank11 Q | Rank12 Q | Rank13 Q | Rank14 Q | Rank15 Q | Results0 Q | Results1 Q | Results2 Q | Results3 Q | Results4 Q | Results5 Q | Results6 Q | Results7 Q | Results8 Q | Results9 Q | Results10 Q | Results11 Q | Results12 Q | Results13 Q | Results14 Q | Results15 Q | Overall Rank T | Rank0 T | Rank1 T | Rank2 T | Rank3 T | Rank4 T | Rank5 T | Rank6 T | Rank7 T | Rank8 T | Rank9 T | Rank10 T | Rank11 T | Rank12 T | Rank13 T | Rank14 T | Rank15 T | Results0 T | Results1 T | Results2 T | Results3 T | Results4 T | Results5 T | Results6 T | Results7 T | Results8 T | Results9 T | Results10 T | Results11 T | Results12 T | Results13 T | Results14 T | Results15 T |
|---------|------------|--------------------------|--------------------|------------------------|---------------------|----------------|----------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|-------------|-------------|-------------|-------------|-------------|-------------|----------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|-------------|-------------|-------------|-------------|-------------|-------------|
| G2_T11  | 8          | 0                        | 5.9                | 2.1                    | 0                   | 97.9           | 18.1           | 10      | 27      | 2       | 6       | 31      | 30      | 40      | 41      | 8       | 10      | 26       | 11       | 5        | 19       | 11       | 12       | 48.91      | 41.56      | 194.96     | 217.52     | 47.08      | 40.83      | 300.02     | 321.9      | 597.12     | 621.04     | 78.05       | 54.23       | 363.05      | 386.59      | 921.53      | 951.56      | 97.9           | 21      | 74      | 99      | 94      | 45      | 95      | 126     | 122     | 133     | 127     | 39       | 91       | 122      | 118      | 131      | 129      | 15         | 31         | 531        | 531        | 15         | 31         | 1343       | 1328       | 11813      | 11859      | 15          | 31          | 1015        | 1032        | 10969       | 10985       |

| Team ID | Score (/9) | Penalty for failed cases | Quality score (/6) | Performance score (/3) | No. of failed cases | Overall Rank T | Overall Rank Q | Rank0 Q | Rank1 Q | Rank2 Q | Rank3 Q | Rank4 Q | Rank5 Q | Rank6 Q | Rank7 Q | Rank8 Q | Rank9 Q | Rank10 Q | Rank11 Q | Rank12 Q | Rank13 Q | Rank14 Q | Rank15 Q | Results0 Q | Results1 Q | Results2 Q | Results3 Q | Results4 Q | Results5 Q | Results6 Q | Results7 Q | Results8 Q | Results9 Q | Results10 Q | Results11 Q | Results12 Q | Results13 Q | Results14 Q | Results15 Q | Overall Rank T | Rank0 T | Rank1 T | Rank2 T | Rank3 T | Rank4 T | Rank5 T | Rank6 T | Rank7 T | Rank8 T | Rank9 T | Rank10 T | Rank11 T | Rank12 T | Rank13 T | Rank14 T | Rank15 T | Results0 T | Results1 T | Results2 T | Results3 T | Results4 T | Results5 T | Results6 T | Results7 T | Results8 T | Results9 T | Results10 T | Results11 T | Results12 T | Results13 T | Results14 T | Results15 T |
|---------|------------|--------------------------|--------------------|------------------------|---------------------|----------------|----------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|-------------|-------------|-------------|-------------|-------------|-------------|----------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|-------------|-------------|-------------|-------------|-------------|-------------|
| G2_T11  | 7.9        | 0                        | 5.8                | 2.1                    | 0                   | 96.3           | 19.5           | 6       | 13      | 22      | 12      | 14      | 49      | 34      | 7       | 36      | 33      | 28       | 9        | 8        | 5        | 22       | 14       | 48.91      | 41.56      | 778.11     | 847.93     | 47.08      | 40.58      | 300.02     | 321.9      | 695.64     | 783.89     | 78.05       | 51.86       | 361.04      | 386.59      | 1004.84     | 1067.64     | 96.3           | 52      | 53      | 114     | 108     | 61      | 68      | 139     | 140     | 111     | 107     | 55       | 22       | 138      | 135      | 120      | 117      | 31         | 16         | 1937       | 1953       | 31         | 31         | 1562       | 1656       | 1562       | 1562       | 31          | 15          | 1171        | 1203        | 1359        | 1375        |


## Notes

We also used [GPS Visualizer](https://www.gpsvisualizer.com/map_input?form=google) to visualise the points and paths generated.

![ct1](https://i.imgur.com/Cu1isiP.jpg)
Plotting out the points of the datasets (mixed, random and clustered).

![ct2](https://i.imgur.com/VzrXiiC.jpg)
During the process, we also visualised our various approaches to ensure that our algorithm is really working. Here's how we visualised three different versions of our p2q1 algorithm using GPS Visualizer.

## Authors

Goi Jia Jian ([@gjj](https://github.com/gjj)) and Nicolas Wijaya ([@nicoonnicolas](https://github.com/nicoonnicolas))
