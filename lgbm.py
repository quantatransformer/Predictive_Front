import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection, preprocessing
import warnings
warnings.filterwarnings("ignore")
from scipy import stats
from scipy.stats import norm, skew
import graphviz
import xgboost as xgb
from sklearn.model_selection import cross_val_score
from xgboost.sklearn import XGBRegressor
from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.decomposition import PCA, KernelPCA

df_train=pd.read_csv('train1.csv')
df_test=pd.read_csv('test.csv')

df_train.drop(df_train[(df_train["GrLivArea"]>4000)&(df_train["SalePrice"]<300000)].index,inplace=True)
df_train.drop(df_train[(df_train["LotArea"]>100000)].index,inplace=True)




df_all=pd.concat([df_train,df_test],ignore_index=True)
print 'The shape of df_train is:',df_train.shape
print 'The shape of df_test is:',df_test.shape
print 'The shape of df_all is:',df_all.shape

predict_df = df_test[['Id']]
df_all.drop('Id',axis=1,inplace=True)
df_all.drop('SalePrice',axis=1,inplace=True)

missing = (df_all.isnull().sum() / len(df_all)) * 100
missing = missing.drop(missing[missing == 0].index).sort_values(ascending=False)[:30]
missing_data = pd.DataFrame({'Missing Ratio' :missing})
#missing_data.head(10)

for feature in df_all.columns:
    if df_all[feature].dtype=='object':
        df_all[feature]=df_all[feature].fillna('Missing')
    if df_all[feature].dtype!='object':
        #df_all[feature]=df_all[feature].fillna(np.mean(df_all[feature].values))
        df_all[feature]=df_all[feature].fillna(-999)
		
#df_all['2ndFlrSF'].fillna(np.mean(df_all['2ndFlrSF'].values))
def categorial_feature(rate,dataset):
    global qualitative, quantitative
    likely_cat = {}
    for var in dataset.columns:
        likely_cat[var] = 1.*dataset[var].nunique()/dataset[var].count() < float(rate)
    qualitative = [f for f in dataset.columns if likely_cat[f]==True]
    quantitative = [f for f in dataset.columns if likely_cat[f]==False]
    print'There are %d quantitative features and %d qualitative features'%(len(quantitative),len(qualitative))
    return 0
	
categorial_feature(0.05,df_all)

def feature_encoding(dataset):
    for f in qualitative:
        lbl = preprocessing.LabelEncoder()
        dataset[f]=lbl.fit_transform(list(dataset[f].values)) 
        #lbl.transform(list(dataset[f].values))
    print 'encoding finished'
    return 0
	
feature_encoding(df_all)

def displot_feature(feature,dataset):
    sns.distplot(dataset[feature] , fit=norm);

    # Get the fitted parameters used by the function
    (mu, sigma) = norm.fit(dataset[feature])
    print '\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu, sigma)

    #Now plot the distribution
    plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)],
            loc='best')
    plt.ylabel('Frequency')
    plt.title('%s distribution'%(feature))

    #Get also the QQ-plot
    fig = plt.figure()
    res = stats.probplot(dataset[feature], plot=plt)
    plt.show()
    return 0
def show_skewness(dataset):
    global skewness
    numeric_feats = dataset.columns

    # Check the skew of all numerical features
    skewed_feats = dataset[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
    skewness = pd.DataFrame({'Skew' :skewed_feats})
    return 0
	
#show_skewness(df_all)

df_train['SalePrice'] = np.log1p(df_train['SalePrice'])
#df_all['LotArea'] = np.log1p(df_all['LotArea'])
#df_all['GrLivArea'] = np.log1p(df_all['GrLivArea'])
#df_all['1stFlrSF'] = np.log1p(df_all['1stFlrSF'])
#df_all['2ndFlrSF'] = np.log1p(df_all['2ndFlrSF'])
#df_all['TotalBsmtSF'] = np.log1p(df_all['TotalBsmtSF'])
#df_all['LotArea'] = np.log1p(df_all['LotArea'])
#df_all['GrLivArea'] = np.log1p(df_all['GrLivArea'])
#df_all['1stFlrSF'] = np.log1p(df_all['1stFlrSF'])
#df_all['2ndFlrSF'] = np.log1p(df_all['2ndFlrSF'])
#df_all['TotalBsmtSF'] = np.log1p(df_all['TotalBsmtSF'])

#displot_feature('SalePrice',df_train)

def log_transformation(skew_value,dataset):
    global skewness
    skewness=skewness[abs(skewness)>0.75].dropna()
    print "There are {} skewed numerical features to log transform".format(skewness.shape[0])
    skewed_features = skewness.index
    for feat in skewed_features:
        dataset[skewed_features] = np.log1p(dataset[skewed_features])
    print '......'
    print 'transform finished'
    return 0
def boxcox_transformation(skew_value,lam,dataset):
    skewness=skewness[abs(skewness)>0.75].dropna()
    print "There are {} skewed numerical features to Box Cox transform".format(skewness.shape[0])
    from scipy.special import boxcox1p
    skewed_features = skewnessvalue.index
    for feat in skewed_features:
        dataset[feat] = boxcox1p(dataset[feat], lam)
    print '......'
    print 'transform finished'
    return 0

#log_transformation(0.75,df_all)

#df_all=pd.get_dummies(df_all)

df_all.head(5)

ntrain=df_train.shape[0]
ntest=df_test.shape[0]


################################################################
#add new features
################################################################

#df_all['TotalQual']=df_all['OverallQual']+df_all['ExterQual']+df_all['GarageQual']
#df_all['TotalCond']=df_all['BsmtCond']+df_all['ExterCond']+df_all['GarageCond']


print df_all.shape

train_data = df_all[:ntrain]
test_data = df_all[ntrain:]

#scaler=RobustScaler()
#train_data = scaler.fit_transform(train_data)
#test_data = scaler.fit_transform(test_data)
#pca = PCA(n_components=80)
#train_data=pd.DataFrame(pca.fit_transform(train_data))
#test_data=pd.DataFrame(pca.fit_transform(test_data))

################################################################
#method 1
################################################################
train_x1=train_data
train_y1=df_train['SalePrice']
test_x1=test_data
#nonan=pd.concat([train_x1,train_y1],ignore_index=True)
#nonan.dropna(inplace=True)
#print 'nonan',nonan.shape
#train_x1=nonan.drop('SalePrice')
#train_y1=nonan['SalePrice']
print 'The shape of train_x is',train_x1.shape
print 'The shape of train_y is',train_y1.shape
print 'The shape of test_x is',test_x1.shape

import lightgbm as lgb
d_train = lgb.Dataset(train_x1, label=train_y1)
model_lgb = lgb.LGBMRegressor(objective='regression',num_leaves=5,
                               learning_rate=0.01, n_estimators=1900,
                               max_bin = 55, bagging_fraction = 0.8,
                         bagging_freq = 5, feature_fraction = 0.5,
                                feature_fraction_seed=9, bagging_seed=9,
                      min_data_in_leaf =6, min_sum_hessian_in_leaf =1.1)
print"\nFitting LightGBM model ..."
model_lgb.fit(train_x1,train_y1)
print'Predicting...'
pred_y = model_lgb.predict(test_x1)
pred_y=np.expm1(pred_y)
predict_df['SalePrice'] = pred_y
print pred_y


