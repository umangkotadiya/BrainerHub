from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer
from django.db import transaction
from rest_framework.generics import ListAPIView
# from rest_framework.decorators import @login
from rest_framework.permissions import IsAuthenticated

class FileUploadView(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request):
        file = request.FILES['file']
        file_ext = str(file.name.split('.')[1])
        file_type_allow = ['csv', 'xlsx']

        Company.objects.all().delete()
        Employee.objects.all().delete()

        # Check file and file extension.
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        elif file_ext and file_ext not in file_type_allow:
            return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

        # Read file
        read_file = pd.read_excel(file) if file_ext == 'xlsx' else pd.read_csv(file)

        # Define essential variables
        companies = {}
        employees_data = []
        errors = []

        # Get row one by one
        for index, row in read_file.iterrows():
            company_name = row['COMPANY_NAME']
            if company_name not in companies:
                if company_name:
                    company_dict = {
                        'name': row['COMPANY_NAME'],
                    }
                    com_serializer = CompanySerializer(data=company_dict)
                    if com_serializer.is_valid():
                        company_instance = com_serializer.save()  # Save and get the company instance
                        companies[company_name] = company_instance.id
                    else:
                        errors.append({
                            'row': index + 1,
                            'errors': com_serializer.errors
                        })
                        continue

            employe = {
                'first_name': row['FIRST_NAME'],
                'last_name': row['LAST_NAME'],
                'phone_number': row['PHONE_NUMBER'],
                'company': companies[company_name],
                'salary': row['SALARY'],
            }
            # Append employee object
            emp_serializer = EmployeeSerializer(data=employe)
            if emp_serializer.is_valid():
                employees_data.append(Employee(**emp_serializer.validated_data))  # Append validated data
            else:
                errors.append({
                    'row': index + 1,
                    'errors': emp_serializer.errors
                })

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            with transaction.atomic():
                # Bulk create employees
                if employees_data:
                    # employee_instances = [Employee(**data) for data in employees_data]
                    Employee.objects.bulk_create(employees_data)
            return Response({"message": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)



class EmployeeListView(ListAPIView):
    model = Employee
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()