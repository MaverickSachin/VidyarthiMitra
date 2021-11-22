import pandas as pd
import numpy as np

from math import floor


pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.options.display.float_format = '{:.2f}'.format


df = pd.read_excel("Input - DSE_final_all with %.xlsx")

df_obj = df.select_dtypes(['object'])
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip() if type(x) == str else x)

df["MHT-CET"] = df["MHT-CET"].apply(lambda x: round(x * 100, 2) if floor(x) == 0 else round(x, 2))

df.drop('Unnamed: 0', axis=1, inplace=True)

cap_rounds = df['CAP'].unique().tolist()

df1 = df.copy(deep=True)
final = pd.DataFrame()

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

                male_filter = (df_category['Gender'] == 'M')
                df_male = df_category[male_filter]

                female_filter = (df_category['Gender'] == 'F')
                df_female = df_category[female_filter]

                male_max_filter = (df_male['MHT-CET'] == df_male['MHT-CET'].max())
                df_male_max = df_male[male_max_filter]

                df_male_max.insert(1, 'Opening MHT-CET', df_male['MHT-CET'].min())
                df_male_max.rename(columns={'MHT-CET': 'Closing MHT-CET'}, inplace=True)

                female_max_filter = (df_female['MHT-CET'] == df_female['MHT-CET'].max())
                df_female_max = df_female[female_max_filter]

                df_female_max.insert(1, 'Opening MHT-CET', df_female['MHT-CET'].min())
                df_female_max.rename(columns={'MHT-CET': 'Closing MHT-CET'}, inplace=True)

                df_male_max['Opening MHT-CET'] = df_male_max['Opening MHT-CET'].apply(lambda x: round(x, 2))
                df_male_max['Closing MHT-CET'] = df_male_max['Closing MHT-CET'].apply(lambda x: round(x, 2))

                df_female_max['Opening MHT-CET'] = df_female_max['Opening MHT-CET'].apply(lambda x: round(x, 2))
                df_female_max['Closing MHT-CET'] = df_female_max['Closing MHT-CET'].apply(lambda x: round(x, 2))

                final = pd.concat([final, df_male_max], axis=0)
                final = pd.concat([final, df_female_max], axis=0)

final.reset_index(drop=True, inplace=True)
final.index = np.arange(1, len(final) + 1)
final.to_excel("Output - DSE_final_all with %.xlsx", index=True, index_label="Sr. No.")
