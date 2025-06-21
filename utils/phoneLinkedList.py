
class PhonemeNode:
    def __init__(self, phoneme, bin, prob):
        self.__phoneme = phoneme
        self.__bin = bin
        self.__prob = prob
        self.__next = None
        self.__prev = None

    def __repr__(self):
        return f"{self.__phoneme}: {self.__prob}"

    def getPhoneme(self):
        return self.__phoneme
    
    def getBin(self):
        return self.__bin
    
    def getProb(self):
        return self.__prob
    
    def getNext(self):
        return self.__next
    
    def getPrev(self):
        return self.__prev
    
    def setNext(self, node):
        self.__next = node

    def setPrev(self, node):
        self.__prev = node
    
    def compareNode(self, node):
        return self.__bin == node.bin

    def printNode(self):
        print(f"Phoneme {self.__phoneme} with encoding {bin(self.__bin)} has prob {self.__prob}")
        return [self.__phoneme, self.__bin, self.__prob]
    
    def deleteNode(self):
        del self


class PhonemeList:
    
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__count = 0

    def deleteList(self):
        node = self.__head

        while node:
            temp_node = node.getNext()
            del node
            node = temp_node

        del self

    def getHead(self):
        return self.__head
    
    def getTail(self):
        return self.__tail
    
    def getCount(self):
        return self.__count

    def printList(self, limit = -50):
        node = self.__head
        while node and node.getProb() > limit:
            node.printNode()
            node = node.getNext()

    def addNode(self, phoneme, bin, prob):
        node = PhonemeNode(phoneme, bin, prob)
        self.__count += 1
        
        # Initial Node
        if not (self.__head or self.__tail):
            self.__head = node
            self.__tail = node
            return node

        curr_node = self.__head
        
        while curr_node.getProb() > node.getProb():
        
            # Tail
            if not curr_node.getNext():
                curr_node.setNext(node)
                node.setPrev(curr_node)
                self.__tail = node
                return node
            
            curr_node = curr_node.getNext()
        
        # Head
        if not curr_node.getPrev():
            curr_node.setPrev(node)
            node.setNext(curr_node)
            self.__head = node
            return node
        
        curr_node.getPrev().setNext(node)
        node.setPrev(curr_node.getPrev())
        curr_node.setPrev(node)
        node.setNext(curr_node)
        return node


    def copyList(self):
        new_list = PhonemeList()

        curr_node = self.__head

        while curr_node:
            new_list.addNode(curr_node.getPhoneme(), curr_node.getBin(), curr_node.getProb())
            curr_node = curr_node.getNext()

        return new_list
    

    def findNode(self, bin):
        node = self.__head
        
        while node:
            if node.getBin() == bin:
                return node
            
            node = node.getNext()
            
        print(f"Error: Node with number {bin} could not be found")


    def removeNode(self, bin):
        node = self.findNode(bin)
        
        if node:
            if node.getPrev() is not None:
                node.getPrev().setNext(node.getNext())
                
                if node.getNext() is None:
                    self.__tail = node.getPrev()
            
            if node.getNext() is not None:
                node.getNext().setPrev(node.getPrev())

                if node.getPrev() is None:
                    self.__head = node.getNext()
            
            node.deleteNode()

        self.__count -= 1


    def modNodeProb(self, bin, prob):
        node = self.findNode(bin)
        phoneme = node.getPhoneme()

        # Remove old node
        self.removeNode(bin)

        # Readd node with new prob
        self.addNode(phoneme, bin, prob)
