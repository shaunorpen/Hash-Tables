# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.resized = False
        self.usedCapacity = 0

    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        pass


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return abs(self._hash(key)) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        '''

        index = self._hash_mod(key)

        if self.storage[index] == None:
            self.storage[index] = LinkedPair(key, value)
        else:
            curVal = self.storage[index]
            while curVal:
                if curVal.key == key:
                    curVal.value = value
                    return
                else:
                    if curVal.next:
                        curVal = curVal.next
                    else:
                        curVal.next = LinkedPair(key, value)
                        return
        
        self.usedCapacity += 1

        if self.usedCapacity / self.capacity >= 0.7 and self.resized == True:
            self.resize()

    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''

        index = self._hash_mod(key)

        curVal = self.storage[index]
        nextVal = curVal.next

        if nextVal is None:
            self.storage[index] = None
        else:
            if curVal.key == key:
                self.storage[index] = nextVal
            else:
                while nextVal:
                    if nextVal.key == key:
                        curVal.next = nextVal.next
                        return
                    else:
                        curVal = nextVal
                        nextVal = curVal.next

        self.usedCapacity -= 1

        if self.usedCapacity / self.capacity <= 0.2 and self.resized == True:
            self.resize()


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)

        value = self.storage[index]

        if value is None:
            return None
        while value.next or value.value:
            if value.key == key:
                return value.value
            else:
                value = value.next

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        newCapacity = 2 * self.capacity if self.usedCapacity / self.capacity >= 0.7 else int(0.5 * self.capacity)
        newStorage = [None] * newCapacity
        oldStorage = self.storage

        self.capacity = newCapacity
        self.storage = newStorage

        for i in oldStorage:
            if i is None:
                continue
            else:
                self.insert(i.key, i.value)
                while i.next is not None:
                    i = i.next
                    self.insert(i.key, i.value)

        self.resized = True



if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
