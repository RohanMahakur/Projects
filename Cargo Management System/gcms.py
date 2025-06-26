from bin import Bin
from avl import AVLTree
from object import Object
from exceptions import NoBinFoundException


class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self._cap_tree = AVLTree()
        self._binid_tree = AVLTree()
        self._objid_tree = AVLTree()

    def add_object(self, object_id, size, color):
        new_obj = Object(object_id, size, color)

        if color.value == 1:
            found_bin = self._cap_tree.compact_least(size)
        elif color.value == 2:
            found_bin = self._cap_tree.compact_greatest(size)
        elif color.value in (3, 4):
            max_node = self._cap_tree.maximum()
            if max_node.key < size:
                raise NoBinFoundException
            found_bin = (
                self._cap_tree.largest_least(size) if color.value == 3 else max_node.element.maximum().element)
        else:
            raise NoBinFoundException

        if not found_bin:
            raise NoBinFoundException
        self._objid_tree.insert(object_id, found_bin)
        self._cap_tree.del_cap_tree(found_bin)
        found_bin.add_object(new_obj)
        if found_bin._capacity >= 0:
            self._cap_tree.insert_cap_tree(found_bin._capacity, found_bin)

    def delete_object(self, object_id):
        obj_node = self._objid_tree.search(object_id)
        if obj_node is None:
            raise Exception("Object with the given ID does not exist")
        obj_bin = obj_node.element
        self._objid_tree.delete(object_id)
        if obj_bin:
            self._cap_tree.del_cap_tree(obj_bin)
        obj_bin.remove_object(object_id)
        if obj_bin._capacity is not None:
            self._cap_tree.insert_cap_tree(obj_bin._capacity, obj_bin)

    def add_bin(self, bin_id, capacity):
        binn = Bin(bin_id, capacity)
        self._binid_tree.insert(bin_id, binn)
        if capacity is not None:
            self._cap_tree.insert_cap_tree(capacity, binn)

    def object_info(self, object_id):
        object_node = self._objid_tree.search(object_id)
        if not object_node:
            raise Exception("Object with the given ID does not exist")
        return object_node.element._bin_id

    def bin_info(self, bin_id):
        bin_node = self._binid_tree.search(bin_id)
        if not bin_node:
            raise Exception("Bin with the given ID does not exist")
        found_bin = bin_node.element
        return found_bin._capacity, found_bin._tree1.list_of_obj()
