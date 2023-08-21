
diskLabel=None
diskname='adas1'
diskList=list()
diskDetail=dict()
diskDetail['label']=diskLabel
diskDetail['name']=diskname
diskList.append(diskDetail)
print ("diskList:",diskList)
for disk in diskList:
  if disk['label']!=None:
    print("No label");
  else:
    print("label is:",disk['label'])
