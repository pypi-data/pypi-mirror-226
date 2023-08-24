### CLISe: Command Line Input Setter

Command liner for python routines using JSON based input parameter files. It
dives into a module with CLI and execute a routine just as herons dive into
water and catch fish. It also uses JSON text to create task lists to automatize
multiple executions of the routine: ver 0.2.0 by Jaesub Hong
(jhong@cfa.harvard.edu)

       Usage: clise JSON_input_file1 -options_for_file1 ... \
            [json_input_file2 -options_for_file2 ...] \
            [--with common_json_files -common_options ...] \
            [--WITH common_json_files -common_options ...]

       clise --help [keys]
       clise [json_files ...] --Help 
       clise --main module.routine --Help 


### Quick overview of the basic concept

There are many command line interface tools for python (e.g., pyCLI, clize,
etc.). They usually provide decorators and other useful functions to deal with
arguments. They also provide routines to generate the executable scripts for
the user routines. While these are great for developing a large code or
project, it can be a bit redundant for a quick test of a routine in a code you
don't have access to modify. In the latter, you may have to write your own
wrapper to bypass that. CLISe takes a different approach, perhaps suitable for
small or moderate size projects.

CLISe enables executions of any routine as a command script only with command
line options and input files (in an extended JSON format). CLISe dynamically
make a decorator for the called routine, handling the input and output
parameters of the routine, so the user doesn't need to modify the original
routine. One of the input parameters required for CLISe is the routine and
module names. So when the input parameter is stored in a file (recommended),
the user doesn't need to remember the routine name in future runs. For more
complex operations, CLISe allows sequential calls of multiple routines, and
provide a simple mechanics to generate multiple calls of multiple routines.

The main objective of CLISe is an efficient separation and maintenance of
essential input parameters of a task or tasks from the programming part for the
task(s). While CLISe enables a few simple variables and math operations in
setting input parameters for convenience, their features are (subjectively)
limited to leave out the programming part: i.e., "rabbit.py" provides the
routines that enables the auto task repetition with variations in input
parameters, but it doesn't provide, for instance, a range-based for-loop
functionality, which belongs to the programming.

The input parameter files contain the name of the routine to call: e.g.,
"-main": "module.routine".  Assume that a python script example.py has

      def my_sum(name, x, y):
           """ This is my sum. """
           print(name+':', x+y)

Then with a JSON file input.json,

      "-main": "example.my_sum",
          "x": 5,
          "y": 7,
       "name": "answer",

One can execute the routine 'my_sum' in a shell command prompt like

      % clise input.json
      answer: 12

Keys starting with alphabets (x, y, and name in the above example) are assumed
to be fed into the main routine set by "-main" key.  In principle, all the
contents in the JSON files can be fed as a long string in the command line or
as optional parameters for individual keys with "-". So the above example is
equivalent to the followings even without the JSON file input.json.

      %  clise --main example.my_sum -#x 5 -#y 7 -name "answer"
      %  clise '{"-main":"example.my_sum","x":5,"y":7,"name":"answer"}'

or some combination of all three examples:

      %  clise '{"-main":"example.my_sum","name":"answer"}' -#x 5 -#y 7
      %  clise input.json '{"name":"answer"}' -#x 15 -#y 27

When both JSON files and command line input options are available for the same
key, the command line options take a priority.  In the last example,
'input.json' has x of 5, which is replaced by the command line option x=15.
Note # in -#x ensures it is a number but not a string.  See more details with
'clise --help cli'. Note --Help (capital H) prints out the doc string of
the routine.

      % clise input.json --Help
      This is my sum.

Calling multiple JSON files execute them in sequence.

      % clise input.json input.json
      answer: 12
      answer: 12

      % clise input.json -#x 7 input.json -#x 6
      answer: 14
      answer: 13

As you may have guessed it by now, in the command line, "--" is reserved for
options for clise itself, and "-" is reserved for options and keys of the
user routine. In JSON files, the parameters lose one "-", so "-var" are 
for the clise, and "var" without "-" is for the user routine.

Find out what kind of parameters are needed to call the routine using --show
func option.

      % clise --main os.path.isfile --show func
       main: os.path.isfile
       path

The above example shows isfile expect a parameter called path.

      % clise --main os.path.isfile -path clise.py --show output
      True

Can check how the parameters get fed to the routine.

      % clise --main os.path.isfile -path clise.py --show feed
       main: os.path.isfile
       path << str .py

      % clise input.json --show feed
       main: example.my_sum
       name << str answer
          x << int 5
          y << int 7

Can call a routine needing no input parameters.

      % clise --main datetime.datetime.now --show output
      2022-04-27 22:11:52.983532

One can force the parameters to a function with --pars option.

      % clise --main math.sin --pars x --show output -#x 1.0
      0.8414709848078965

In the case of the built-in functions: e.g.,

      % clise --main eval --pars x --show output -x 3+3
      6

      % clise --main pow -*-pars x,y --show output -#x 1.5 -#y 3
      3.375

      % clise --main eval --pars x --show output -x 'pow(1.5,3)'
      3.375


