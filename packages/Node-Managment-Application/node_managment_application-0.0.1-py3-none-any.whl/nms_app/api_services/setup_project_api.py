import os
import pathlib
import uuid
from rest_framework import status

from nms_app.models import SetupProjectDetails
from nms_app.nms_services.api_key_valdation import get_node_id
from nms_app.nms_services.common_services import background_processing, download_file_from_url, run_command


def project_setup_func(request):
    node_id = request.query_params.get('node_id')
    node_category = request.query_params.get('node_category')
    ref = str(uuid.uuid4())
    spd_node_category = SetupProjectDetails.objects.values_list('spd_node_category', flat=True)
    if "GUARDIAN" in spd_node_category or "MASTER" in spd_node_category:
        return {'status': 'fail',
                'Message': f"{spd_node_category[0]} project already setup."}, status.HTTP_401_UNAUTHORIZED
    else:
        unique_value = SetupProjectDetails(spd_node_id=node_id,
                                           spd_node_category=node_category,
                                           spd_ref_id=ref, )
        unique_value.save()
        if node_id == get_node_id():
            if node_category.upper() == 'MASTER':
                location = r'/home/ubuntu/L2_App/'
                path = pathlib.Path(location)
                path.mkdir(parents=True, exist_ok=True)
                urls = ['wget https://alkimi-bid-resources.s3.eu-west-2.amazonaws.com/L1L2Apps/node-l2.tar',
                        'wget https://alkimi-bid-resources.s3.eu-west-2.amazonaws.com/L1L2Apps/docker-compose.yml',
                        'wget https://alkimi-bid-resources.s3.eu-west-2.amazonaws.com/L1L2Apps/createEnvFile.sh']
                SetupProjectDetails.objects.filter(spd_ref_id=ref).update(spd_download_location=location)
                os.chdir(location)
                for url in urls:
                    run_command(url)
                SetupProjectDetails.objects.filter(spd_ref_id=ref).update(spd_download_status=True)
                return {'status': 'success',
                        'Message': f"{node_category} project setup successfully."}, status.HTTP_200_OK
            if node_category.upper() == 'GUARDIAN':
                location = r'/home/ubuntu/L1_App/'
                path = pathlib.Path(location)
                path.mkdir(parents=True, exist_ok=True)
                urls = ['wget -O cl-keytool_1.9.1.jar https://github.com/Constellation-Labs/tessellation/releases'
                        '/download/v1.9.1/cl-keytool.jar',
                        'wget https://alkimi-bid-resources.s3.eu-west-2.amazonaws.com/L1L2Apps/tessellation-core'
                        '-assembly-1.9.1.jar']
                SetupProjectDetails.objects.filter(spd_ref_id=ref).update(spd_download_location=location)
                os.chdir(location)
                for url in urls:
                    run_command(url)
                # os.chdir(r'/home/ubuntu/L1_App/')
                # run_command('export CL_KEYSTORE=key.p12 CL_KEYALIAS=walletalias CL_PASSWORD=welcome123')
                # run_command('java -jar cl-keytool_1.9.1.jar generate')
                SetupProjectDetails.objects.filter(spd_ref_id=ref).update(spd_download_status=True)
                # background_processing(download_file_from_url, [url, location, ref, filenames])
                return {'status': 'success',
                        'Message': f"{node_category} project setup successfully."}, status.HTTP_200_OK
            else:
                return {'status': 'fail', 'Message': "Invalid node category."}, status.HTTP_401_UNAUTHORIZED
        else:
            return {'status': 'fail', 'Message': "Invalid Node Id."}, status.HTTP_401_UNAUTHORIZED
