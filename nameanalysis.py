#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 14:49:26 2019

@author: Marta
"""

import pandas as pd
names2017 = pd.read_csv('yob2017.txt', names = ["Names", "Gender", "Frequency"])
names2017.head(10)

#### IMPORT 1 FILE ####
#### Calculate births in 2017
### Total Births
totalbirths = names2017["Frequency"].sum()
totalbirths
### Calculate births for boys and girls separately
names2017.groupby("Gender")["Frequency"].sum()
### Plot the births in a barplot based on gender
df = names2017.groupby("Gender")["Frequency"].sum()
df.plot.bar()

#### Frequent names
mostpopularnames = names2017[names2017["Frequency"] >= 1000].shape #gives a tuple
#with how many rowns and columns this data dramce contains
## Extract the number of rows from the tuple
mostpopularnames = mostpopularnames[0]
mostpopularnames

#### Percentage of frequency of a given name
names2017["PercentageFromTotal"] = names2017["Frequency"] * 100 / totalbirths
### Verify that the sum of percentage is 100%
names2017["PercentageFromTotal"].cumsum()
### Calculate the percentage of the top 10 names on all births
sorted = names2017.sort_values('Frequency', ascending = False)
frequencycolumn = sorted.iloc[0:10, 3]
percentageoftop10namesfromall = frequencycolumn.sum()

#### Search your name
names2017[names2017["Names"] == "Marta"]

#### Create a bar plot for selected names
#pick random 5 names
selectednames = names2017.sample(n=5)
# set the colour of the bar based on gender
colours = []
for i in list(selectednames["Gender"].values):
    if i == "F":
        colours.append("red")
    else:
        colours.append("blue")
# Create a bar plot
selectednames.plot.bar(x= "Names", y= "Frequency", color= colours)

#### IMPORT ALL FILES ####
#Create a huge dataset containing all files
years = range(1880, 2018)        
data = []
for y in years:
    fn = f'yob{y}.txt'
    df = pd.read_csv(fn, names = ["Names", "Gender", "Frequency"])
    df['Year'] = y
    data.append(df)
    
hugedataset = pd.concat(data)
hugedataset.shape

#Extract all rows with my name
martas = hugedataset[hugedataset["Names"] == "Marta"]
#Take out all males with my name from the dataset
martas = martas[martas["Gender"] == "F"]


#Plot my name over time and save image
from matplotlib import pyplot as plt
martas.plot("Year", "Frequency")
plt.title("Martas over time")
plt.axis([1880, 2017, 0, 500])
plt.ylabel("Frequency")
plt.savefig('Martasovertime.png', dpi=600)

#Create plots for celebrity names
#Create dataset for Harries
hermiones = hugedataset[hugedataset["Names"] == "Hermione"]
hermiones = hermiones[hermiones["Gender"] == "F"]
#Create dataset for Arnolds
Arnies = hugedataset[hugedataset["Names"] == "Arnold"]
Arnies = Arnies[Arnies["Gender"] == "M"]
#Create dataset for Madonnas
Madonnas = hugedataset[hugedataset["Names"] == "Madonna"]
Madonnas = Madonnas[Madonnas["Gender"] == "F"]
#Create dataset for Kennedies
Kennedies = hugedataset[hugedataset["Names"] == "Kennedy"]
Kennedies = Kennedies[Kennedies["Gender"] == "M"]
#Create a dataset for Leias
Leias = hugedataset[hugedataset["Names"] == "Leia"]
Leias = Leias[Leias["Gender"] == "F"]
#Create a dataset for Britneys
Britney = hugedataset[hugedataset["Names"] == "Britney"]
Britney = Britney[Britney["Gender"] == "F"]

#Add all datasets of filtered names into one 
allnames = pd.concat([hermiones, Arnies, Madonnas, Kennedies, Leias, Britney])
#set the names and year as indices
allnames.set_index(["Names", "Year"], inplace = True)
#Only for the Frequency column, because gender is unnecessary.
#Take the 0.index column(names) and unstack it (create columns out of it)
allnames = allnames["Frequency"].unstack(0)
#plot the dataset of all names
allnames.plot()
plt.title("Selected Names")
plt.ylabel("Frequency")
plt.savefig('Selected_Names.png', dpi=600)

#total birth rate in the US over time
birthsovertime = hugedataset.groupby('Year')['Frequency'].sum()
birthsovertime.plot()
#plot both genders separately
separatedgenders = hugedataset.groupby(['Year', "Gender"])['Frequency'].sum()
separatedgenders = separatedgenders.unstack(1)
separatedgenders.plot()

#Relative Frequency
#Get the relative frequency of each name in relation to total number of births
#in that year
#Calculate the total births of each year and call them birthsovertime
birthsovertime= (hugedataset.groupby('Year')[['Frequency']].sum()) #a series
birthsovertime[1880] #the year works as an index for the total births of that year
#Take the Year and Frequency values of each row
#Calculate the relfreq = (frequency of the name in that year)/(total births in that year)
#append the relative frequency value to an empty list
a = []
for y, f in hugedataset[["Year", "Frequency"]].values:
    relfreq = f / birthsovertime[y]
    a.append(relfreq)
#compare whether the lenght of the relative frequency list equals the lenght of the complete dataset
#so that there is a relative frequency value for each row
len(a) == len(hugedataset)
#Create a new column in hugedataset for each row which is relative frequency of the name
#(Frequency of the name in that year)/(Total births in that year)
hugedataset["RelativeFrequencyofName"] = a

##2nd option for relative frequency
#If 2 square brackets, makes it as a dataframe 
birthsovertime= (hugedataset.groupby('Year')[['Frequency']].sum())
birthsovertime.reset_index(inplace = True)
#"on" specifies which two columns of the 2 datasets should be merged
#"how" specifies which dataset should be merged on which, i.e.,
#in this case, merge on LEFT
supermerged = pd.merge(hugedataset, birthsovertime, on="Year", how="left")
supermerged["Total births of that year"] = supermerged["Frequency_y"]
supermerged["RelFreqofName"] = supermerged["Frequency_x"] / supermerged["Total births of that year"]
supermerged.head()

#Diversity of names
#How many different names there are in each year
hugedataset.groupby("Year")["Names"].count().plot()
#Yes, the baby names have become more diverse over time,
#because the number of names per year have increased with time

#Lenght of the names
#Create a function that counts the characters
def countlenght(i):
    return len(i)
#Apply the function to "Names"
hugedataset["Lenght"] = hugedataset["Names"].apply(countlenght)
hugedataset.head()
#Lenght of the names option2 
#with lambda, create fucntion in one line
hugedataset["Lenght2"] = hugedataset["Names"].apply(lambda x: len(x))
#Delete columns
hugedataset.drop("Lenght2", axis= 1, inplace= True)
#Print the 10 longest names
longestnames = hugedataset.sort_values(by=["Lenght"], ascending = False)
print(longestnames.head(10))

#First letter statistics
#Create a new column with initial of the name
def get_initial(s):
    return s[0]
hugedataset['Initial'] = hugedataset['Names'].apply(get_initial)
##count how many names start with A
grouped = hugedataset.groupby(['Names', "Initial"])[["Frequency"]].sum()
grouped1 = grouped["Frequency"].unstack(1)
grouped1["A"].count()
#plot the occurence of initials over time
yearinitial = hugedataset.groupby(['Year', "Initial"]).sum()
aa = yearinitial["Frequency"].unstack(1)
aa.plot()

#Last letter statistics
#create a new column with the last letter of the name
def get_lastletter(s):
    return s[-1]
hugedataset['Lastletter'] = hugedataset['Names'].apply(get_lastletter)
#separate for boys and girls
boysgirls = hugedataset.groupby(['Lastletter', "Gender"])[["Frequency"]].sum()
boysgirls = boysgirls["Frequency"].unstack(1)
boysgirls.plot.bar()
#conclusion= girls names end with "a" most often
#the last letter of boys names differs much more

#e-rich names (find names that contain letter e at least 4 times)
def howmanye(n):
    if n.count("e") >= 4:
        return n
#create a new column that reprints the name if the name has 4e of more
hugedataset['erich'] = hugedataset['Names'].apply(howmanye)
#groupby the names that have 4e or more and add them up to avoid duplicates
#over several years
qqq = hugedataset.groupby("erich")["Frequency"].sum()
#count how many different names that contain 4e or more are there = 92
qqq.count()







