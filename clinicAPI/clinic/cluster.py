import os.path
import shutil
import xlwt
from xlwt import Workbook
import random
from .models import Clinic, Appointment

def create_analysis(clinic):
    selectedClinic = Clinic.objects.get(name__iexact=clinic)
    appointments = Appointment.objects.filter(clinic=selectedClinic, appointment_status='Approved')

    workbook = Workbook()
    style0 = xlwt.easyxf('font: bold on; align: wrap on,vert centre, horiz center; '
                         'borders: left thick, right thick, top thick, bottom thick; '
                         'pattern: pattern solid, fore_color white;')

    style1 = xlwt.easyxf('align: wrap on,vert centre, horiz center; '
                         'borders: left thin, right thin, top thin, bottom thin; '
                         'pattern: pattern solid, fore_color white;')

    #BASIC DATA LAYOUT
    clinic_sheet = workbook.add_sheet('Raw Data')
    clinic_sheet.write(0, 0, 'DATE', style0)
    clinic_sheet.write(0, 1, 'APPOINTEE', style0)
    clinic_sheet.write(0, 2, 'CATEGORY', style0)
    clinic_sheet.write(0, 3, 'DOCTOR', style0)
    clinic_sheet.write(0, 4, 'COVID SYMPTOMS', style0)
    clinic_sheet.write(0, 5, 'VACCINATED', style0)

    #CLUSTER LEGEND
    cluster_sheet = workbook.add_sheet('Clustered')
    cluster_sheet.write(0, 0, 'CLUSTER ANALYSIS', style0)
    cluster_sheet.write(2, 0, 'BASIS:', style0)
    cluster_sheet.write(3, 0, 'CATEGORY', style0)
    cluster_sheet.write(4, 0, 'COVID SYMPTOMS', style0)
    cluster_sheet.write(5, 0, 'VACCINATION', style0)

    #CLUSTER ANALYSIS
    cluster_sheet.write(0, 2, 'APPOINTMENT NUMBER', style0)
    cluster_sheet.write(0, 3, 'CATEGORY CLUSTER', style0)
    cluster_sheet.write(0, 4, 'SYMPTOMS CLUSTER', style0)
    cluster_sheet.write(0, 5, 'VACCINATION CLUSTER', style0)
    cluster_sheet.write(0, 6, 'PREDICTED CLUSTER', style0)


    #SETTING STYLES
    clinic_sheet.col(0).width = 256 * 32
    clinic_sheet.col(1).width = 256 * 32
    clinic_sheet.col(2).width = 256 * 32
    clinic_sheet.col(3).width = 256 * 32
    clinic_sheet.col(4).width = 256 * 32
    clinic_sheet.col(5).width = 256 * 32

    cluster_sheet.col(0).width = 256 * 32
    cluster_sheet.col(2).width = 256 * 32
    cluster_sheet.col(3).width = 256 * 32
    cluster_sheet.col(4).width = 256 * 32
    cluster_sheet.col(5).width = 256 * 32
    cluster_sheet.col(6).width = 256 * 32

    #SETTING VALUES IN CELLS
    current_row = 1
    for appointment in appointments:
        clinic_sheet.write(current_row, 0, f'{appointment.date_created}', style1)
        clinic_sheet.write(current_row, 1, appointment.patient.get_full_name(), style1)
        clinic_sheet.write(current_row, 2, f'{appointment.category}', style1)
        clinic_sheet.write(current_row, 3, appointment.doctor.user.get_full_name(), style1)

        symptoms = 0
        vaccinated = 0
        randomized_true = round(1+((random.uniform(0, 1)-.5)/5), 4)
        randomized_false = round(0+((random.uniform(0, 1)-.5)/5), 4)

        if appointment.health_check:
            clinic_sheet.write(current_row, 4, 'Yes', style1)
            cluster_sheet.write(current_row, 4, randomized_true, style1)
            symptoms = 1
        else:
            clinic_sheet.write(current_row, 4, 'No', style1)
            cluster_sheet.write(current_row, 4, randomized_false, style1)


        if appointment.vaccinated:
            clinic_sheet.write(current_row, 5, 'Yes', style1)
            cluster_sheet.write(current_row, 5, randomized_true, style1)
            vaccinated = 1
        else:
            clinic_sheet.write(current_row, 5, 'No', style1)
            cluster_sheet.write(current_row, 5, randomized_false, style1)

        #WRITING CLUSTER DATA
        cluster_sheet.write(current_row, 2, appointment.id, style1)
        cluster_sheet.write(current_row, 3, getCategoryCluster(appointment.category), style1)

        #WRITING CLUSTER
        cluster_sheet.write(current_row, 6,
                            round((getCluster(appointment.category, symptoms, vaccinated) + (random.uniform(0, 1)-.5)/5), 4),
                            style1)

        current_row = current_row + 1


    workbook.save(f'{clinic}-Cluster-Analysis.xls')
    print('Cluster Success!')

    move_path = f'C:\\Users\Lord Geese\Documents\GitHub\clinic-system-API\clinicAPI\clinic\clusteranalysis'
    existing_path = f'{move_path}\\{clinic}-Cluster-Analysis.xls'
    current_path = f'C:\\Users\Lord Geese\Documents\GitHub\clinic-system-API\clinicAPI\\{clinic}-Cluster-Analysis.xls'

    if(os.path.exists(existing_path)):
        os.remove(existing_path)
        shutil.move(current_path, move_path)
    else:
        shutil.move(current_path, move_path)

def getCategoryCluster(category):
    if category == 'New Patient':
        return 0
    elif category == 'Follow-Up Patient':
        return 1
    elif category == 'Return Patient':
        return 2
    elif category == 'Referral':
        return 3


def getCluster(category, symptoms, vaccination):
    returned_category = getCategoryCluster(category)
    sum = symptoms + vaccination

    if(returned_category == 0):

        if (sum == 0):
            return 0
        if symptoms == 1 and vaccination == 0:
            return 1
        if symptoms == 0 and vaccination == 1:
            return 2
        if (sum == 2):
            return 3


    elif (returned_category == 1):

        if (sum == 0):
            return 4
        if symptoms == 1 and vaccination == 0:
            return 5
        if symptoms == 0 and vaccination == 1:
            return 6
        if (sum == 2):
            return 7

    elif (returned_category == 2):

        if (sum == 0):
            return 8
        if symptoms == 1 and vaccination == 0:
            return 9
        if symptoms == 0 and vaccination == 1:
            return 10
        if (sum == 2):
            return 11

    elif (returned_category == 3):

        if (sum == 0):
            return 12
        if symptoms == 1 and vaccination == 0:
            return 13
        if symptoms == 0 and vaccination == 1:
            return 14
        if (sum == 2):
            return 15
