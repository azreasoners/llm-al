# LLM + AL: Bridging Large Language Models and Action Languages for Complex Reasoning about Actions (AAAI 2025)

This repository contains the implementation of the paper **"LLM + AL: Bridging Large Language Models and Action Languages for Complex Reasoning about Actions"** (AAAI 2025). 


## Repository Structure
Below is an overview of the directory structure and the purpose of each folder and file:
```
llm-al/
├── app/                           # Main application folder.
│   ├── envs/                      # Contains files for running domains.
│   ├── experiments/               # Contains outputs from baseline and llm-al experiments.
│   ├── prompts/                   # Prompts used in the pipeline separated in .txt files for viewing.
│   ├── keys.py                    # OpenAI API keys (should be filled in).
│   ├── main.py                    # Main file which runs the llm-al pipeline.
│   ├── prompts.py                 # Prompts used in the pipeline.
│   ├── utils.py                   # Useful functions used in the pipeline.
│   ├── utils_cplus2asp.py         # Useful functions related to the Cplus2ASP integration.
├── Dockerfile                     # Dockerfile for containerizing the application.
├── README.md                      # Description of the repository and instructions for usage.
├── appendix.pdf                   # Appendix for the paper.
```

---

## Setup

### API Keys
Place your OpenAI API keys in `app/keys.py` file in the following format:
```python
API_KEY = "your_openai_api_key"
```


There are two ways to set up the environment for running llm-al. The first option is to use Docker, which is most convenient. Alternatively you can choose the second option and manually install all dependencies.




### Option 1: Docker

0. Clone the repo:
   ```bash
   git clone https://github.com/azreasoners/llm-al.git \
   cd llm-al
   ```

1. Build the Docker image:
   ```bash
   docker build -t llm-al .
   ```
2. Then run a container:
   ```bash
   docker run -it llm-al
   ```
<!--- To run the code, skip to the [Running LLM-AL](#running-llm-al) section. -->

### Option 2: Manual Installation

0. Clone the repo:
   ```bash
   git clone https://github.com/azreasoners/llm-al.git \
   cd llm-al
   ```
   
1. Create and activate a Conda environment:
   ```bash
   conda create --name llm-al -c conda-forge python=3.11 \
   conda activate llm-al
   ```

2. Install dependencies:
   ```bash
   conda install numpy \
   pip install openai==0.27.7
   ```

3. Install **Cplus2ASP** from its [GitHub repository](https://github.com/azreasoners/Cplus2ASP).

---


## Running LLM-AL

### Running a Task
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
- **`--model <LLM MODEL>`**: LLM model to use (default: `"o1-preview"`. Options: `"gpt-4o"`, `"o1-preview"`).
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
