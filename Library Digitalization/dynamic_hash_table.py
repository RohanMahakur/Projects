from prime_generator import get_next_size
from hash_table import HashSet, HashMap

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)

    def rehash(self):
        n = get_next_size()
        origlist = self.list
        self.num_elements = 0

        if self.collision_type == "Double":
            self.params = (*self.params[:3], n)
            self.list = [None for _ in range(n)]
            for key in origlist:
                if key:
                    self.insert(key)

        elif self.collision_type == "Linear":
            self.params = (*self.params[:1], n)
            self.list = [None for _ in range(n)]
            for key in origlist:
                if key:
                    self.insert(key)
        else:
            self.params = (*self.params[:1], n)
            self.list = [[] for _ in range(n)]
            for arr in origlist:
                if arr:
                    for key in arr:
                        self.insert(key)

    def insert(self, x):
        super().insert(x)
        if self.get_load() >= 0.5:
            self.rehash()

    def __str__(self):
        output = []
        if self.collision_type == "Chain":
            for bucket in self.list:
                if bucket:
                    output.append(" ; ".join(str(element) for element in bucket))
                else:
                    output.append("<EMPTY>")
            result = " | ".join(output)
        else:
            result_parts = []
            for element in self.list:
                if element is None:
                    result_parts.append("<EMPTY>")
                else:
                    result_parts.append(str(element))
            result = " | ".join(result_parts)

        return result


class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)

    def rehash(self):
        n = get_next_size()
        origlist = self.list
        self.num_elements = 0

        if self.collision_type == "Double":
            self.params = (*self.params[:3], n)
            self.list = [None for _ in range(n)]
            for key in origlist:
                if key:
                    self.insert(key)

        elif self.collision_type == "Linear":
            self.params = (*self.params[:1], n)
            self.list = [None for _ in range(n)]
            for key in origlist:
                if key:
                    self.insert(key)
        else:
            self.params = (*self.params[:1], n)
            self.list = [[] for _ in range(n)]
            for arr in origlist:
                if arr:
                    for key in arr:
                        self.insert(key)
        
    def insert(self, x):
        super().insert(x)
        if self.get_load() >= 0.5:
            self.rehash()

    def __str__(self):
        output = []
        if self.collision_type == "Chain":
            for bucket in self.list:
                if bucket:
                    output.append(" ; ".join(str(element) for element in bucket))
                else:
                    output.append("<EMPTY>")
            result = " | ".join(output)
        else:
            result_parts = []
            for element in self.list:
                if element is None:
                    result_parts.append("<EMPTY>")
                else:
                    result_parts.append(str(element))
            result = " | ".join(result_parts)

        return result