import pandas as pd
from bertConnector.models import Question
import numpy as np

df = pd.read_csv('./csv_files/question_10_000.csv')
questions = np.array(df['question'])

for question in questions:
    questionModel = Question()
    questionModel.question = question
    questionModel.save()

# python manage.py shell < file_loader.py
