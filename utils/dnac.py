from dnacentersdk import DNACenterAPI
from utils.config_extraction import get_updated_destination_config
from utils.config import DNAC_BASE_URL


def updated_config(encoded_auth:str,source_ip:str,destination_ip:str):
    dnac = DNACenterAPI(encoded_auth=encoded_auth, base_url=DNAC_BASE_URL, version='2.3.3.0', verify=False)

    try:
        source_id = dnac.devices.get_network_device_by_ip(source_ip).response.id
        source_device_config = dnac.devices.get_device_config_by_id(source_id).response
    except:
        print("WTF!!!")

    try:
        destiantion_id = dnac.devices.get_network_device_by_ip(destination_ip).response.id
        destination_device_config = dnac.devices.get_device_config_by_id(destiantion_id).response
    except:
        print("WTF!!!")

    # extracted mapping and new config from source and destination
    new_config, mapping = get_updated_destination_config(source_device_config, destination_device_config)
    return new_config, mapping
