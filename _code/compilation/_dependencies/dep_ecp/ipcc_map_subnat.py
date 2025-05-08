# Mapping of subnational inventory sector names with IPCC category codes
import json
import os

def load_ipcc_mapping_from_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Set paths to mapping files
mapping_dir = "/Users/gd/GitHub/ECP/_code/compilation/_dependencies/dep_ecp"
mappings = {
    "canada": load_ipcc_mapping_from_json(os.path.join(mapping_dir, "ipcc_mapping_canada.json")),
    "china": load_ipcc_mapping_from_json(os.path.join(mapping_dir, "ipcc_mapping_china.json")),
    "usa": load_ipcc_mapping_from_json(os.path.join(mapping_dir, "ipcc_mapping_usa.json"))
}

# Access mappings like this
category_names_ipcc_can_map = mappings["canada"]
category_names_ipcc_chn_map = mappings["china"]
category_names_ipcc_usa_map = mappings["usa"]

#'Abandoned Oil and Gas Wells', 'MVAC', 'Petroleum Systems', 'Electrical Transmission and Distribution',
# 'LULUCF Carbon Stock Change', 'LULUCF N2O Emissions', 'LULUCF CH4 Emissions', 'Natural Gas Systems',
#'Urea Consumption for Non-Agricultural Purposes':'', 'HCFC-22 Production', 'Phosphoric Acid Production',
# 'Transport - Natural gas pipeline', 'Carbon Dioxide Consumption',



