import re
import json


class JsonChecker:
    def __init__(self,file_name:str):
        with open(file_name) as file:
            # KeyName:IsRequired
            self.RolePolicyKeys = {"PolicyName": True, "PolicyDocument": True}
            # KeyName:[Checkers, Values]
            self.RolePolicyKeysChecks = {
                "PolicyName": [[self.type_check,str],[self.regex_check,"[\w+=,.@-]+"]],
                "PolicyDocument": [[self.type_check,dict]]
            }
            # KeyName:IsRequired
            self.PolicyDocumentKeys = {"Version": True, "Statement": True}
            # KeyName:[Checkers, Values]
            self.PolicyDocumentKeysChecks = {
                "Version": [[self.type_check, str], [self.value_in_check, ["2012-10-17", "2008-10-17"]]],
                "Statement": [[self.type_check, list]]
            }
            # KeyName:IsRequired
            self.StatementKeys = {"Sid": False, "Effect": True, "Action": True, "Resource": False, "Condition": False}
            # KeyName:[Checkers, Values]
            self.StatementKeysChecks = {
                "Sid": [[self.type_check, str]],
                "Effect": [[self.type_check, str], [self.value_in_check, ["Allow", "Deny"]]],
                "Action": [[self.type_check, list]],
                "Resource": [[self.type_check, list]],
                "Condition": [[self.type_check, dict]],
            }

            self.json_dict = json.loads(file.read())

    def check(self) -> bool:
        # Checking Role Policy
        # Checking amount of keys
        if len(self.json_dict.keys()) != len(self.RolePolicyKeys.keys()): return False
        for key in self.RolePolicyKeys.keys():
            # Checking key name and if key is required
            if key not in self.json_dict.keys():
                if self.RolePolicyKeys[key]: return False

        # Checking Role Policy -> Policy Name
        name = self.json_dict["PolicyName"]
        for func,value  in self.RolePolicyKeysChecks["PolicyName"]:
            if not func(value, name): return False

        # Checking Role Policy -> Policy Document
        policy = self.json_dict["PolicyDocument"]

        # Checking amount of keys
        if len(policy.keys()) != len(self.PolicyDocumentKeys.keys()): return False
        for key in self.PolicyDocumentKeys.keys():
            # Checking key name and if key is required
            if key not in policy.keys():
                if not self.PolicyDocumentKeys[key]: return False

        # Role Policy -> Policy Document -> Version
        for func,value in self.PolicyDocumentKeysChecks["Version"]:
            if not func(value,policy["Version"]): return False

        # Role Policy -> Policy Document -> Statement
        for func, value in self.PolicyDocumentKeysChecks["Statement"]:
            if not func(value, policy["Statement"]): return False

        # Role Policy -> Policy Document -> Statement
        for s in policy["Statement"]:
            if not self.type_check(dict,s): return False
            # Checking amount of keys
            if len(s.keys()) > len(self.StatementKeys.keys()): return False
            for key in self.StatementKeys.keys():
                # Checking key name and if key is required
                if key not in s.keys():
                    if self.StatementKeys[key]: return False
                else:
                    for func,value in self.StatementKeysChecks[key]:
                        if not func(value,s[key]): return False


        return True


    def type_check(self,t,check) -> bool:
        if t == type(check): return True
        return False

    def regex_check(self,pattern:str, text:str) -> bool:
        if re.fullmatch(pattern,text) is None: return False
        return True

    def value_in_check(self,pattern:list, value) -> bool:
        if value in pattern: return True
        return False