import os
import subprocess
import sys
import re
from datetime import datetime

def load_env():
    config = {}
    env_path = ".env"
    if not os.path.exists(env_path):
        env_path = os.path.join("..", ".env")
        
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        config[parts[0].strip()] = parts[1].strip()
    return config

def main():
    config = load_env()
    
    # Defaults from config
    user = config.get("SSH_USER")
    server = config.get("SSH_SERVERS", "").split(",")[0].strip()
    port = config.get("SSH_PORT", "22")
    password = config.get("SSH_PASSWORD")
    
    jump_server = None
    jump_port = "22"
    jump_user = None
    jump_pass = None
    
    local_date_arg = ""
    extra_args = []
    machine_name = "commands" # Default fallback

    # Robust Argument Parsing
    # Expected from reports.py: 
    # [0]script [1]password [2]server [3]port [4]user [5]jump_server... [N]machine_name [N+1]local_date [N+2]p_inter...
    if len(sys.argv) >= 5:
        password = sys.argv[1]
        server = sys.argv[2]
        port = sys.argv[3]
        user = sys.argv[4]

        # Check if we have jump server info (next 4 args)
        if len(sys.argv) >= 12 and ("." in sys.argv[5] or ":" in sys.argv[5]):
            jump_server = sys.argv[5]
            jump_port = sys.argv[6]
            jump_user = sys.argv[7]
            jump_pass = sys.argv[8]
            machine_name = sys.argv[9].lower()
            local_date_arg = sys.argv[10]
            extra_args = sys.argv[11:]
        elif len(sys.argv) >= 7:
            machine_name = sys.argv[5].lower()
            local_date_arg = sys.argv[6]
            extra_args = sys.argv[7:]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmd_file = os.path.join(script_dir, f"remote_{machine_name}.sh")
    
    # Fallback to common script if specific one missing
    if not os.path.exists(cmd_file):
        cmd_file = os.path.join(script_dir, "remote_commands.sh")

    if not user or not server or not os.path.exists(cmd_file):
        print(f"ERROR: Missing config (User: {user}, Server: {server})")
        sys.exit(1)

    # Log file for debugging
    log_file = os.path.join(script_dir, "..", "ssh_debug.log")
    
    # Local Date for remote matching (Format: "May 26")
    # Use provided arg if not empty, otherwise current date
    local_date = local_date_arg if local_date_arg else datetime.now().strftime("%b %e").replace("  ", " ")
    
    with open(log_file, "a") as log:
        log.write(f"\n--- SESSION START: {server} ({'JUMP' if jump_server else 'DIRECT'}) ---\n")
        log.write(f"DATE_ARG: '{local_date}' | EXTRA_ARGS: {extra_args}\n")
        
        if jump_server:
            # Jump logic: Pass local_date and extra paths as arguments to script via bash -s
            # Construct argument string for bash -s
            bash_args = f'"{local_date}"'
            for arg in extra_args:
                bash_args += f' "{arg}"'
                
            plink_cmd = [
                "plink.exe", "-batch", "-ssh", jump_server, 
                "-P", jump_port, "-l", jump_user, "-pw", jump_pass,
                f"ssh -o StrictHostKeyChecking=no {user}@{server} 'bash -s {bash_args}'"
            ]
            with open(cmd_file, "rb") as f:
                script_content = f.read().replace(b"\r\n", b"\n")
            
            process = subprocess.Popen(plink_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process.stdin.write(script_content)
            process.stdin.close()
        else:
            # Standard logic: Now also using bash -s via stdin for reliable arguments
            bash_args = f'"{local_date}"'
            for arg in extra_args:
                bash_args += f' "{arg}"'

            plink_cmd = [
                "plink.exe", "-batch", "-ssh", server, 
                "-P", port, "-l", user, "-pw", password, 
                f"bash -s {bash_args}"
            ]
            with open(cmd_file, "rb") as f:
                script_content = f.read().replace(b"\r\n", b"\n")
                
            process = subprocess.Popen(plink_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process.stdin.write(script_content)
            process.stdin.close()

        try:
            # Read output as bytes and decode
            for line_bytes in process.stdout:
                line = line_bytes.decode('utf-8', errors='replace')
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line)
                log.flush()
            process.wait()
            log.write(f"--- SESSION END: EXIT CODE {process.returncode} ---\n")
        except KeyboardInterrupt:
            log.write("--- SESSION INTERRUPTED BY USER ---\n")
            process.terminate()
            try:
                process.wait(timeout=5)
            except:
                process.kill()
            raise

if __name__ == "__main__":
    main()
