from datetime import datetime

COMMENTS = [
    {
        'id': 1,
        'paper_id': 1,
        'username': "abc",
        'content': "abc",
        'create_datetime': datetime.now(),
        'modify_datetime': datetime.now(),
        'like_count': 0
    },
    {
        'id': 2,
        'paper_id': 1,
        'username': "abc",
        'content': "abcd",
        'create_datetime': datetime.now(),
        'modify_datetime': datetime.now(),
        'like_count': 0
    },
    {
        'id': 3,
        'paper_id': 2,
        'username': "abc",
        'content': "abcde",
        'create_datetime': datetime.now(),
        'modify_datetime': datetime.now(),
        'like_count': 0
    },
    {
        'id': 4,
        'paper_id': 3,
        'username': "abc",
        'content': "abcdef",
        'create_datetime': datetime.now(),
        'modify_datetime': datetime.now(),
        'like_count': 0
    },
]

def get_comment(comment_id: int):
    for comment in COMMENTS:
        if comment['id']==comment_id:
            return comment

def get_comment_list(paper_id: int, skip: int = 0, limit: int = 10):
    _comment_list = []
    for comment in COMMENTS:
        if comment['paper_id']==paper_id:
            _comment_list.append(comment)

    total = len(_comment_list)
    comment_list = _comment_list[skip : skip + limit]

    return total, comment_list

def create_comment(paper_id: int, content: str):
    COMMENTS.append({
        'id': 5,
        'paper_id': paper_id,
        'content': content,
        'create_datetime': datetime.now(),
        'modify_datetime': None
    })

def update_comment(comment_id: int, content: str):
    for comment in COMMENTS:
        if comment['id']==comment_id:
            comment['content'] = content
            comment['modify_datetime'] = datetime.now()
            break

def delete_comment(comment_id: int):
    for idx in range(len(COMMENTS)):
        if COMMENTS[idx]['id']==comment_id:
            COMMENTS.pop(idx)
            break