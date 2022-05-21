import boto3
from .models import User
from botocore.exceptions import ClientError
# ENV
class Cognito():
    def __init__(self):
        self.idp_client = boto3.client('cognito-idp', region,
                                  aws_access_key_id = AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
        self.ci_client = boto3.client('cognito-identity', region_name= region)

    def sign_in(self, request):
        try:
            username_ = request.data['username']
            password_ = request.data['password']
            real_password = User.objects.get(username = username_).password
            if(password_ != real_password):
                return -1
            
            try:
                resp = self.idp_client.admin_initiate_auth(UserPoolId= user_pool_id,
                                                ClientId= app_client_id,
                                                AuthFlow='ADMIN_NO_SRP_AUTH',
                                                AuthParameters={'USERNAME': username_,'PASSWORD': password_} )
                token = resp['AuthenticationResult']['IdToken']

            except ClientError as e: # Cognito Exceptions
                 print(e)

        except:
            return 0 # No User Found
        
        return token

