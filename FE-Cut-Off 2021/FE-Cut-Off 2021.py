import pandas as pd
import numpy as np

from math import floor

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.options.display.float_format = '{:.2f}'.format


df = pd.read_excel("Input - FE Cut-offs 2021.xlsx")

df_obj = df.select_dtypes(['object'])
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

df = df[~df['MHT-CET'].isna()]
df["MHT-CET"] = df["MHT-CET"].apply(lambda x: round(x * 100, 2) if floor(x) == 0 else round(x, 2))

df.drop('Unnamed: 0', axis=1, inplace=True)

cap_rounds = df['CAP'].unique().tolist()

final = pd.DataFrame()
df1 = df.copy(deep=True)

for cap in cap_rounds:
    cap_filter = (df1['CAP'] == cap)
    df_cap = df1[cap_filter]

    institute_codes = df1['Institute Code'].unique().tolist()

    for institute_code in institute_codes:
        institute_code_filter = (df_cap['Institute Code'] == institute_code)
        df_institute = df_cap[institute_code_filter]

        course_names = df_institute['Course name'].unique().tolist()

        for course in course_names:
            course_names_filter = (df_institute['Course name'] == course)
            df_course = df_institute[course_names_filter]

            categories = df_course['Candidate Category'].unique().tolist()

            for category in categories:
                categories_filter = (df_course['Candidate Category'] == category)
                df_category = df_course[categories_filter]

                df_male = df_category[(df_category['Gender'] == 'M')]
                df_female = df_category[(df_category['Gender'] == 'F')]

                male_min_filter = (df_male['MHT-CET'] == df_male['MHT-CET'].min())
                df_male_min = df_male[male_min_filter].head(1)

                df_male_min.insert(2, 'Closing MHT-CET', df_male['MHT-CET'].max())
                df_male_min.rename(columns={'MHT-CET': 'Opening MHT-CET'}, inplace=True)

                female_min_filter = (df_female['MHT-CET'] == df_female['MHT-CET'].min())
                df_female_min = df_female[female_min_filter].head(1)

                df_female_min.insert(2, 'Closing MHT-CET', df_female['MHT-CET'].max())
                df_female_min.rename(columns={'MHT-CET': 'Opening MHT-CET'}, inplace=True)

                df_male_min.round({'Opening MHT-CET': 2, 'Closing MHT-CET': 2})
                df_female_min.round({'Opening MHT-CET': 2, 'Closing MHT-CET': 2})

                final = pd.concat([final, df_male_min, df_female_min], axis=0)

final.reset_index(drop=True, inplace=True)
final.index = np.arange(1, len(final) + 1)
final.to_excel("Output - FE Cut-offs 2021.xlsx", index=True, index_label="Sr. No.")
