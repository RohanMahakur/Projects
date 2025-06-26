from node import Node
from exceptions import NoBinFoundException


def comp_1(node_1, node_2):
    if node_1.key == node_2.key:
        return 0
    elif node_1.key > node_2.key:
        return 1
    else:
        return -1


def _height(node):
    if not node:
        return 0
    else:
        return node.height


def _update_height(node):
    node.height = 1 + max(_height(node.left), _height(node.right))


def _minimum(node):
    curr = node
    while curr.left is not None:
        curr = curr.left
    return curr


def _maximum(node):
    curr = node
    while curr.right is not None:
        curr = curr.right
    return curr


def _balance_factor(node):
    if not node:
        return 0
    return _height(node.left) - _height(node.right)


def _rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    _update_height(y)
    _update_height(x)
    return x


def _rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    _update_height(x)
    _update_height(y)
    return y


def _balance(node):
    if _balance_factor(node) > 1:
        if _balance_factor(node.left) < 0:
            node.left = _rotate_left(node.left)
        return _rotate_right(node)

    if _balance_factor(node) < -1:
        if _balance_factor(node.right) > 0:
            node.right = _rotate_right(node.right)
        return _rotate_left(node)

    return node


class AVLTree:
    def __init__(self, comparator_function=comp_1):
        self.root = None
        self.size = 0
        self.comparator = comparator_function

    def _insert(self, node, new_node):
        if node is None:
            self.size = self.size + 1
            return new_node
        comp = self.comparator(new_node, node)
        if comp == 0:
            node.element = new_node.element
        elif comp < 0:
            node.left = self._insert(node.left, new_node)
        else:
            node.right = self._insert(node.right, new_node)

        _update_height(node)
        return _balance(node)

    def insert(self, key, element):
        new = Node(key, element)
        self.root = self._insert(self.root, new)

    def minimum(self):
        if self.root:
            return _minimum(self.root)
        return None

    def maximum(self):
        if self.root:
            return _maximum(self.root)
        return None

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        target = Node(key, None)
        result = self.comparator(target, node)

        if result == 0:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            succ = _minimum(node.right)
            node.key = succ.key
            node.element = succ.element
            node.right = self._delete(node.right, succ.key)

        elif result > 0:
            node.right = self._delete(node.right, key)
        else:
            node.left = self._delete(node.left, key)

        _update_height(node)
        return _balance(node)

    def search(self, key):
        node = self._search(self.root, key)
        if node is not None:
            return node
        else:
            return None

    def _search(self, node, key):
        if not node:
            return None

        target = Node(key, None)
        result = self.comparator(target, node)

        if result == 0:
            return node
        elif result > 0:
            return self._search(node.right, key)
        else:
            return self._search(node.left, key)

    def _objects(self, node, lt):
        if node:
            if node.left:
                self._objects(node.left, lt)
            lt.append(node.key)
            if node.right:
                self._objects(node.right, lt)

    def list_of_obj(self):
        list_obj = []
        if self.root:
            self._objects(self.root, list_obj)
        return list_obj if list_obj else []

    def _closest(self, curr, key, closest=None):
        if curr is None:
            return closest

        search_node = Node(key, None)
        comp = self.comparator(search_node, curr)

        if comp == 0:
            return curr
        elif comp < 0:
            if curr.left is not None:
                if closest is not None:
                    closest_compare = self.comparator(closest, curr)
                    if closest_compare >= 0:
                        return self._closest(curr.left, key, curr)
                    else:
                        return self._closest(curr.left, key, closest)
                else:
                    return self._closest(curr.left, key, curr)

            else:
                if closest is None:
                    return curr
                else:
                    closest_compare = self.comparator(closest, curr)
                    if closest_compare < 0:
                        return closest
                    else:
                        return curr
        else:
            if curr.right is None:
                return closest
            else:
                return self._closest(curr.right, key, closest)

    def compact_greatest(self, key):
        search_node = self.search(key)
        if search_node:
            return search_node.element.maximum().element

        node = self.root
        if node:
            node = self._closest(node, key)
            if node:
                return node.element.maximum().element
            raise NoBinFoundException
        raise NoBinFoundException

    def compact_least(self, key):
        search_node = self.search(key)
        if search_node:
            return search_node.element.minimum().element

        node = self.root
        if node:
            node = self._closest(node, key)
            if node:
                return node.element.minimum().element
            raise NoBinFoundException
        raise NoBinFoundException

    def largest_least(self, key):
        maxx = self.maximum()
        node = maxx
        if node is None:
            raise NoBinFoundException
        else:
            return node.element.minimum().element

    def insert_cap_tree(self, key, element_bin):
        existing_node = self.search(key)
        if existing_node:
            existing_node.element.insert(element_bin._bin_id, element_bin)
        else:
            new_tree = AVLTree()
            new_tree.insert(element_bin._bin_id, element_bin)
            self.insert(key, new_tree)

    def del_cap_tree(self, bin_obj):
        target_node = self.search(bin_obj._capacity)
        if target_node.element.root.height != 1:
            target_node.element.delete(bin_obj._bin_id)
        else:
            self.delete(bin_obj._capacity)
