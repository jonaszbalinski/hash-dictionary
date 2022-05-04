from random import randrange
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class HashTableChaining:
    def __init__(self, isRehashEnabled = True, maxHashRange = 1000000):
        self.data = []
        self.size = 0
        self.hashRange = 16
        self.hashRangeModifier = 4
        self.isRehashEnabled = isRehashEnabled
        if not isRehashEnabled:
            self.hashRange = maxHashRange

        for _ in range(self.hashRange):
            self.data.append([])

    def find(self, value):
        counter = 0
        h = hash(value) % self.hashRange
        for i in range(len(self.data[h])):
            counter += 1
            if self.data[h][i] == value:
                return h, i, counter
        return h, -1, counter

    def insert(self, value):
        h, i, _ = self.find(value)
        if i == -1:
            self.data[h].append(value)
            self.size += 1
        else:
            self.data[h][i] = value

        if self.isRehashEnabled:
            if self.size >= self.hashRange * self.hashRangeModifier:
                print(f"\tRehashing from {self.hashRange} to ",
                f"{self.hashRange * self.hashRangeModifier} (size: {self.size})")
                self.rehash_data(self.hashRange*  self.hashRangeModifier)

    def delete(self, value):
        if self.size > 0:
            h, i, _ = self.find(value)
            if i != -1:
                self.data[h][i] = list(self.data[h]).pop
                self.size -= 1
            if self.isRehashEnabled:
                if self.size * self.hashRangeModifier <= self.hashRange and self.size > 16:
                    print(f"\tRehashing from {self.hashRange} to ",
                        f"{int(self.hashRange / self.hashRangeModifier)} (size: {self.size})")
                    self.rehash_data(int(self.hashRange / self.hashRangeModifier))

    def rehash_data(self, size):
        self.hashRange = size
        newData = []
        for _ in range(self.hashRange):
            newData.append([])

        for table in self.data:
            for value in table:
                h = hash(value) % self.hashRange
                # no need to check for duplicate values
                newData[h].append(value)

        self.data.clear()
        self.data = newData

class DeletedValue:
    pass

class HashTableOpenAddressing:
    def __init__(self, isRehashEnabled = True, maxHashRange = 1000000):
        self.data = []
        self.size = 0
        self.hashRange = 16
        self.hashRangeModifier = 4
        self.isRehashEnabled = isRehashEnabled
        if not isRehashEnabled:
            self.hashRange = maxHashRange

        for _ in range(self.hashRange):
            self.data.append(None)

    def scan_for(self, value):
        firstHash = hash(value) % self.hashRange
        deletedCellIndex = -1
        i = firstHash
        counter = 0
        
        counter += 1 #while
        while self.data[i] != None:
            counter += 2 #if+if or if+elif
            if isinstance(self.data[i], DeletedValue):
                if deletedCellIndex == -1:
                    deletedCellIndex = i
            elif self.data[i] == value:
                return i, counter

            i = (i + 1) % self.hashRange
            counter += 1
            if i == firstHash:
                return deletedCellIndex, counter

            counter += 1 #while

        counter += 1
        if deletedCellIndex != -1:
            return deletedCellIndex, counter

        return i, counter
    
    def find(self, value):
        i, counter = self.scan_for(value)

        counter += 3
        if i == -1:
            counter -= 2
            return None, counter
        elif self.data[i] == None:
            counter -= 1
            return None, counter
        elif isinstance(self.data[i], DeletedValue):
            return None, counter

        return i, counter
    
    def insert(self, value):
        i, _ = self.scan_for(value)
        if i == -1:
            if self.isRehashEnabled:
                print(f"\tRehashing from {self.hashRange} to ",
                    f"{self.hashRange * self.hashRangeModifier} (size: {self.size})")
                self.rehash_data(self.hashRange * self.hashRangeModifier)
                self.insert(value)
        elif value != self.data[i]:
            self.size += 1
            self.data[i] = value

    def delete(self, value):
        if self.size > 0:
            i, _ = self.scan_for(value)
            if (i != -1 and self.data[i] != None and 
                not isinstance(self.data[i], DeletedValue)):
                dV = DeletedValue()
                self.data[i] = dV
                self.size -= 1
            if self.isRehashEnabled:
                if self.size * (self.hashRangeModifier * 2) <= self.hashRange and self.size > 16:
                    print(f"\tRehashing from {self.hashRange} to ",
                        f"{int(self.hashRange / self.hashRangeModifier)} (size: {self.size})")
                    self.rehash_data(int(self.hashRange / self.hashRangeModifier))


    def rehash_data(self, size):
        self.hashRange = size
        newData = []
        for _ in range(self.hashRange):
            newData.append(None)

        for value in self.data:
            if isinstance(value, DeletedValue) or value == None:
                continue

            firstHash = hash(value) % self.hashRange
            i = firstHash
            sum = i
            while newData[i] != None and value != newData[i]:
                i = (i + 1) % self.hashRange
                sum += 1

            newData[i] = value

        self.data.clear()
        self.data = newData

if __name__ == "__main__":
    insertRange = 25000
    deleteRange = 100000
    findRange = 16
    randomRange = 10000

    print("\n", "#"*20, "  Hash table (chaining)  ", "#"*20, "\n")

    print("\n\t ~ Inserting random values ~\n")
    newHashMap = HashTableChaining()
    for _ in range(insertRange):
        newHashMap.insert(randrange(randomRange))

    print("\n\n\t ~ Searching for random values ~\n")
    for j in range(findRange):
        rand = randrange(randomRange)
        h, i, _ = newHashMap.find(rand)
        if i != -1:
            print(f"\tFind value {rand} in {h} (position in list: {i})")
    print()

    print("\n\t ~ Deleting random values ~\n")
    for _ in range(deleteRange):
        newHashMap.delete(randrange(randomRange))

    print("\n\n", "#"*20, "-"*23, "#"*20, "\n")


    print(".\n"*5) ##############################################


    print("\n", "#"*20, "  Hash table (open addressing)  ", "#"*20, "\n")

    print("\n\t ~ Inserting random values ~\n")
    newHashMap = HashTableOpenAddressing()
    for _ in range(insertRange):
        newHashMap.insert(randrange(randomRange))

    print("\n\n\t ~ Searching for random values ~\n")
    for j in range(findRange):
        rand = randrange(randomRange)
        i, _ = newHashMap.find(rand)
        if i != -1 and i != None:
            print(f"\tFind value {rand} in {i}")
    print()

    print("\n\t ~ Deleting random values ~\n")
    for _ in range(deleteRange):
        newHashMap.delete(randrange(randomRange))

    print("\n\n", "#"*20, "-"*30, "#"*20, "\n")


    print(".\n"*5) ##############################################
    print("\t\tPlot visualisation\n") 

    sampleRange = 100000 
    randomRange = 500000
    maxHashRange = 10000

    ### Chaining method without rehash ###
    print("\n\t ~ Chaining method without rehash ~\n")
    newHashMap = HashTableChaining(False, maxHashRange)
    x = []
    y = []

    while len(x) < sampleRange:
        hashMapSize = newHashMap.size
        while hashMapSize == newHashMap.size:
            newHashMap.insert(randrange(randomRange))
        x.append(newHashMap.size)

        a, b, counter  = newHashMap.find(randrange(randomRange))
        y.append(counter)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.ylabel('Number of comparisons')
    plt.xlabel('Hash table size')
    plt.suptitle('Chaining method without rehash')
    plt.show()
    

    ### Chaining method with rehash ###
    print("\n\t ~ Chaining method with rehash ~\n")
    newHashMap = HashTableChaining()
    x = []
    y = []

    while len(x) < sampleRange:
        hashMapSize = newHashMap.size
        while hashMapSize == newHashMap.size:
            newHashMap.insert(randrange(randomRange))
        x.append(newHashMap.size)

        a, b, counter  = newHashMap.find(randrange(randomRange))
        y.append(counter)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.ylabel('Number of comparisons')
    plt.xlabel('Hash table size')
    plt.suptitle('Chaining method with rehash')
    plt.show()

    ### Open addressing method without rehash ###
    print("\n\t ~ Open addressing method without rehash ~\n")
    newHashMap = HashTableOpenAddressing(False, sampleRange*2)
    x = []
    y = []

    while len(x) < sampleRange:
        hashMapSize = newHashMap.size
        while hashMapSize == newHashMap.size:
            newHashMap.insert(randrange(randomRange))
        x.append(newHashMap.size)

        a, counter  = newHashMap.find(randrange(randomRange))
        y.append(counter)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.ylabel('Number of comparisons')
    plt.xlabel('Hash table size')
    plt.suptitle('Open addressing method without rehash')
    plt.show()

    ### Open addressing method with rehash ###
    print("\n\t ~ Open addressing method with rehash ~\n")
    newHashMap = HashTableOpenAddressing()
    x = []
    y = []

    while len(x) < sampleRange:
        hashMapSize = newHashMap.size
        while hashMapSize == newHashMap.size:
            newHashMap.insert(randrange(randomRange))
        x.append(newHashMap.size)

        a, counter  = newHashMap.find(randrange(randomRange))
        y.append(counter)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.ylabel('Number of comparisons')
    plt.xlabel('Hash table size')
    plt.suptitle('Open addressing method with rehash')
    plt.show()
