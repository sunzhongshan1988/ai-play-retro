import heapq
from vision.node import Node 

class AStarGraph:
    """
    A* search graph for path finding.
    """
    def __init__(self, width, height, obstacles):
        """Initialize the A* search graph.
        Args:
            width (int): The width of the graph.
            height (int): The height of the graph.
            obstacles (list[tuple]): A list of obstacles.
        """
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]
        self.width = width
        self.height = height
        self.obstacles = obstacles
        self._build_graph()

    def _build_graph(self):
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in self.obstacles:
                    self.nodes[x][y].is_obstacle = True
                    continue
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # For 4 directions (up, down, left, right)
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and not self.nodes[nx][ny].is_obstacle:
                        self.nodes[x][y].add_neighbor(self.nodes[nx][ny])

    def heuristic(self, node, goal):
        # Use Manhattan distance as the heuristic
        return abs(node.x - goal.x) + abs(node.y - goal.y)

    def a_star_search(self, start, goal):
        for row in self.nodes:
            for node in row:
                node.g = node.h = node.f = float('inf')
                node.parent = None

        start_node = self.nodes[start[0]][start[1]]
        goal_node = self.nodes[goal[0]][goal[1]]
        open_set = []
        heapq.heappush(open_set, (start_node.f, start_node))

        start_node.g = 0
        start_node.h = self.heuristic(start_node, goal_node)
        start_node.f = start_node.g + start_node.h

        while open_set:
            current_node = heapq.heappop(open_set)[1]

            if current_node == goal_node:
                return self.reconstruct_path(goal_node)

            for neighbor in current_node.neighbors:
                tentative_g = current_node.g + 1  # Assuming the cost between two nodes is 1

                if tentative_g < neighbor.g:
                    neighbor.parent = current_node
                    neighbor.g = tentative_g
                    neighbor.h = self.heuristic(neighbor, goal_node)
                    neighbor.f = neighbor.g + neighbor.h

                    if neighbor not in [n[1] for n in open_set]:
                        heapq.heappush(open_set, (neighbor.f, neighbor))

        return None

    def reconstruct_path(self, end_node):
        path = []
        current = end_node
        while current:
            path.append((current.x, current.y))
            current = current.parent
        path.reverse()  # Reverse the path to get the correct order
        return path
