# TODO: implement PaperRecommendApp with Collaborative Filtering, Airflow

import numpy as np

from database import execute_select_sql

def main():
    
    # get dataset from DB
    query_results = execute_select_sql("SELECT paper_id, user_id, rating FROM paper_rating")

    # preprocess
    paper_indices = []
    user_indices = []
    score_dataset = []

    for row in query_results:
        paper_id, user_id, score = row['paper_id'], row['user_id'], row['rating']

        if paper_id not in paper_indices.keys():
            paper_indices[paper_id] = len(paper_indices)
        if user_id not in user_indices.keys():
            user_indices[user_id] = len(user_indices)

        score_dataset.append((paper_id, user_id, score))

    # make matrix
    features = 10
    P = np.zeros(len(user_indices), features)
    Q = np.zeros(len(paper_indices), features)

    

    pass