import pandas as pd
import numpy as np
from scipy.stats import *

def LoadFromCSV(CSVPath):
  return pd.read_csv(CSVPath)

def LoadFromDict(dictData):
  return pd.DataFrame(dictData)

def LoadFromExcel(ExcelPath):
    return pd.read_csv(ExcelPath)

""" Pearson's, Spearman's and  D'Agostino's correlation test
Parameters (Input):
===================================================================================
df*        : Pandas DataFrame

*: Required Parameter

Return (Output):
===================================================================================
Type: dictionary
Description: Pearson's, Spearman's and  Kendall's correlation tests stats
"""

def Correlation(df):

  if df is None:
    raise Exception("No data loaded")

  pearsonCrls,spearmanCrls,kendallCrls =[],[],[]
 
  for column1 in df.columns:
   
    for column2 in df.columns:
 
      stat,p=pearsonr(df[column1], df[column2])
   
      resObj={
        column1 + "_" + column2:{
          "correlation":stat,
          "p":p
          }
        }
   
      pearsonCrls.append(resObj)

      stat, p = spearmanr(df[column1], df[column2])
   
      resObj={
        column1 + "_" + column2:{
        "correlation":stat,
        "p":p
        }
      }
   
      spearmanCrls.append(resObj)

      stat, p = kendalltau(df[column1], df[column2])
      
      resObj={
        column1 + "_" + column2:
        {
          "correlation":stat,
          "p":p
          }
      }
      
      kendallCrls.append(resObj)
  
  return {
      "TestName":"correlation",
      "Pearsons":pearsonCrls,
      "Spearmans":spearmanCrls,
      "Kendalls":kendallCrls
      }

""" Kolmogorov-Smirnov, Shapiro-Wilk and  D'Agostino's Normality Tests
Parameters (Input):

===================================================================================
df*        : Pandas DataFrame

*: Required Parameter

Return (Output):
===================================================================================
Type: dictionary
Description: Kolmogorov-Smirnov, Shapiro-Wilk and  D'Agostino's tests normality stats
"""
def Normality(df):

  if df is None:
    raise Exception("No data loaded")
  
  kolmogorovSmirnov,shapiroWilk,dAgostino =[],[],[]

  for column in df.columns:

    data=df[column]
    
    #Perform to Kolmogorov-Smirnov normality test
    stat,p=kstest(data, 'norm')

    resObj={
      column:{
          "normality":stat,
          "p":p
        }
      }

    kolmogorovSmirnov.append(resObj)
    
    #Perform to Shapiro normality test
    stat,p=shapiro(data)

    resObj={
      column:{
        "normality":stat,
        "p":p
        }
      }

    shapiroWilk.append(resObj)
    
    #Perform to D' Agostino's normality test
    stat,p=normaltest(data) 

    resObj={
      column:{
        "normality":stat,
        "p":p
        }
      }

    dAgostino.append(resObj)
    

  #return the results 
  return {
      'TestName':'normality',
      'KolmogorovSmirnov':kolmogorovSmirnov,
      'ShapiroWilk':shapiroWilk,
      'DAgostino':  dAgostino
      }

""" Independent T-Test
Parameters (Input):
==================================================
df        : Pandas DataFrame

variable1*: string
                Independent variable (X)
                Name of DataFrame column object

variable2*: string
                Dependent variable (Y)
                Name of DataFrame column object

*: Required Parameter

Return (Output):
===================================================
Type: dictionary
Description: T-Test Stats
"""
def IndTTest(df,variable1,variable2):

  if df is None:
    raise Exception("No data loaded")

  if len(df[variable1].value_counts().index)>2:
    raise Exception("The number of groups cannot be greater than 2")

  # Create a dictionary object for the store data and etc.
  dataCollection=dict()

  # Extract the groups from DataFrame and put into the dataCollection dictionary object
  for idx in df[variable1].value_counts().index:
    dataCollection[idx]={"data":df.query(variable1 + "==" + str(idx))[variable2]}

  # Extract the raw data from dictionary object to pass scipy.stats functions
  rawData=list()
  for item in dataCollection:
    rawData.append(dataCollection[item]["data"])

  data1,data2=rawData[0],rawData[1]

  # Calculate Indepentend T-Test
  result1 = ttest_ind(data1, data2)

  # Calculate Levent Test
  result2=levene(data1, data2,center='mean')

  # Calculate Indepentend Welch Test
  result3= ttest_ind(data1, data2,equal_var = False)

  # Calculate Degree of Freedom score
  dofF=len(data1)+len(data2)-2

  # Calculate group descriptive statistics
  groupStats=list()
  for item in dataCollection:
    group=dict()
    group={"Group":item,
            "N":dataCollection[item]["data"].count(),
                   "Mean":round(dataCollection[item]["data"].mean(),3),
                   "StdDev":round(dataCollection[item]["data"].std(),3),
                   "StdErr": round(dataCollection[item]["data"].sem(),3)
    }
    groupStats.append(group)

  # Create  dictionary object(dictReturn) to return stats
  dictReturn={
        "TestName":"indt",
        "Ind_Variable":variable1,
        "Dep_Variable":variable2,

        # Groups statistics
        "groupStats":groupStats,

        # T-Test results
        "TTest":{
            "t":round(result1[0],3),
            "df":dofF,
            "sigTwoTailed":round(result1[1],3)
        },

        # Levene test results
        "LeveneTest":
        {
         "F":round(result2[0],3),
         "sigTwoTailed":round(result2[1],3)

        },

        # Welch test results
        "WelchTest":{
            "t":round(result3[0],3),
            "sigTwoTailed":round(result3[1],3)
        }
  }

  return dictReturn


""" Mann-Whitney U Test
Parameters (Input):
==================================================
df        : Pandas DataFrame

variable1*: string
                Independent variable (X)
                Name of DataFrame column object

variable2*: string
                Dependent variable (Y)
                Name of DataFrame column object

*: Required Parameter

Return (Output):
===================================================
Type: dictionary
Description: Mann-Whitney U Test Stats
"""
def MannWhitneyU(df,variable1,variable2):
  from statistics import mean

  if df is None:
    raise Exception("No data loaded")

  if len(df[variable1].value_counts().index)>2:
    raise Exception("The number of groups cannot be greater than 2")

  # Create a dictionary object for the store data and etc.
  dataCollection=dict()

  # Extract the groups from DataFrame and put into the dataCollection dictionary object
  for idx in df[variable1].value_counts().index:
    dataCollection[idx]={"data":df.query(variable1 + "==" + str(idx))[variable2]}

  # Extract the raw data from dictionary object to pass scipy.stats functions
  rawData=list()
  for item in dataCollection:
    rawData.append(dataCollection[item]["data"])

  data1,data2=rawData[0],rawData[1]

  # Calculate Mann-Whitney U Test
  result = mannwhitneyu(data1, data2)

  ranks=list()
  for item in dataCollection:
    group=dict()
    meanRank=mean(dataCollection[item]["data"].rank())
    group={"Group":item,
              "N":dataCollection[item]["data"].count(),
                   "MeanRank":round(meanRank,3),
                   "SumOfRanks": round(meanRank*dataCollection[item]["data"].count(),3)
    }
    ranks.append(group)

  # Create  dictionary object(dictReturn) to return stats
  dictReturn={
        "TestName":"mannwhitneyu",
        "Ind_Variable":variable1,
        "Dep_Variable":variable2,

       # Ranks
        "ranks":ranks,

        # Mann-Whitney U Test results
        "MannWhitneyUTest":{
            "u":round(result[0],3),
            "sigTwoTailed":round(result[1],3)
        }

  }

  return dictReturn

""" Html output for the Independent Samples T-Test Results  
Parameters (Input):
==================================================
testResult*        : Python dictionary returning from IndTTest function 

destination*: string
                
              Destination path for html file

*: Required Parameter

Return 
No return value:
"""

def HtmlOutputIndTTest(testResult):
 
  import uuid
  
  htmlOutput='<html><head><metacontent="text/html;charset=UTF-8"http-equiv="content-type"><style>table,tr,th,td{border:1px black solid;}</style></head><body><table><tr><td colspan="9" rowspan="1">Independent Samples Test</td></tr><tr><td colspan="2" rowspan="1"></td><td colspan="2" rowspan="1">Levene&rsquo;s Test for Equality of Variances</td><td colspan="3" rowspan="1">T-Test for Equality of Variances</td></tr><tr><td colspan="2" rowspan="1"></td><td colspan="1" rowspan="1">F</td><td colspan="1" rowspan="1">Sig.</td><td colspan="1" rowspan="1">t</td><td colspan="1" rowspan="1">df</td><td colspan="1" rowspan="1">Sig.(2-Tailed)</td></tr><tr><td colspan="1" rowspan="2">' + str(testResult['Ind_Variable']) + '</td><td colspan="1" rowspan="1">EqualVariancesAssumed</td><td colspan="1" rowspan="1">' + str(testResult['LeveneTest']['F']) +'</td><td colspan="1" rowspan="1">'+ str(testResult['LeveneTest']['sigTwoTailed']) +'</td><td colspan="1" rowspan="1">'+ str(testResult['TTest']['t']) +'</td><td colspan="1" rowspan="1">'+ str(testResult['TTest']['df']) +'</td><td colspan="1" rowspan="1">'+ str(testResult['TTest']['sigTwoTailed']) +'</td></tr><tr><td colspan="1" rowspan="1">EqualVariancesNotAssumed</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">'+ str(testResult['WelchTest']['t']) +'</td><td colspan="1" rowspan="1">'+ str(testResult['TTest']['df']) +'</td><td colspan="1" rowspan="1">'+ str(testResult['WelchTest']['sigTwoTailed']) +'</td></tr></table><br>Group Stats <br><table><thead><tr><th>' + str(testResult['Ind_Variable']) + '</th><th>N</th><th>Mean</th><th>Std. Deviation</th><th>Std. Error Mean</th></tr></thead><tbody><tr><td>' + str(testResult["groupStats"][0]["Group"])  +'</td><td>' + str(testResult["groupStats"][0]["N"])  +'</td><td>' + str(testResult["groupStats"][0]["Mean"])  +'</td><td>' + str(testResult["groupStats"][0]["StdDev"])  +'</td><td>' + str(testResult["groupStats"][0]["StdErr"])  +'</td></tr><tr><td>'+ str(testResult["groupStats"][1]["Group"])  +'</td><td>' + str(testResult["groupStats"][1]["N"])  +'</td><td>' + str(testResult["groupStats"][1]["Mean"])  +'</td><td>' + str(testResult["groupStats"][1]["StdDev"])  +'</td><td>' + str(testResult["groupStats"][1]["StdErr"])  +'</td></tr></tbody></table></body></html>'
 
  outputFileName='IndTTest_' +  str(uuid.uuid4().hex) + '.html'

  with open(outputFileName,'wt') as outputFile:
    outputFile.write(htmlOutput)

  print('The output file ' + outputFileName + ' was created successfully')

def HtmlOutputMannWUTest(testResult):

  import uuid

  htmlOutput='<html><head><metacontent="text/html;charset=UTF-8"http-equiv="content-type"><style>table,tr,th,td{border:1px black solid;}</style></head><body><h3>Mann Whitney Test</h3> <br>Ranks<table><thead><tr><th></th><th>Group</th><th>N</th><th>Mean Rank</th><th>Sum of Rank</th></tr></thead><tbody><tr><td rowspan="3">' + str(testResult['Ind_Variable']) + '</td><td>'+ str(testResult["ranks"][0]["Group"])  +'</td><td>' + str(testResult["ranks"][0]["N"])  +'</td><td>' + str(testResult["ranks"][0]["MeanRank"])  +'</td><td>' + str(testResult["ranks"][0]["SumOfRanks"])  +'</td></tr><tr><td>'+ str(testResult["ranks"][1]["Group"])  +'</td><td>' + str(testResult["ranks"][1]["N"])  +'</td><td>' + str(testResult["ranks"][1]["MeanRank"])  +'</td><td>' + str(testResult["ranks"][1]["SumOfRanks"])  +'</td></tr><tr><td></td><td>' + str(testResult["ranks"][0]["N"]+testResult["ranks"][1]["N"])  +'</td><td></td><td></td></tr></tbody></table><br>Test statistics <br> <table><thead><tr><th></th><th>' + str(testResult['Ind_Variable']) + '</th></tr></thead><tbody><tr><td>Mann-Whitney U</td><td>' + str(testResult['MannWhitneyUTest']['u']) + '</td></tr><tr><td>Sig.</td><td>' + str(testResult['MannWhitneyUTest']['sigTwoTailed']) + '</td></tr></tbody></table> </body></html>'

  outputFileName='MannWUTest_' +  str(uuid.uuid4().hex) + '.html'

  with open(outputFileName,'wt') as outputFile:
    outputFile.write(htmlOutput)
  print('The output file ' + outputFileName + ' was created successfully')
