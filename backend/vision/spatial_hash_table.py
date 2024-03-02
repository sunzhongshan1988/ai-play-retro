class SpatialHashTable:
    """
    SpatialHashTable class to store objects in a grid of cells for efficient spatial queries.
    """
    def __init__(self, width, height, cell_size):
        """ Initialize the spatial hash table with the given width, height, and cell size. 
        Args:
            width (int): The width of the table.
            height (int): The height of the table.
            cell_size (int): The size of each cell.

        Returns:
            None
        """
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.columns = int(width / cell_size)
        self.rows = int(height / cell_size)
        self.table = [[[] for _ in range(self.columns)] for _ in range(self.rows)]

    def _get_bucket_indices(self, x, y, width, height):
        """Calculate the indices of the buckets that the object covers.
        Args:
            x (int): The x position of the object.
            y (int): The y position of the object.
            width (int): The width of the object.
            height (int): The height of the object.

        Returns:
            tuple: A tuple of 4 integers, each integer represents the index of the bucket.
        """

        start_row, start_col = int(y / self.cell_size), int(x / self.cell_size)
        end_row, end_col = int((y + height) / self.cell_size), int((x + width) / self.cell_size)
        return start_row, start_col, end_row, end_col

    def insert(self, obj, x, y, width, height):
        """Insert the object into all the covering buckets.
        Args:
            obj (object): The object to insert.
            x (int): The x position of the object.
            y (int): The y position of the object.
            width (int): The width of the object.
            height (int): The height of the object.

        Returns:
            None
        """

        start_row, start_col, end_row, end_col = self._get_bucket_indices(x, y, width, height)
        for row in range(start_row, min(end_row + 1, self.rows)):
            for col in range(start_col, min(end_col + 1, self.columns)):
                self.table[row][col].append(obj)

    def query(self, x, y, width, height):
        """Query the objects in the given area.
        Args:
            x (int): The x position of the area.
            y (int): The y position of the area.
            width (int): The width of the area.
            height (int): The height of the area.
        Returns:
            list: A list of objects in the area.
        """

        objects = set()  # Use a set to avoid duplicates
        start_row, start_col, end_row, end_col = self._get_bucket_indices(x, y, width, height)
        for row in range(start_row, min(end_row + 1, self.rows)):
            for col in range(start_col, min(end_col + 1, self.columns)):
                objects.update(self.table[row][col])
        return list(objects)

    def remove(self, obj, x, y, width, height):
        """Remove the object from the covering buckets.
        Args:
            obj (object): The object to remove.
            x (int): The x position of the object.
            y (int): The y position of the object.
            width (int): The width of the object.
            height (int): The height of the object.
        Returns:
            None
        """

        start_row, start_col, end_row, end_col = self._get_bucket_indices(x, y, width, height)
        for row in range(start_row, min(end_row + 1, self.rows)):
            for col in range(start_col, min(end_col + 1, self.columns)):
                if obj in self.table[row][col]:
                    self.table[row][col].remove(obj)


    def print_elements_positions(self, elements: list[str]):
        """Print all the elements positions in the spatial hash table. Only testing! 
        Args:
            spatial_hash_table (SpatialHashTable): The spatial hash table.
            elements (list[str]): A list of elements to print their positions.
        Returns:
            None
        """
        for row in range(self.rows):
            for col in range(self.columns):
                if self.table[row][col] and any([e in self.table[row][col] for e in elements]):
                    print(f"({row}, {col}): {self.table[row][col]}")
