from hash_table import *


class DigitalLibrary:
    def __init__(self):
        pass

    def distinct_words(self, book_title):
        pass

    def count_distinct_words(self, book_title):
        pass

    def search_keyword(self, keyword):
        pass

    def print_books(self):
        pass


class MuskLibrary(DigitalLibrary):
    def __init__(self, book_titles, texts):
        self.count_list = [0] * len(book_titles)
        self.book_titles, self.texts = self.merge_sort_zipped(book_titles, texts)
        self.unique_list = [[] for _ in range(len(book_titles))]
        for i in range(len(self.texts)):
            self.texts[i] = self.merge_sort(self.texts[i])
            for j in range(1, len(self.texts[i])):
                if self.texts[i][j] != self.texts[i][j - 1]:
                    self.unique_list[i].append(self.texts[i][j])
                    self.count_list[i] += 1
            if self.texts[i]:
                self.unique_list[i].insert(0, self.texts[i][0])
                self.count_list[i] += 1
            self.texts[i] = self.unique_list[i]

    def distinct_words(self, book_title):
        i = self.binary_search(book_title, self.book_titles)
        if i >= 0:
            return self.unique_list[i]

    def count_distinct_words(self, book_title):
        i = self.binary_search(book_title, self.book_titles)
        if i >= 0:
            return self.count_list[i]

    def search_keyword(self, keyword):
        books_list = []
        for i in range(len(self.book_titles)):
            j = self.binary_search(keyword, self.texts[i])
            if j >= 0:
                books_list.append(self.book_titles[i])
        return books_list

    def merge_sort_zipped(self, list1, list2):
        n=len(list1)
        if n < 2:
            return list1, list2

        mid = n // 2
        left1,left2=list1[0:mid],list2[0:mid]
        right1,right2=list1[mid:n],list2[mid:n]
        left1, left2 = self.merge_sort_zipped(left1,left2)
        right1, right2 = self.merge_sort_zipped(right1, right2)

        return self.merge_zipped(left1, right1, left2, right2)

    def merge_zipped(self, left1, right1, left2, right2):
        sorted_list1 = []
        sorted_list2 = []

        while left1 or right1:
            if left1 and (not right1 or left1[0] < right1[0]):
                sorted_list1.append(left1[0])
                sorted_list2.append(left2[0])
                left1.pop(0)
                left2.pop(0)
            else:
                sorted_list1.append(right1[0])
                sorted_list2.append(right2[0])
                right1.pop(0)
                right2.pop(0)

        return sorted_list1, sorted_list2

    def merge_sort(self, list):
        size = len(list)
        if size > 1:
            mid = size // 2
            left = list[0:mid]
            right = list[mid:size]
            left = self.merge_sort(left)
            right = self.merge_sort(right)
            list = self.merge(left, right)

        return list

    def merge(self, left, right):
        i, j = 0, 0
        result = []
        len_left = len(left)
        len_right = len(right)

        while i < len_left and j < len_right:
            if left[i]>right[j]:
                result.append(right[j])
                j += 1
            elif left[i] <= right[j]:
                result.append(left[i])
                i += 1

        result.extend(left[i:] if i < len(left) else right[j:])
        return result

    def binary_search(self, item, list):
        left = 0
        right = len(list) - 1

        while left <= right:
            mid = (left + right) // 2
            if item < list[mid]:
                right = mid - 1
            elif item > list[mid]:
                left = mid + 1
            else:
                return mid

        return -1

    def print_books(self):
        for i in range(len(self.book_titles)):
            print(f"{self.book_titles[i]}: {' | '.join(self.texts[i])}")


class JGBLibrary(DigitalLibrary):
    def __init__(self, name, params):
        self.name = name
        self.params = params
        if name == "Jobs":
            self.collision_type = "Chain"
        elif name == "Gates":
            self.collision_type = "Linear"
        else:
            self.collision_type = "Double"
        self.hash = HashMap(self.collision_type, params)

    def add_book(self, book_title, text):
        text_hash = HashSet(self.collision_type, self.params)
        length = len(text)
        for i in range(length):
            if not text_hash.find(text[i]):
                text_hash.insert(text[i])
        book_exists = self.hash.find(book_title)
        if not book_exists:
            self.hash.insert((book_title, text_hash))

    def count_distinct_words(self, book_title):
        book = self.hash.find(book_title)
        return book.num_elements if book is not None else 0

    def distinct_words(self, book_title):
        book = (self.hash.find(book_title)).list
        word_list = []
        if book:
            for text in book:
                if text:
                    if self.collision_type != "Chain":
                        word_list.append(text)
                    else:
                        for word in text:
                            word_list.append(word)

        return word_list

    def search_keyword(self, keyword):
        final_list = []
        for x1 in self.hash.list:
            if x1:
                if self.name == "Jobs":
                    for x2 in x1:
                        if x2[1].find(keyword):
                            final_list.append(x2[0])
                elif x1[1].find(keyword):
                    final_list.append(x1[0])
        return final_list

    def print_books(self):
        print(self.hash)