class ItemExistsException(Exception):
    pass

class NotFoundException(Exception):
    pass

class MyHashableKey:

    def __init__(self, int_value, string_value):
        self.int_value = int_value
        self.string_value = string_value
        


    def __eq__(self, other):
        h = hash(self)
        o = hash(other)
        if h == o:
            return True
        return False



    def __hash__(self):
        mask = (1 << 32) -1 
        h=0
        count = 0
        for integer in str(self.int_value):
            count += 1
            h = (h << count) | (h >> (mask - count))
            h += ord(integer) 
        return h
        
class Node():
    def __init__(self, key, data, next = None):
        self.key = key
        self.data = data
        self.next = None

    

class Bucket():
    def __init__(self):
        self.head = None
        self.size = 0

    def insert(self, key, data):
        if not self.head:
            self.head = Node(key, data, self.head)
            self.size += 1
        else:
            temp = self.head
            while temp.next:
                if temp.key == key:
                    raise ItemExistsException
                temp = temp.next
            temp.next = Node(key, data)
            self.size += 1
        

    def remove(self, key):
        current = self.head
        prev = None
        while current:
            if current.key == key:
                self.head = current.next
                self.size -= 1
                return
            else:
                while current.next:
                    prev = current
                    current = current.next
                    if current.key == key:
                        prev.next = current.next
                        self.size -= 1
                    raise NotFoundException

            

    def update(self, key, data):
        current = self.head
        while current:
            if current.key == key:
                current.data = data
                return
            current = current.next
        raise NotFoundException
        

    def find(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current.data
            current = current.next
        raise NotFoundException

    def contains(self, key):
        current = self.head
        while current:
            if current.key == key:
                return True
            current = current.next
        return False

    def __setitem__(self, key, data):
        current = self.head
        while current:
            if current.key == key:
                current.data = data
                return current.data
            current = current.next
        return self.insert(key, data)

    def __getitem__(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current.data
            current = current.next
        raise NotFoundException


    def __len__(self):
        return self.size

        
class HashMap():
    def __init__(self) -> None:
        self.s = 0
        self.capacity = 7
        self.map = [None] * self.capacity
        self.temp_map = []
    
    
    def rebuild(self):
        if self.s/self.capacity >= 1.2:
            self.capacity *= 2
            self.temp_map = self.map
            self.map = [None] * self.capacity
            self.s = 0
            for i in range(self.capacity // 2):
                self.rebuildAdd(i)


    def rebuildAdd(self, index):
        if self.temp_map[index] is not None:
            current = self.temp_map[index].head
            while current:
                self.insert(current.key, current.data)
                current = current.next

    def getIndex(self, key):
        h = hash(key)
        return h % self.capacity
 

    def insert(self, key, data):
        self.rebuild()
        index = self.getIndex(key)
        if self.map[index] is None:
            self.map[index] = Bucket()
            self.map[index].insert(key, data)
            self.s +=1
            return 
        else:
            raise ItemExistsException
            

    def update(self, key, data):
        index = self.getIndex(key)
        if self.map[index] is not None:
            self.map[index].update(key, data)
        else:
            raise NotFoundException


    def find(self, key):
        index = self.getIndex(key)
        if self.map[index] is not None:
            return self.map[index].find(key)
        else:
            raise NotFoundException


    def contains(self, key):
        index = self.getIndex(key)
        return self.map[index].contains(key)
    

    def remove(self, key):
        index = self.getIndex(key)
        self.map[index].remove(key)
        self.s -= 1

        
    def __setitem__(self, key, data):
        index = self.getIndex(key)
        if self.map[index] is not None:
            if not self.map[index].contains(key):
                self.rebuild()
                self.s += 1
            self.map[index][key] = data
        else:
            return self.insert(key, data)
        
        
    def __getitem__(self, key):
        index = self.getIndex(key)
        node = self.map[index]
        if node is not None:
            return self.find(key)
        raise NotFoundException


    def __len__(self):
        return self.s