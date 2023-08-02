from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import requests
from api.models import Employee
from rbac_demo.settings import AZURE_AD_TENANT_ID, AZURE_AD_CLIENT_ID, AZURE_AD_CLIENT_SECRET
import jwt
class AzureADAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            response = requests.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': f'Bearer {access_token}'})
            # if response.status_code == 200:
            #     return (None, access_token)
            if response.status_code == 200:
                print(response.json())
                decoded_token = jwt.decode(access_token, options={"verify_signature": False})
                tenant_id = decoded_token.get('tid')
                # print(decoded_token)
                if tenant_id == AZURE_AD_TENANT_ID  and decoded_token.get('appid') == AZURE_AD_CLIENT_ID:
                    
                    return (None, access_token)
    
            if not access_token:
                return "Not Valid Token"
            
            if not access_token:
                raise AuthenticationFailed('Invalid access token.')
        except Exception as e:
            raise AuthenticationFailed('Invalid access token.')

        
        

class AzureADAuthorization(BasePermission):
    def has_permission(self, request, view):
        try:
            access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            response = requests.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': f'Bearer {access_token}'})
            if response.status_code == 200:
                user_data = response.json()
                # print(user_data['userPrincipalName'])
                return True

            return False
        except Exception as e:
            raise AuthenticationFailed('Invalid access token.')

class AzureADSoftwareEng(BasePermission):
    def has_permission(self, request, view):
        access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': f'Bearer {access_token}'})
        if response.status_code == 200:
            user_data = response.json()
            mail = user_data['userPrincipalName']
            empl = Employee.objects.get(mail=mail)
            if empl.role == 'Software Engineer':
                return True
        return False
class AzureADCloudEng(BasePermission):
    def has_permission(self, request, view):
        access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': f'Bearer {access_token}'})
        if response.status_code == 200:
            user_data = response.json()
            mail = user_data['userPrincipalName']
            empl = Employee.objects.get(mail=mail)
            if empl.role == 'Cloud Engineer':
                return True
        return False

def get_by_role(request):
    access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code == 200:
        user_data = response.json()
        mail = user_data['userPrincipalName']
        empl = Employee.objects.get(mail=mail)
        return empl.role

""" 
if response.status_code == 200:
            user_data = response.json()
            tenant_id = user_data.get('id')
            if tenant_id and tenant_id == EXPECTED_TENANT_ID:
                request.tenant_id = tenant_id  # Store the tenant ID in the request object
                return (None, access_token)
"""


"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests
from api.models import Employee

class AzureADAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            response = requests.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': f'Bearer {access_token}'})
            if response.status_code == 200:
                user_data = response.json()
                tenant_id = user_data.get('id')
                print(tenant_id)
                print(AZURE_AD_TENANT_ID)
                if tenant_id != AZURE_AD_TENANT_ID:
                    print("Invalid Tenent")
                    raise AuthenticationFailed('Invalid tenant.')
                
                # Verify client ID and secret if needed
                client_id = request.GET.get('client_id')
                print(client_id)
                client_secret = request.GET.get('client_secret')
                if client_id != AZURE_AD_CLIENT_ID or client_secret != AZURE_AD_CLIENT_SECRET:
                    raise AuthenticationFailed('Invalid client credentials.')

                return (None, access_token)
            else:
                raise AuthenticationFailed('Invalid access token.')
        except Exception as e:
            raise AuthenticationFailed('Invalid access token.')

"""




"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import requests
from api.models import Employee


AZURE_AD_TOKEN_INTROSPECTION_URL = "https://login.microsoftonline.com/{0}/v2.0/.well-known/openid-configuration".format(AZURE_AD_TENANT_ID)  # Replace {your_tenant_id} with your Azure AD tenant ID
AZURE_AD_CLIENT_ID = "your_client_id_here"  # Replace this with your Azure AD application's client ID

class AzureADAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if not auth_header or 'bearer' not in auth_header.lower():
                return None

            access_token = auth_header.split(' ')
            # print(access_token)
            introspection_url = AZURE_AD_TOKEN_INTROSPECTION_URL.format(AZURE_AD_TENANT_ID)
            introspection_response = requests.get(introspection_url)
            if introspection_response.status_code == 200:
                introspection_data = introspection_response.json()
                introspection_endpoint = introspection_data.get("token_introspection_endpoint")
                print(introspection_endpoint)
                if introspection_endpoint:
                    response = requests.post(
                        introspection_endpoint,
                        data={'token': access_token, 'client_id': AZURE_AD_CLIENT_ID},
                    )
                    
                    if response.status_code == 200:
                        token_data = response.json()
                        if token_data.get('active') and token_data.get('aud') == AZURE_AD_CLIENT_ID:
                            user_data = self.get_user_data(access_token)
                            request.user_data = user_data
                            return (None, access_token)

            raise AuthenticationFailed('Invalid access token.')

        except AuthenticationFailed:
            raise
        except Exception:
            raise AuthenticationFailed('Invalid access token.')

    def get_user_data(self, access_token):
        try:
            response = requests.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': f'Bearer {access_token}'})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            raise AuthenticationFailed('Error fetching user data.')

# class AzureADAuthorization(BasePermission):
#     def has_permission(self, request, view):
#         user_data = getattr(request, 'user_data', None)
#         if user_data:
#             print(user_data['userPrincipalName'])
#             return True

#         return False

# # Rest of the code remains the same...
"""


