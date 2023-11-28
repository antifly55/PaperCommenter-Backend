# TODO: implement PaperRecommendApp with Collaborative Filtering, Airflow

import torch
import torch.nn.functional as F
import numpy as np

from database import execute_select_sql

def main():
    
    # get dataset from DB
    query_results = execute_select_sql("SELECT paper_id, user_id, rating FROM paper_rating")

    # preprocess
    paper_indices = []
    user_indices = []

    papers = []
    users = []
    ratings = []

    for row in query_results:
        paper_id, user_id, rating = row['paper_id'], row['user_id'], row['rating']

        if paper_id not in paper_indices.keys():
            paper_indices[paper_id] = len(paper_indices)
        if user_id not in user_indices.keys():
            user_indices[user_id] = len(user_indices)

        papers.append(paper_indices[paper_id])
        users.append(user_indices[user_id])
        ratings.append(rating)

    ## convert types
    ## papers, users, ratings to torch.Long/FloatTensor

    # make matrix
    features = 10
    P = np.zeros(len(users), features, requires_grad=True)
    Q = np.zeros(len(papers), features, requires_grad=True)

    # train default MF
    optimizer = torch.optim.Adam([P, Q], lr=0.1)

    for epoch in range(100):
        hypothesis = torch.sum(P[papers], Q[users], dim=1)
        cost = F.mse_loss(hypothesis, ratings)

        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f"epoch: {epoch}, cost: {round(cost.item(), 4)}")

    # test
    ## convert types
    papers_test = []
    users_test = []

    # get ratings of papers_test & users_test
    with torch.no_grad():
        hypo_test = torch.sum(P[papers_test], Q[users_test], dim=1)
        