# Python Conventions & Guidelines

[[_TOC_]]

What follows is a list of dos and don'ts on how to write readable code in Python.
Many of them are applicable to other programming languages.

I have collected and formulated these rules over 12 years in software - I do not claim originality - 
I've learned much from others even as I have passed this knowledge on.

Enjoy!

## Regarding PEP8

Generally, we use PEP8 as our style guide, *this does not mean we worship it*.
We will have more and more exceptions to PEP8 in time, and they will be detailed here.

Exceptions to PEP8:

* PEP8 line width: we allow with 180 characters per line, instead of the default 79 characters.
* If PEP8 wants to format some code one way, but you think it's nicer another way - *you* are the boss, not PEP8.
* PEP8 demands to use `staticmethod` whenever a method does not use `self` - we reject this. A static method 
  communicates that the method belongs under the class as a sort of namespace - which is a semantic point, not a technical one.

So the general rule is - PEP8 is a baseline, however, **PEP8 works for us, we don't work for PEP8.**

If adhering do it makes code ugly - we don't adhere to it.

## Never Use Mutable Values As Default Values for Function Arguments

This is a common mistake for the uninitiated.

```python
#bad! this is a bug
def add_to(element, to={}):
    to['a'] = element
    return to
```

What happens here is that an empty `dict` is created when the `def` is executed, i.e. *once*,
and this `dict` is now the default value - even if it mutates and becomes non-empty.

In short, **NEVER DO THIS, THE BUGS WILL DRIVE YOU NUTS**

The proper way to have mutable default values is:

```python
#good:)
def add_to(element, to=None):
    if to is None:
        to['a'] = element
        return to
```

## Never Say Never

Every rule here has its exceptions, there is no one way 
to write code for every occasion. 

## Don't Employ Default Values Unless You Have a Really Good Reason To

This is a special form of [preparing for the future](#preparing_for_the_future), see the discussion over there.

## No "helpers", "utilities" or "utils" module

Generic "helper" modules are hard to understand, since
"help" or "utility" is a very abstract concept.

They also tend to become garbage modules with lots of unrelated code - every time 
someone doesn't know where to put something - into the helper module it goes! 

Instead, write a module with a meaningful name, even
if it only has one function inside:

```python
# bad!
from . import utils

...
encoded = utils.encode_message(message) # utils probably has lots and lots of other stuff unrelated to encoding

# good!

from . import encoder
...
encoded = encoder.encode(message)
```

## (Almost) Never Write Comments <a name="never_write_comments"></a>

When you want to write a comment,
it means that *you* think that the code is not very readable, hence the need 
to explain it.


Comments are bad because there is no enforcing their correctness.
As a result, they degenerate over time. After a few sprints,
the comment is probably irrelevant and confusing, 
since the code has changed, but the comment remains.

So, what to do?  **DON'T write the comment, take the time, and put in effort to make the code more readable**

Here are some basic techniques.

### Use constants with meaningful names
```python
#bad!
time.sleep(60) # allow server to reboot

#good :)
ALLOW_SERVER_TO_REBOOT = 60
time.sleep(ALLOW_SERVER_TO_REBOOT)
```

Such explanatory variables are written in `ALL_CAPS` because they are *shouting*
at the reader

```python
# HEY! READER!!! PAY ATTENTION!!! I WROTE THIS JUST FOR YOU!!!
ALLOW_SERVER_TO_REBOOT = 60
```

<a name="mongo_does_not">Another example of this</a> may be to clarify some unclear libraries we use.
This is a real life example: for some reason, using `ordered=False` in a MongoDB `insert_many` 
command makes MongoDB not raise exceptions if some records cannot be inserted. We wanted 
to use this, but this is a very obscure detail, so:
```python
#bad!
await Client.db.manual_access.insert_many(records, ordered=False) # wtf? why is ordered=False???

#good :)
PREVENT_MONGO_FROM_RAISING_ON_INSERT_ERRORS = {'ordered': False}
await Client.db.manual_access.insert_many(records, **PREVENT_MONGO_FROM_RAISING_ON_INSERT_ERRORS) # ahh, that's why
```

### Extract code to function/class with explanatory name

```python
#bad!
class ParseRecords:
    ...
    def go(self):
        count = 0
        for record in self.__records:
            # save record type 
            record_type = great_project.record_types.RecordType(record.name, record.id)
            record_type_id = await record_type.write()

            if record_type_id is None:
                continue
            count += 1
        return count

#good :)
class ParseRecords:
    ...
    def go(self):
        count = 0
        for record in self.__records:
            if not self.__save_record_type(record):
                continue
            count += 1
        return count

    def _save_record_type(self, record):
        record_type = great_project.record_types.RecordType(record.name, record.id)
        record_type_id = await record_type.write()
        return record_type_id is not None
```

### Use a Log Instead of a Comment

We return to the `time.sleep` example from before:

```python
#bad!
time.sleep(60) # allow server to reboot

#good :)
def stall(duration, reason):
    logger.info(f'stalling for {duration} seconds to: {reason}')
    time.sleep(duration)

stall(60, 'allow server to reboot')
```

## Private and Public Entities

### Calling Base Class `__init__` Functions

We do this like so:

```python
class Base:
    def __init__(self, x):
        ...

class Derived(Base):
    def __init__(self, x, y):
        Base.__init__(self, x)
        self.__y = y
        ...
```

If the Derived class does not need an `__init__`,
then don't write one. Python will use the base class's init in 
this case:

```python
class Base:
    def __init__(self, x):
        ...

class Derived(Base):
    def some_method(self):
        ...

d = Derived(x=3) # no problem, python calls Base's __init__
```

## Naming Conventions

* class names are in `CamelCase`
* module name, local variables, and functions are in `lower_snake_case`
* constants are in `ALL_CAPS`
* explanatory variables, e.g. `ALLOW_SERVER_TO_REBOOT` above, are in `ALL_CAPS`. 
* **one file per public class**: a class named `EatingWare` will be inside a file named `eating_ware.py`.
  
  note the "public" part, the `eating_ware.py` file may include a private, `__Utensil` class, if
  it's not too large.

Here's a summary:

```python
# this is the_best.py

class TheBest: # class in CamelCase, has same name as module
    KNOWN_THINGS = 'alpha', 'beta', 'gamma' # constant in ALL_CAPS

    def __init__(self, what):
        self.__what = what

    def a_public_method(self): # snake_case
        ...
```

## No Shorthand!

Our code should aspire to remind us of the English language. 
A common bad practice is to use shorthand instead of complete words, e.g.

* `conn` instead of `connection`
* `dest` instance of `destination`
* `err` instead of `error`
* `fname` instead of `filename`
* `inst` instead of `instance`
* `pckt` instead of `packet`
* `src` instead of `source`

I could go on forever. These shorthands obscure meaning and 
save us nothing, not even typing, since the IDE has autocomplete.
   
Exceptions to this rule are things like `HTML`. We write `HTML` not `hyper text markup language`.

```python
# bad!

conn, _ = srvr.accept()
s = None
while s != '':
    s = conn.recv(1024)
    conn.send('echoing back: ' + s)
    

# good :)
connection, _ = server.accept()
input = None
while input != '':
    input = connection.recv(1024) # "recv" is bad, it should be "receive". But that's and external API, so what can we do...
    connection.send(f'echoing back: {input}')
```


## Do Not Name Variables After Their Type

Sometimes you may see code like this:
```python
file_list = files_from_directory()
for file in file_list:
    print(f'yay, I found a file: {file}')
```

The problem here is that in most cases, nobody cares if the thing I'm iterating
on is a list, a set, dictionary values, whatever, so why call it `file_list`? the `_list` here 
tells us something that we don't care about - hence, it's a waste of our brain power to process it.
Our brain power is a scarce resource - let's not waste it.

This is much better:

```python
directory_files = files_from_directory()
for file in directory_files:
    print(f'yay, I found a file: {file}')
```

It's also closer to English, which is what we always strive for.

If, for some reason, it's really important to specify the 
type, use an annotation:

```python
files: list = files_from_directory()
...
```

## Namespaces and `import`s

The Python language has the feature that the directory structure of our Python files
is also the namespace structure we have in our Python program.

Namespaces are important. Therefore, we observe the following rule:

** IMPORT MODULES, NOT NAMES **

This means we almost never do this:

```python
from pathlib import Path

...

home_directory = Path.home()
```

Instead, we do this:

```python
import pathlib
...
home_directory = pathlib.Path.home()
```

Another exmaple:
```python
#GOOD!
import os
...
kernel_version = os.uname() # explicitly states that uname comes from os
```

Don't do this:
```python
#BAD!
from os import uname

kernel_version = uname() # can't tell where uname comes from without help from some IDE
```

However, you can use `from . import thing` if `thing` belongs in the same namespace, e.g. your files are structures like so:


    .
    └── animals
        ├── __init__.py
        ├── dogs/
            ├── __init__.py
            ├── dog.py
            ├── golden_retriever.py
            └── labrador.py          
        ├── great_cats/

and say we're looking at `labrador.py` file:

```python
#labrador.py

#bad!
import animals.dogs.dog
class Labrador(animals.dogs.dog.Dog)
    ...

#good :)
from . import dog
class Labrador(dog.Dog):
    ...

```

this has the following advantages:
* it's still explicit that `dog` and `labrador` belongs in the `animals.dogs` namespace
* we still don't import actual names from inside modules, only *modules* themselves.

### Namespace Inflation

Given this tree:

    parsers
    ├─ textual_parsers
    │   ├── perl_textual_parser.py
    ├─ binary_parsers

The fully qualified import statement for the `perl_textual_parser` module is:
```python
import parsers.textual_parsers.perl_textual_parser
```

Note that the word "textual" appears twice, and the word "parser" appears 3 times.
This is called _namespace inflation_.

Take for example the name `PerlTextualParser`: we already know it's a
textual parser, since it belongs to the `textual_parsers` namespace, so we
shouldn't repeat that information again. In fact, `textual_parsers` should be
called `textual` - since we already know we're dealing with parsers, because we're in the
`parsers` namespace.

The fully qualified import should be:
```python
import parsers.textual.perl # DRY - don't repeat yourself
...
``` 

At least that's how you should import this module from outside the `parsers` namespace.
From *inside* the `parsers` namespace, you should write

```python
# this is parsers/textual/perl.py
from . import parser # imports parsers/textual/parser.py

class Perl(parser.Parser):
    ...
```

This explicitly imports from within our larger namespace context, and when we
reference something we don't have to mention `textual` or `parser` all the time.

Note that the class inside the `perl.py` module is called `Perl`.


## Using Context

The preceding discussion is an example of a general rule:

**We use context to avoid over-verbose code**

```python
import shutil # file utilities from the standard python library

#bad!
class RenameFiles:
    def rename_files(file_list): # it can be any iterable, who cares if it's a list or a set?
        for filename in file_list:
            new_filename = f'{filename}.new' # if there's a new_filename, then filename should probably be called old_filename
            shutil.move(filename, new_filename)

rename_files = RenameFiles()
rename_files.rename_files(my_files) # my eyes hurt from all these repeated "rename" and "files" 

#good :)
class RenameFiles:
    def go(files):                          # RenameFiles tells the story, so we can simply use "go"
        for old_name in files:
            new_name = f'{old_name}.new'    # "new_name" and not "new_filename", of course it's a file name, no need to repeat that
            shutil.move(old_name, new_name)

renamer = RenameFiles() # only one line from RenameFiles() to the user of renamer, so 
renamer.go(my_files)    # we can use a shorter name "renamer" instead of "rename_files" or "file_renamer"
```

### Using Context: Variable Names

Using context properly means that a global variable's name will
probably be quite long - since it is in global context, its name
has to carry a lot of information.

Lucky for us, Python doesn't really have a truly global context, so 
the worst case scenario is module context. Still, module level 
or package-level names may be longer.

A local variable inside a function can probably have a short name,
since the surrounding context conveys much of the information
regarding the meaning of this variable.

## No Magic Numbers

Magic numbers must always be somehow named or explained,
e.g.

```python
# bad
import http

raise HTTPError(400)

# good
raise HTTPError(http.HTTPStatus.BAD_REQUEST)
```

## Avoid Nesting Important Flows - Prefer to Nest Unimportant Flows

Here's code that processes files. I demonstrate here
good and bad ways to defend against file not existing, 
and defending against processing comments.

```python
#bad! don't do this!
for file in files:
    if file.exists():
        for line in file.readlines():
            if not line.startswith('#'):
                # this is the code we care about
                # but it's nested *four* indents in!
                do_something_1(line)                         
                do_something_2(line)


#good :) do this:
for file in files:
    if not file.exists():
        continue
    for line in file.readlines():
        process(line)

def process(line):
    if line.startswith('#'):
        return
    
    do_something_1(line) # this is the code we care about
    do_something_2(line) # this time, it's only minimally nested
```

## Short Files, Short Functions

Long files almost certainly contain code that does too many things,
and should be broken into smaller files with smaller responsibilities.

A file should have one (public) class, with the same name as the file.

* Most files should be at most 70-80 lines long. 
* A 100 line file is probably too long.
* A 150 line file is surely too long. 

Functions should also be short and sweet.


* Functions should usually be at most 7 lines of code.
* A 10 line function is probably too long.
* A 15 line function is surely too long.


*There is a known exception to this rule*: test files. Tests can be long files, with up to ~500 lines,
since they cover many different cases, and they tend to be more verbose. If a test file passes the 500 
line mark - it's suspect, and probably should be broken to smaller files.

Even one-line functions may be useful, if they enhance meaning:

```python
class ProcessLines:
    def go(self, lines):
        for line in lines:
            if self.__comment(line):
                continue
            ...

    def __comment(self, line):
        return line.startswith('#')
```

Sometimes a one liner is clear enough such that it doesn't need a function describing it.

## Type Annotations

Type annotations are useful for enhancing readability and also for linters.

We use type annotations when they help us, and don't use them when they 
only introduce clutter.

Here's a good example of when to use them:
```python
# this is old school python
def exists(root, value):
    # root of what? what kind of value?
    ...

# this is annotated, easier to understand
def exists(root: TreeElement, value: str) -> bool
    # ahhhh, it's a tree that holds strings
    # and we return True or False
    ...

```

An example of clutter is something like

```python
def login(username: str) -> Union[None, String]
    # This Union thing is unreadable and annoying
    # also, when is username *not* a string?
    ...
```

## Module-Level Constants

Module level constants are useful in two cases:

* if they are public, and used in many places, so that if we need to change their value, we change only the definition.
* if they constitute some config value that should be immeidately obvious

However, people tend to use them when this is not the case.

Here's an example:

```python
#bad!
AWS = 'aws'
AZURE = 'azure'

# then somewhere down the same file...
...
def type_of(cloud_object: str):
    if AWS in cloud_object:
        return AWS
    elif AZURE in cloud_object:
        return AZURE
```

Two comments here:

1. The constants AWS and AZURE essentialy replace the immutable strings 'ami'
   and 'azure' with immutable names AWS and AZURE. This accomplishes nothing.
1. They are not used outside this module
1. They are only used in `type_of()`, not in any other place in the module

In this case a better choice would be

```python
#good :)
# no constants defined, use explicit strings
def type_of(cloud_object: str):
    if 'AWS' in cloud_object:
        return 'AWS'
    elif 'AZURE' in image:
        return 'AZURE'
```

A similar abuse happens in tests:

```python
#bad!
def test_something():
    FILE_PATH = 'file_path'
    output = parser.parse(FILE_PATH)
    assert output == 'whatever makes sense here'
```

There's no utility to the constants here, much better to use explicit values
(in general, a good practice for tests):

```python
#good :)
def test_something():
    output = parser.parse('file_path')
    assert output == 'whatever makes sense here'
    # short and sweet
```

## Python `property` Setter Abuse

First thing's first - *not all properties need a setter*. 
You can have read-only properties, there's no rule that you must write a setter.

Sometimes, however, we want to have a property with a setter, e.g.
```python
class Klass:
    ...
    @property # this is the getter
    def name(self):
        return self.__name

    @name.setter # this is a good, simple setter
    def name(self, value):
        self.__name = value
```

Setters make the following possible:
```python
instance = Klass()
instance.name = 'Joe' # invokes setter function with 'Joe'
```

Since setting a property looks exactly like a simple assignment,
*we do not want nontrivial code in a setter*.

Example of what *not* to do:
```python
#bad!
class BadApp:
    ...
    @property
    def configuration(self):
        return self.__configuration

    @configuration.setter
    def configuration(self, yaml_file): # this is a bad, complex setter
        self.__parse_yaml(yaml_file)
        self.__compensate_for_missing_values(yaml_file)
        self.__backup_config_to_remote_server()
        ...
        
# someplace else in the code
app = BadApp()
app.configuration = 'config.yaml' # looks like assignment, but lots of action happens here
```

## Using Exceptions

* We do not use exceptions for flow control, that's what `if`, `while` and
  `for` do. If some condition is expected (e.g. some file might not exist) -
  either leave the code to try and find it and raise on its own, or test for
  the condition beforehand and handle it (unless it's racy - that's something else).
* We don't raise exception classes that belong to standard (or third party)
  namespaces, e.g. we don't write `raise OSError` from our code - that exception class
  belongs to Python's `os` module. 
  raising `Exception` objects is also an exception (ha ha) to this rule, we do raise those. This allows the following rule:
* We do not subclass `Exception`, unless we use our subclass, e.g.:
    * we explicitly filter for it in an `except` clause
    * we subclass those exceptions that are later meant to be passed in a standardised format to another module (e.g. RPC call)
    * meant to add meaning to some other error (e.g. FileNotFoundError means nothing to our caller, wrap it in ConfigurationNotFoundError)

If in doubt - start by raising `Exception('a message')` and only define
your own exception class if you see you actually need it.

## Conditions Should Be explicitly True or False

Python considers many values to be `falsey`, e.g.
```python
#bad!
people = list_of_persons() # let's say this returns []
if not people: 
     # [] is falsey, so this code runs
     print("I'm all alone")
```

The problem with this is that the reader has to remember this "empty is falsey" stuff,
and moreover, the phrase "not people" is not very English like.

Much better to be explicit:
```python
#good :)
people = list_of_persons() # assume this returns []
if len(people) == 0: # no doubts here
    print("I'm all alone")

# another possibility
if people == []:
    ...

```

Remember the [Zen of Python](https://en.wikipedia.org/wiki/Zen_of_Python): explicit is better than implicit.

However, don't do this:
```python
path = pathlib.Path('/path/to/myfile')
if path.is_dir() == True:
    # do directory stuff
    ...
```

These sorts of "query" functions, such as `is_dir` already imply Boolean values.
This is true even if the functions name does not contain "is", e.g. (in fact, there is a considerable body of opinion that believes that "is is evil", and even more importantly - we agree!)
```python
# bad! overly explicit, non-English code
if person.underage() == True:
    raise NoAlcoholForYouError()

# bad! this is truly evil
if person.is_underage() == True:
    raise NoAlcoholForYouError()

# good :) English like code
if person.is_underage():
    raise NoAlcoholForYouError()

# also good :) 
if person.underage():
    raise NoAlcoholForYouError()
```

## The Query-Command Principle

Try as much as possible to observe the "Query-Command Principle".
This means that you either write functions that *return* values, but don't
change *state* and don't perform I/O (performing I/O is changing the state of
the world, and of internal structures such as streams),
or else you write functions that *change state*, or perform I/O, but do not calculate anything
(you may return some value indicating result of I/O, but `None` is perfectly acceptable in many cases).

```python
class Entity:
    # this is a Query
    def signature(self):
        a = self.__calculation1()  # __calculation1 does not change state
        b = self.__calculation2(a) # __calculation2 does not change state
        return a + b

    # this is a Command
    def save_to_database(self):
        self.__database.entities.create({'id': self.__id, ** self.__properties})
```

Essentially the Query-Command Principle separates _functions_ and _procedures_.
The _functions_ are the ones that don't change state, and the _procedures_ are 
the ones that do change state.

By the way, if a function does not change state, and also *always returns the same result for the same arguments*,
it is called a "pure" function. You might want to look into that.

Separating state changes from calculations makes code much easier to debug, since
you can insert logs between a query and a state-changing operation with confidence
that nothing happened due to the query.

## `Get` is Evil

As in the `NoAlcoholForYouError` example, the use of `get` breaks
the English language.

```python
#bad! 
for birthday in birthdays:
    month = birthday.get_month()  # this get breaks my teeth
    histogram[month] += 1

#good :)
for birthday in birthdays:
    month = birthday.month()  # ah, much more English-like
    histogram[month] += 1
```

Note that the version with `get` sounds unnatural.

## Avoid Lengthy `if` Conditions

Human brains are poor logic machines, that's why we use computers. It's 
hard to follow something like

```python
#bad!
if login.password is not None and if login.username is not None:
   do_something()
```

do this:
```python
#good :)
if login.password is not None:
    if login.username is not None:
        do_something()
```

This is a good solution for `and` conjugations.
Other complex conditions should have a descriptive variable
or function to describe them:


```python
#bad!
if login.password is not None or if login.username is not None:
    logger.info(f'some credentials are available!')

#good :)
credentials_exist = (login.password, login.username) != (None, None)
if credentials_exist:
    logger.info(f'some credentials are available!')

#better:
def credentials_exist(login):
    return (login.password, login.username) != (None, None)

if credentials_exist(login):
    logger.info(f'some credentials are available!')
```

# Further Good Practices For Readable Code

## Do Not Write Code That "Prepares for the Future" <a name="preparing_for_the_future"></a>

A common example is using default values to make our code more flexible, e.g.

```python
#bad!
def read_all(socket, chunk_size=1024): 
    # in the future, I will be able to easily change chunk_size! I'm so smart!
    read = socket.recv(chunk_size)
    bytes_ = b''
    while read != '':
        bytes_ += read
        read = socket.recv(chunk_size)

    return bytes_

def actual_usage_of_read_all():
    input_ = read_all(socket) # chunk_size never actually used

```

What's so terrible, you ask? 

* The Only Reason for Bugs - Is Code.
* Code that does not exist, does not contain bugs.

Therefore:

* Code that is never used, should not exist

Moreover, this is usually contagious, i.e. in real life the result of `chunk_size`'s default value in `read_all`
is that `actual_usage_of_read_all` will also have the same, often unused, default value.

```python
# from bad to worse!
def actual_usage_of_read_all(chunk_size=1024):
    # since I was so smart before, I want a default value here too,
    # so I can keep everything flexible!
    input_ = read_all(socket, chunk_size) # chunk_size never actually used
```

Now the disease has spread! In fact, what this means, is that if one is to have
a default value at all - it should only be on the outermost layer.

But again, it's better not to have them unless you really know that you need them:


```python
#good :)
def read_all(socket):
    CHUNK_SIZE = 1024 # easy to change, clear to read
    # moreover we can add the previous default parameter implementation
    # *if and when* we *actually* need it
    read = socket.recv(CHUNK_SIZE)
    bytes_ = b''
    while read != '':
        bytes_ += read
        read = socket.recv(CHUNK_SIZE)

    return bytes_
```

Always remember this important fact:

**NO ONE CAN PREDICT THE FUTURE**

**NO ONE CAN PREDICT THE FUTURE**

**NO ONE CAN PREDICT THE FUTURE**

Anticipating the future is something we should all be doing - at planning meetings. Not when actually coding.

## Use Benign Values for Failures Instead of None

Many times, you see stuff like this:
```python
people = get_people_from_database()
if people is not None:
    for person in people:
        say_hi(person)
```

The only reason we need the `if people is not None` clause, is because
the `get_people_from_database()` function has a similar clause:
```python
def get_people_from_database():
    ...
    if not found:
        return None
    
    return list_of_people
```

It would be much better to return a *benign value*, a value that has no bad
effect on the system, e.g.:

```python
def get_people_from_database():
    if not found:
        return []
    ...

#then:
for person in get_people_from_database(): # empty list? nothing bad happens
    say_hi(person)
```

## No Private `staticmethod`s Please
A `staticmethod` is essentially an ordinary function, but it is defined under a class:
```python
class SomeClass:
    @staticmethod
    def list_options():
        ...
```

Note that the static method does not have a reference to `self`.
Essentially, we're using `SomeClass` as a namespace:
```python
SomeClass.list_options()
```

This pattern is good for, e.g., alternative constructors (factory functions).

First sign of abusing `staticmethod` is that your static method is *private*.

Example: sometimes we just need a helper function in our class, that does not depend on `self`,
but is actually used only in the context of an object (a `self`), e.g.

```python
class Algorithm:
    def calculate(self):
        ...
        for point in self.__points:
            if self.__outside(point):
                outside_count += 1
            ...

    def __outside(self, point): # note, self is not really used
        return point.x < 1000 or point.y > 9000 # some nontrivial condition that needs a name, i.e. "_outside"
```

Some IDEs say it's wrong to have the `__outside` function not be static, since `self` is not used.
We disagree - this is perfectly fine, and if you use `staticmethod`, you should have a better reason to.

## Force Caller to Use Kwargs

"Kwargs" is shorthand for "keyword arguments", e.g. `force` in 

    remove(filename, force=True) # the force= pattern makes it a kwarg

In Python 3, we can mandate the caller to use kwargs:

```python

# use of kwargs optional, 
# caller can use remove('file', True)
# or remove('file', force=True)
def remove(filename, force):
    ...

# use of kwargs mandated
# caller can only use remove('file', force=True)
def remove(filename, *, force):
    ...

```

This can make some code more readable when functions are called,
e.g. the `force` parameter we just discussed. Also,
compare

    # less readable
    once_every(10) # 10 what?

with 
    
    # more readable
    once_every(seconds=10) # ah, now I get it


## Use Generators and Iterators

In Python, a text file is an iterator for it's lines.
Especially if it's a large file, don't to this:
```python
for line in file.readlines():
    print(line)
```

do this:
```python
with open('some_file') as file:
    for line in file:
        print(line.strip()) # must use strip to lose the '\n' in the end, alas
```
