# LIGHTWEIGHT ENUMS, RUST-STYLED! (LERS)

This module serves the purpose of doing exactly what the name implies:
providing a lightweight enum with little but base functionality, all whilst
attempting to replicate Rust enums' style, syntax, and features. In short, the
core principles listed are:
- **Lightweight** _(very small module.)_
- **Simple** _(minimum amount of syntax, should feel like native python!)_
- **Rust-styled** _(features, syntax, behaviour. Only inspiration, not strict.)_

Creating an enum is straightforward, but highly customizable for improved user
experience. You can create an enum variant in a few styles to your preference,
with little to no functional difference between any options. Observe the three
different ways of defining an enum variant:

```python
class Example(Enum):
    Foo = evar()
    Bar = {}
    Baz = ()
```
_(figure 0)_

All three variants create identical enum variants. (with the exception that each
variant is considered its very own type, and thus, Foo != Bar != Baz.)

The benefit of using LERS over the built-in enum module lies in just a few, but
important differences. One of these important differences is the support of
match statements!

```python
... # cont'd from figure 0

foo = Example.Foo()
match foo:
    case Example.Foo:
        print('I am Foo!')
    case Example.Bar:
        print('I am Bar!')
    case Example.Baz:
        print('I am Baz!')
    case _:
        print("I am not an Example.")
```
_(figure 1)_

The expected output of course being "I am Foo!". Very nifty little feature
which denounces long if-elif-else chains, though you can still do that if
you so choose.

```python
assert Example.Foo() == Example.Foo
```
_(figure 2)_

Okay, I'll admit, a *little* cursed. This is, however, what makes match
statements work the way they do, with so little extra user input.

Another advantage of LERS is a very useful Rust enum feature, that being that
enum variants can have properties! In fact, LERS enums can have properties,
ordered and named like Rust, but can also have both at the same time! (unlike
Rust.)

```python
class Animal(Enum):
    Insect = evar(
        leg_count=int,
        eye_count=int
    )

    SheepMatrix = evar(int, int, int)

    InsectMatrix = evar(
        int, int, int,
        leg_count=int,
        eye_count=int
    )
```
_(figure 3)_

A slightly silly example, though I'm sure you'll have more practical uses for
this module than sheep math.

If you don't like the syntactical look of evar, good news! This module has a
pinch of sugar for a sweeter look, should you so choose. You can instead use
dictionaries and tuples to define an enum variant, although to define an enum
variant which has both ordered and named properties, evar will be necessary.

```python
class Employee(Enum):
    Boss = {
        'name': str,
        "salary": str
    }

    MindlessWorker = (int)
```
_(figure 4)_

Accessing the properties of an enum variant is also extremely straightforward.
Just make sure that the variant you are working on is correct, lest you raise
an exception.

```python
class Example(Enum):
    Foo = {'prop': int}
    Bar = (int)
    Baz = evar(int, 'prop': int)

f = Example.Foo(prop=15) # properties MUST be assigned using keyword arguments!
b = Example.Bar(30)
z = Example.Baz(45, prop=60)

assert f.prop == 15
assert b[0] == 30
assert z[0] == 45 and z.prop == 60
```
_(figure 5)_

Properties can also be assigned just like how you would expect:

```python
... # cont'd from figure 5

f.prop += 1
b[0] = 40
Z[0] = -Z[0]
z.prop *= z.prop

```
_(figure 6)_

Now for one more crucially important feature! Methods! You can call methods on
your enum variants, but where would you define them...? Why, the same place
you would in Rust. This is inspired by Rust, after all!

```python
class Example(Enum):
    Foo = evar()
    Bar = {}
    Baz = (int)

    def who_am_i(self):
        match self:
            case Example.Foo:
                print('I am Foo!')
            case Example.Bar:
                print('I am Bar!')
            case Example.Baz:
                print(f'I am Baz, and I have a value of {self[0]}!')

Example.Foo().who_am_i()    # outputs 'I am Foo!'
Example.Bar().who_am_i()    # outputs 'I am Bar!'
Example.Baz(50).who_am_i()  # outputs 'I am Baz, and I have a value of 50!'         
```

Enum variants are expected to have common behaviour afterall, so they cannot
each have their own functions. Instead, when creating a function within an enum,
all enum variants inherit this function.

## Like what you see?

Thanks! Don't be afraid to make suggestions, fork, or contribute! This project
is licensed under MIT, and I encourage you to do the same with your project.
(though totally of your own discretion, not required as per the license's terms.)
Thank you for choosing LERS!
