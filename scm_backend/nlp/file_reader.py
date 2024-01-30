import pandas as pd
import traceback
import configparser

from controls.models import Control
from constraints.models import Constraint, ConstraintAssociation

SECURITY_CONTROL_SPECIFICATION_PATH = "static/nist_security_controls.xlsx"

class FileReader():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')

        self.path = SECURITY_CONTROL_SPECIFICATION_PATH
        self.security_control_list = list()
    
    def read_nist_controls(self):
        print("--- Start Reading NIST Controls from Excel File ---")
        try:
            # read by default 1st sheet of an excel file
            security_controls_excel = pd.read_excel(self.path)

            print("  --> Read of excel file complete adding controls to DB")
            
            # print(security_controls_excel.loc[0])
            count = 0
            for index, row in security_controls_excel.iterrows():
                if count <= -1:
                    count += 1
                    continue

                cn = str(row["Control Identifier"])
                name = str(row["Control (or Control Enhancement) Name"])
                description = str(row["Control Text"]) + "\n" + str(row["Discussion"])
                
                name, parent_control_name = self.__detect_parent(name)
                
                if parent_control_name is not None:
                    found_parent = False
                    for security_control in self.security_control_list:
                        if security_control.name == parent_control_name:
                            found_parent = True
                            control = Control.objects.create(cn=cn, name=name, description=description, parent_control=security_control)
                            self.security_control_list.append(control)
                    if not found_parent:
                        control = Control.objects.create(cn=cn, name=name, description=description, parent_control=None)
                        self.security_control_list.append(control)
                else:
                    control = Control.objects.create(cn=cn, name=name, description=description, parent_control=None)
                    self.security_control_list.append(control)

                self.__set_impact(control, str(row["Security Control Baseline - Low"]), str(row["Security Control Baseline - Moderate"]), 
                    str(row["Security Control Baseline - High"]))

                count += 1

                if count >= int(self.config["Import"]["max_controls"]) and not int(self.config["Import"]["max_controls"]) <= 0:
                    break
            
            print("--- Import of controls completed ---")
            return "SUCCESS"
        except Exception:
            print(traceback.format_exc())
            return "FAIL"
    
    def __detect_parent(self, name):
        parent_control_name = None
        if "|" in name:
            parent_control_name = name.split("|")[0]
            parent_control_name = parent_control_name[0:len(parent_control_name) - 1]

            name  = name.split("|")[1]
            name  = name[1:len(name)]
        
        return name, parent_control_name
    
    def __set_impact(self, control_object, low_impcat_value, medium_impcat_value, high_impact_value, ):
        constraint = Constraint.objects.get(name="Impact")
        if low_impcat_value == "x": 
            ConstraintAssociation.objects.create(name="Impact_low_"+control_object.name,constraint=constraint,selected_value={"int_value": 1, "value": "low"},
                control=control_object)
        if medium_impcat_value == "x":
            ConstraintAssociation.objects.create(name="Impact_medium_"+control_object.name,constraint=constraint,selected_value={"int_value": 2, "value": "medium"},
                control=control_object)
        if high_impact_value == "x":
            ConstraintAssociation.objects.create(name="Impact_high_"+control_object.name,constraint=constraint,selected_value={"int_value": 3, "value": "high"},
                control=control_object)
