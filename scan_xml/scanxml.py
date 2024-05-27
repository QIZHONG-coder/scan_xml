import os
# importing element tree
import csv
moduleList=["TS Integrity Test", "Elute from column", "Labeling Flexible", "Cell Load to Chamber Flexible",
            "Cell Load to Column","Rinse Source to Column", "Wash After Cell Load", "Wash Cells On Column",
            "CheckAndPrimeSOlutionConnection", "Install TS", "Prime TS Separation", "Remove TS","TS Integrity Test",
            "TS Rebuffering", "Cell Wash Flexible","Volume Reduction", ""]

starter='?xml version="1.0" encoding="UTF-8"?programname/namedescription/descriptionmajor/majorminor/minorrevision/revisionwarning/warningcrc/crccommandscommandid/idname/nameposition/positionslotsslotid/idname/nametype/typeunit/unitvalue/value/slotslotid/idname/nametype/typeunit/unitvalue/value/slot'
secondList=[]
def findFiles(dir_path):
    # list to store files
    fileList = []
    # Iterate directory
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(dir_path, file_path)):
            if os.path.splitext(file_path)[1]==".xml":
                # add filename to list
                fileList.append(os.path.join(dir_path, file_path))
        else:
            fileList.extend(findFiles(os.path.join(dir_path,file_path)))
    return fileList
def betweenTag(str,tag):
    return str.split("<"+tag+">")[1].split("</"+tag+">")[0]

def commandList(commands):
    return commands.split("</command>")
def main():
    # directory/folder path
    dir_path = "./xml/"
    stats={}
    moduleStats={}
    blockStats={}
    for fl in findFiles(dir_path):
        with open(fl, 'r') as file:
            data = file.read().replace('\n', '').replace('\t','')
        left=data.split("<")[0:50]
        right=[]
        middle=[] 
        for str in left:
            if str!="":
                if str[-1]==">":
                    right.append(str[0:len(str)-1])
                else:
                    temp=str.split(">")
                    right.append(temp[0])
                    middle.append(temp[1])
        print("".join(right))
        if("".join(right)!=starter):
            secondList.append(middle[0])
            break
        else:
            commands=betweenTag(data,"commands")
            attrList=[]
            slotsList=[]
            attrModule=[]
            for com in commandList(commands):        
                commandSplit=com.split("<slots>")
                if(len(commandSplit)>1): 
                    attrList.append(commandSplit[0])
                    slotsList.append(commandSplit[1])
                
            for attr, slot in zip(attrList,slotsList):
                attrName=betweenTag(attr,"name")
                if attrName in moduleList:
                    if(attrName in moduleStats):
                        moduleStats[attrName]=moduleStats[attrName]+1
                    else:
                        moduleStats[attrName]=1 
                elif attrName=="BLOCK":
                    slotName=slot.split("<name>")
                    blockName=betweenTag(slotName[1],"value")
                    original=betweenTag(slotName[5], "value")
                    if original in blockStats:
                        blockStats[original]=blockStats[original]+1
                    else:
                        blockStats[original]=1
                else:
                    if(attrName in stats):
                        stats[attrName]=stats[attrName]+1
                    else:
                        stats[attrName]=1 

    with open('./command_usages.csv', 'w', newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(['Commands','Usages'])
        writer.writerow([])
        for key, value in stats.items():
            writer.writerow([key, value])
        writer.writerow([])
        writer.writerow(['Module','Usages'])
        writer.writerow([])
        for key, value in moduleStats.items():
            writer.writerow([key, value])
        writer.writerow([])    
        writer.writerow(['BLOCK Original Template', 'Usages'])
        writer.writerow([])
        for key, value in blockStats.items():
            writer.writerow([key, value])
        writer.writerow([])    
        writer.writerow(['Names of XML With Different Structures'])
        writer.writerow([])
        writer.writerow([secondList])
if __name__ == "__main__":
    main()