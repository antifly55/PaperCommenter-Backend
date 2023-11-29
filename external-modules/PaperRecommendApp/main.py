# TODO: implement PaperRecommendApp with Collaborative Filtering, Airflow

import torch
import torch.nn.functional as F
import numpy as np

import pickle

from database import execute_select_sql

## papers, users, ratings to torch.Long/FloatTensor

def download_dataset(data_path):
    dataset = execute_select_sql("SELECT paper_id, user_id, rating FROM paper_rating")
    with open(data_path, 'wb') as f:
        pickle.dump(dataset, f)

def preprocess(data_path):
    with open(data_path, 'rb') as f:
        dataset = pickle.load(f)

    paper_indices = []
    user_indices = []

    papers = []
    users = []
    ratings = []

    for row in dataset:
        paper_id, user_id, rating = row['paper_id'], row['user_id'], row['rating']

        if paper_id not in paper_indices.keys():
            paper_indices[paper_id] = len(paper_indices)
        if user_id not in user_indices.keys():
            user_indices[user_id] = len(user_indices)

        papers.append(paper_indices[paper_id])
        users.append(user_indices[user_id])
        ratings.append(rating)

    ## save paper_indices, user_indices (pickle)
    ## save papers, users, ratings (torch)

def train_model(features=10):

    ## load users, papers, ratings (torch)
    users = None
    papers = None
    ratings = None

    P = np.zeros(len(users), features, requires_grad=True)
    Q = np.zeros(len(papers), features, requires_grad=True)

    optimizer = torch.optim.Adam([P, Q], lr=0.1)

    for epoch in range(100):
        hypothesis = torch.sum(P[papers] * Q[users], dim=1)
        cost = F.mse_loss(hypothesis, ratings)

        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

# 하이퍼파라미터 입력, model 실제 수행
def inference_recommend_rating():
    papers_test = []
    users_test = []

    # get ratings of papers_test & users_test
    with torch.no_grad():
        hypo_test = torch.sum(P[papers_test], Q[users_test], dim=1)

# 위 단계에서 구한 값으로 DB 업뎃
def update_recommend_rating():
    pass