import sys
import time
import os
import readline  # For command history and auto-completion
from colorama import init, Fore, Style

# Initialize colorama
init()

HISTORY_FILE = os.path.expanduser("~/.py_interpreter_history")

def completer(text, state):
    options = [cmd for cmd in ['exit', 'help', 'clear', 'save', 'load'] if cmd.startswith(text)]
    matches = [s for s in options if s and s.startswith(text)]
    matches.extend([s for s in globals().keys() if s.startswith(text)])
    matches.extend([s for s in locals().keys() if s.startswith(text)])
    try:
        return matches[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

# Load command history
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

def save_history():
    readline.write_history_file(HISTORY_FILE)

def main():
    env = {}
    print(Fore.GREEN + "Simple Python Interpreter. Type 'exit' to quit. Type 'help' for commands." + Style.RESET_ALL)
    while True:
        try:
            code = input(Fore.CYAN + ">>> " + Style.RESET_ALL)
            if code.strip().lower() == "exit":
                save_history()
                break
            elif code.strip().lower() == "help":
                print(Fore.YELLOW + "Available commands:" + Style.RESET_ALL)
                print(Fore.YELLOW + "  exit - Exit the interpreter" + Style.RESET_ALL)
                print(Fore.YELLOW + "  help - Display this help message" + Style.RESET_ALL)
                print(Fore.YELLOW + "  clear - Clear the screen" + Style.RESET_ALL)
                print(Fore.YELLOW + "  save <filename> - Save the session to a file" + Style.RESET_ALL)
                print(Fore.YELLOW + "  load <filename> - Load a script from a file" + Style.RESET_ALL)
                continue
            elif code.strip().lower() == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            elif code.strip().lower().startswith("save "):
                filename = code.strip().split(" ", 1)[1]
                with open(filename, "w") as f:
                    f.write("\n".join(readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)))
                print(Fore.GREEN + f"Session saved to {filename}" + Style.RESET_ALL)
                continue
            elif code.strip().lower().startswith("load "):
                filename = code.strip().split(" ", 1)[1]
                if os.path.exists(filename):
                    with open(filename, "r") as f:
                        for line in f:
                            exec(line, {}, env)
                    print(Fore.GREEN + f"Script {filename} loaded" + Style.RESET_ALL)
                else:
                    print(Fore.RED + f"File {filename} not found" + Style.RESET_ALL)
                continue
            
            start_time = time.time()
            try:
                compiled = compile(code, "<stdin>", "eval")
                result = eval(compiled, {}, env)
                if result is not None:
                    print(Fore.MAGENTA + str(result) + Style.RESET_ALL)
            except SyntaxError as e:
                try:
                    exec(code, {}, env)
                except Exception as exec_e:
                    print(Fore.RED + f"Execution Error: {exec_e}" + Style.RESET_ALL)
            end_time = time.time()
            print(Fore.BLUE + f"Execution time: {end_time - start_time:.4f} seconds" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.RED + "\nExiting..." + Style.RESET_ALL)
            save_history()
            break

if __name__ == "__main__":
    main()
