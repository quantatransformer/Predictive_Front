import sys
from flask import render_template,Flask,request
import pandas as pd
from werkzeug.utils import secure_filename
import csv
import re
from ssh import SSHConnection
import os
import urllib.request as urllib2
from bs4 import BeautifulSoup
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/crawling',methods=['GET','POST'])
def crawler_homepage():
	def get_s(name):
		return request.values.get(name)	
	if request.method == 'POST':
		url = str(get_s('url'))
		reponse = urllib2.urlopen(url)


		return render_template('crawler.html')
	else:
	    return render_template('crawler_homepage.html')

@app.route('/index')
def index():
    return render_template('index.html',mydata=mydata)
@app.route('/charts')
def charts():
	return render_template('charts.html',mydata=mydata)
@app.route('/charts_l')
def charts_l():
	return render_template('charts_l.html',mydata_l=mydata_l)
@app.route('/upload')
def choose():
	return render_template('choose.html')

@app.route('/choose_l')
def choose_l():
	return render_template('choose_l.html')

@app.route('/online',methods=['GET','POST'])
def choose_s():
	def get_s(name):
		return request.values.get(name)
	if request.method == 'POST':
		global dic_s
		dic_s={}
		dic_s['host'] = str (get_s('host'))
		dic_s['port'] = int (get_s('port'))
		dic_s['username'] = str (get_s('username'))
		dic_s['password'] = str (get_s('password'))
		dic_s['remote work directory path'] = str (get_s('remote work directory path'))
		return render_template('choose.html',dic_s=dic_s)
	else:
		return render_template('Login_account.html')

@app.route('/upload_h_l',methods=['GET','POST'])


def upload_h_l():
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
	if request.method == 'POST':

		f = request.files['file']
		f.save(secure_filename(f.filename))
		global mydata_l
		df = pd.read_csv('train1.csv')
		mydata_l = getdata(df)
		return render_template('index_h_l.html',mydata_l=mydata_l)
	else:
		return render_template('upload_h_l.html')

@app.route('/upload_h',methods=['GET','POST'])
def upload_h():
	if request.method == 'POST':

		f = request.files['file']
		f.save(secure_filename(f.filename))
		print(f.filename)
		global ssh
		ssh = SSHConnection(dic_s['host'],dic_s['port'],dic_s['username'],dic_s['password'])
		ssh.connect()
		ssh.upload(str(os.getcwd()) + '\\' + str(f.filename),dic_s['remote work directory path'] + '/lgbm/train1.csv')
		
		
		global mydata 
		mydata = eval(ssh.cmd('cd py2;source bin/activate;cd ..;cd lgbm;python data_v.py'))
		
		return render_template('index_h.html',mydata=mydata)
	else:
		return render_template('upload_h.html')

@app.route('/upload_s',methods=['GET','POST'])
def upload_s():
	if request.method == 'POST':

		f = request.files['file']
		f.save(secure_filename(f.filename))
		print(dic_s['password'])
		ssh_1=SSHConnection(dic_s['host'],dic_s['port'],dic_s['username'],dic_s['password'])
		ssh_1.connect()
		ssh_1.upload(str(os.getcwd()) + '\\' + str(f.filename),dic_s['remote work directory path'] + '/FlaskIndexPrediction/data/data.csv')  # INPUT YOUR PATH
		return render_template('index_s.html')

	else:
		return render_template('upload_s.html')
@app.route('/upload_s_l',methods=['GET','POST'])
def upload_s_l():
	if request.method == 'POST':

		f = request.files['file']
		f.save(secure_filename(f.filename))
		return render_template('index_s_l.html')
	else:
		return render_template('upload_s_l.html')
@app.route('/choose_s')
def choose_s_0():
	return render_template('choose_s.html')
	

		

@app.route('/upload_p',methods=['GET','POST'])
def upload_p():
	def get(name):
		return request.values.get(name)
	if request.method == 'POST':
		dic={}
		dic['e'] = int(get('e'))
		dic['lb'] = int (get('lb'))
		dic['lr'] = float (get('lr'))
		dic['tp'] = float (get('tp'))
		ssh_s=SSHConnection(dic_s['host'],dic_s['port'],dic_s['username'],dic_s['password'])
		ssh_s.connect(  )
		s='cd py2;source bin/activate;cd ..;cd FlaskIndexPrediction;python main.py -e {e} -lb {lb} -lr {lr} -tp{tp}'
		ssh_s.cmd(s.format(e=dic['e'],lb=dic['lb'],lr=dic['lr'],tp=dic['tp']))

		
		ssh_s.download(dic_s['remote work directory path'] + '/FlaskIndexPrediction/output/outputTest.csv', str(os.getcwd())  + '\\' +  'outputTest.csv')
		ssh_s.download(dic_s['remote work directory path'] + '/FlaskIndexPrediction/output/outputTrain.csv',str(os.getcwd())  + '\\' +  'outputTrain.csv')
		ssh_s.download(dic_s['remote work directory path'] + '/FlaskIndexPrediction/output/outputTrainTest.csv',str(os.getcwd())  + '\\' +  'outputTrainTest.csv')


		outputTest = pd.read_csv('outputTest.csv')
		outputTrain = pd.read_csv('outputTrain.csv')
		outputTrainTest = pd.read_csv('outputTrainTest.csv')
		Test_time = outputTest['Unnamed: 0']
		Test_origin = outputTest['origin']
		Test_predict = outputTest['predict']
		Train_time = outputTrain['Unnamed: 0']
		Train_origin = outputTrain['origin']
		Train_predict = outputTrain['predict']
		TrainTest_time = outputTrainTest['Unnamed: 0']
		TrainTest_origin = outputTrainTest['origin']
		TrainTest_predict = outputTrainTest['predict']
		
		stock_data={'Test_time':Test_time,'Test_origin':Test_origin,
		'Test_predict':Test_predict,'Train_time':Train_time,
		'Train_origin':Train_origin,'Train_predict':Train_predict,
		'TrainTest_time':TrainTest_time,'TrainTest_origin':TrainTest_origin,
		'TrainTest_predict':TrainTest_predict}
		return render_template('ZhangYD.html',stock_data = stock_data)
	else:
		return render_template('index_p.html')

@app.route('/upload_p_l',methods=['GET','POST'])
def upload_p_l():
	def get(name):
		return request.values.get(name)
	if request.method == 'POST':
		dic={}
		dic['e'] = int(get('e'))
		dic['lb'] = int (get('lb'))
		dic['lr'] = float (get('lr'))
		dic['tp'] = float (get('tp'))
		
		a = os.popen('python main.py -e {e} -lb {lb} -lr {lr} -tp{tp}'.format(e=dic['e'],lb=dic['lb'],lr=dic['lr'],tp=dic['tp']))

		


		outputTest = pd.read_csv('outputTest.csv')
		outputTrain = pd.read_csv('outputTrain.csv')
		outputTrainTest = pd.read_csv('outputTrainTest.csv')
		Test_time = outputTest['Unnamed: 0']
		Test_origin = outputTest['origin']
		Test_predict = outputTest['predict']
		Train_time = outputTrain['Unnamed: 0']
		Train_origin = outputTrain['origin']
		Train_predict = outputTrain['predict']
		TrainTest_time = outputTrainTest['Unnamed: 0']
		TrainTest_origin = outputTrainTest['origin']
		TrainTest_predict = outputTrainTest['predict']
		
		stock_data={'Test_time':Test_time,'Test_origin':Test_origin,
		'Test_predict':Test_predict,'Train_time':Train_time,
		'Train_origin':Train_origin,'Train_predict':Train_predict,
		'TrainTest_time':TrainTest_time,'TrainTest_origin':TrainTest_origin,
		'TrainTest_predict':TrainTest_predict}
		return render_template('ZhangYD_l.html',stock_data = stock_data)
	else:
		return render_template('index_p_l.html')
			



@app.route('/LSTM',methods=['GET','POST'])
def LSTM():
	def get(name):
		return request.values.get(name)
	

	if request.method == 'POST':
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
			print(sortedValues)
			writer.writerow(sortedValues)
		fileobj.close()

		ssh.upload(str(os.getcwd())  + '\\' +  'test.csv','/root/lgbm/test.csv')

		show = ssh.cmd('cd py2;source bin/activate;cd ..;cd lgbm;python lgbm.py')
		show_l = show.split('\n')
		pred_y = eval(show_l[-2])
		pred_y_show=pred_y[0]
		quantitative = re.findall("\d+",show_l[3])[0]
		qualitative = re.findall("\d+",show_l[3])[1]
		train_x1 = show_l[6]
		train_y1 = show_l[7]
		test_x1 = show_l[8]
		return render_template('lgbm_output.html',pred_y=round(pred_y_show,2),train_x1=train_x1,train_y1=train_y1
			,test_x1=test_x1,quantitative=quantitative,qualitative=qualitative)

	else:
		return render_template('LSTM.html',mydata=mydata)

@app.route('/LSTM_l',methods=['GET','POST'])
def LSTM_l():
	def get(name):
		return request.values.get(name)
	

	if request.method == 'POST':
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
			print(sortedValues)
			writer.writerow(sortedValues)
		fileobj.close()

		a = os.popen('python lgbm.py')
		show = a.readlines()
		pred_y_show=eval(show[-1])[0]
		# quantitative = re.findall("\d+",show_l[3])[0]
		# qualitative = re.findall("\d+",show_l[3])[1]
		# train_x1 = show_l[6]
		# train_y1 = show_l[7]
		# test_x1 = show_l[8]
		return render_template('lgbm_output_l.html',pred_y=round(pred_y_show,2),train_x1='The shape of train_x is (1018, 11)',train_y1='The shape of test_x is (1, 11)'
			,test_x1='The shape of test_x is (1, 11)',quantitative=3,qualitative=8)

	else:
		return render_template('LSTM_l.html',mydata_l=mydata_l)

@app.route('/PCA')
def PCA():

	return render_template('PCA.html')


@app.route('/SVM')
def SVM():
	outputTest = pd.read_csv('outputTest.csv')
	outputTrain = pd.read_csv('outputTrain.csv')
	outputTrainTest = pd.read_csv('outputTrainTest.csv')
	Test_time = outputTest['Unnamed: 0']
	Test_origin = outputTest['origin']
	Test_predict = outputTest['predict']
	Train_time = outputTrain['Unnamed: 0']
	Train_origin = outputTrain['origin']
	Train_predict = outputTrain['predict']
	TrainTest_time = outputTrainTest['Unnamed: 0']
	TrainTest_origin = outputTrainTest['origin']
	TrainTest_predict = outputTrainTest['predict']
	
	stock_data={'Test_time':Test_time,'Test_origin':Test_origin,
	'Test_predict':Test_predict,'Train_time':Train_time,
	'Train_origin':Train_origin,'Train_predict':Train_predict,
	'TrainTest_time':TrainTest_time,'TrainTest_origin':TrainTest_origin,
	'TrainTest_predict':TrainTest_predict}
	return render_template('charts_sb.html',stock_data = stock_data)	




@app.route('/bar')
def bar():
	return render_template('index_sb.html')
@app.route('/pie')
def pie():
	return render_template('pie.html')
if __name__ == "__main__":
    app.run(debug=True)
