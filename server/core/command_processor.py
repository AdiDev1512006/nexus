def process_command(command: str) -> str:
    command = command.strip().lower()

    if command == "hello":
        return "Hello! Nico is connected to NEXUS."
    if command == "status":
        return "NEXUS is online and operational."
    if command == "time":
        return "Time service is not implemented yet."

    return f"I don't understand the command: {command}"