# LLM + AL: Bridging Large Language Models and Action Languages for Complex Reasoning about Actions (AAAI 2025)

This repository contains the implementation of the paper **"LLM + AL: Bridging Large Language Models and Action Languages for Complex Reasoning about Actions"** (AAAI 2025). 

# Introduction
LLM-AL is an automated method which bridges an LLM with an action language (BC+) to solve problems which require complex reasoning and/or planning. From some input files describing a domain, the LLM generates a (1) program signature, (2) natural language commonsense and domain-specific knowledge, and converts this knowledge into (3) BC+ rules and a query. The LLM is then responsible for performing a series of revisions, if needed, based on the outputs from the BC+ reasoner (Cplus2ASP). This process is applied to sample queries generated by the LLM to ensure that the results align with the domain. Finally, the refined BC+ program is used to automatically generate a plan.


## Repository Structure
Below is an overview of the directory structure and the purpose of each folder and file:
```
llm-al/
├── envs/                      # Contains files for running domains.
├── experiments/               # Contains outputs from baseline and llm-al experiments.
├── prompts/                   # Prompts used in the pipeline separated in .txt files for viewing.
├── Dockerfile                 # Dockerfile for containerizing the application.
├── appendix.pdf               # Appendix for the paper.
├── keys.py                    # OpenAI API keys (should be filled in).
├── main.py                    # Main file which runs the llm-al pipeline.
├── prompts.py                 # Prompts used in the pipeline.
├── README.md                  # Description of the repository and instructions for usage.
├── utils.py                   # Useful functions used in the pipeline.
├── utils_cplus2asp.py         # Useful functions related to the Cplus2ASP integration.
```

---
❌ indicates failure to produce a solution, ✔️ indicates an optimal solution was found, Δ indicates human intervention was used to produce a correct result, (n) indicates the number of attempts ChatGPT-4+Code makes at writing a program, and the number of manual corrections required for LLM+AL. † indicates that the solution found was not optimal and * indicates that the LLM generated Python code though it was not instructed to. [n] indicates the number of attempts that ChatGPT-4+Code makes writing a program, and (n) indicates the number of manual corrections required for LLM+AL.
For baseline experiments, the input to the LLM is a concatenation of the problem description, signature description, and query, in the domain folders in [envs](envs).


### Missionaries and Cannibals Elaborations
| Problem                                              |  **Total**                                                                   |  [MCP (basic)](envs/mcp_basic)                                               |  [1 (the boat is a rowboat)](envs/mcp_1_rowboat)                             |  [2 (missionaries and cannibals can exchange hats)](envs/mcp_2_hats)         |  [3 (there are 4 missionaries and 4 cannibals)](envs/mcp_3_4each)            |  [4 (the boat can carry three)](envs/mcp_4_carry3)                           |  [5 (an oar on each bank)](envs/mcp_5_oars)                                  |  [6 (only one missionary and one cannibal can row)](envs/mcp_6_notEveryone)  |  [7 (missionaries cannot row)](envs/mcp_7_mi_cant_row)                       |  [8 (a very big cannibal must cross alone)](envs/mcp_8_bigcannibal)          |  [9 (big cannibal and small missionary)](envs/mcp_9_big_small)               |  [10 (a missionary can walk on water)](envs/mcp_10_jesus)                    |  [11 (missionaries can convert cannibals)](envs/mcp_11_convert)              |  [13 (there is bridge that can cross two)](envs/mcp_13_bridge)               |  [14 (the boat leaks with two people on it)](envs/mcp_14_leaks)              |  [16 (there is an island)](envs/mcp_16_island)                               |  [17 (cannibals can become hungry)](envs/mcp_17_fast_rower)                  |  [19 (there are two sets of groups)](envs/mcp_19_two_sets)                  |
|:----------------------------------------------------|:-------------:|:---------:|:-------------:|:--------------:|:-------------:|:-------------:|:----:|:----:|:----:|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|:-----:|:---:|:---:|:---:|
| Optimal Length     |                 |  11             |  11             |  11             |  (unsolvable)   |  (unsolvable)   |  13             |  13             |  (unsolvable)   |  15             |  11             |  7              |  9              |  4              |  11             |  19             |  13             |  22            |
| LLM +AL           |  7+10Δ     |  ✔️    |  ✔️    |  Δ(1)  |  Δ(2)  |  ✔️    |  Δ(2)  |  Δ(4)  |  ✔️    |  Δ(2)  |  Δ(6)  |  Δ(7)  |  ✔️†   |  ✔️†   |  Δ(3)  |  ✔️    |  Δ(3)  |  Δ(1) |
| Chat GPT4 (04/26/24)  |   3         |    ❌      |    ❌      |   ✔️        |    ❌       |    ❌      |   ❌        |   ❌        |    ❌      |   ❌        |   ❌        |   ❌        |    ❌       |    ❌       |   ✔️        |    ❌       |   ❌        |   ✔️       |
| Chat GPT4o (01/08/25)  |    0      |   ❌     |   ❌     |    ❌   |    ❌   |   ❌     |    ❌*   |    ❌    |   ❌     |    ❌    |    ❌    |    ❌    |   ❌*   |   ❌    |    ❌    |   ❌    |    ❌    |    ❌   |
|Claude 3 Opus (04/22/24)  |  0              |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌            |
| Gemini 1 Ultra (04/22/24)  |  0               |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌            |
| ChatGPT4 Code (04/22/24)  |  5+2Δ            |  ✔️ [1]      |  ✔️ [1]      |  ✔️ [2]      |  Δ [6]        |  ❌ [2]      |  ❌ [1]      |  ❌ [1]      |  Δ [6]        |  ❌ [2]      |  ❌ [1]      |  ✔️† [1]     |  ✔️† [2]     |  ❌ [6]      |  ❌ [1]      |  ❌ [4]      |  ❌ [4]      |  ❌ [1]     |
| o1-mini (01/08/25)  |    6    |  ✔️      |  ✔️      |  ✔️       |   ✔️      |  ✔️       |  ❌      |  ❌      |  ❌      |  ❌      |  ❌      |  ❌      |  ✔️†      |  ❌       |  ❌       |  ❌       |  ❌       |  ❌      |
| o1 (preview) (09/24)  |  7              |  ✔️            |  ✔️            |  ❌            |  ✔️            |  ✔️            |  ❌            |  ❌            |  ✔️            |  ❌            |  ❌            |  ❌            |  ❌            |  ✔️†           |  ❌            |  ❌            |  ❌            |  ✔️           |
| o1 (12/22/24)   |  10     |   ❌   |  ✔️    |   ❌   |   ✔️   |  ✔️    |  ✔️    |   ❌   |  ✔️    |  ✔️†   |  ✔️    |   ❌   |  ✔️†   |   ❌   |  ✔️    |   ❌   |   ❌   |  ✔️   |
| o3-mini (01/21/25) |     9     |   ✔️    |   ✔️    |  ❌     |  ✔️     |  ❌     |  ❌     |  ❌     |  ✔️     |  ❌     |  ✔️     |  ✔️†     |  ✔️†     |  ❌     | ✔️      |   ❌     |  ❌      |  ✔️     |
| Gemini 2.0 Flash (12/22/24) |  2     |  ✔️    |   ❌   |   ❌   |   ❌   |   ❌   |   ❌   |  ❌    |   ❌   |  ❌    |  ❌    |   ❌   |  ❌    |   ❌   |   ✔️   |   ❌   |  ❌    |   ❌  |
| QwQ-32B-preview (11/29/24)  |   4     |  ❌    |   ❌   |  ❌    |  ✔️    |  ✔️    |  ❌    |  ❌    |   ✔️   |  ❌    |  ❌    |  ❌    |  ❌    |  ❌    |  ❌    |   ❌   |  ✔️    |  ❌   |
| DeepSeek-V3 (01/08/25)  |   2       |   ❌       |   ❌       |   ❌       |   ✔️       |   ❌       |   ❌       |   ❌       |   ❌       |   ❌       |   ❌       |   ❌       |   ❌       |   ❌       |   ✔️       |   ❌       |   ❌       |   ❌      |
| DeepSeek-R1-Lite-Preview (01/08/25)  |  3       |  ✔️       |  ❌       |  ❌       |  ❌       |  ✔️       |  ❌       |  ❌       |  ❌       |  ❌       |  ❌       |  ❌       |  ❌       |  ❌       |  ❌       |  ❌       |  ✔️       |  ❌      |
| DeepSeek R1 (01/21/25) |     5     |   ✔️    |   ✔️    |  ✔️     |  ❌     |  ❌     |  ❌     |  ❌     |  ✔️     |  ❌     |  ❌     |  ❌     |  ❌     |  ❌     | ❌      |   ❌     |  ❌      |  ✔️     |
| early-grok-3 (02/19/25) |     2     |   ❌    |   ✔️    |  ❌     |  ❌     |  ❌     |  ❌     |  ❌     |  ❌     |  ❌     |  ❌     |  ❌     |  ❌     |  ❌     | ❌      |   ❌     |  ❌      |  ✔️     |

### Puzzles and Variations
| Problem                               |  **Total**                                           |  [River Cross (basic)](envs/river)                   |  [River Cross (var1)](envs/river_1)                  |  [Tower of Hanoi (3-disk, basic)](envs/hanoi3)       |  [Tower of Hanoi (3-disk, var1)](envs/hanoi3_1)      |  [Tower of Hanoi (5-disk, basic)](envs/hanoi5)       |  [Tower of Hanoi (5-disk, var1)](envs/hanoi5_1)      |  [Tower of Hanoi (7-disk, basic)](envs/hanoi7)       |  [Tower of Hanoi (7-disk, var1)](envs/hanoi7_1)      |  [Sudoku1](envs/sudoku1)                             |  [Sudoku2](envs/sudoku2)                             |  [Sudoku3](envs/sudoku3)                             |  [Sudoku (var1)](envs/sudoku%20(var1))               |  [Sudoku (var2)](envs/sudoku%20(var2))              |
|:-------------------------------------|:-----------:|:---------:|:-------------:|:--------------:|:---------------:|:------------:|:----:|:----:|:----:|:-------------:|:----:|:----:|:----:|:----:|
| Optimal Length  |               |  7            |  6            |  7            |  6            |  31           |  27           |  127          |  11           |  0            |  0            |  0            |  (unsolvable) |  (unsolvable)|
| LLM +AL        |  8+5Δ              |  ✔️             |  ✔️             |  ✔️             |  Δ(1)           |  ✔️             |  ✔️             |  ✔️             |  Δ(1)           |  Δ(2)           |  ✔️             |  ✔️             |  Δ(1)           |  Δ(6)          |
|Chat GPT4  |  5            |  ✔️           |  ❌           |  ❌           |  ❌           |  ✔️*          |  ❌           |  ❌           |  ❌           |  ✔️*          |  ✔️*          |  ❌*          |  ✔️*          |  ❌*         |
| Claude 3 Opus  |  1               |  ✔️             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌             |  ❌            |
| Gem. 1.0 Ultra  |  1               |  ✔️              |  ❌              |  ❌              |  ❌              |  ❌              |  ❌              |  ❌              |  ❌              |  ❌              |  ❌              |  ❌              |  ❌              |  ❌             |
| ChatGPT-4 +Code  |  8+1Δ                |  ✔️ [5]           |  ❌ [3]           |  ✔️ [1]           |  ❌ [1]           |  ✔️ [1]           |  ❌ [4]           |  ✔️ [1]           |  ❌ [2]           |  ✔️ [1]           |  ✔️ [1]           |  ✔️ [3]           |  Δ [3]            |  ✔️ [0]         |
| o1 (preview)  |  5              |  ✔️            |  ✔️            |  ✔️            |  ✔️            |  ✔️            |  ❌            |  ❌            |  ❌            |  ❌            |  ❌            |  ❌            |  ❌            |  ❌            |
| o1  |   9    |  ✔️    |   ✔️†  |   ✔️   |   ✔️   |  ✔️    |  ❌   |  ❌   |  ✔️†   |  ❌    |   ✔️   |   ❌   |   ✔️   |   ✔️  |
| Gemini 2.0 Flash  |    1    |  ✔️    |  ❌    |  ❌    |   ❌   |   ❌   |   ❌   |   ❌   |  ❌    |  ❌    |  ❌    |  ❌    |   ❌   |  ❌   |
| QwQ-32B-preview  |  1          |   ❌       |   ❌       |   ✔️       |  ❌        |  ❌        |  ❌         |   ❌        |  ❌        |  ❌        |  ❌        |  ❌        |   ❌       |   ❌      |

---

## Setup

There are two ways to set up the environment for running llm-al. The first option is to use Docker, which is most convenient. Alternatively you can choose the second option and manually install all dependencies.

### Option 1: Docker

0. Clone the repo:
   ```bash
   git clone https://github.com/azreasoners/llm-al.git \
   && cd llm-al
   ```
2. Place your OpenAI API keys in `keys.py` file in the following format:
   ```python
   API_KEY = "your_openai_api_key"
   ```
3. Build the Docker image:
   ```bash
   docker build -t llm-al .
   ```
4. Then run a container (named `instance1` in this case):
   ```bash
   docker run -it --name instance1 llm-al
   ```
To exit, use the command CTRL+D.

To return to the container, run the following:
   ```bash
   docker start instance1 \
   && docker attach instance1
   ```
**Note**: If running Docker with WSL, make sure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed, and under Settings > Resources > WSL integration, the distro you wish to use Docker on is enabled (you may need to restart Docker Desktop and wsl after doing so). More details are found [here](https://docs.docker.com/desktop/features/wsl/). Otherwise the `docker build` will not work properly.
<!--- To run the code, skip to the [Running LLM-AL](#running-llm-al) section. -->

### Option 2: Manual Installation

0. Clone the repo:
   ```bash
   git clone https://github.com/azreasoners/llm-al.git \
   && cd llm-al
   ```
2. Place your OpenAI API keys in `keys.py` file in the following format:
   ```python
   API_KEY = "your_openai_api_key"
   ```
3. Create and activate a Conda environment:
   ```bash
   conda create --name llm-al -c conda-forge python=3.11 \
   && conda activate llm-al
   ```

4. Install dependencies:
   ```bash
   conda install numpy \
   && pip install openai==0.27.7
   ```

3. Install **Cplus2ASP** from its [GitHub repository](https://github.com/azreasoners/Cplus2ASP).

---


## Running LLM-AL

### Running a Task
Execute the main script with the desired task name:
```bash
python main.py --task <TASK NAME>
```

### Additional Parameters
- **`--o <OUTPUT FOLDER NAME>`**: Output folder name (default: same as the task name).
- **`--model <LLM MODEL>`**: LLM model to use (default: `"o1-preview"`. Options: `"gpt-4o"`, `"o1-preview"`, `"o1"`, `"o3-mini"`).
- **`--max_updates <MAX LLM REVISIONS>`**: Maximum number of revisions from the LLM (default: 8).
- **`--concurrency`**: Enables concurrent actions when running Cplus2ASP.
### Examples:
To run on the river task with default parameters, use:
```bash
python main.py --task river
```

To run on Tower of Hanoi (3-disk) with `gpt-4o` as the underlying LLM, with at most 15 updates, use:
```bash
python main.py --task hanoi3 --model gpt-4o --max_updates 15
```

To run on MCP #13 (There is a bridge), which allows concurrency (crossing the river on boat and on the bridge are possibly concurrent actions), with `o1-preview` as the underlying LLM, use:
```bash
python main.py --task mcp_13_bridge --model o1-preview --concurrency
```

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
