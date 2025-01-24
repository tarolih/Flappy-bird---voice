# Flappy-bird---voice
# Voice-Pitch Controlled Flappy Game

This Python project is a voice-pitch controlled game developed using Pygame, where the game level can be selected through voice commands and the character's jump is controlled by the pitch of the player's voice.

## Prerequisites

Before running the game, you will need Python installed on your system. This game has been tested with Python 3.8. It is highly recommended to use a virtual environment to avoid conflicts with other packages.

## Setup

### Clone the Repository

```bash
git clone https://github.com/tarolih/Flappy-bird---voice.git
```

### Create and Activate a Virtual Environment

#### For Windows:

```bash
python -m venv env
env\Scripts\activate
```

#### For macOS and Linux:

```bash
python3 -m venv env
source env/bin/activate
```

### Install Required Packages

Install all required packages using the command below:

```bash
pip install -r requirements.txt
```

## Running the game

```bash
python game.py
```

Ensure your microphone is set as the default recording device, as the game uses voice input to control the gameplay.

## Game Controls

- **Voice Command**: Speak the difficulty level ("easy", "medium", "hard") at the start to set the game difficulty.
- **Pitch Control**: Change the pitch of your voice to make the character jump higher or lower.

## Exiting the Game

You can exit the game at any time by closing the game window.
