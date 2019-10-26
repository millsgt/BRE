import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import csr_matrix

from sklearn.metrics.pairwise import euclidean_distances

df = pd.DataFrame([
    [0, 5, 4, 0, 0, 0],
    [0, 5, 5, 5, 0, 0],
    [5, 0, 0, 5, 0, 0],
    [0, 5, 4, 0, 0, 5],
    [0, 0, 0, 5, 3, 5]
])

euclidean_distances(df)

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from lightfm import LightFM

# Quick Data Prep

df = pd.read_csv('data/candy.csv')
users = df['user'].value_counts()[df['user'].value_counts() >= 5].index
df = df[df['user'].isin(users)]
df['product'] = df['product'].str.replace('/reviews/', '')
df

#### WIP

df=df.copy()
ratings='stars'
users='user'
items='product'

_ratings = np.array(df[ratings])
_users = np.array(df[users])
_items = np.array(df[items])
# heavy lifting encoders
user_encoder = LabelEncoder()
item_encoder = LabelEncoder()
# preparation for the csr matrix
u = user_encoder.fit_transform(_users)
i = item_encoder.fit_transform(_items)
lu = len(np.unique(u))
li = len(np.unique(i))
# the good stuff
interactions = csr_matrix((_ratings, (u, i)), shape=(lu, li))

peek = pd.DataFrame(
    interactions.todense(),
    index=user_encoder.classes_,
    columns=item_encoder.classes_
)

peek.loc['07julia12'].sort_values(ascending=False)[:7]

df[df['user'] == '07julia12']

model = LightFM(loss='warp')
model.fit(interactions, epochs=100)

person = '07julia12'
user_id = user_encoder.transform([person])[0]
preds = model.predict(user_id, list(range(li)))

pred_df = pd.DataFrame({
    'product': item_encoder.classes_,
    'rating': preds
}).sort_values('rating', ascending=False)

pred_df

from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score

precision_at_k(model, interactions, k=10).mean()
auc_score(model, interactions).mean()

reco = pred_df['product'].values.tolist()

tried = df[df['user'] == person]['product'].tolist()

[candy for candy in reco if candy not in tried][:5]


person = 'kitkatkittikat'
df[df['user'] == person]
