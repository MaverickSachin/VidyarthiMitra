import pandas as pd
import numpy as np

df = pd.read_excel("Input - NEET Opening Closing 2020.xlsx")

starting_points = df.loc[df['Unnamed: 0'].str.contains('Admissions', na=False), 'Unnamed: 0'].index.tolist()
end_points = df.loc[df['Unnamed: 0'].str.contains('LEGEND', na=False), 'Unnamed: 0'].index.tolist()

categories = ['SC', 'ST', 'VJ', 'NT1', 'NT2', 'NT3', 'OBC', 'EWS', 'OPEN', 'D1', 'D2', 'D3', 'PH', 'MKB', 'NRI']
columns = ['Code', 'College Name', 'Category', 'S - AIR', 'M - Marks Obtained', 'Course', 'College Type']

final = pd.DataFrame(columns=columns)

df1 = df.copy(deep=True)

# dropping the first column from the dataframe
df1.drop('Unnamed: 0', axis=1, inplace=True)

for start, end in zip(starting_points, end_points):

    df2 = df1.loc[start + 2:end - 1]

    # Name of the course and type of the college
    course_college_type = df1.iloc[start + 1, :].dropna()[0].split("Quotawise List of Last Admitted Candidates In ")[1:][0].strip()

    split_by = '  ' if '  ' in course_college_type else ' '
    course_college_type = course_college_type.split(split_by)
    course = course_college_type[0]
    college_type = course_college_type[1] if len(course_college_type) >= 2 else "N/A"

    college_names = df2["Unnamed: 1"].tolist()[1:]

    # dropping the first column from the dataframe
    df2.drop('Unnamed: 1', axis=1, inplace=True)
    df2.drop('Unnamed: 2', axis=1, inplace=True)
    df2.reset_index(drop=True, inplace=True)

    df2, df2.columns = df2[1:], df2.iloc[0]
    df2.replace(np.NaN, 'N/A', inplace=True)
    df2 = df2.loc[:, df2.columns.notnull()]

    df2.reset_index(drop=True, inplace=True)

    missing_categories = list(set(categories) - set(df2.columns.tolist()))

    for category in missing_categories:
        df2[category] = 'N/A'

    df2 = df2[categories]

    output = []
    for i in range(0, len(college_names), 2):
        first_part = college_names[i]
        if first_part[-1] == ":":
            first_part = first_part[:-4]

        if pd.isna(college_names[i + 1]):
            second_part = ""
        else:
            second_part = college_names[i + 1]
            if second_part[-1] == ":":
                second_part = second_part[:-4]

        output.append(first_part.strip() + ' ' + second_part.strip())

    i = 0
    for item in output:
        if item.split(" ")[0].isnumeric() and item.split(" ")[1].isnumeric():
            college_code = item.split(" ")[1]
            college_name = "".join(item.split(" ")[2:])
        else:
            college_code = item.split(" ")[0]
            college_name = " ".join(item.split(" ")[1:])

        college_code = [college_code] * 15
        college_name = [college_name] * 15

        course = [course_college_type[0]] * 15
        college_type = [course_college_type[1] if len(course_college_type) >= 2 else "N/A"] * 15

        # rankings AIR
        rankings = df2.iloc[i, :].tolist()

        # marks obtained
        marks = df2.iloc[i + 1, :].tolist()
        i += 2

        new_df = pd.DataFrame(list(zip(college_code, college_name, categories, rankings, marks, course, college_type)), columns=columns)
        final = pd.concat([final, new_df], axis=0)

final.reset_index(drop=True, inplace=True)
final.to_excel("Output - NEET Opening Closing 2020.xlsx", index=True, index_label="Sr. No.")
