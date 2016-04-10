# PyLisp
A Lisp written in Python. It is designed to have access to variables created in the Python script from which it is run.

It currently has a major problem, namely how to extract things with the dot syntax, which is kind of a big deal in Python.

It also has a lot of minor problems, like:
* Comments are not yet implemented
* The lexical analyzer is very slow
* Only single quoted strings are allowed
* It is a toy and is not tested
* I'm not done building the default environment

Some examples:

```
pl> (define a 3)
R: 3
pl> (print (+ a 3) )
6
NR~
```

What is happening here is I am setting a variable (which is now accessible in Python, too, through the env table) called a. I then print (using the standard Python print function) the result of a + 3. Of course, print returns nothing, so the interpreter informs me of this with `NR~`.

```
pl> (define a 1)
R: 1
pl> (if (= a 1) (print 'Yes') (print 'No'))
Yes
NR~
```
Here, I'm using an if statement. It is a special form. I plan to implement it as a Python function and put it in the symbol table eventually.

