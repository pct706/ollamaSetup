import os
import subprocess
import sys
import time
import concurrent.futures
import threading

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
        # Check if session already exists
        result = subprocess.run(['tmux', 'has-session', '-t', session_name], 
                              capture_output=True, 
                              check=False)
        if result.returncode != 0:
            subprocess.run(['tmux', 'new-session', '-d', '-s', session_name], check=True)
            print(f"Created tmux session: {session_name}")
        else:
            print(f"Tmux session '{session_name}' already exists")
    except subprocess.CalledProcessError as e:
        print(f"Error creating tmux session: {e}")

def install_ollama():
    """Install Ollama using the official install script."""
    try:
        subprocess.run('curl -fsSL https://ollama.com/install.sh | sh', shell=True, check=True)
        print("Ollama installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Ollama: {e}")

def start_ollama_service(session_name='ollama'):
    """Start the Ollama service inside tmux session."""
    try:
        # Send ollama serve command to tmux session
        subprocess.run([
            'tmux', 'send-keys', '-t', session_name,
            'ollama serve', 'C-m'
        ], check=True)
        print("Ollama service started in tmux session")
        
        # Wait for service to start
        time.sleep(2)
        
    except subprocess.CalledProcessError as e:
        print(f"Error starting Ollama service in tmux: {e}")

def pull_model(model):
    """Pull a single Ollama model."""
    try:
        subprocess.run(['ollama', 'pull', model], check=True)
        print(f"Pulled model: {model}")
    except subprocess.CalledProcessError as e:
        print(f"Error pulling model {model}: {e}")

def pull_models_parallel():
    """Pull specified Ollama models in parallel."""
    models_to_pull = [
        'llama3.2:3b-instruct-fp16',
        'nomic-embed-text',
        'qwen2.5-coder',
        'granite3-dense'
    ]
    
    # Create a thread pool and pull models in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(models_to_pull)) as executor:
        # Submit all pull tasks
        futures = [executor.submit(pull_model, model) for model in models_to_pull]
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

def main():
    """Main function to execute all Ollama setup steps."""
    print("Starting Ollama setup...")
    
    session_name = 'ollama'
    
    # Setup steps
    touch_no_auto_tmux()
    create_tmux_session(session_name)
    install_ollama()
    start_ollama_service(session_name)
    pull_models_parallel()
    
    print("Ollama setup completed!")
    print(f"To attach to the Ollama service, run: tmux attach -t {session_name}")

if __name__ == '__main__':
    main()
