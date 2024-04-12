# Zadanie rekrutacyjne Remitly
wykonane przez Gilbert Guszcza

## Opis zadania

[Pełna treść zadania](Home%20Exercise%202024.docx.pdf)

## Uruchomianie
Można skorzystać z komendy
```
python check_json.py [file]
```
gdzie w pole [file] należy wstawić ścieżkę do pliku.

Można również zaimportować moduł JsonChecker
```python
import JsonChecker
```

## Wykonanie
Zrobiłem projekt w PyCharm 2023.2, kod pisałem w Python 3.10.11.

Sprawdzanie pliku wykonuje obiekt klasy JsonChecker, który w konstruktorze przyjmuje ścieżkę do pliku.
Aby zwrócić czy plik jest w formacie AWS::IAM::Role
Policy, nalezy wywołać funkcje check().

```python
import re
import json


class JsonChecker:
    def __init__(self,file_name:str):
    #
    
    def check(self) -> bool:
    #
```


[JsonChecker.py](JsonChecker/__init__.py)

### Testy
Testy jednostowe klasy JsonChecker

[]()