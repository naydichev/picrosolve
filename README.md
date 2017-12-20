# picrosolve
a simple picross solver

# Install
To install just clone and `python setup.py install`

# Use

Create a puzzle file that looks like the following:

```sh
cat sample_puzzle.txt
[rows]
1 1
3
1 1

[cols]
3
1
3
```

Execute with the following

```sh
picrosolve solve sample_puzzle.txt
 ==== Solved ====
----------------
|    | 3| 1| 3|
----------------
| 1 1|⬛|❌|⬛|
|   3|⬛|⬛|⬛|
| 1 1|⬛|❌|⬛|
----------------
There are 6/6 solved sequences
```
