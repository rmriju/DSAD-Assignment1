# Drug Node class as a binary tree
fout = None


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
            drugExists = self._searchNode(uid)
            if drugExists:
                drugExists.chkoutCtr = drugExists.chkoutCtr + 1
                if drugExists.chkoutCtr % 2 == 0:
                    if drugExists.avCount - availCount > -1:
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

    def readDrugList(self, validFlag=0):
        file = open("inputPS1.txt")
        content = file.read()
        lines = content.split('\n')
        for line in lines:
            drug = line.split(',')
            if len(drug) > 1:
                if len(drug) == 2:
                    self._addDrug(int(drug[0]), int(drug[1]))
                    validFlag = validFlag + 1
                else:
                    print('Invalid drug! - Please correct inputPS1')
        return validFlag

    def executePromptsTags(self):
        file = open("promptsPS1.txt")
        global fout
        self._createOutputFile()
        content = file.read()
        lines = content.split('\n')
        for line in lines:
            tag = line.split(':')
            if len(tag) >= 1:
                print()
                if len(tag) == 2 and tag[0] == 'updateDrugList':
                    args = tag[1].split(',')
                    if len(args) > 1 and args[0] and args[1]:
                        self._updateDrugList(int(args[0]), int(args[1]))

                elif len(tag) == 2 and tag[0] == 'freqDemand':
                    args = tag[1].split(',')
                    print("------ freqDemand:", args[0].strip(), ",", args[1], "------", file=fout)
                    print("Drugs with", args[0].strip(), "entries more than", args[1], "times are:", file=fout)
                    # args[0] carries status(Sale/Buy), and args[1] holds freq
                    self._highDemandDrugs(args[0], int(args[1]))

                elif len(tag) == 1 and tag[0] == 'printDrugInventory':
                    if self is not None:
                        totalMedicines = countTotalMedicines(self)
                    print("------- printDrugInventory --------", file=fout)
                    print('Total number of medicines entered in the inventory - ', totalMedicines, file=fout)
                    self._printDrugInventory()

                elif len(tag) == 1 and tag[0] == 'printStockOut':
                    print("---------- printStockOut -----------", file=fout)
                    print("The following medicines are out of stock:", file=fout)
                    self._printStockOut()

                elif len(tag) == 2 and tag[0] == 'checkDrugStatus':
                    print("------ checkDrugStatus:", tag[1], "-------", file=fout)
                    self._checkDrugStatus(int(tag[1]))

                elif len(tag) == 2 and tag[0] == 'supplyShortage':
                    print("------- supplyShortage:", tag[1], "--------", file=fout)
                    print("minunits:", tag[1], file=fout)
                    print("Drugs with supply shortage:", file=fout)
                    self._supplyShortage(int(tag[1]))
                if len(tag) > 0 and (
                        tag[0] == 'freqDemand' or tag[0] == 'printDrugInventory' or tag[0] == 'printStockOut'
                        or tag[0] == 'checkDrugStatus' or tag[0] == 'supplyShortage'):
                    print("------------------------------------\n", file=fout)

            else:
                print('File Input - invalid format')
        fout.close()

    def _updateDrugList(self, uid, availCount):
        # Get the drug node to update
        drugToUpdate = self._searchNode(uid)
        if drugToUpdate:
            drugToUpdate.chkoutCtr = drugToUpdate.chkoutCtr + 1
            # Sale order
            if drugToUpdate.chkoutCtr % 2 == 0:
                if drugToUpdate.avCount - availCount > -1:
                    drugToUpdate.avCount = drugToUpdate.avCount - availCount
                    print("Sale order for", drugToUpdate.uid, ", qty =", availCount, ", Bal Stock =",
                          drugToUpdate.avCount)
                else:
                    print("Insufficient stock!\nOnly", drugToUpdate.avCount, "stock left for medicine",
                          drugToUpdate.uid)
            # Buy order
            else:
                drugToUpdate.avCount = drugToUpdate.avCount + availCount
                print("Buy order for", drugToUpdate.uid, ", qty =", availCount, ", Bal Stock =", drugToUpdate.avCount)
        else:
            print("Invalid drug input for update!")

    def _searchNode(self, uid):
        # Search in left
        if uid < self.uid and self.left is not None:
            return self.left._searchNode(uid)
        # returns if the medicine matches
        elif self.uid == uid:
            return self
        # Search in right
        elif uid > self.uid and self.right is not None:
            return self.right._searchNode(uid)

    def _printDrugInventory(self):
        if self.left:
            self.left._printDrugInventory()
        print(self.uid, ",", self.avCount, file=fout),
        if self.right:
            self.right._printDrugInventory()

    def _printStockOut(self):
        # Traverse to next left
        if self.left:
            self.left._printStockOut()
        # Inorder traversal - LNR
        if self and self.avCount == 0:
            print(self.uid, file=fout)
        # Traverse to next right
        if self.right:
            self.right._printStockOut()

    def _checkDrugStatus(self, uid):
        # file update with appropriate msg if the medicine matches
        if self.uid == uid:
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
            return
        # Traverse to left
        elif uid < self.uid and self.left is not None:
            return self.left._checkDrugStatus(uid)
        # Traverse to right
        elif uid > self.uid and self.right is not None:
            return self.right._checkDrugStatus(uid)
        else:
            # file update if the drug is not found
            print("Drug id", self.uid, "does not exist\n", file=fout)
            return

    def _supplyShortage(self, minunits, flag=0):
        # Traverse to next left
        if self.left:
            self.left._supplyShortage(minunits, flag)
        # Inorder traversal - LNR
        if self.avCount <= minunits:
            print(self.uid, ",", self.avCount, file=fout)
        # Traverse to next right
        if self.right:
            self.right._supplyShortage(minunits, flag)

    def _highDemandDrugs(self, status, frequency):
        # Traverse to next left
        if self.left:
            self.left._highDemandDrugs(status, frequency)
        # For even counter, buy and sale count are equal
        if self.chkoutCtr % 2 == 0 and (self.chkoutCtr / 2) > frequency:
            print(self.uid, ",", self.chkoutCtr, file=fout)
        # For buy, it will be counter/2 + 1 frequency
        if status.strip() == 'buy' and self.chkoutCtr % 2 == 1 and (self.chkoutCtr // 2) + 1 > frequency:
            print(self.uid, ",", self.chkoutCtr, file=fout)
        if status.strip() == 'sell' and self.chkoutCtr % 2 == 1 and (self.chkoutCtr // 2) > frequency:
            print(self.uid, ",", self.chkoutCtr, file=fout)
        # Traverse to next right
        if self.right:
            self.right._highDemandDrugs(status, frequency)

    def _createOutputFile(self):
        global fout
        fout = open("outputPS1.txt", "w")
        fout.close()
        fout = open("outputPS1.txt", "a")


def countTotalMedicines(drugNode):
    if drugNode is None:
        return 0
    return 1 + countTotalMedicines(drugNode.left) + countTotalMedicines(drugNode.right)


if __name__ == '__main__':
    drugList = DrugNode()
    if drugList.readDrugList():
        drugList.executePromptsTags()
    else:
        print("Invalid drug list entered !")
