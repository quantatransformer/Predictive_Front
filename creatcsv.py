import csv 
def get(name):
    return request.values.get(name)
Id = get("Id")
LotArea = get("LotArea")
Neighborhood = get("Neighborhood")
YearBuilt = get("YearBuilt")
GrLivArea = get("GrLivArea")
Street = get("Street")
Utilities = get("Utilities")
LotConfig = get("LotConfig")
HouseStyle = get("HouseStyle")
RoofStyle = get("RoofStyle")
SaleType = get('SaleType')
SaleCondition = get('SaleCondition')
lgbm_data=[LotArea,Street,Utilities,LotConfig,Neighborhood,
HouseStyle,YearBuilt,RoofStyle,GrLivArea,SaleType,SaleCondition]
lgbm_data_1=",".join(lgbm_data)

def getSortedValues(row):
    sortedValues=[]
    keys=row.keys()
    keys.sort()
    for key in keys:
        sortedValues.append(row[key])
    return sortedValues

rows = [{'Column1': 1, 'Column2': LotArea,'Column3': Street,'Column4':Utilities,'Column5':LotConfig,
        'Column6':Neighborhood,'Column7':HouseStyle,'Column8':YearBuilt,'Column9':RoofStyle,
        'Column10':GrLivArea,'Column11':SaleType,'Column12':SaleCondition},
        ]

names={'Column1': 'Id', 'Column2': 'LotArea','Column3': 'Street','Column4':'Utilities','Column5':'LotConfig',
        'Column6':'Neighborhood','Column7':'HouseStyle','Column8':'YearBuilt','Column9':'RoofStyle',
        'Column10':'GrLivArea','Column11':'SaleType','Column12':'SaleCondition'}


fileobj=open('test.csv','wb')


fileobj.write('\xEF\xBB\xBF')


writer = csv.writer(fileobj)


sortedValues = getSortedValues(names)
writer.writerow(sortedValues)


for row in rows:
    sortedValues = getSortedValues(row)
    print (sortedValues)
    writer.writerow(sortedValues)
fileobj.close()