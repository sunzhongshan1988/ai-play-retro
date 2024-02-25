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
        # 计算对象覆盖的所有桶的索引
        start_row, start_col = int(y / self.cell_size), int(x / self.cell_size)
        end_row, end_col = int((y + height) / self.cell_size), int((x + width) / self.cell_size)
        return start_row, start_col, end_row, end_col

    def insert(self, obj, x, y, width, height):
        # 将对象插入到所有覆盖的桶中
        start_row, start_col, end_row, end_col = self._get_bucket_indices(x, y, width, height)
        for row in range(start_row, min(end_row + 1, self.rows)):
            for col in range(start_col, min(end_col + 1, self.columns)):
                self.table[row][col].append(obj)

    def query(self, x, y, width, height):
        # 查询给定区域内的对象
        objects = set()  # 使用集合避免重复
        start_row, start_col, end_row, end_col = self._get_bucket_indices(x, y, width, height)
        for row in range(start_row, min(end_row + 1, self.rows)):
            for col in range(start_col, min(end_col + 1, self.columns)):
                objects.update(self.table[row][col])
        return list(objects)

    def remove(self, obj, x, y, width, height):
        # 从覆盖的桶中移除对象
        start_row, start_col, end_row, end_col = self._get_bucket_indices(x, y, width, height)
        for row in range(start_row, min(end_row + 1, self.rows)):
            for col in range(start_col, min(end_col + 1, self.columns)):
                if obj in self.table[row][col]:
                    self.table[row][col].remove(obj)
