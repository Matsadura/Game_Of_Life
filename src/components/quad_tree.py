class QuadTree:
    """QuadTree class for storing alive cells."""
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Boundary of the node (x, y, width, height)
        self.capacity = capacity  # Maximum number of points in this node
        self.cells = []  # List of living cells
        self.divided = False  # Indicates if this node is divided

    def subdivide(self):
        """Subdivide the current node into four child nodes."""
        x, y, w, h = self.boundary
        nw = QuadTree((x, y, w / 2, h / 2), self.capacity)
        ne = QuadTree((x + w / 2, y, w / 2, h / 2), self.capacity)
        sw = QuadTree((x, y + h / 2, w / 2, h / 2), self.capacity)
        se = QuadTree((x + w / 2, y + h / 2, w / 2, h / 2), self.capacity)
        self.northwest = nw
        self.northeast = ne
        self.southwest = sw
        self.southeast = se
        self.divided = True

    def insert(self, cell):
        """Insert a cell into the quadtree."""
        if not self.contains(cell):
            return False

        if len(self.cells) < self.capacity:
            self.cells.append(cell)
            return True
        else:
            if not self.divided:
                self.subdivide()
            return (self.northwest.insert(cell) or 
                    self.northeast.insert(cell) or 
                    self.southwest.insert(cell) or 
                    self.southeast.insert(cell))

    def contains(self, cell):
        """Check if a cell is within the boundary of this quadtree node."""
        x, y, width, height = self.boundary
        cell_x, cell_y = cell
        return (x <= cell_x < x + width) and (y <= cell_y < y + height)
