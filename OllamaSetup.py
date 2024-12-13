import os
import subprocess
import sys

def touch_no_auto_tmux():
    """Create a .no_auto_tmux file in the home directory."""
    no_auto_tmux_path = os.path.expanduser('~/.no_auto_tmux')
    try:
        with open(no_auto_tmux_path, 'w') as f:
            f.write('# Prevent automatic tmux session')
        print(f"Created {no_auto_tmux_path}")
    except Exception as e:
        print(f"Error creating .no_auto_tmux file: {e}")

def create_tmux_session(session_name='ollama'):
    """Create a new tmux session."""
    try:
        subprocess.run(['tmux', 'new-session', '-d', '-s', session_name], check=True)
        print(f"Created tmux session: {session_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating tmux session: {e}")

def install_ollama():
    """Install Ollama using the official install script."""
    try:
        subprocess.run('curl -fsSL https://ollama.com/install.sh | sh', shell=True, check=True)
        print("Ollama installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Ollama: {e}")

def start_ollama_service():
    """Start the Ollama service."""
    try:
        subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Ollama service started")
    except Exception as e:
        print(f"Error starting Ollama service: {e}")

def pull_and_run_models():
    """Pull and run specified Ollama models."""
    models_to_pull = [
        'llama3.2:3b-instruct-fp16',
        'nomic-embed-text',
        'qwen2.5-coder',
        'granite3-dense'
    ]

    for model in models_to_pull:
        try:
            # Pull the model
            subprocess.run(['ollama', 'pull', model], check=True)
            print(f"Pulled model: {model}")
        except subprocess.CalledProcessError as e:
            print(f"Error with model {model}: {e}")

def main():
    """Main function to execute all Ollama setup steps."""
    print("Starting Ollama setup...")
    
    # Uncomment or comment out steps as needed
    touch_no_auto_tmux()
    create_tmux_session()
    install_ollama()
    start_ollama_service()
    pull_and_run_models()
    
    print("Ollama setup completed!")

if __name__ == '__main__':
    main()
