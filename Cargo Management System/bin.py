from avl import AVLTree

class Bin:
    def __init__(self, bin_id, capacity):
        temp = AVLTree()
        self._tree1 = temp
        self._bin_id = bin_id
        self._capacity = capacity

    def add_object(self, object):
        self._capacity -= object._size
        self._tree1.insert(object._object_id, object)

    def remove_object(self, object_id):
        object_node = self._tree1.search(object_id)
        if object_node is not None:
            obj = object_node.element
            object_size = obj._size
            self._capacity += object_size
            self._tree1.delete(object_id)

        
