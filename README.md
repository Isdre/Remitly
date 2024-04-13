# Remitly Recruitment Task
made by Gilbert Guszcza

## Task description

[Full task content](Home%20Exercise%202024.docx.pdf)

## How to run
You can use the command
```
python check_json.py [file]
```
where the path to the file should be entered in the [file] field.

You can also import the JsonChecker module
```python
import JsonChecker
```

## Execution
I created the project in PyCharm 2023.2, I wrote the code in Python 3.10.11.

File checking is performed by an object of the JsonChecker class, which in its constructor takes the path to a JSON file in the AWS::IAM::Role Policy format.
To return whether the file is valid, call the check() function.

```python
import d
json import


classJsonChecker:
     def __init__(self,file_name:str):
     #
    
     def check(self) -> bool:
     #
```


[JsonChecker.py](JsonChecker/__init__.py)

### Tests
Unit tests of the JsonChecker class and check method

[test_check.py](tests/test_check.py)
