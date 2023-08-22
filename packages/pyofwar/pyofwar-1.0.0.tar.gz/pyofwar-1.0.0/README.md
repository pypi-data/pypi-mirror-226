# pyofwar
Python library for Sun Tzu's most popular quotes

Most of the quotes were taken from the website [quotefancy](https://quotefancy.com/sun-tzu-quotes)

### Selected quotes
```python
from pyofwar import pow

print("Sun Tzu once said...")
print(pow.quote(1, True))
```
outputs
```
Sun Tzu once said...
"Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt."
```
### Random quotes

```python
from pyofwar import pow

print("Sun Tzu once said...")
print(pow.quote_random(2, False))
```
outputs
```
Sun Tzu once said...
Know thy self, know thy enemy.
If their forces are substantial, prepare for them; if their forces are strong, avoid them.
```

And if you want to limit the range of randomness

```python
from pyofwar import pow

print("Sun Tzu once said...")
print(pow.quote_random(3, True, 0, 0))
```

outputs
```
Sun Tzu once said...
"Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt."
"Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt."
"Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt."
```
