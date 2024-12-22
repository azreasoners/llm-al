This is an implementation of "LLM + AL: Briding Large Language Models and Action Languages for Complex Reasoning about Actions" (AAAI 2025).

## Set up
Run the following commands to set up the environment with Conda.
conda create --name llm-al -c conda-forge python=3.11
conda activate llm-al
pip install openai==0.27.7

Install Cplus2ASP from https://github.com/azreasoners/Cplus2ASP. 

Put OpenAI API keys in the `keys.py` file.

## Run

From the root folder run:
`python main.py --task <TASK NAME>`

For example:
`python main.py --task river`

Additional parameters:
--o <OUTPUT FOLDER NAME> (default: is the same as the task name)
--model <LLM MODEL> (default: "o1-preview". "gpt-4o" and "gpt-4" are also supported)
--max_updates <MAX LLM REVISIONS> (default: 8. The maximum number of revisions from the LLM)
--concurrency (allows concurrent actions when running Cplus2ASP)

## Outputs
The intermediate outputs and output are in the `outputs` folder.

## Adding problems
To add a problem, create a folder in the `envs` directory, with the name of the domain. For example see the `envs/river`, which is copied below as an example.

In this folder add 3 files:
(1) `prob_desc.txt` - This is a description of the domain.
Example: 
There is a mouse, a snake, and a piece of cheese, and you need to get them across a river using a boat. However, you must ensure that the snake doesn't eat the mouse, and the mouse doesn't eat the cheese. As long as they are not left alone, then they cannot eat. You (the human) and the boat are in the same position always. The boat cannot carry more than one item.

(2) `query.txt` - This represents an instance of the domain. It should include the initial state and final state.
Example: 
The mouse, snake, and cheese are on side leftBank, along with the boat. Find a plan to get the mouse, snake, and piece of cheese across the river, on the side RightBank.

(3) `signature.txt` - This is should list (i) the types of objects, the (ii) instantiation of objects for the instance, and (iii) the actions. The following example format is suggested:
Example:
There are two types of objects: "thing" and "side".

Mouse, Snake, Cheese, and boat are the things.
LeftBank, RightBank are the sides of the river.

Actions
moveBoat moves the boat from one side to the other.
boardBoat puts a thing on the boat.
unboardBoard takes a thing off of the boat.

To run this problem, assuming the folder in `env` is called `river`, use the following:

`python main.py --task river`

