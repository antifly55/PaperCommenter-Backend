import torch
import torch.nn.functional as F

import pickle

from database import execute_select_sql

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

def train_model(features=10, lr=0.1, start_epoch=0, end_epoch=100):

    ## load users, papers, ratings (torch)
    ## type convert - torch.Long/FloatTensor
    users = None
    papers = None
    ratings = None

    if not start_epoch:
        P = torch.randn(len(users), features, requires_grad=True)
        Q = torch.randn(len(papers), features, requires_grad=True)
        optimizer = torch.optim.Adam([P, Q], lr=lr)
    else:
        ## load P, Q, optimizer
        pass 

    for epoch in range(start_epoch, end_epoch):
        hypothesis = torch.sum(P[papers] * Q[users], dim=1)
        cost = F.mse_loss(hypothesis, ratings)

        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

        ## log cost

    ## save P, Q, optimizer
    ## Xcom으로 가장 cost가 낮은 model 정보 저장

def inference_recommend_rating(model_path):

    ## Xcom으로 가장 cost가 낮은 model 정보 불러오기
    ## load model
    P = None
    Q = None

    # get ratings of papers_test & users_test
    with torch.no_grad():
        hypo_test = torch.sum(P * Q, dim=1)