# <u>Data fundamentals Project :</u> Data Pipeline in Python

## <u>Table of contents :</u>

- [Introduction](#introduction)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Data Processing steps](#data-processing-steps)
  - [Data Collection](#data-collection)
  - [Data Cleaning](#data-cleaning)
  - [Data Transformation](#data-transformation)
- [How to use this project](#how-to-use-this-project)
- [Conclusion](#conclusion)

---

## <a id="introduction"><u>Introduction: </u></a>

This project covers the fundamentals of data processing and visualization using Jupyter Notebooks. 
It includes data collection, cleaning, transformation, and visualization, helping users understand key 
data operations and best practices.

## <a id="installation"><u>Installation:</u></a>

To run this project, you need to have Python installed on your system.
Ensure you have Python 3.12 or above installed. To install the required dependencies, run the following command:

```python
pip install -r requirements.txt
```

Alternatively, you can create a virtual environment to keep dependencies isolated:

```python
python -m venv venv

source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows

pip install -r requirements.txt
```

## <a id="project-structure"><u>Project Structure:</u></a>

The project structure is as follows:

```bash
📂 project-root
│── 📂 data                    # Raw and processed data files
│──── 📂 processed                 # Processed data files
│──── 📂 raw                       # Raw data files
│── 📂 models                  # Python models if necessary (to ignore in this case with the scripts)
│── 📜 Main.ipynb              # Python scripts for automation in Jupyter Notebook
│── 📜 requirements.txt        # Dependencies
│── 📜 README.md               # Documentation (this file)
```

## <a id="data-processing-steps"><u>Data Processing steps:</u></a>

Each step is crucial for effective data processing:

- <u>Data Collection:</u> Reliable data sources ensure trustworthy analysis.

- <u>Data Cleaning:</u> Poor data quality leads to misleading conclusions.

- <u>Data Transformation:</u> Standardized data ensures comparability across features.

- <u>Data Visualization:</u> Helps identify patterns and insights that might not be obvious from raw data.

The data processing steps include:

### 1. <a id="data-collection"><u>Data Collection:</u></a>

##### <u>Objective:</u> Retrieve datasets from various sources.

##### <u>Methods:</u>
- Downloading datasets from the project documentation.
- Uploading dataset from local storage.
- Understanding the data structure and features with pandas functions.
  - With the `head()` function, you can view the first few rows of the dataset.
  - The `info()` function provides a summary of the dataset, including the number of non-null values and data types.
  - The `shape` attribute returns the number of rows and columns in the dataset.
  - The `describe()` function gives a statistical summary of the dataset, including the mean, standard deviation, and quartiles.
  - The `dtypes` attribute returns the data types of each column in the dataset.



### 2. <a id="data-cleaning"><u>Data Cleaning:</u></a>

##### <u>Objective:</u> Ensure data quality by handling missing, duplicate, or inconsistent values. Remove inconsistencies and errors from the data.

##### <u>Methods:</u>

#### 2.1. <u>Handling Missing Values:</u>
The first step in data cleaning is to handle missing values. Missing values can occur for a variety of reasons, 
such as data entry errors, equipment malfunctions, or data corruption. It is essential to identify and handle missing 
values to ensure the quality of the data and the accuracy of the analysis.
Looking at the result of the .info() function, we can easily say that there are no missing values.
However, it is always a good idea to check for missing values explicitly using the .isnull() function.

```bash
#   Column                   Non-Null Count  Dtype  
---  ------                   --------------  -----  
 0   ClientID                 1000 non-null   object 
 1   Nom                      1000 non-null   object 
 2   Prénom                   1000 non-null   object 
 3   Email                    1000 non-null   object 
 4   Téléphone                1000 non-null   object 
 5   Adresse                  1000 non-null   object 
 6   Ville                    1000 non-null   object 
 7   CodePostal               1000 non-null   int64  
 8   Pays                     1000 non-null   object 
 9   DateNaissance            1000 non-null   object 
 10  Âge                      1000 non-null   int64  
 11  Sexe                     1000 non-null   object 
 12  NuméroCarteCrédit        1000 non-null   int64  
 13  TypeCarteCrédit          1000 non-null   object 
 14  DateExpirationCarte      1000 non-null   object 
 15  SoldeCompte              1000 non-null   float64
 16  TypeClient               1000 non-null   object 
 17  NombreAchats             1000 non-null   int64  
 18  MontantTotalAchats       1000 non-null   float64
 19  DernierAchat             1000 non-null   object 
 20  ProduitPréféré           1000 non-null   object 
 21  CatégorieProduitPréféré  1000 non-null   object 
 22  FréquenceAchatMensuel    1000 non-null   int64  
 23  PanierMoyen              1000 non-null   float64
 24  ScoreFidélité            1000 non-null   int64  
 25  NombreRemboursements     1000 non-null   int64  
 26  MontantTotalRemboursé    1000 non-null   float64
 27  AvisClient               1000 non-null   object 
 28  AbonnementNewsletter     1000 non-null   bool   
 29  TypePaiementFavori       1000 non-null   object 
 30  StatutCompte             1000 non-null   object 
```

#### 2.2. <u>Handling Duplicate Values:</u>
The next step in data cleaning is to handle duplicate values. Duplicate values can occur when the same data is entered
multiple times or when data is collected from multiple sources. It is essential to identify and remove duplicate values
to ensure the quality of the data and the accuracy of the analysis.
But in the analysis of the data, we can see that there are no duplicate values.

```python
print(f"The number of duplicates in the dataset is : {dataset.duplicated().sum()}")
```

```bash
The number of duplicates in the dataset is : 0
```

If the result was greater than 0 in your dataset, we can remove the duplicates using the .drop_duplicates() function, and then check 
again if there are any duplicates.

```python
dataset = dataset.drop_duplicates() # to remove the duplicates from the dataset
print(f"The dataset shape after removing duplicates is : {dataset.shape}") #to see the new shape of the dataset after removing duplicates
```

#### 2.3. <u>Correcting errors:</u>
Fortunately, there are no errors in the dataset. However, if there were errors, we could correct them using the .replace() function.
But in this case, we will not need to correct any errors. but first of all we verify if there are any errors in the dataset by verifying the unique values of come critical columns.

```python
columns_to_verify = ['Sexe', 'CatégorieProduitPréféré', 'AvisClient', 'AbonnementNewsletter', 'TypePaiementFavori', 'StatutCompte'] #to see the columns that we want to verify

for col in columns_to_verify:
    print(f"\n🔹 {col} : {dataset[col].nunique()} unique values") #to see the number of unique values in each column of the dataset
    print(dataset[col].unique())  # to see the unique values in each column of the dataset
```

#### 2.4. <u>Standardizing data:</u>
Standardizing data is the process of transforming data into a common format to make it easier to compare and analyze.
Normally, we should standardize the data by encoding categorical variables and normalizing numerical data as for countries and cities 
names which have to be capitalized or rounding float and the date format etc .
In the countries and cities names all the first lettre are already capitalize, so we don't need to standardize them.
but for the others columns we need to standardize them.

In this dataset, we have to standardize the following columns:
- date
- countries and cities names
- float numbers

#### 2.5. <u>Handling Outliers:</u>
In this dataset, we have to handle the outliers in the PanierMoyen column. We can use the IQR method to detect and remove the outliers.

```python
# Quartiles and IQR for outliers detection
Q1 = dataset['PanierMoyen'].quantile(0.25)
Q3 = dataset['PanierMoyen'].quantile(0.75)
IQR = Q3 - Q1

# bounds definition for outliers detection
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# outliers identification
outliers = dataset[(dataset['PanierMoyen'] < lower_bound) | (dataset['PanierMoyen'] > upper_bound)]
print(f"Outliers numbers find : {len(outliers)}")
display(outliers)
```

Fortunately, there are no outliers in the dataset.
NB: I use to search for outliers in the PanierMoyen column because it's the combination of two analysis factors which are MontantTotalAchat et NombreAchats.
Those two factors are very important in the analysis of the dataset because if we only referred to the MontantTotalAchat column, we could have outliers in the dataset.
However, we have a customer with 9055.95 (the 86th row) as MontantTotalAchat, but this value is not an outlier because this customer has made 19 purchases.
So it's normal to have this amount.

#### 2.6. <u>Standardizing data types:</u>
In this dataset, we have to standardize the data types of the date columns to datetime and the float columns to int. We did it to facilitate the analysis of the dataset.
In this dataset we standardize the dateNaissance and the DernierAchat columns to datetime and the SoldeCompte, MontantTotalAchats, PanierMoyen, MontantTotalRemboursé columns to int.

### 3. <a id="data-transformation"><u>Data Transformation:</u></a>

##### <u>Objective:</u> Convert data into a more suitable format for analysis. Prepare data for analysis by encoding categorical variables, normalizing numerical data, and creating new features.

##### <u>Methods:</u>

#### 3.1. <u>Anonymisation:</u>
Anonymisation is the process of removing or modifying personal data to prevent the identification of individuals.
In this dataset, we have to anonymize the following columns:
- Nom
- Prénom
- Email
- Adresse
- Téléphone

To anonymize those columns, we used the hashlib library to hash the values of the columns. but we could use the faker library instead.
We used the hashlib library because it's more secure than the faker library for nom, prénom, email columns, and for others columns we only used string replacement.

#### 3.2. <u>Pseudonymization:</u>
Pseudonymization is the process of replacing personal data with pseudonyms to prevent the identification of individuals.
In this dataset, we have to pseudonymize the following columns:
- NuméroCarteCrédit
- DateExpirationCarte
- CodePostal

To pseudonymize those columns, we simply used functions with strings replacement.

#### 3.3. <u>Aggregation:</u>
Aggregation is the process of combining data to create summary statistics or new features. And we used it on the age column to create age groups.
So we group the ages into 7 groups:
- 0-18
- 19-25
- 26-35
- 36-45
- 46-55
- 56-65
- 65+

#### 3.4. <u>Data Reduction:</u>
Data reduction is the process of reducing the size of the dataset while preserving its integrity and quality.
In this dataset, we have to reduce the size of the dataset by removing the columns that are not useful for the analysis.
So we removed the following columns:
- Nom
- Prénom
- Email
- Téléphone
- Adresse
- CodePostal
- DateNaissance
- NuméroCarteCrédit
- DateExpirationCarte
- SoldeCompte

And we reduce the size of the dataset from 31 columns to 21 columns. But the lines reduction is on the dataset is on the cleaning step with the following :
```python
dataset = dataset[dataset['MontantTotalRemboursé'] <= dataset['MontantTotalAchats']]
```

#### 3.5. <u>Data Addition:</u>
Data addition is the process of adding new features to the dataset to enhance the analysis.
In this dataset, we have to add the following columns:
- Taux de remboursement
- Montant total depensé
- the customer with at least 5 buys
- Customer category

### 5. <a id="data-validation"><u>Data Validation:</u></a>

##### <u>Objective:</u> 
Validate the data to ensure its accuracy and reliability. Check for inconsistencies and errors in the data after all the cleaning and transformation process.

## <a id="how-to-use-this-project"><u>How to use this project:</u></a>

To use this project, follow these steps:

### 1. <u>Clone the repository:</u>

```bash
git clone https://github.com/BRENHINES/PipelineData.git
cd PipelineData
```

### 2. <u>Install dependencies:</u>

```bash
pip install -r requirements.txt
```

### 3. <u>Run Jupyter Notebook:</u>

```bash
jupyter notebook
```
Open the relevant notebook and start analyzing the data.

---

## <a id="conclusion"><u>Conclusion:</u></a>

This project successfully demonstrates the complete data processing pipeline, integrating **data ingestion, cleaning, transformation, anonymization, and visualization**. Using **Python**, we automated the data workflow to ensure efficient and secure handling of e-commerce transaction data while adhering to best practices in data engineering.

Key achievements include:
- **Data Preprocessing & Anonymization**: Sensitive customer data was pseudonymized or anonymized to comply with privacy regulations (e.g., GDPR).
- **Feature Engineering**: New insights were extracted, including customer segmentation, refund rates, and purchasing behaviors.

### **Key Takeaways**
- **Scalability**: The use of python allows for easy integration with various data sources and scalable data processing.
- **Data-Driven Insights**: The generated KPIs help e-commerce businesses better understand their customer behavior.
- **Automation & Efficiency**: The project showcases how data engineering pipelines can be designed to minimize manual interventions.

This work highlights the **importance of data workflows for businesses**, ensuring **data integrity, security, and meaningful analytics**. Future improvements could include **real-time data processing, API integrations, or machine learning models for advanced analytics**.

**This project serves as a foundation for building robust and scalable data engineering solutions, ready for real-world applications!**  
