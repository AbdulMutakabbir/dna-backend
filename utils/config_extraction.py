import re
# import os
# import sys
import json
from utils.config import SKIP_DESTINATION_ETHERNET_TYPES, SKIP_LINES


def get_config_line_number_range(lines, init_index, stop_pattern = "!"):
    init_index += 1
    for index, line in enumerate(lines[init_index:]):
        if (line.strip() == "!"):
            return (init_index+1, init_index + index)
    return (None, None)


def get_all_config_meta_data(lines):
    config_ranges = []

    port_pattern = re.compile(r"(interface (\w+Ethernet)(\d+)/(\d+)/(\d+))")

    for index, line in enumerate(lines):
        if (line.strip() == "!"):
            next_line = lines[index+1]
            port_pattern_matches = port_pattern.findall(next_line)
            if (port_pattern_matches is not None) and (len(port_pattern_matches) == 1):
                ethernet_type = port_pattern_matches[0][1]
                slot = port_pattern_matches[0][2]
                sub_slot = port_pattern_matches[0][3]
                port = port_pattern_matches[0][4]
                config_range = get_config_line_number_range(lines, index)
                if (config_range[0] is not None) and (config_range[1] is not None):
                    confg_data = {
                        'start_index': config_range[0],
                        'end_index': config_range[1],
                        'ethernet_type': ethernet_type,
                        'slot': slot,
                        'sub_slot': sub_slot,
                        'port': port
                    }
                    config_ranges.append(confg_data)
                
    return config_ranges

def get_all_configs(data, skip_port_list=[], selected_port_list=[]):
    configs = []

    groups = []

    
    line_data = data.split("\n")
    
    config_meta = get_all_config_meta_data(line_data)
    
    for meta_data in config_meta:

        port_name = get_port_name(meta_data['ethernet_type'],
                                    meta_data['slot'],
                                    meta_data['sub_slot'],
                                    meta_data['port'])

        group = get_group_name(meta_data['ethernet_type'],
                                meta_data['slot'],
                                meta_data['sub_slot'])
        
        config = "\n".join(line_data[meta_data['start_index']:meta_data['end_index']])

        description = ""
        description_pattern = re.compile(r"description\s(.*)\n")
        description_match = description_pattern.search(config)
        if description_match is not None:
            description = description_match.group(1)
        
        if group in groups:
            for config_info in configs:
                if config_info['label'] == group:
                    config_info['children'].append(
                        {
                            'label': port_name,
                            'value': config,
                            'checked': True if (meta_data['ethernet_type'] not in skip_port_list) and (port_name in selected_port_list) else False,
                            'title': description,
                        }
                    )
                    break
        else:
            groups.append(group)
            configs.append(
                {
                    'label': group,
                    'value': group,
                    'checked': True,
                    'title': group,
                    'children': [
                        {
                            'label': port_name,
                            'value': config,
                            'checked': True if (meta_data['ethernet_type'] not in skip_port_list) and (port_name in selected_port_list) else False,
                            'title': description,
                        }
                    ]
                }
            )

    # check parent also all childeren are checked
    for port_group in configs:
        for port in port_group['children']:
            if not port['checked']:
                port_group['checked'] = False
                break

    return configs

def get_port_name(ethernet_type:str,slot:int,sub_slot:int,port:int):
    return f"{ethernet_type}{slot}/{sub_slot}/{port}"

def get_group_name(ethernet_type:str,slot:int,sub_slot:int):
    return f"{ethernet_type}{slot}/{sub_slot}"

def get_all_configs_meta(data):
    configs = []
    
    line_data = data.split("\n")
    
    config_meta = get_all_config_meta_data(line_data)
    
    for meta_data in config_meta:
        config = "\n".join(line_data[meta_data['start_index']:meta_data['end_index']])
        meta_data['config'] = config
        configs.append(meta_data)
        
    return configs

def get_updated_destination_config(source_data, destination_data, selected_source_ports, selected_destination_ports):
    source_configs = get_all_configs_meta(source_data)
    destination_configs = get_all_configs_meta(destination_data)

    new_destination_config = []
    destination_config = destination_data.split("\n")
    if (len(destination_configs) == 0) or (len(source_configs) == 0):
        return destination_data, {}

    update_mapping = {}
    update_mapping["skip_source_ports"] = []

    len_source = len(source_configs)
    source_index = 0

    new_destination_config.extend(destination_config[0:destination_configs[0]['start_index']])

    for destination_index, config_info in enumerate(destination_configs):

        # add intial config part
        new_destination_config.extend(destination_config[destination_configs[destination_index-1]['end_index']:config_info['start_index']])

        source_update_info = None
        destiantion_port_name = get_port_name(config_info['ethernet_type'],
                                                config_info['slot'],
                                                config_info['sub_slot'],
                                                config_info['port'])
        update_mapping[destiantion_port_name] = source_update_info

        # skip if the destionation port not in selceted list 
        # skip if destination port is an uplink port
        # if (config_info['ethernet_type'] in SKIP_DESTINATION_ETHERNET_TYPES) or (any(string in config_info['config'] for string in SKIP_LINES)):
        if (destiantion_port_name not in selected_destination_ports) or (any(string in config_info['config'] for string in SKIP_LINES)):
            new_destination_config.append(config_info['config'])
            continue

        # get next source port
        found_next_source_port = False
        while not found_next_source_port:
            if source_index < len_source:
                source_config = source_configs[source_index]
                source_index += 1
                if len(source_config['config']):
                    source_update_info = get_port_name(source_config['ethernet_type'],
                                                       source_config['slot'],
                                                       source_config['sub_slot'],
                                                       source_config['port'])

                    # skip if source port not in selected list 
                    # skip if source port is uplink port
                    # if(any(string in source_config['config'] for string in SKIP_LINES)):
                    if(source_update_info not in selected_source_ports) or (any(string in source_config['config'] for string in SKIP_LINES)):
                        update_mapping["skip_source_ports"].append(source_update_info)
                        continue

                    new_destination_config.append(source_config['config'])
                    update_mapping[destiantion_port_name] = source_update_info
                    found_next_source_port = True
            else:
                new_destination_config.append(config_info['config'])
                break

    new_destination_config.extend(destination_config[destination_configs[-1]['end_index']:])

    new_destination_config = "\n".join(new_destination_config)
    update_mapping
    return new_destination_config, update_mapping
