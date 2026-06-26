# Lunar Lander Reactive Agent
Team project developed for the "Fundamentals of Artificial Intelligence" course.

**📋 Project Description** 
- **Objective of the project:** Develop an agent that can safely land the spacecraft by controlling the engines.
- **Environment:**  Lunar Lander is a 2D environment, contemplating space and the lunar surface, where the landing platform is located at coordinates (0,0).

- **Agent**: The agent must use information extracted from observations of the environment to control the spacecraft, control that will be done through the available actions.
  
- **Challenges of the landing process**:
  - The spacecraft is subject to the force of gravity, which is continuously pulling it downwards.
  - The agent must maneuver the spacecraft, controlling its position, speed, and orientation.
  - For a landing to be successful, the following conditions must be met:
      - Maintain a low vertical speed.
      - Land with an approximately vertical orientation.
      - Land within the area delimited by the two flags, with both legs in contact with the ground.

**💻 Stack**
- **Programming Languages**: Python
- **Technologies**: Gymnasium, NumPy, Pygame

**▶ How to run**
- Make sure you have Python installed.
- Create a virtual environment: python -m venv .tp1_env
- If using PowerShell, allow script execution: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
- Activate the virtual environment: .tp1_env\Scripts\Activate.ps1
- Install the required modules: pip install gymnasium pygame numpy
- Run the file: python .\ReactiveAgent_Wind.py

