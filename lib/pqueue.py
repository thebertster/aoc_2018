class PriorityQueue:
    # Implements a priority queue for unique items. Lowest priority
    # is popped first.

    def __init__(self, reverse_priority=False):
        self._heap = [0]
        self._size = 0
        self._lookup = {}

    def lookup(self, value):
        return self._lookup.get(value, None)

    def size(self):
        return self._size

    def _swap(self, index1, index2):
        (self._heap[index1],
         self._heap[index2]) = (self._heap[index2],
                               self._heap[index1])
        self._lookup[self._heap[index1][1]] = index1
        self._lookup[self._heap[index2][1]] = index2

    def _bubble_up(self, index):
        while index > 1:
            parent = index // 2
            if self._heap[index][0] < self._heap[parent][0]:
                self._swap(parent, index)
            index = parent

    def _bubble_down(self, index):
        while index * 2 < self._size:
            left = index * 2
            right = index*2 + 1
            if left > self._size or self._heap[left][0] < self._heap[right][0]:
                min_child = left
            else:
                min_child = right
            self._swap(min_child, index)
            index = min_child

    def pop(self):
        if self._size == 0:
            return None
        popped_item = self._heap[1]
        self._heap[1] = self._heap[self._size]
        self._lookup[self._heap[1][1]] = 1
        self._heap.pop()
        self._size -= 1
        self._bubble_down(1)
        self._lookup.pop(popped_item[1])
        return popped_item

    def push(self, priority, value):
        # If value is already in the queue, reprioritise it,
        # otherwise add it.
        if value in self._lookup:
            old_index = self._lookup[value]
            if old_index > self._size:
                print('Ahh!')
            old_priority = self._heap[old_index][0]
            if old_priority < priority:
                self._heap[old_index][0] = priority
                self._bubble_down(old_index)
            elif old_priority > priority:
                self._heap[old_index][0] = priority
                self._bubble_up(old_index)
        else:
            self._heap.append([priority, value])
            self._size += 1
            self._lookup[value] = self._size
            self._bubble_up(self._size)
