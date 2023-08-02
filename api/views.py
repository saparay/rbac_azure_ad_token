from django.shortcuts import render
from .models import Department,Employee, JobPosting
from .serializers import DepartmentSerializer,EmployeeSerializer,JobPostingSerializer
from rbac_azure_ad_token.custom_auth import AzureADAuthentication, AzureADAuthorization, AzureADSoftwareEng, AzureADCloudEng, get_by_role
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rbac_azure_ad_token.settings import AZURE_AD_AUTHORITY, AZURE_AD_CLIENT_ID, AZURE_AD_CLIENT_SECRET, AZURE_AD_REDIRECT_URI, AZURE_AD_SCOPE
from django.shortcuts import redirect
from urllib.parse import urlencode
# Create your views here.
import logging
import msal
from django.http import JsonResponse

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AzureADAuthorization])
@authentication_classes([AzureADAuthentication])
def get_job_postings(request):

    job_postings = JobPosting.objects.filter(title = get_by_role(request=request))
    serializer = JobPostingSerializer(job_postings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_departments(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_employee_profile(request, pk):
    employee = Employee.objects.get(id=pk)
    serializer = EmployeeSerializer(employee, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AzureADSoftwareEng])
@authentication_classes([AzureADAuthentication])
def software_engineer(request):
    return JsonResponse({'message': 'Message for only software engineer.'})

@api_view(['GET'])
@permission_classes([AzureADCloudEng])
@authentication_classes([AzureADAuthentication])
def cloud_engineer(request):
    return JsonResponse({'message': 'Message for only cloud engineer.'})




def azure_ad_login(request):
    auth_url = f"{AZURE_AD_AUTHORITY}/oauth2/v2.0/authorize"
    params = {
        "client_id": AZURE_AD_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": AZURE_AD_REDIRECT_URI,
        "response_mode": "query",
        "scope": " ".join(AZURE_AD_SCOPE),
    }
    return redirect(auth_url + '?' + urlencode(params))

@api_view(['GET'])
def get_azure_ad_token(request):
    if 'code' in request.GET:
        
        msal_app = msal.ConfidentialClientApplication(
            AZURE_AD_CLIENT_ID,
            client_credential=AZURE_AD_CLIENT_SECRET,
            authority=AZURE_AD_AUTHORITY
        )
        result = msal_app.acquire_token_by_authorization_code(
            request.GET['code'],
            scopes=AZURE_AD_SCOPE,
            redirect_uri=AZURE_AD_REDIRECT_URI
        )

        logger.debug("Token acquisition result:", result)

        if 'error' in result:
            logger.error(f"Token acquisition error: {result.get('error_description', 'Unknown error')}")
            return JsonResponse({'error': 'Authentication failed.'}, status=400)

        if 'access_token' in result:
            access_token = result['access_token']
            return JsonResponse({'access_token': access_token})

    return JsonResponse({'error': 'Authentication failed.'}, status=400)