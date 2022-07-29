from dnacentersdk import DNACenterAPI
from utils.config_extraction import get_all_configs, get_updated_destination_config
from utils.config import DNAC_BASE_URL, COMMAND_RNUNNER_SHOW_INTERFACE_STATUS, PHYSICAL_PORT_MAPPING
import json
import re
import time

def auth(encoded_auth:str):
    dnac = None

    try:
        dnac = DNACenterAPI(encoded_auth=encoded_auth, base_url=DNAC_BASE_URL, version='2.3.3.0', verify=False)
    except:
        print(f"Unable to authenticate to DNAC!!!")
    
    return dnac

def get_id_from_ip(dnac, ip:str):
    device_id = None

    try:
        device_id = dnac.devices.get_network_device_by_ip(ip).response.id
    except:
        print(f"Unknown switch: {ip} !!!")

    return device_id


def get_config(encoded_auth:str, skip_port_list:list, ip:str):
    dnac = auth(encoded_auth)
    
    device_id = get_id_from_ip(dnac, ip)
    try:
        device_config = dnac.devices.get_device_config_by_id(device_id).response
    except:
        print(f"Unable to extract config for ip: {ip}")

    physical_port_list = []

    physical_ports = run_cmd_show_interface_status_without_auth(dnac, ip)

    physical_port_list = [port['port'] for port in physical_ports]
    
    return get_all_configs(device_config, skip_port_list, physical_port_list)

def updated_config(encoded_auth:str,source_ip:str,destination_ip:str, selected_source_ports:list, selected_destination_ports:list):
    dnac = auth(encoded_auth)

    source_id = get_id_from_ip(dnac, source_ip)
    try:
        source_device_config = dnac.devices.get_device_config_by_id(source_id).response
    except:
        print("WTF!!!")

    destiantion_id = get_id_from_ip(dnac, destination_ip)
    try:
        destination_device_config = dnac.devices.get_device_config_by_id(destiantion_id).response
    except:
        print("WTF!!!")

    # extracted mapping and new config from source and destination
    new_config, mapping = get_updated_destination_config(source_device_config, destination_device_config, selected_source_ports, selected_destination_ports)
    return new_config, mapping

def get_task_by_id(dnac, task_id):
    task_response = dnac.task.get_task_by_id(task_id=task_id)
    return task_response

def get_filtered_device_list(encoded_auth:str, family_list:list=['Switches and Hubs']):
    dnac = auth(encoded_auth)   
    
    devices = dnac.devices.get_device_list(family=family_list)

    return devices

def run_cmd_show_interface_status_without_auth(dnac, ip:str):
    device_id = get_id_from_ip(dnac, ip)

    cmd_runner_res = dnac.command_runner.run_read_only_commands_on_devices(commands=[COMMAND_RNUNNER_SHOW_INTERFACE_STATUS],deviceUuids=[device_id])
    
    task_id = cmd_runner_res['response']['taskId']
    
    while(True):
        task_response = get_task_by_id(dnac, task_id)
        try:
            file_id = json.loads(task_response['response']['progress'])['fileId']
            break
        except:
            time.sleep(1)

    cmd_op = json.loads(dnac.file.download_a_file_by_fileid(file_id).data)[0]['commandResponses']['SUCCESS'][COMMAND_RNUNNER_SHOW_INTERFACE_STATUS]

    physical_port_pattern = r"(([a-zA-Z]{2}\d+/\d+/\d+).*)"
    physical_port_pattern_compiled = re.compile(physical_port_pattern)

    physical_ports = re.findall(physical_port_pattern_compiled, cmd_op)

    port_list = [
        {
            "port": PHYSICAL_PORT_MAPPING[port[1][:2]] + port[1][2:],
            "description": port[0][10:28].strip() 
        } for port in physical_ports]

    return port_list


def run_cmd_show_interface_status(encoded_auth:str,ip:str):
    dnac = auth(encoded_auth)

    port_list = run_cmd_show_interface_status_without_auth(dnac, ip)

    return port_list

    

