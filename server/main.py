print("NEXUS server starting...")

while True:
    command = input("NEXUS > ")

    if command.lower() == "status":
        print("NEXUS is online.")

    elif command.lower() == "hello":
        print("Hello from NEXUS.")

    elif command.lower() == "exit":
        print("NEXUS shutting down.")
        break

    else:
        print("Unknown command.")