# CT Project 2

COR-IS1702 Computational Thinking AY19/20 Term 2 Project 2

## p2q1 Flag Game: Single Player

Seems to be a variant of TSP: prize collecting TSP. Our solver uses the greedy approach with objective to `max(points per distance travelled)` to construct an initial route, then use 2-opt to improve the initial route and thereafter, uses a trim function if the route returns more points than required.

We found that in some cases, using the [Euclidean squared distance method](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#euclidean-distance-squared) return a much shorter route. No idea why, but thanks to [@xinweiiiii](https://github.com/xinweiiiii) for pointing it out.

So we decided to run the same greedy algorithm twice, both with the same objective but different distance calculating method (first being the Euclidean distance using Mok’s method in `utility.py`, and second being the one that does not square root).

Total complexity of our solver is `O(n^3)`, where `n` is the number of flags – the worst case happens when `p = sum(flag points)` as the all flags will be part of the best route.

## p2q2 Flag Game: Multi Player

Again, seems to be the prize collecting VRP problem. We adopted a similar greedy + 2-opt approach for question 2, and we created greedy_multiple, try2opt_multiple and get_route_dist_multiple wrapper functions that loop through m (number of players) and call our question 1’s functions. We also have two decisions here:

- When `n = 1`, immediately return our question 1’s `get_route()` results
- When `p <= 800` (a threshold set by us), we run our `get_route()` in single player mode for comparison with our multiplayer algorithm later – complexity for `get_route()` is `O(n^3)`

For the greedy approach, it was modified to allow up to two players to take one greedy step at a time using the same objective, except that we only used the Euclidean distance method (i.e. the one with square root).

Total complexity is still `O(n^3)` as it largely follows our question 1 logic, where `n` is the number of flags, and also because we do not account for `m` as we analysed the results of sending out `2` players vs. `m` players – sending out only 2 players is almost always the better option for our algorithm design.

## To Run
p2q1.py
```
py p2q1_main.py
```

p2q2.py
```
py p2q2_main.py
```
