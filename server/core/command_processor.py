from datetime import datetime

COMMANDS = {
    # SYSTEM COMMANDS
    "hello": {
        "category": "system",
        "intent": "system.greeting",
        "device": None,
        "action": None,
        "execution_status": "completed",
        "response": "Hello! Nico is connected to NEXUS."
    },
    "status": {
        "category": "system",
        "intent": "system.status",
        "device": None,
        "action": None,
        "execution_status": "completed",
        "response": "NEXUS is online and operational."
    },
    # UTILITY COMMANDS
    "help": {
        "category": "utility",
        "intent": "utility.help",
        "device": None,
        "action": None,
        "execution_status": "completed",
        "response": (
            "Try: hello, status, time, help, tv status, "
            "turn on the tv, turn off the tv, lights status, "
            "turn on the lights, turn off the lights, "
            "camera status."
        )
    },
    # TV COMMANDS
    "tv status": {
        "category": "device",
        "intent": "device.status",
        "device": "tv",
        "action": "get_status"
    },
    "turn on the tv": {
        "category": "device",
        "intent": "device.power_on",
        "device": "tv",
        "action": "power_on"
    },
    "turn off the tv": {
        "category": "device",
        "intent": "device.power_off",
        "device": "tv",
        "action": "power_off",
        "execution_status": "not_connected"
    },
    # LIGHT COMMANDS
    "lights status": {
        "category": "device",
        "intent": "device.status",
        "device": "lights",
        "action": "get_status"
    },
    "turn on the lights": {
        "category": "device",
        "intent": "device.power_on",
        "device": "lights",
        "action": "power_on"
    },
    "turn off the lights": {
        "category": "device",
        "intent": "device.power_off",
        "device": "lights",
        "action": "power_off"
    },
    # CAMERA COMMANDS
    "camera status": {
        "category": "device",
        "intent": "device.status",
        "device": "camera",
        "action": "get_status"
    }
}

# Alternative phrases mapped to their main commands.
ALIASES = {
    "hi": "hello",
    "hey nico": "hello",
    "nexus status": "status",

    "what time is it": "time",
    "what is the time": "time",
    "what's the time": "time",

    "turn on tv": "turn on the tv",
    "turn off tv": "turn off the tv",

    "turn on lights": "turn on the lights",
    "turn off lights": "turn off the lights",

    "check tv": "tv status",
    "check the camera": "camera status"
}

def process_command(command: str) -> dict:
    # Step 1: Normalize the input.
    normalized = " ".join(command.strip().lower().split())

    # Step 2: Resolve alternative phrases.
    matched_command = ALIASES.get(normalized, normalized)

    # Step 3: Handle the time command dynamically.
    if matched_command == "time":
        current_time = datetime.now().astimezone().strftime(
            "%I:%M %p"
        )
        return {
            "command": command,
            "normalized_command": normalized,
            "matched_command": matched_command,
            "recognized": True,
            "category": "utility",
            "intent": "utility.current_time",
            "device": None,
            "action": "read_time",
            "execution_status": "completed",
            "response": (
                f"The current time on the NEXUS server is "
                f"{current_time}."
            )
        }

    # Step 4: Look up the command.
    command_details = COMMANDS.get(matched_command)

    # Step 5: Handle unknown commands.
    if command_details is None:
        return {
            "command": command,
            "normalized_command": normalized,
            "matched_command": None,
            "recognized": False,
            "category": "unknown",
            "intent": "unknown",
            "device": None,
            "action": None,
            "execution_status": "unrecognized",
            "response": (
                "I don't recognize that command yet. "
                "Type 'help' to see what I understand."
            )
        }

    # Step 6: Return a structured result.
    if command_details["category"] == "device":
        return {
            "command": command,
            "normalized_command": normalized,
            "matched_command": matched_command,
            "recognized": True,
            "category": "device",
            "intent": command_details["intent"],
            "device": command_details["device"],
            "action": command_details["action"]
        }

    # Step 7: Return system and utility command results.
    return {
        "command": command,
        "normalized_command": normalized,
        "matched_command": matched_command,
        "recognized": True,
        **command_details
    }