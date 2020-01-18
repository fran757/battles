# usage
"tools" will apply useful decorators based on given keyword arguments (cache, clock, log)
function data is recorded by function name and module (useful for nested functions)
tool action will be executed on each function call.

:Example :
>>> @tools(log="{bar}")
... def foo(bar):
...     pass

is equivalent to :
>>> @log("{bar}")
... def foo():
...     pass

It is therefore preferred to only import tools from tools.

On empty call, will be applied to neutral lambda and called upon it (useful for logging)

:Example : to (immediately) log current value of variable "bar"
>>> tools(log=f"{bar}")()

which is equivalent to :
>>> tools(log=f"{bar}")(lambda: None)()

or even :
>>> @tools(log=f"{bar}")
... def foo():
...     pass
>>> foo()
