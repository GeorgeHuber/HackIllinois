from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import test

df = pd.read_csv("out.csv")
X = df[["Ladder", "Positive Effect","Social support", "Freedom", "Corruption", "Generosity", "Log of GDP per capita", "Healthy life expectancy", "CO2 Emissions", "Population", "Yearly Change", "Density", "Land Area", "Urban Pop %"]]
y  = df['Country']

scaler = preprocessing.RobustScaler().fit(X)
X_1 = scaler.transform(X)
second_scaler = preprocessing.MinMaxScaler(feature_range=(0,1)).fit(X_1)
X_scaled = second_scaler.transform(X_1)

#clf = RandomForestClassifier(max_depth = 5)
#clf = LogisticRegression()
#clf = KNeighborsClassifier()
clf = SVC(probability=True)
clf.fit(X_scaled, y)


# Need to move this somewhere else, but will keep this for now
def main():
    print("Starting")

def pred_country(model_input):
    #"Ladder", "Positive affect","Social support", "Freedom", "Corruption", "Generosity", "Log of GDP per capita", "Healthy life expectancy", "CO2 Emissions", "Population", "Yearly Change", "Density", "Land Area", "Urban Pop %"
    model_input = pd.Series(model_input)
    model_input = model_input / 100
    res = clf.predict_proba([model_input])
    res = res[0] * 100
    countries = df['Country']
    output = list(zip(countries, res))
    output.sort(key=lambda tup: tup[1])
    return output[len(output) - 1][0]

def pred_prob(model_input):
    model_input = pd.Series(model_input)
    model_input = model_input / 100
    res = clf.predict_proba([model_input])
    res = res[0] * 100
    countries = df['Country']
    output = list(zip(countries, res))
    output = Convert(output, {})
    
    return showPlot(output)
    
def showPlot(map_in):
    country_list = map_in.keys()
    probs = []
    for country in country_list:
        probs.append(map_in[country][0])
    temp_map = {
        'Country': country_list,
        'Prob': probs
    }
    df2 = pd.DataFrame(temp_map)
    df2['code'] = df['code']
    return test.config(df2)


def Convert(tup, di):
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di

if __name__ == "__main__":
    main()






