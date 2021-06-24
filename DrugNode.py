# Drug Node class as a binary tree
class DrugNode:
    def __init__(self, uid=None, availCount=None):
        self.uid = uid
        self.avCount = availCount
        self.chkoutCtr = 1
        self.left = None
        self.right = None

    def _addDrug(self, uid, availCount):
        if self.uid:
            if uid < self.uid:
                if self.left is None:
                    self.left = DrugNode(uid, availCount)
                else:
                    self.left._addDrug(uid, availCount)
            elif uid > self.uid:
                if self.right is None:
                    self.right = DrugNode(uid, availCount)
                else:
                    self.right._addDrug(uid, availCount)
        else:
            self.uid = uid
            self.avCount = availCount

    # Print the tree
    def printTree(self, pos):
        print(self.uid, "(", self.avCount, ",", pos, ")"),
        if self.left:
            self.left.printTree('L')
        if self.right:
            self.right.printTree('R')

    def readDrugList(self):
        file = open("inputPS1.txt")
        content = file.read()
        lines = content.split('\n')
        for line in lines:
            drug = line.split(',')
            print(drug, len(drug))
            if len(drug) > 1:
                if len(drug) == 2:
                    self._addDrug(int(drug[0]), int(drug[1]))
                else:
                    print('File Input - invalid format')

    def executePromptsTags(self):
        file = open("promptsPS1.txt")
        content = file.read()
        lines = content.split('\n')
        for line in lines:
            tag = line.split(':')
            if len(tag) >= 1:
                print("Tag ", tag)
                if len(tag) == 2 and tag[0] == 'updateDrugList':
                    print("For update ", tag)
                    args = tag[1].split(',')
                    return self._updateDrugList(int(args[0]), int(args[1]))
                elif len(tag) == 2 and tag[0] == 'freqDemand':
                    args = tag[1].split(',')
                    return None
                elif len(tag) == 1 and tag[0] == 'printDrugInventory':
                    return None
                elif len(tag) == 1 and tag[0] == 'printStockOut':
                    return None
                elif len(tag) == 1 and tag[0] == 'printDrugInventory':
                    return None
                elif len(tag) == 1 and tag[0] == 'checkDrugStatus':
                    return None
                elif len(tag) == 1 and tag[0] == 'supplyShortage':
                    return None
            else:
                print('File Input - invalid format')

    def _updateDrugList(self, uid, availCount):
        # Get the drug node to update
        drugToUpdate = self.searchNode(uid)
        print("To update qty for ", drugToUpdate)
        drugToUpdate.chkoutCtr = drugToUpdate.chkoutCtr + 1
        # Sell order
        if drugToUpdate.chkoutCtr % 2 == 0:
            drugToUpdate.avCount = drugToUpdate.avCount - availCount
        # Buy order
        else:
            drugToUpdate.avCount = drugToUpdate.avCount + availCount

    def searchNode(self, uid):
        # If value is found in the given binary tree then, set the flag to true
        if self.uid == uid:
            print("Got the record ", uid)
            return self
        # Search in left
        elif uid < self.uid and self.left is not None:
            return self.left.searchNode(uid)
        # Search in right
        elif uid > self.uid and self.right is not None:
            return self.right.searchNode(uid)


if __name__ == '__main__':
    drugList = DrugNode()
    # drugList.addDrug(111, 10)
    # drugList.addDrug(112, 6)
    # drugList.addDrug(113, 1)
    # drugList.addDrug(114, 25)
    # drugList.addDrug(112, 3)

    drugList.readDrugList()
    drugList.printTree('0')

    drugList.executePromptsTags()
    drugList.printTree('0')
