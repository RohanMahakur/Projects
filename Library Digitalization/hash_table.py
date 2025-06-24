from prime_generator import get_next_size


class HashTable:
    def __init__(self, collision_type, params):
        self.collision_type = collision_type
        self.params = params
        self.num_elements = 0

        if self.collision_type == "Linear" or self.collision_type == "Double":
            self.list = [None] * self.params[-1]
        else:
            self.list = [[] for _ in range(self.params[-1])]

    def insert(self, x):
        temp_x = 0
        power = 1
        z = self.params[0]
        key = x[0] if isinstance(x, tuple) else x

        for i in range(len(key)):
            if ord(key[i]) < ord('a'):
                val = ord(key[i]) - ord('A')
                val = val + 26
            else:
                val = ord(key[i]) - ord('a')
            temp_x += (val * power) % self.params[-1]
            power = (power * z) % self.params[-1]
        temp_x %= self.params[-1]

        if self.collision_type == "Linear":
            self.num_elements += 1
            if self.get_load() > 1.0:
                raise Exception("Table is full")
            else:
                self.num_elements -= 1
            z, n = self.params[0], self.params[1]
            while self.list[temp_x]:
                temp_x += 1
                temp_x %= n
            self.list[temp_x] = x

        elif self.collision_type == "Double":
            self.num_elements += 1
            if self.get_load() > 1.0:
                raise Exception("Table is full")
            else:
                self.num_elements -= 1
            z, z2, c2, n = self.params[0], self.params[1], self.params[2], self.params[3]
            temp_x2 = 0
            power = 1
            if self.list[temp_x]:
                for i in range(len(key)):
                    if ord(key[i]) < ord('a'):
                        val = ord(key[i]) - ord('A')
                        val = val + 26
                    else:
                        val = ord(key[i]) - ord('a')
                    temp_x2 += (val * power) % c2
                    power = (power * z2) % c2
                temp_x2 = c2 - temp_x2 % c2
            while self.list[temp_x]:
                temp_x += temp_x2
                temp_x %= n
            self.list[temp_x] = x

        else:
            self.list[temp_x].append(x)
        self.num_elements += 1

    def find(self, key):
        temp_x = 0
        power = 1
        z = self.params[0]
        for i in range(len(key)):
            if ord(key[i]) < ord('a'):
                val = ord(key[i]) - ord('A')
                val = val + 26
            else:
                val = ord(key[i]) - ord('a')
            temp_x += (val * power) % self.params[-1]
            power = (power * z) % self.params[-1]
        temp_x %= self.params[-1]

        if self.collision_type == "Linear":
            while self.list[temp_x] is not None and self.list[temp_x] != key:
                temp_x = (temp_x + 1) % self.params[-1]
            return self.list[temp_x] == key

        elif self.collision_type == "Double":
            z, z2, c2, n = self.params[0], self.params[1], self.params[2], self.params[3]
            temp_x2 = 0
            power = 1
            if self.list[temp_x] is not None:
                if self.list[temp_x] != key:
                    for i in range(len(key)):
                        if ord(key[i]) < ord('a'):
                            val = ord(key[i]) - ord('A')
                            val = val + 26
                        else:
                            val = ord(key[i]) - ord('a')
                        temp_x2 += (val * power) % c2
                        power = (power * z2) % c2
                    temp_x2 = c2 - temp_x2 % c2
            while self.list[temp_x] != key and self.list[temp_x] is not None:
                temp_x = (temp_x + temp_x2) % n
            return self.list[temp_x] == key

        else:
            ok = 0
            for item in self.list[temp_x]:
                if item == key:
                    ok = 1
                    break
            if ok:
                return True
            else:
                return False

    def get_slot(self, key):
        temp_x = 0
        power = 1
        n = self.params[-1]
        z = self.params[0]
        for i in range(len(key)):
            temp_x += (key[i] * power) % n
            power = (power * z) % n
        temp_x = temp_x % n

        if self.collision_type == "Linear":
            while self.list[temp_x] is not key:
                temp_x = (temp_x + 1) % n
            return temp_x

        elif self.collision_type == "Double":
            z, z2, c2, n = self.params[0], self.params[1], self.params[2], self.params[3]
            temp_x2 = 0
            power = 1
            if self.list[temp_x] is not key:
                for i in range(len(key)):
                    temp_x2 += (key[i] * power) % c2
                    power = (power * z2) % c2
                temp_x2 = c2 - temp_x2 % c2
            while self.list[temp_x] is not key:
                temp_x = temp_x + temp_x2
                temp_x %= n
            return temp_x

        else:
            return temp_x

    def get_load(self):
        return self.num_elements / self.params[-1]

    def rehash(self):
        pass

    def __str__(self):
        output = []

        if self.collision_type == "Chain":
            for book in self.list:
                if book:
                    for text in book:
                        first_element, second_element = text[0], text[1]

                        if second_element.list:
                            bucket_str = []
                            for bucket in second_element.list:
                                bucket_str.append(" ; ".join(str(elem) for elem in bucket) if bucket else "<EMPTY>")
                            output.append(f"{first_element}: {' | '.join(bucket_str)}")
                        else:
                            output.append(f"{first_element}: <EMPTY>")
        else:
            for tup in self.list:
                if tup:
                    first_element, second_element = tup[0], tup[1]

                    second_element_str = []
                    for elem in second_element.list:
                        second_element_str.append(str(elem) if elem else "<EMPTY>")

                    output.append(f"{first_element}: {' | '.join(second_element_str)}")

        return "\n".join(output)


class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)

    def insert(self, x):
        super().insert(x)

    def find(self, key):
        return super().find(key)

    def get_slot(self, key):
        return super().get_slot(key)

    def get_load(self):
        return super().get_load()

    def rehash(self):
        return super().rehash()

    def __str__(self):
        return super().__str__()


class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)

    def get_load(self):
        return super().get_load()

    def insert(self, x):
        super().insert(x)

    def rehash(self):
        return super().rehash()

    def __str__(self):
        return super().__str__()

    def find(self, key):
        x = key
        temp_x = 0
        power = 1
        z = self.params[0]

        for i in range(len(x)):
            if ord(x[i]) < ord('a'):
                val = ord(x[i]) - ord('A') + 26
            else:
                val = ord(x[i]) - ord('a')
            temp_x += (val * power) % self.params[-1]
            power = (power * z) % self.params[-1]
        temp_x %= self.params[-1]

        if self.collision_type == "Linear":
            while self.list[temp_x] is not None:
                if self.list[temp_x][0] == key:
                    break
                temp_x = (temp_x + 1) % self.params[-1]
            if self.list[temp_x]:
                if self.list[temp_x][0] == key:
                    return self.list[temp_x][1]
            return None

        elif self.collision_type == "Double":
            temp_x2 = 0
            power = 1
            z, z2, c2, n = self.params[0], self.params[1], self.params[2], self.params[3]
            if self.list[temp_x] is not None and self.list[temp_x][0] != key:
                for i in range(len(x)):
                    if ord(x[i]) < ord('a'):
                        val = ord(x[i]) - ord('A') + 26
                    else:
                        val = ord(x[i]) - ord('a')
                    temp_x2 += (val * power) % c2
                    power = (power * z2) % c2
                    temp_x2 %= c2
                temp_x2 = c2 - temp_x2 % c2
            while self.list[temp_x] is not None:
                if self.list[temp_x][0] == key:
                    break
                temp_x = (temp_x + temp_x2) % n
            if self.list[temp_x]:
                if self.list[temp_x][0] == key:
                    return self.list[temp_x][1]
            return None

        else:
            for item in self.list[temp_x]:
                if item:
                    if item[0] == key:
                        return item[1]
            return None

    def get_slot(self, key):
        temp_x = 0
        power = 1
        z = self.params[0]
        x = key

        for i in range(len(x)):
            if x[i].isupper():
                val = ord(x[i]) - ord('A') + 26
            else:
                val = ord(x[i]) - ord('a')
            temp_x += (val * power) % self.params[-1]
            power = (power * z) % self.params[-1]
        temp_x %= self.params[-1]

        if self.collision_type == "Linear":
            while self.list[temp_x]:
                if self.list[temp_x][0] == key:
                    break
                temp_x = (temp_x + 1) % self.params[-1]
            return temp_x

        elif self.collision_type == "Double":
            z2, c2, n = self.params[1:4]
            temp_x2 = 0
            power = 1
            if self.list[temp_x]:
                if self.list[temp_x][0] != key:
                    for i in range(len(x)):
                        temp_x2 += (x[i] * power) % c2
                        power = (power * z2) % c2
                        temp_x2 %= c2
                    temp_x2 = c2 - temp_x2 % c2
            while self.list[temp_x] and self.list[temp_x][0] != key:
                temp_x = (temp_x + temp_x2) % n
            return temp_x

        else:
            return temp_x