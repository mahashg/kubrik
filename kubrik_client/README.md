#Setup

1. pip install -r requirements.txt


# Execution

First do setup by running registration
```python kub.py register -email mahesh.msg.24@gmail.com```

Then add directory(ies) to be backedup
```python kub.py snapshot -directory /Users/Mahesh.Gupta/Downloads```


To restore a directory
```python kub.py restore -directory /Users/Mahesh.Gupta/Downloads```
