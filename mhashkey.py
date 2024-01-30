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


    