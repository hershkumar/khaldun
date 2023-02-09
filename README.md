# Khaldun

Khaldun is a tool that runs code blocks in markdown files. Currently, khaldun supports Python and Haskell.

## Usage
To designate a code block to run, insert a markdown comment that starts with the phrase `khaldun`, followed by any necessary arguments:

```<!---khaldun argname="value" ... --->```

### Arguments
Khaldun commands have two types, `input` and `output`. `input` commands specify that the following code block is code that the user wants to run, and `output` commands specify that a code block with the output of a code block should be placed after the command.

#### `input` commands
In order to specify a code block to be run, there are 3 arguments that must be given to khaldun, the type of the command, the name of the code block, and the language that the code block is written in. For example, here is a full input command:

```<!---khaldun type="input" name="code block 1" language="python" --->```

#### `output` commands
In order to specify where to place the output of a code block, `output` commands are used. Output commands only require 2 arguments, the type and the name of the code block. The name of the code block **must** be the same as the matching input code block. An example full output command is shown below, matching the input command shown above:

```<!---khaldun type="output" name="code block 1" --->```


After all commands are inserted into the markdown file, the python script can then be run:

```python3 khaldun.py <source_filename> <target_filename>```

Khaldun does not modify the original markdown file, it generates a new file, whose filename is specified by the second command line argument.

## Sample Output
This README contains the following code blocks, with khaldun instructions (repeated in code formatting, the commands are not visible in the rendered markdown), and the output file for the README is README2.md, which can be found [here](README2.md).


`<!---khaldun type="input" name="python sample" language="python"--->`
<!---khaldun type="input" name="python sample" language="python"--->
```python
print("Hello World!")

def khaldun():
	print("khaldun is such a cool tool!")
	return True

boolin = khaldun()
print("Is Khaldun cool? ", boolin)
```

`<!---khaldun type="output" name="python sample"--->`
<!---khaldun type="output" name="python sample"--->



`<!---khaldun type="input" name="haskell sample" language="haskell"--->`
<!---khaldun type="input" name="haskell sample" language="haskell"--->
```haskell
-- add up numbers in list 
sumlist :: [Integer] -> Integer
sumlist [] = 0
sumlist (x:xs) = sumlist xs + x

main = do 
    print $ sumlist [1,2,3,4,5,6]
```

`<!---khaldun type="output" name="haskell sample"--->`
<!---khaldun type="output" name="haskell sample"--->
