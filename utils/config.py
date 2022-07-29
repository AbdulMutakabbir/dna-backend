####################################################################################
#### CONFIG EXTRACTION GLOABL SCOPE ################################################
####################################################################################

SKIP_DESTINATION_ETHERNET_TYPES = ["TenGigabitEthernet",
                                   "AppGigabitEthernet",
                                   "FortyGigabitEthernet"]
SKIP_SOURCE_ETHERNET_TYPES = ["GigabitEthernet"]
SKIP_LINES = ["switchport mode trunk"]

COMMAND_RNUNNER_SHOW_INTERFACE_STATUS  = "show interfaces status"

PHYSICAL_PORT_MAPPING = {
    "Fa": "FastEthernet",
    "Gi": "GigabitEthernet",
    "Fi": "FiveGigabitEthernet",
    "Te": "TenGigabitEthernet",
    "Ap": "AppGigabitEthernet",
}



####################################################################################
#### DNAC GLOABL SCOPE #############################################################
####################################################################################

DNAC_BASE_URL = "https://itsdnac.carleton.ca"