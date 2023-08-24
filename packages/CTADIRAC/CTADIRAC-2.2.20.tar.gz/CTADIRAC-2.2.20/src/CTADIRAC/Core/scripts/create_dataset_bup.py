#!/usr/bin/env python
"""
Create datasets descriptions (in json format) for DL2 processing with ctapipe
The produced json files can be used as inputs to cta-prod-add-dataset

Usage:
   cta-prod-create-dataset-description
Arguments:
   json file with dataset query dict
   The file should have the .json extension, e.g. my_dataset.json
"""

__RCSID__ = "$Id$"

import json

import DIRAC
from DIRAC.Core.Base.Script import Script

#@Script()
def main():
    Script.registerSwitch('', 'MCCampaign', 'MCCampaign')
    Script.registerSwitch('', 'site', 'site')
    Script.registerSwitch('', 'array_layout', 'array_layout')
    Script.registerSwitch('', 'az', 'azimuth angle')
    Script.registerSwitch('', 'zen', 'zenith angle')
    Script.registerSwitch('', 'nsb', 'nsb')
    Script.registerSwitch('', 'ctapipe_ver', 'ctapipe_version')
    switches, argss = Script.parseCommandLine(ignoreErrors=True)

    MCCampaign = "PROD5b"
    site = "LaPalma"
    array_layout = "Alpha"
    particle = "gamma"
    #configuration_id = 8
    phiP = 180.0
    thetaP = 20
    nsb = 1
    analysis_prog_version = "v0.19.0"

    for switch in switches:
        if switch[0] == 'MCCampaign':
            MCCampaign = switch[1]
        elif switch[0] == 'site':
            site = switch[1]
        elif switch[0] == 'array_layout':
            array_layout = switch[1]
        elif switch[0] == 'az':
            phiP = az
        elif switch[0] == 'dumpFull':
            dumpFullFlag = True

    file_ext_list = [".DL1ImgParDL2Geo.json", ".DL1ParDL2Geo.json", ".DL2GeoEneGam.json"]
    for file_ext in file_ext_list:
        if file_ext == ".DL1ImgParDL2Geo.json":
            analysis_prog = "ctapipe-merge"
            merged = 1
        if file_ext == ".DL1ParDL2Geo.json":
            analysis_prog = "ctapipe-merge"
            merged = 2
        if file_ext == ".DL2GeoEneGam.json":
            analysis_prog = "ctapipe-apply-models"
            merged = 0

        MDdict_common = {'analysis_prog': analysis_prog, 'data_level': {'=': 2}, 'merged': {'=': merged}, 'sct': 'False', 'outputType': 'Data'}


        for particle in ["gamma-diffuse", "proton", "gamma", "electron"]:

            MDdict = {'MCCampaign': MCCampaign, 'site': site, 'array_layout': array_layout, 'particle': particle, \
                    'thetaP': {'=': thetaP}, 'phiP': {'=': phiP}, 'nsb' : {'=': nsb}, 'analysis_prog_version': analysis_prog_version}

            if particle == "gamma-diffuse":
                if file_ext == ".DL2GeoEneGam.json":
                    split_list = ["test"]
                else:
                    split_list = ["train_en", "train_cl", "test"]
            elif particle == "proton":
                if file_ext == ".DL2GeoEneGam.json":
                    split_list = ["test"]
                else:
                    split_list = ["train_cl", "test"]
            elif particle in ["gamma", "electron"]:
                split_list = ["test"]

            for split in split_list:
                fields = []
                MDdict["split"] = split

                for key, value in MDdict.items():
                    if key == "thetaP":
                        fields.append("zen0" + str(value["="]))
                    elif key == "phiP":
                        if value["="] == 180:
                            az = "000"
                        elif value["="] == 0:
                            az = "180"
                        fields.append("az" + az)
                    elif key == "split":
                        fields.append(str(value) + "_merged")
                    elif key == "nsb":
                        fields.append("nsb0" + str(value["="]) + "x")
                    elif isinstance(value, str):
                        fields.append(value.lower())
                    else:
                        fields.append(str(value))

                if particle in ["gamma", "electron"]:
                    MDdict.pop("split")

                MDdict.update(MDdict_common)
                json_string = json.dumps(MDdict)
                file_name = "_".join(fields[0:4]) + "_" + "".join(fields[4:7]) + "_" + "_".join(fields[7:9])
                f = open(file_name.capitalize() + file_ext, 'w')
                f.write(json_string.replace('"',"'") + '\n')
                f.close()


####################################################
if __name__ == "__main__":
    main()
