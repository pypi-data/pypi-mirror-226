import pandas as pd
import subprocess as sp
import sys
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# データのダウンロード（必要に応じて）
sp.call('wget -nc https://github.com/i-inose/covidimpact/raw/main/Monthly_Counts_of_Deaths_by_Select_Causes__2014-2019.csv', shell=True)
sp.call('wget -nc https://github.com/i-inose/covidimpact/raw/main/Monthly_Provisional_Counts_of_Deaths_by_Select_Causes__2020-2023.csv', shell=True)

# データの読み込み
df1 = pd.read_csv("Monthly_Counts_of_Deaths_by_Select_Causes__2014-2019.csv")
df2 = pd.read_csv("Monthly_Provisional_Counts_of_Deaths_by_Select_Causes__2020-2023.csv")

def plot_cause(keyword):
    df1_filtered = df1.groupby('Year')[keyword].sum().reset_index()
    X = df1_filtered['Year'].values.reshape(-1, 1)
    y = df1_filtered[keyword].values
    reg = LinearRegression().fit(X, y)
    X_pred = df2[['Year']]
    y_pred = reg.predict(X_pred)
    r_squared = r2_score(y, reg.predict(X))

    df1_filtered = df1_filtered[df1_filtered["Year"].isin([2014, 2015, 2016, 2017, 2018, 2019])]
    df1_filtered = df1_filtered.groupby('Year')[keyword].sum().reset_index()
    df2_filtered = df2[df2['Year'].isin([2020, 2021, 2022])]
    df2_filtered = df2_filtered.groupby('Year')[keyword].sum().reset_index()

    impact_df = pd.DataFrame({'Year': df2_filtered['Year'], 'Actual': df2_filtered[keyword], 'Predicted': y_pred[:3].astype(int)})
    impact_df['Impact'] = impact_df['Actual'] / impact_df['Predicted']
    impact_df['Impact'] = impact_df['Impact'].round(2)
    impact_df['Excessive Deaths'] = impact_df['Actual'] - impact_df['Predicted']
    impact_df['Excessive Deaths'] = impact_df['Excessive Deaths'].astype(int)

    data = pd.concat([df1_filtered, df2_filtered])
    ax = data.plot(x='Year', y=keyword, kind='line', marker='o', color='black')

    plt.xlabel('Year')
    plt.ylabel(keyword)
    plt.title(keyword)
    plt.xticks(rotation=90)
    plt.grid()
    for x, y in zip(data['Year'], data[keyword]):
        label = "{:.0f}".format(y)
        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    X_all = data[['Year']]
    y_pred_all = reg.predict(X_all)
    plt.plot(X_all, y_pred_all, linestyle='--', color='black')
    plt.legend(['Data', f'Prediction (R-squared: {r_squared:.3f})'], loc='upper left')
    fig=plt.figure(1)
    fig.set_size_inches(10,3)
    plt.savefig('result.png',dpi=fig.dpi,bbox_inches='tight')
    plt.show()

    impact_df.to_excel(f'{keyword} impact.xlsx', index=False)

def main():
    causes_menu = [
        "All Cause", "Natural Cause", "Septicemia", "Malignant Neoplasms", "Diabetes Mellitus",
        "Alzheimer Disease", "Influenza and Pneumonia", "Chronic Lower Respiratory Diseases",
        "Other Diseases of Respiratory System", "Nephritis, Nephrotic Syndrome, and Nephrosis",
        "Symptoms, Signs, and Abnormal Clinical and Laboratory Findings, Not Elsewhere Classified",
        "Diseases of Heart", "Cerebrovascular Diseases", "Accidents (Unintentional Injuries)",
        "Motor Vehicle Accidents", "Intentional Self-Harm (Suicide)", "Assault (Homicide)", "Drug Overdose"
    ]

    print("Choose a cause:")
    for idx, cause in enumerate(causes_menu, start=1):
        print(f"{idx}. {cause}")

    choice = int(input("Enter the number corresponding to the cause: ")) - 1
    selected_cause = causes_menu[choice]
    
    if selected_cause in df1.columns:
        plot_cause(selected_cause)
    else:
        print("Invalid cause selection.")

if __name__ == "__main__":
    main()
