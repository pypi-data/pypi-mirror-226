# Executable UML External Entity Operation Parser

Parses an *.op file (operation) to yield an abstract syntax tree using python named tuples

### Why you need this

You need to process an *.op file in preparation for populating a database or some other purpose

### Installation

Create or use a python 3.11+ environment. Then

% pip install op-parser

At this point you can invoke the parser via the command line or from your python script.

#### From your python script

You need this import statement at a minimum:

    from op-parser.parser import OpParser

You then specify a path as shown:

    result = OpParser.parse_file(file_input=path_to_file, debug=False)

The `result` will be a list of parsed operation statements. You may find the header of the `visitor.py`
file helpful in interpreting these results.

#### From the command line

This is not the intended usage scenario, but may be helpful for testing or exploration. Since the parser
may generate some diagnostic info you may want to create a fresh working directory and cd into it
first. From there...

    % eeop arrived-at-floor.op

The .op extension is not necessary, but the file must contain operation text. See this repository's wiki for
more about the xsm language. The grammar is defined in the [operation.peg](https://github.com/modelint/op-parser/blob/main/src/op_parser/operation.peg) file. (if the link breaks after I do some update to the code, 
just browse through the code looking for the operation.peg file, and let me know so I can fix it)

You can also specify a debug option like this:

    % eeop arrived-at-floor.op -D

This will create a diagnostics folder in your current working directory and deposit a couple of PDFs defining
the parse of both the state model grammar: `operation_tree.pdf` and your supplied text: `operation.pdf`.

You should also see a file named `op-parser.log` in a diagnostics directory within your working directory