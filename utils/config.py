####################################################################################
#### CONFIG EXTRACTION GLOABL SCOPE ################################################
####################################################################################

SKIP_DESTINATION_ETHERNET_TYPES = ["TenGigabitEthernet",
                                   "AppGigabitEthernet",
                                   "FortyGigabitEthernet"]
SKIP_SOURCE_ETHERNET_TYPES = ["GigabitEthernet"]
SKIP_LINES = ["switchport mode trunk"]




####################################################################################
#### DNAC GLOABL SCOPE #############################################################
####################################################################################

DNAC_BASE_URL = "https://itsdnac.carleton.ca"