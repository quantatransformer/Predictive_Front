import pandas as pd
df = pd.read_csv('train1.csv')
def getdata(df):
    id_num = []
    for each in df['Id']:
        id_num.append(str(each))
    LotArea = []
    for each in df['LotArea']:
        LotArea.append(str(each))
    Area_Price=[]
    for i in range(1,len(df)):
        Area_Price.append([df['Id'][i],df['SalePrice'][i]])
    Street = df['Street']
    Utilities = df['Utilities']
    LotConfig = df['LotConfig']
    Neighborhood=df['Neighborhood']
    YearBuilt = df['YearBuilt']
    RoofStyle = df['RoofStyle']
    GrLivArea = df['GrLivArea']
    SaleType = df['SaleType']
    SaleCondition = df['SaleCondition']
    SalePrice = []
    for each in df['SalePrice']:
        SalePrice.append(str(each))
    HouseStyle = df['HouseStyle']
    labels=sorted(df['Neighborhood'])

    counts = {}
    times=[]
    each_1=[]
    for x in labels:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    for each in counts:
        each_1.append(each)
        times.append(counts[each])	
    Neighborhood_str = ",".join(Neighborhood)
    list_type = (list(df.head(0)))
    list_type_1=",".join(list_type)


    numeric_variables=[]
    categorical_variables=[]

    for each in list_type:
        if len(set(df[each])) < 26:

            categorical_variables.append(each)

        else:

            numeric_variables.append(each)
    categorical_variables_1=",".join(categorical_variables)
    numeric_variables_1= ",".join(numeric_variables)
    numeric_variables_lgbm=numeric_variables
    numeric_variables_lgbm.remove('Id')
    numeric_variables_lgbm.remove('SalePrice')


    mydata = {'numeric_variables_lgbm':numeric_variables_lgbm,'Street':list(set(Street)),'Utilities':list(set(Utilities)),'LotConfig':list(set(LotConfig)),
    'HouseStyle':list(set(HouseStyle)),'RoofStyle':list(set(RoofStyle)),'SaleType':list(set(SaleType)),
    'SaleCondition':list(set(SaleCondition)),'Neighborhood':list(set(Neighborhood)),
    'list_type':list_type_1,'list_type_1':list_type,'listnum':len(df),'Neighborhood_str':Neighborhood_str,
    'Area_Price':Area_Price,'Neighborhood_num_1':len(times),'Neighborhood_num':times,
    'Neighborhood_type':each_1,'id_num':map(int,id_num),'LotArea':map(int,LotArea),
    'SalePrice':map(int,SalePrice),'categorical_variables':categorical_variables_1,
    'numeric_variables':numeric_variables_1,'categorical_variables_1':categorical_variables,
    'numeric_variables_1':numeric_variables
    }
    return mydata
print getdata(df)