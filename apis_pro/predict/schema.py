import graphene
import joblib
import pandas as pd

# Load your trained model
model = joblib.load('bank_loan_approval_model.pkl')

class LoanApprovalPrediction(graphene.Mutation):
    class Arguments:
        age = graphene.Int(default_value=1)
        experience = graphene.Int(default_value=0)
        income = graphene.Int(default_value=0)
        family = graphene.Int(default_value=0)
        ccavg = graphene.Float(default_value=0)
        education = graphene.Int(default_value=0)
        mortgage = graphene.Int(default_value=0) 
        securities_account = graphene.Int(default_value=0)
        cd_account = graphene.Int(default_value=0)
        online = graphene.Int(default_value=0)
        credit_card = graphene.Int(default_value=0)

    is_approved = graphene.Boolean()

    def mutate(self, info, age=1, experience=0, income=0, family=0, ccavg=0, education=0, mortgage=0, securities_account=0, cd_account=0, online=0, credit_card=0):
        input_data = pd.DataFrame([{
            'Age': age, 
            'Experience': experience, 
            'Income': income, 
            'Family': family, 
            'CCAvg': ccavg, 
            'Education': education, 
            'Mortgage': mortgage, 
            'Securities.Account': securities_account, 
            'CD.Account': cd_account, 
            'Online': online, 
            'CreditCard': credit_card
        }])

        input_data = input_data.fillna(value=0)

        prediction = model.predict(input_data)[0]
        return LoanApprovalPrediction(is_approved=bool(prediction))

class Mutation(graphene.ObjectType):
    predict_loan_approval = LoanApprovalPrediction.Field()

schema = graphene.Schema(mutation=Mutation)
