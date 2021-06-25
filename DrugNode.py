import os
import copy

# Drug Node class as a binary tree
class DrugNode:
    def __init__(self, uid=None, availCount=0):
        self.uid = uid
        self.avCount = availCount
        self.chkoutCtr = 1
        self.left = None
        self.right = None
        self.parent = None

    def _addDrug(self, uid, availCount):
        newDrugNode = DrugNode(uid, availCount)
        if self.uid:
            drugExists = self.searchNode(uid)
            if drugExists:
                drugExists.chkoutCtr = drugExists.chkoutCtr + 1
                if drugExists.chkoutCtr % 2 == 0:
                    if(drugExists.avCount - availCount > -1):
                        drugExists.avCount = drugExists.avCount - availCount
                    else:
                        print("Invalid Input! For", drugExists.uid, ",should not have negative stock")
                else:
                    drugExists.avCount = drugExists.avCount + availCount
            elif uid < self.uid:
                if self.left is None:
                    self.left = newDrugNode
                    newDrugNode.parent = self
                else:
                    self.left._addDrug(uid, availCount)
            elif uid >= self.uid:
                if self.right is None:
                    self.right = newDrugNode
                    newDrugNode.parent = self
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

                elif len(tag) == 2 and tag[0] == 'freqDemand':
                    args = tag[1].split(',')
                    print("-------High demand drugs-----")
                    print("Drugs with", args[0].strip(), "entries more than", args[1], "times are:")
                    # args[0] carries status(Sale/Buy), and args[1] holds freq
                    self.highDemandDrugs(args[0], int(args[1]))

                elif len(tag) == 1 and tag[0] == 'printDrugInventory':
                    print("-------Drug Inventory-------")
                    print('Total number of medicines entered in the inventory - ?')
                    self.printDrugInventory()

                elif len(tag) == 1 and tag[0] == 'printStockOut':
                    print("-------Drug Stock out-------")
                    print("The following medicines are out of stock:")
                    self.printStockOut()

                elif len(tag) == 2 and tag[0] == 'checkDrugStatus':
                    self.checkDrugStatus(int(tag[1]))
                    # Check if outputPS1.txt is updated with drug status as per input

                elif len(tag) == 2 and tag[0] == 'supplyShortage':
                    print("-------Supply shortage--------")
                    print("Drugs with supply shortage:")
                    self.supplyShortage(int(tag[1]))

            else:
                print('File Input - invalid format')

    def _updateDrugList(self, uid, availCount):
        # Get the drug node to update
        drugToUpdate = self.searchNode(uid)
        if drugToUpdate:
            drugToUpdate.chkoutCtr = drugToUpdate.chkoutCtr + 1
            # Sell order
            if drugToUpdate.chkoutCtr % 2 == 0:
                if drugToUpdate.avCount - availCount > -1:
                    drugToUpdate.avCount = drugToUpdate.avCount - availCount
                    print("Sale order for", drugToUpdate.uid, ", qty =", availCount, ", Bal Stock =", drugToUpdate.avCount)
                else:
                    print("Insufficient stock!\nOnly", drugToUpdate.avCount, "stock left for medicine", drugToUpdate.uid)
            # Buy order
            else:
                drugToUpdate.avCount = drugToUpdate.avCount + availCount
                print("Buy order for", drugToUpdate.uid, ", qty =", availCount, ", Bal Stock =", drugToUpdate.avCount)

    def searchNode(self, uid):
        # Search in left
        if uid < self.uid and self.left is not None:
            return self.left.searchNode(uid)
        # returns if the medicine matches
        elif self.uid == uid:
            return self
        # Search in right
        elif uid > self.uid and self.right is not None:
            return self.right.searchNode(uid)

    def printDrugInventory(self):
        if self.left:
            self.left.printDrugInventory()
        print(self.uid, ",", self.avCount),
        if self.right:
            self.right.printDrugInventory()

    def printStockOut(self):
        # Traverse to next left
        if self.left:
            self.left.printStockOut()
        # Inorder traversal - LNR
        if self and self.avCount == 0:
            print(self.uid)
        # Traverse to next right
        if self.right:
            self.right.printStockOut()

    def checkDrugStatus(self, uid):
        # file update with appropriate msg if the medicine matches
        if self.uid == uid:
            fout = open("outputPS1.txt", "a")
            # Checking Sale or Buy
            if self.chkoutCtr % 2 == 0:
                print("Drug id", self.uid, "entered", self.chkoutCtr,
                      "times into the system. Its last status was ‘sell’ and currently have", self.avCount,
                      "units available\n", file=fout)
            else:
                print("Drug id", self.uid, "entered", self.chkoutCtr,
                      "times into the system. Its last status was ‘buy’ and currently have", self.avCount,
                      "units available\n", file=fout)
            if self.avCount == 0:
                print("All units of drug id", self.uid, "have been sold\n", file=fout)
            fout.close()
            return
        # Traverse to left
        elif uid < self.uid and self.left is not None:
            return self.left.checkDrugStatus(uid)
        # Traverse to right
        elif uid > self.uid and self.right is not None:
            return self.right.checkDrugStatus(uid)
        else:
            # file update if the drug is not found
            fout = open("outputPS1.txt", "a")
            print("Drug id", self.uid, "does not exist\n", file=fout)
            fout.close()
            return

    def supplyShortage(self, minunits, flag=0):
        # Traverse to next left
        if self.left:
            self.left.supplyShortage(minunits, flag)
        # Inorder traversal - LNR
        if self.avCount <= minunits:
            print(self.uid, ",", self.avCount)
        # Traverse to next right
        if self.right:
            self.right.supplyShortage(minunits, flag)

    def highDemandDrugs(self, status, frequency):
        # Traverse to next left
        if self.left:
            self.left.highDemandDrugs(status, frequency)
        # For even counter, buy and sale count are equal
        if self.chkoutCtr % 2 == 0 and (self.chkoutCtr / 2) > frequency:
            print(self.uid, ",", self.chkoutCtr)
        # For buy, it will be counter/2 + 1 frequency
        if status.strip() == 'buy' and self.chkoutCtr % 2 == 1 and (self.chkoutCtr // 2) + 1 > frequency:
            print(self.uid, ",", self.chkoutCtr)
        if status.strip() == 'sell' and self.chkoutCtr % 2 == 1 and (self.chkoutCtr // 2) > frequency:
            print(self.uid, ",", self.chkoutCtr)
        # Traverse to next right
        if self.right:
            self.right.highDemandDrugs(status, frequency)




if __name__ == '__main__':
    drugList = DrugNode()
    if os.path.exists("outputPS1.txt"):
        os.remove("outputPS1.txt")

    drugList.readDrugList()
    drugList.executePromptsTags()
