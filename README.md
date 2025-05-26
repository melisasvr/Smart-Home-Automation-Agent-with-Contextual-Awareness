# Smart Home Automation Agent with Contextual Awareness
This project presents a simplified Smart Home Automation Agent designed to manage various smart devices and automate routines based on contextual awareness. It leverages the MCP (Model Context Protocol) for enhanced contextual understanding and decision-making within the smart home environment.

## ✨ Features
- **Device Management**: Control and monitor various smart devices, including lights, thermostats, security cameras, door locks, and motion sensors.
- **Contextual Rules**: Define and execute automation rules based on conditions like time of day, occupancy status, and device states.
- **Default Setups**: Comes pre-configured with default devices and automation routines (e.g., "Welcome Home," "Bedtime," "Away Security," "Good Morning").
- **Contextual Suggestions**: Provides smart suggestions for actions based on the current time and home occupancy.
- **Interactive CLI Demo**: A command-line interface for easy interaction and demonstration of the agent's capabilities.
- **Status Dashboard**: A detailed display of the current state of all devices, occupancy, and active suggestions.

## 🛠️ Installation
- To set up and run this project, you'll need Python 3.7+ and the MCP-Model Context Protocol
1. Clone the repository
- `git clone <repository_url>`
- `cd <repository_name>`
2. Install Dependencies:
Make sure you have the MCP-Model Context Protocol installed. If not, you can typically install it via pip:
- `pip python`
- `pip install MCP-Model-Context-Protocol # (Assuming this is the correct package name for MCP)`
- If the package name is different or requires a specific installation method, please refer to the MCP documentation.

3. Run the script:
- `python smart_home_agent.py`

## 🚀 Usage
Upon running the script, the interactive demo will start, and you'll see a welcome message and a list of available commands.
```
🏠 Smart Home Automation Agent with Contextual Awareness
============================================================
🏠 Smart Home Agent initialized successfully!

🚀 Welcome to Smart Home Automation Agent Demo!
Available commands:
1. status - Show system status
2. lights <on/off> [room] - Control lights
3. temp <temperature> - Set thermostat
4. routine <welcome_home/bedtime_routine/security_mode/morning_routine> - Execute routine
5. occupy <room> <true/false> - Set occupancy
6. suggestions - Get contextual suggestions
7. quit - Exit
```

## 💡 How it Works
- The SmartHomeAgent class is the core of this system.
1. **Device and ContextualRule Data Structures**: These dataclass objects define the schema for smart devices and automation rules, making the code clean and readable.
2. **setup_default_devices() and setup_default_rules()**: These methods populate the agent with initial devices and automation rules upon initialization.
3. **Control Methods (e.g., control_light, control_thermostat)**: These methods handle the logic for changing the state and properties of individual devices.
4. **get_contextual_suggestions()**: This function analyzes the current time and home occupancy to provide relevant automation suggestions, potentially leveraging MCP's capabilities for deeper context.
5. **execute_contextual_rule()**: This method takes a rule ID, checks its conditions, and then executes the associated device actions.
6. **set_occupancy_status()**: A simple method to update the occupancy state, which is crucial for contextual automation.
7. **display_status()**: Provides a comprehensive overview of the smart home's current state.

## 🤝 Contributing
- Feel free to fork this repository, suggest improvements, or add more device types and automation rules. This simplified agent, enhanced by MCP, provides a solid foundation for exploring smart home automation concepts.
