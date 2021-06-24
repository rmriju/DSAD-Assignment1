import os

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
                    # args[0] carries status(Sale/Buy), and args[1] holds freq
                    self.highDemandDrugs(args[0], args[1])

                elif len(tag) == 1 and tag[0] == 'printDrugInventory':
                    print("Drug Inventory")
                    print("----------------------------------------")
                    self.printDrugInventory()

                elif len(tag) == 1 and tag[0] == 'printStockOut':
                    print("Drug Stock out")
                    print("----------------------------------------")
                    self.printStockOut()

                elif len(tag) == 2 and tag[0] == 'checkDrugStatus':
                    self.checkDrugStatus(int(tag[1]))
                    # Check if outputPS1.txt is updated with drug status as per input

                elif len(tag) == 2 and tag[0] == 'supplyShortage':
                    print("\nDrug supply shortage")
                    print("----------------------------------------")
                    self.supplyShortage(int(tag[1]))

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
            # Logic to be updated for calculating total number of medicines entered
            print('Total number of medicines entered in the inventory - ?')
        print(self.uid, ",", self.avCount),
        if self.left:
            return self.left.printDrugInventory(1)
        if self.right:
            return self.right.printDrugInventory(2)

    def printStockOut(self, flag=0):
        if self.uid:
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

    def checkDrugStatus(self, uid):
        # file update with appropriate msg if the medicine matches
        if self.uid == uid:
            fout = open("outputPS1.txt", "a")
            if self.chkoutCtr % 2 == 0:
                print("Drug id", self.uid, "entered", self.chkoutCtr,"times into the system. Its last status was ‘sell’ and currently have", self.avCount, "units available\n", file=fout)
            else:
                print("Drug id", self.uid, "entered", self.chkoutCtr,"times into the system. Its last status was ‘buy’ and currently have", self.avCount, "units available\n", file=fout)
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
            fout = open("outputPS1.txt", "w")
            print("Drug id", self.uid, "does not exist\n", file=fout)
            fout.close()
            return

    def supplyShortage(self, minunits, flag=0):
        if self.avCount <= minunits:
            if flag == 0:
                print("Drugs with supply shortage:")
                flag = 1
            print(self.uid, ",", self.avCount)

        # Traverse to next left
        if self.left:
            return self.left.supplyShortage(minunits, 1)
        # Traverse to next right
        if self.right:
            return self.right.supplyShortage(minunits, 1)

    def highDemandDrugs(self, status, frequency, flag=0):
        # Logic to be updated for identifying high demand drugs
        #
        # if self.avCount <= minunits:
        #     if flag == 0:
        #         print("Drugs with sell entries more than", frequency,"times are:")
        #         flag = 1
        #     print(self.uid, ",", self.chkoutCtr)

        # Traverse to next left
        if self.left:
            return self.left.highDemandDrugs(status, frequency, flag)
        # Traverse to next right
        if self.right:
            return self.right.highDemandDrugs(status, frequency, flag)


if __name__ == '__main__':
    drugList = DrugNode()
    if os.path.exists("outputPS1.txt"):
        os.remove("outputPS1.txt")

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
