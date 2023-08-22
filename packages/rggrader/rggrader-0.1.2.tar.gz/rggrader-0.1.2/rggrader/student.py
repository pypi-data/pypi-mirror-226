import pandas as pd
import requests

def student_scores(id, submission):
    url = f"https://rea-submitter.fly.dev/student/id?id={id}&submission={submission}"
    response = requests.get(url)
    data = response.json()

    student_info = data['student']
    student_general_info = {k: student_info[k] for k in student_info if k not in ['scores', 'unix_id']}
    scores = student_info['scores']
    scores_good = [score for score in scores if int(score['score']) >= 0]
    df_scores = pd.DataFrame(scores_good)

    for key, value in student_general_info.items():
        print(f"{key}: {value}")

    return df_scores