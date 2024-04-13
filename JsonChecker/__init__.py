import json
import re


class JsonChecker:
    def __init__(self,file_name:str):
        if file_name[-5:] != ".json": raise TypeError(f"{file_name} is not a JSON file")
        with open(file_name) as file:
            # KeyName:IsRequired
            self.RolePolicyKeys = {"PolicyName": True, "PolicyDocument": True}
            # KeyName:[Checkers, Values]
            self.RolePolicyKeysChecks = {
                "PolicyName": [[type_check,str],[regex_check,"[\\w+=,.@-]+"]],
                "PolicyDocument": [[type_check,dict]]
            }
            # KeyName:IsRequired
            self.PolicyDocumentKeys = {"Version": True, "Statement": True}
            # KeyName:[Checkers, Values]
            self.PolicyDocumentKeysChecks = {
                "Version": [[type_check, str], [value_in_check, ["2012-10-17", "2008-10-17"]]],
                "Statement": [[type_check, list]]
            }
            # KeyName:IsRequired
            self.StatementKeys = {"Sid": False, "Effect": True, "Principal":False, "Action": True, "Resource": False, "Condition": False}
            # KeyName:[Checkers, Values]
            self.StatementKeysChecks = {
                "Sid": [[type_check, str]],
                "Effect": [[type_check, str], [value_in_check, ["Allow", "Deny"]]],
                "Principal": [[type_check, dict]],
                "Action": [[check_str_or_lists, list]],
                "Resource": [[check_str_or_lists,None]],
                "Condition": [[type_check, dict]],
            }

            self.json_dict = json.loads(file.read())

    def get_required_statement_keys(self) -> list[str]:
        result = list()
        for key in self.StatementKeys.keys():
            if self.StatementKeys[key]: result.append(key)
        return result

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
            if not type_check(dict,s): return False
            # Checking amount of keys
            if len(s.keys()) < len(self.get_required_statement_keys()) or len(s.keys()) > len(self.StatementKeys.keys()):
                return False
            for key in self.StatementKeys.keys():
                # Checking key name and if key is required
                if key not in s.keys():
                    if self.StatementKeys[key]: return False
                else:
                    for func,value in self.StatementKeysChecks[key]:
                        if not func(value,s[key]): return False


        return True


def type_check(t,check) -> bool:
    if t == type(check): return True
    return False

def regex_check(pattern:str, text:str) -> bool:
    if re.fullmatch(pattern,text) is None: return False
    return True

def value_in_check(pattern:list, value) -> bool:
    if value in pattern: return True
    return False

def check_str_or_lists(placeholder,obj) -> bool:
    if type(obj) in [str,list]: return True
    return False