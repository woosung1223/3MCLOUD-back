import boto3
from .models import User
from botocore.exceptions import ClientError
from config.settings import REGION, USER_POOL_ID, APP_CLIENT_ID, IDENTITY_POOL_ID, ACCOUNT_ID, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID



class Cognito():
    def __init__(self):
        self.idp_client = boto3.client('cognito-idp', REGION,
                                  aws_access_key_id = AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
        self.ci_client = boto3.client('cognito-identity', region_name= REGION)

    def sign_in(self, request):
        try:
            username_ = request.data['username']
            password_ = request.data['password']
            real_password = User.objects.get(username = username_).password
            if(password_ != real_password):
                return -1
            
            try:
                resp = self.idp_client.admin_initiate_auth(UserPoolId= USER_POOL_ID,
                                                ClientId= APP_CLIENT_ID,
                                                AuthFlow='ADMIN_NO_SRP_AUTH',
                                                AuthParameters={'USERNAME': username_,'PASSWORD': password_} )
                AccessToken = resp['AuthenticationResult']['AccessToken']
                IdToken = resp['AuthenticationResult']['IdToken']

            except ClientError as e: # Cognito Exceptions
                 print(e)

        except:
            return 0 # No User Found
        
        return AccessToken, IdToken

    def sign_up(self, request):
        try:
            username_ = request.data['username']
            password_ = request.data['password']
            email = request.data['email']

            resp = self.idp_client.sign_up(ClientId=APP_CLIENT_ID,
                                  Username=username_,
                                  Password=password_,
                                  UserAttributes=[{'Name': 'email', 'Value': email}])
        except:
            return False
        return resp

    def confirm_sign_up(self, request):
        try:
            username_ = request.data['username']
            confirm_code = request.data['confirmcode']
            resp = self.idp_client.confirm_sign_up(ClientId=APP_CLIENT_ID,
                                            Username=username_,
                                            ConfirmationCode=confirm_code)
        except:
            return False
        return resp

    def check_user_auth(self, request):
        token = request.data['AccessToken']
        try:
            resp = self.idp_client.get_user(AccessToken = token)
        except ClientError as e: # Cognito Exceptions
                print(e)
                return False

        return resp['Username']
