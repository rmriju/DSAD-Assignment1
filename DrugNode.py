
# Drug Node class as a binary tree
class DrugNode:
    def __init__(self, uid=None, availCount=0):
        self.uid = uid
        self.avCount = availCount
        self.chkoutCtr = 1
        self.left = None
        self.right = None

    def _addDrug(self, uid, availCount):
        if self.uid:
            if uid == self.uid:
                self.avCount = self.avCount + availCount
            elif uid < self.uid:
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
            if len(drug) > 1:
                if len(drug) == 2:
                    # total_buyOrder = total_buyOrder + 1
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
                print()
                if len(tag) == 2 and tag[0] == 'updateDrugList':
                    args = tag[1].split(',')
                    self._updateDrugList(int(args[0]), int(args[1]))
                    print("----------------------------------------")
                elif len(tag) == 2 and tag[0] == 'freqDemand':
                    args = tag[1].split(',')
                    print("High demand drugs")
                    print("----------------------------------------")
                elif len(tag) == 1 and tag[0] == 'printDrugInventory':
                    print("Drug Inventory")
                    print("----------------------------------------")
                    self.printDrugInventory()

                elif len(tag) == 1 and tag[0] == 'printStockOut':
                    print("Drug Stock out")
                    print("----------------------------------------")
                    self.printStockOut()

                elif len(tag) == 2 and tag[0] == 'checkDrugStatus':
                    print("\nDrug Status from supplied input")
                    print("----------------------------------------")
                elif len(tag) == 2 and tag[0] == 'supplyShortage':
                    print("\nDrug supply shortage")
                    print("----------------------------------------")
            else:
                print('File Input - invalid format')

    def _updateDrugList(self, uid, availCount):
        # Get the drug node to update
        drugToUpdate = self.searchNode(uid)
        if drugToUpdate.avCount - availCount > -1:
            drugToUpdate.chkoutCtr = drugToUpdate.chkoutCtr + 1
            # Sell order
            if drugToUpdate.chkoutCtr % 2 == 0:
                drugToUpdate.avCount = drugToUpdate.avCount - availCount
                # total_saleOrder = total_saleOrder + 1
                print("Sale order for", drugToUpdate.uid, ", qty =", availCount, ", Bal Stock =", drugToUpdate.avCount)
            # Buy order
            else:
                drugToUpdate.avCount = drugToUpdate.avCount + availCount
                # total_buyOrder = total_buyOrder + 1
                print("Buy order for", drugToUpdate.uid, ", qty =", availCount, ", Bal Stock =", drugToUpdate.avCount)
        else:
            print("Insufficient stock!\nOnly", drugToUpdate.avCount, "stock left for medicine", drugToUpdate.uid)

    def searchNode(self, uid):
        # returns if the medicine matches
        if self.uid == uid:
            return self
        # Search in left
        elif uid < self.uid and self.left is not None:
            return self.left.searchNode(uid)
        # Search in right
        elif uid > self.uid and self.right is not None:
            return self.right.searchNode(uid)

    def printDrugInventory(self, flag=0):
        if flag == 0:
            print('Total number of medicines entered in the inventory - ?')
        print(self.uid, ",", self.avCount),
        if self.left:
            return self.left.printDrugInventory(1)
        if self.right:
            return self.right.printDrugInventory(2)

    def printStockOut(self, flag=0):
        if self.avCount == 0:
            if flag == 0:
                print("The following medicines are out of stock:")
            print(self.uid)
            flag = 1
        # Traverse to next left
        if self.left:
            return self.left.printStockOut(flag)
        # Traverse to next right
        if self.right:
            return self.right.printStockOut(flag)


if __name__ == '__main__':
    drugList = DrugNode()
    # global total_buyOrder, total_saleOrder
    # total_buyOrder = 0
    # total_saleOrder = 0

    # drugList.addDrug(111, 10)
    # drugList.addDrug(112, 6)
    # drugList.addDrug(113, 1)
    # drugList.addDrug(114, 25)
    # drugList.addDrug(112, 3)
    drugList.readDrugList()
    drugList.executePromptsTags()
