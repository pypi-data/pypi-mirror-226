## Welcome to EduStatTests
EduStatTests is free Python package for educational statistical analysis.


## Installing

You can install EduStatTests using the Python Package Index (PyPI)

    
**Requirements**
    
- NumPy
- Pandas
- SciPy

**PyPI Command**

    pip install git+https://github.com/hguldal/EduStatTests.git
    
## How to Use EduStatTests

## Data

EduStatTests uses Pandas DataFrame as data format. You can use CSV format or Python dictionary object while creating the DataFrame.

**Loading data from CSV files**

Comma Seperates Values (CSV) is a widely used data exchange format. In EduStatTests, the **LoadFromCSV** function is used to read and load CSV files into the DataFrame object.

The code below shows how to load data from CSV file into DataFrame object in EduStatTests.

    dfObj=LoadFromCSV("drive/MyDrive/Datasets/test/test_data.csv")

**Loading data from Python Dictionary**

You can also load your data into the DataFrame in Python dictionary form by using the **LoadFromDict** function. The code below shows how to do this.

    dataDict={
    "Gender": [1,1,0,0,1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0],
    "Attitude":[1,2,1,3,4,1,1,3,4,1,3,1,2,1,4,1,4,1,4,3,3,1,1,1,1,1,3,1,3,1,1,1,1,1,1,1,1,4,3,1,4,4,1,2,1,1,1,1,1,2,4,1,4,2,1,4,1,4,1,1,1]
    }
    
	dfObj=LoadFromDict(dataDict)

## Tests

You can perform the following tests with EduStatTests.

 - Independent Samples T-Test
 - Mann-Whitney U Test
 - Correlation Tests (Pearson's, Spearman's and  Kendall's)
 - Normality Tests (Kolmogorov-Smirnov, Shapiro-Wilk and  D'Agostino's)


**Independent  Samples T-Test**

You can perform Independent T-Test using **IndTTest** function in EduStatTests. **IndTTest** function has three parameters. First paramater is Pandas DataFrame contain your data. Second parameter is independent variable name in your data. Third parameter is dependent variable name in your data. The code below shows how to perform Independent T-Test in EduStatTests.

	from EduStatTests import *
    dataDict={
    "Gender": [1,1,0,0,1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0],
    "Attitude":[1,2,1,3,4,1,1,3,4,1,3,1,2,1,4,1,4,1,4,3,3,1,1,1,1,1,3,1,3,1,1,1,1,1,1,1,1,4,3,1,4,4,1,2,1,1,1,1,1,2,4,1,4,2,1,4,1,4,1,1,1]
    }
    
	dfObj=LoadFromDict(dataDict)
	results=IndTTest(dfObj,"Gender","Attitude")
	print(results)

----------
You can also see analysis results as html file on web browser using **HtmlOutputIndTTest** function. The code below shows how to results were saved as html file format.
	
    from EduStatTests import *
    dataDict={
    "Gender": [1,1,0,0,1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0],
    "Attitude":[1,2,1,3,4,1,1,3,4,1,3,1,2,1,4,1,4,1,4,3,3,1,1,1,1,1,3,1,3,1,1,1,1,1,1,1,1,4,3,1,4,4,1,2,1,1,1,1,1,2,4,1,4,2,1,4,1,4,1,1,1]
    }
    
	dfObj=LoadFromDict(dataDict)
    results=IndTTest(dfObj,"Gender","Attitude")
    
    HtmlOutputIndTTest(results)

**Mann-Whitney U Test**

You can perform Mann-Whitney U Test using **MannWhitneyU** function in EduStatTests. **MannWhitneyU** function has three parameters. First paramater is Pandas DataFrame contain your data. Second parameter is independent variable name in your data. Third parameter is dependent variable name in your data. The code below shows how to perform Mann-Whitney U in EduStatTests.

	from EduStatTests import *
    dataDict={
    "Gender": [1,1,0,0,1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0],
    "Attitude":[1,2,1,3,4,1,1,3,4,1,3,1,2,1,4,1,4,1,4,3,3,1,1,1,1,1,3,1,3,1,1,1,1,1,1,1,1,4,3,1,4,4,1,2,1,1,1,1,1,2,4,1,4,2,1,4,1,4,1,1,1]
    }

	dfObj=LoadFromDict(dataDict)
	results=MannWhitneyU(dfObj,"Gender","Attitude")
	print(results)

----------
You can also see analysis results as html file on web browser using **HtmlOutputMannWUTest** function. The code below shows how to results were saved as html file format.

    from EduStatTests import *
    dataDict={
    "Gender": [1,1,0,0,1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0],
    "Attitude":[1,2,1,3,4,1,1,3,4,1,3,1,2,1,4,1,4,1,4,3,3,1,1,1,1,1,3,1,3,1,1,1,1,1,1,1,1,4,3,1,4,4,1,2,1,1,1,1,1,2,4,1,4,2,1,4,1,4,1,1,1]
    }

	dfObj=LoadFromDict(dataDict)
    results=IndTTest(dfObj,"Gender","Attitude")

    HtmlOutputMannWUTest(results)
