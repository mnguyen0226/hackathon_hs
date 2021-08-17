# Hackathon Heron Systems R&D 2021

![alt text](docs/imgs/acewall_hackathon.jpg)

# About
This repository forks the Pokemon-Showdown, poke-env directories to get the up-to-date set-up, tutorials, implementations for practicing Machine Learning Reinforcement Learning Pokemon Battle Bots against Heron's benchmark scripted agents and trained agents.

This repository contains:
- About Heron Systems.
- Rules of Hackathon and Heron Systems' MLE and SWE contact info for Hackathon Q&A
- Resource, tips, and tricks to setup poke-env environment on Linux. (SB, RLlib, Poke-env, About Showdown)
- Tutorial on rendering 2 scripted agents on Pokemon Showdown.
- Tutorial on having you play against 2 scripted agents on Pokemon Showdown on 2 machines.
- Tutorial on training and rendering simple DQN agent on Pokemon Showdown.
- Tutorial on having you play against 2 scripted agents on Pokemon Showdown on 2 machine.
- Tutorial on having your RL agents vs scripted agents on Pokemon Showdown on 2 machine

# About Heron Systems
- [Heron Systems](https://heronsystems.com/about/) is a lean organization, our leadership remains active in our technical projects, offering partners highly responsive customer service.  Our technical approach is guided by a firm commitment to quality engineering, open architecture, and flexible, extensible systems.
- We built [autonomous fighting jet](https://www.janes.com/defence-news/news-detail/heron-systems-ai-defeats-human-pilot-in-us-darpa-alphadogfight-trials).
- We broke [games balance](https://heronsystems.com/work/gamebreaker/).
- We established foundations for future [MOSAIC Warfare](https://heronsystems.com/work/gamebreaker/).
- We protected [US borders](https://heronsystems.com/work/).

# Hackathon 2021 & Contact Infos

## Rules
- Team of 3?
- There are two optional projects that you 
    - Option 1: Build the coolest ML/RL/Robotics Project/Application.
    - Option 2: Alpha Poke-fight Trials.

## Contact Infos
- Alex
- Brett

## Option 1: Build the coolest ML/RL/Robotics Project/Application
![alt text](docs/imgs/ai.jpg)

- What's your/your friends'/your family's daily problems? Can you apply your ML/RL/SW skills to solve it?
- What we want to see?
    - Ability...
- Submission:

## Option 2: Alpha Poke-fight Trials
![alt text](docs/imgs/APT.jpg)

- You think you are good at Pokemon? Submit your agents to fight 5 rounds and get prizes.
- To enable everyone to fight with each other and compatible with our RL agents, we limit everyone to use the easy-to-use, easy-to-apply [poke-env](https://poke-env.readthedocs.io/en/latest/).
- What we want to see?
    - Ability...
- Submission:

### Installation
- **Step 1:** On your Python workspace, install [Poke-env](https://poke-env.readthedocs.io/en/latest/) with 
```
pip install poke-env
```
- **Step 2:** Install NodeJS v10+. 
    - [For Linux](https://github.com/nodesource/distributions/blob/master/README.md#debinstall).
    - [For Windows](https://nodejs.org/en/download/).
    - [For MacOS](https://nodejs.org/en/download/).
- **Step 3:** Set up training server.
    - Unzip src/Pokemon-Showdown-master.zip.
```
cd Pokemon-Showdown
node pokemon-showdown start --no-security
```
    
    - You should see something like this:

```
RESTORE CHATROOM: lobby
RESTORE CHATROOM: staff
Worker 1 now listening on 0.0.0.0:8000
Test your server at http://localhost:8000
```

    - "http://localhost:8000" is the local server that you will use to train your ML/RL agents.


## Resources - Jupyter Notebook
### General Resources:
- 

### Tutorial 1
- 

### Tutorial 2
- 

### Tutorial 3
- 

### Tutorial 4
- 

### Tutorial 5
- 