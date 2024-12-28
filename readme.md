# LLM + AL: Bridging Large Language Models and Action Languages for Complex Reasoning about Actions (AAAI 2025)

This repository contains the implementation of the paper **"LLM + AL: Bridging Large Language Models and Action Languages for Complex Reasoning about Actions"** (AAAI 2025)..


## Docker

1. Build the Docker image:
   ```bash
   docker build -t llm-al .
   ```
2. Then run a container:
   ```bash
   docker run -it llm-al
   ```

To run the code, skip to the [Run](#run) section.

---

## Manual Installation

1. Create and activate a Conda environment:
   ```bash
   conda create --name llm-al -c conda-forge python=3.11
   conda activate llm-al
   ```

2. Install dependencies:
   ```bash
   pip install openai==0.27.7
   ```

3. Install **Cplus2ASP** from its [GitHub repository](https://github.com/azreasoners/Cplus2ASP).

---


## How to Use

### API Keys
Place your OpenAI API keys in a `keys.py` file in the following format:
```python
OPENAI_API_KEY = "your_openai_api_key"
```

### Running the Code
Navigate to the `apps` folder and execute the main script with the desired task name:
```bash
python main.py --task <TASK NAME>
```

#### Example:
```bash
python main.py --task river
```

### Additional Parameters
- **`--o <OUTPUT FOLDER NAME>`**: Output folder name (default: same as the task name).
- **`--model <LLM MODEL>`**: LLM model to use (default: `"o1-preview"`. Options: `"gpt-4o"`, `"gpt-4"`).
- **`--max_updates <MAX LLM REVISIONS>`**: Maximum number of revisions from the LLM (default: 8).
- **`--concurrency`**: Enables concurrent actions when running Cplus2ASP.

---

## Outputs

The intermediate outputs and final results are stored in the `outputs` folder.

---

## Adding Problems

To add a new problem, create a folder in the `envs` directory with the name of the domain. For example, see the folder `envs/river`, which is detailed below as a reference.

### Files Required:
1. **`prob_desc.txt`**: Describes the domain.  
   Example:
   ```
   There is a mouse, a snake, and a piece of cheese, and you need to get them across a river using a boat. However, you must ensure that the snake doesn't eat the mouse, and the mouse doesn't eat the cheese. As long as they are not left alone, then they cannot eat. You (the human) and the boat are in the same position always. The boat cannot carry more than one item.
   ```

2. **`query.txt`**: Represents an instance of the domain, including the initial state and the desired final state.  
   Example:
   ```
   The mouse, snake, and cheese are on side leftBank, along with the boat. Find a plan to get the mouse, snake, and piece of cheese across the river, on the side RightBank.
   ```

3. **`signature.txt`**: Lists the types of objects, object instances, and actions.  
   Example:
   ```
   There are two types of objects: "thing" and "side".

   Mouse, Snake, Cheese, and boat are the things.
   LeftBank, RightBank are the sides of the river.

   Actions
   moveBoat moves the boat from one side to the other.
   boardBoat puts a thing on the boat.
   unboardBoat takes a thing off of the boat.
   ```

### Running the New Problem
If the folder is named `river`, run the following command:
```bash
python main.py --task river
```
