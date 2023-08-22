"""Initialize the cdc_tech_environment_service subpackage of data_ecosystem_services package"""

# allow absolute import from the root folder
# whatever its name is.
import data_ecosystem_services.az_storage_service.az_storage_queue
import data_ecosystem_services.cdc_tech_environment_service.job_core
import data_ecosystem_services.cdc_tech_environment_service.repo_core
import data_ecosystem_services.cdc_security_service.security_core
import data_ecosystem_services.cdc_admin_service.environment_logging
import data_ecosystem_services.cdc_tech_environment_service.environment_spark
import data_ecosystem_services.cdc_tech_environment_service.environment_file
import data_ecosystem_services.cdc_tech_environment_service.environment_core
import data_ecosystem_services.cdc_tech_environment_service.dataset_crud
import data_ecosystem_services.cdc_tech_environment_service.dataset_core
import data_ecosystem_services.cdc_tech_environment_service.environment_http
import sys  # don't remove required for error handling
import os

# Import from sibling directory ..\cdc_tech_environment_service
OS_NAME = os.name

sys.path.append("..")

if OS_NAME.lower() == "nt":
    print("cdc_tech_environment_service: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(
        os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("cdc_tech_environment_service: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))
