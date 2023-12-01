import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv('data.csv')

X = df.drop(['ID', 'ZIP.Code', 'Personal.Loan'], axis=1)
y = df['Personal.Loan']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

print("Model accuracy:", model.score(X_test, y_test))

joblib.dump(model, 'bank_loan_approval_model.pkl')
