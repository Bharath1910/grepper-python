# Grepper Python Client
The Grepper Python library provides convenient access to the Grepper API from applications written in the Python language.

## Requirements
Python 3.7 and later.

## PIP
```
pip install grepper-python
```

## Manual Installation
```bash
git clone https://github.com/CantCode023/grepper-python
cd grepper-python
python setup.py install
```

## Getting Started
Simple usage:
```py
grepper = Grepper("your-grepper-api-key")
answers = grepper.search("query")
print(answers)
```

python client library

## Search function

This function searches all answers based on a query.

## Arguements required

1. ``query (str, optional)``: Query to search through answer titles.
2. ``similarity (Optional[int], optional)``: How similar the query has to be to the answer title. 1-100 where 1 is really loose matching and 100 is really strict/tight match. Defaults to 60.

## Returned value

GrepperAnswer

## Example of the function by using in a code:

```py
import grepper_python

grepper = grepper_python.Grepper("YOUR API")

data = grepper.search("cat videos")
for i in data:
    print(i)
```

## Output

```py

GrepperAnswer(id=667265, content='{"tags":[{"tag":"p","content":"Get back to work"}]}', 

author_name='Smyth Family', 

author_profile_url='https://www.grepper.com/profile/smyth-family',

 title='cat videos', 

 upvotes=4, 

 downvotes=0)

```