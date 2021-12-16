import pandas as pd
import fitz  # this is pymupdf

with fitz.open("FE_CAP Round_I_2021.pdf") as doc:
    text = ""
    for page in doc:
        text += page.get_text()

    lines = text.split("\n")
    college_indexes, college_codes, college_names = [], [], []

    for index, line in enumerate(lines):
        if ' - ' in line:
            code = line.split(" - ")[0].strip()
            college = line.split("-")[1].strip()
            if 'college' in college.lower() or 'university' in college.lower():
                if (len(code) == 4) and code.isdigit():
                    if (code not in college_codes):
                        college_indexes.append(index)
                        college_codes.append(code)
                        college_names.append(college)
    
    last_college_index = college_indexes[-1]
    cleaned_college_names = [c[:-1] if c[-1] == '.' else c for c in college_names]
    cleaned_college_codes = [int(c) for c in college_codes]

    stages = [0, ]
    for i, c in enumerate(college):
        if c == 'Stage':
            stages.append(i)
    last_stage_course = stages[-1]

    for j, _ in enumerate(stages):
        if _ != last_stage_course:
            course = college[stages[j+1]:stages[j]]

            start = course.index('State Level') + 1
            end = course.index('  I')

            categories = course[start:end]
            for i, category in enumerate(categories):
                if len(category) == 1:
                    categories[i-1] += category
                    del categories[i]

            values = course[end+1:]

            smls = [int(s) for s in values[::2] ]
            cet_scores = [round(float(score[1:-1]), 2) for score in values[1::2]]

            n = len(cet_scores)

            c_code = [int(college_codes[0])] * n
            c_name = [college_names[0]] * n
            course_code = [course[0].split(' - ')[0]] * n
            course_name = [course[0].split(' - ')[1]] * n
            status = [course[course.index('Status:') + 1]] * n
            genders = [g[0] for g in categories]
            hos_types = ['S'] * n

            df = pd.DataFrame({
                "College Code": c_code,
                "College Name": c_name,
                "Course Code": course_code,
                "Course Name": course_name,
                "Status": status,
                "Category": categories,
                "SML": smls,
                "CET Score": cet_scores,
                "Gender": genders,
                "H O S Type": hos_types
            })
            
            
