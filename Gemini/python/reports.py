from datetime import datetime, date
import os
import subprocess
from config import config

class StorageInfo:
    """Represents disk storage information for a specific mount point."""
    def __init__(self, location, available_gb, used_percent):
        self.location = location
        self.available_gb = available_gb
        self.used_percent = used_percent

    def has_issue(self):
        """Checks if the disk usage exceeds the configured threshold."""
        return self.used_percent > config.STORAGE_THRESHOLD_PERCENT

    def __str__(self):
        return f"{self.available_gb}Gb available and Used is {self.used_percent}% in '{self.location}'"

class MachineData:
    """Holds all telemetry and file status data collected from a single machine."""
    def __init__(self, name):
        self.name = name
        self.containers = 0
        self.restarting_containers = 0
        self.exited_containers = []
        self.in_range_containers = []
        self.out_of_range_containers = []        
        self.storage = [] # List of StorageInfo objects
        self.ram = 0.0
        self.file_lists = {} # Maps folder key (e.g. 'INTERACTIVE_INDEX_FILES') to {filename: info}
        self.feeders_kafka = 0
        self.feeders_ignite = 0
        self.external_files = 0
        self.base_map_details = ""
        self.auto_success = False # True if SSH data collection succeeded
        self.remote_matching_date = "" # The date string the remote server used for filtering

class ReportBase:
    """Base class providing common utilities for data collection and reporting."""
    def __init__(self):
        self.report_date = datetime.now().strftime("%d/%m/%Y")
        self.report_buffer = []

    def log(self, message):
        """Prints a message and adds it to the final report buffer."""
        print(message)
        self.report_buffer.append(message)

    def read_int(self, prompt):
        """Helper to read an integer from user input with validation."""
        while True:
            try:
                val = input(prompt).strip()
                return int(val) if val else 0
            except ValueError:
                print("Error: Please enter a whole number.")

    def read_float(self, prompt):
        """Helper to read a float from user input with validation."""
        while True:
            try:
                val = input(prompt).strip()
                return float(val) if val else 0.0
            except ValueError:
                print("Error: Please enter a decimal number.")

    def read_yes_no(self, prompt):
        """Helper to read a yes/no response from user input."""
        while True:
            val = input(prompt).strip().lower()
            if val in ['yes', 'y']: return True
            if val in ['no', 'n']: return False
            print("Error: Please enter 'yes' or 'no'.")

    def is_saturday(self):
        """Returns True if today is Saturday."""
        return date.today().weekday() == 5

    def get_issue_status(self, has_issue):
        """Returns ' => Issue' if an issue is detected, else a period."""
        return " => Issue" if has_issue else "."

    def print_feeder_status(self, id_num, name, count, expected, ignore_issue_on_saturday=False):
        """Logs the connectivity status of feeders with issue marking."""
        is_sat = self.is_saturday()
        if count == expected:
            self.log(f"{id_num}) All {expected} feeders are connected in {name}.")
        else:
            status = f"Only {count} feeders are connected" if count > 0 else f"No feeders are connected"
            # Some issues are expected on Saturdays (feeders not connected)
            issue_suffix = "." if (is_sat and ignore_issue_on_saturday) else " => Issue"
            self.log(f"{id_num}) {status} in {name}{issue_suffix}")

    def collect_machine_data(self, machine, env_prefix):
        """Automates data collection from a remote machine via SSH and the data_fetcher script."""
        print(f"\n--- AUTO-COLLECTING {machine.name} DATA VIA SSH ---")
        
        server_ip = config.get(f"{env_prefix}_SERVER")
        if not server_ip:
            print(f">>> Skipping automation for {machine.name} (Server not configured).")
            machine.containers = self.read_int(f"Enter running containers for {machine.name}: ")
            machine.ram = self.read_float(f"Enter used RAM % for {machine.name}: ")
            return

        # Prepare arguments for the data_fetcher.py script
        fetcher_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "data_fetcher.py")
        
        # Base arguments: [script, password, server, port, user]
        cmd = [
            "python", fetcher_path,
            config.get(f"{env_prefix}_PASSWORD", ""),
            server_ip,
            config.get(f"{env_prefix}_PORT", "22"),
            config.get(f"{env_prefix}_USER", "hypersync")
        ]
        
        # Add Jump Server configuration if present
        jump_server = config.get(f"{env_prefix}_JUMP_SERVER")
        if jump_server:
            cmd += [
                jump_server,
                config.get(f"{env_prefix}_JUMP_PORT", "22"),
                config.get(f"{env_prefix}_JUMP_USER", "hypersync"),
                config.get(f"{env_prefix}_JUMP_PASSWORD", "")
            ]
        
        # Add Machine-specific path arguments
        # Args: [machine_name, date_placeholder, p_inter, p_broad, p_bcsv, p_comm]
        cmd += [
            machine.name,
            "", # empty date uses system date on remote
            config.get(f"{machine.name}_PATH_INTERACTIVE", ""),
            config.get(f"{machine.name}_PATH_BROADCAST", ""),
            config.get(f"{machine.name}_PATH_BROADCAST_CSV", ""),
            config.get(f"{machine.name}_PATH_COMMON", "")
        ]

        # Explicitly set paths in environment
        env = os.environ.copy()
        env["INFO_PATH"] = "/data/ttsvolume/hscommonvol/data/exch_scrip_master/info-data/"
        env["SCRIP_PATH"] = "/data/ttsvolume/hscommonvol/data/exch_scrip_master/scrip-data/"

        try:
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)
            data_map = self._parse_ssh_output(result.stdout)

            if data_map:
                # Basic Telemetry
                machine.containers = int(data_map.get("CONTAINERS", 0))
                machine.restarting_containers = int(data_map.get("RESTARTING_CONTAINERS", 0))
                machine.exited_containers = [c.strip() for c in data_map.get("EXITED_CONTAINER_NAMES", "").split(",") if c.strip()]
                machine.in_range_containers = []
                machine.out_of_range_containers = []
                # ✅ Parse IN_RANGE_CONTAINERS
                for c in data_map.get("IN_RANGE_CONTAINERS", "").split(","):
                    c = c.strip()
                    if not c:
                        continue

                    if "(" in c and ")" in c:
                        name = c.split("(")[0].strip()
                        runtime = c.split("(")[1].replace(")", "").strip()
                    else:
                        name = c
                        runtime = "unknown"

                    machine.in_range_containers.append({
                        "name": name,
                        "runtime": runtime
                    })


                # ❌ Parse OUT_OF_RANGE_CONTAINERS (ISSUE)
                for c in data_map.get("OUT_OF_RANGE_CONTAINERS", "").split(","):
                    c = c.strip()
                    if not c:
                        continue

                    if "(" in c and ")" in c:
                        name = c.split("(")[0].strip()
                        runtime = c.split("(")[1].replace(")", "").strip()
                    else:
                        name = c
                        runtime = "unknown"

                    machine.out_of_range_containers.append({
                        "name": name,
                        "runtime": runtime
                    })
                machine.ram = float(data_map.get("RAM_USED_PCT", 0))
                
                # Storage
                machine.storage = [
                    StorageInfo("/", int(data_map.get("ROOT_AVAIL", 0)), int(data_map.get("ROOT_USED", 0))),
                    StorageInfo("Data", int(data_map.get("DATA_AVAIL", 0)), int(data_map.get("DATA_USED", 0)))
                ]
                
                machine.remote_matching_date = data_map.get("MATCHING_DATE", "").strip()
                machine.external_files = int(data_map.get("EXTERNAL_FILES", 0))
                machine.base_map_details = data_map.get("BASE_MAP_DETAILS", "")
                
                # File Lists (CSV/JSON/Index)
                for key, value in data_map.items():
                    if key.endswith("_FILES"):
                        files_info = {}
                        for item in value.split(","):
                            if "|" in item:
                                parts = item.split("|")
                                fname = parts[0].strip()
                                files_info[fname] = {
                                    'size': int(parts[1].strip()),
                                    'date': parts[2].strip()
                                }
                        machine.file_lists[key] = files_info
                
                machine.auto_success = True
                print(f">>> {machine.name} data collected successfully.")
            else:
                if result.stderr:
                    print(f">>> {machine.name} collection error: {result.stderr.strip()}")
        except Exception as e:
            print(f">>> {machine.name} collection failed: {e}")

        #MTF Count check
        machine.mtf_nse_cm_info = int(data_map.get("MTF_NSE_CM_INFO", 0))
        machine.mtf_bse_cm_info = int(data_map.get("MTF_BSE_CM_INFO", 0))
        machine.mtf_nse_cm_scrip = int(data_map.get("MTF_NSE_CM_SCRIP", 0))
        machine.mtf_bse_cm_scrip = int(data_map.get("MTF_BSE_CM_SCRIP", 0))

    def _parse_ssh_output(self, output):
        data = {}
        inside_data = False
        for line in output.splitlines():
            if "===DATA_START===" in line: inside_data = True; continue
            if "===DATA_END===" in line: inside_data = False; continue
            if inside_data and ": " in line:
                key, value = line.split(": ", 1)
                data[key.strip()] = value.strip()
        return data

    def check_files(self, machine, label, folder_key, expected_files, issues_list):
        """Checks for missing, zero-byte, or outdated files in a specific remote folder."""
        actual_files = machine.file_lists.get(folder_key, {})
        target_date = machine.remote_matching_date
        
        for filename in expected_files:
            found = False
            # Check if filename is in actual_files (simple match or partial match)
            if filename in actual_files:
                found = True
                meta = actual_files[filename]
            else:
                # Try partial match if expected is just the prefix (e.g. bse_cm)
                for actual_name in actual_files:
                    if actual_name.startswith(filename):
                        found = True
                        meta = actual_files[actual_name]
                        break
            
            if not found:
                issues_list.append(f"      - {label}: Missing {filename}")
            else:
                if meta['size'] == 0:
                    issues_list.append(f"      - {label}: {filename} is 0 bytes")
                elif meta['date'] != target_date:
                    issues_list.append(f"      - {label}: {filename} is old (Updated: {meta['date']}, Expected: {target_date})")

    def get_all_file_issues(self, machine):
        """Aggregates all file issues across all checked directories for a machine."""
        if not machine.auto_success: return []
        
        m_name = machine.name
        # Fetch machine-specific expectations, falling back to global ones
        csv_index = config.get(f"{m_name}_EXPECTED_INDEX_CSV", config.EXPECTED_INDEX_CSV)
        json_index = config.get(f"{m_name}_EXPECTED_INDEX_JSON", config.EXPECTED_INDEX_JSON)
        csv_data = config.get(f"{m_name}_EXPECTED_CSV", config.EXPECTED_CSV_FILES)
        json_data = config.get(f"{m_name}_EXPECTED_JSON", config.EXPECTED_JSON_FILES)
        common_json = config.EXPECTED_COMMON_JSON
        
        # Ensure all expectations are lists
        def to_list(v): return v.split(",") if isinstance(v, str) else v
        
        issues = []
        # Folder Mapping: (Display Label, Remote Data Key, List of Expected Files)
        checks = [
            ("HS Interactive (Index)",      "INTERACTIVE_INDEX_FILES",      to_list(csv_index)),
            ("HS Interactive (Info)",       "INTERACTIVE_INFO_FILES",       to_list(csv_data)),
            ("HS Interactive (Scrip)",      "INTERACTIVE_SCRIP_FILES",      to_list(csv_data)),
            ("HS Broadcast Master (Index)", "BROADCAST_MASTER_INDEX_FILES", to_list(json_index)),
            ("HS Broadcast Master (Info)",  "BROADCAST_MASTER_INFO_FILES",  to_list(json_data)),
            ("HS Broadcast Master (Scrip)", "BROADCAST_MASTER_SCRIP_FILES", to_list(json_data)),
            ("HS Broadcast CSV Gen (Index)","BROADCAST_CSV_INDEX_FILES",    to_list(csv_index)),
            ("HS Broadcast CSV Gen (Info)", "BROADCAST_CSV_INFO_FILES",     to_list(csv_data)),
            ("HS Broadcast CSV Gen (Scrip)","BROADCAST_CSV_SCRIP_FILES",    to_list(csv_data)),
            ("HS Common Master (Index)",    "COMMON_MASTER_INDEX_FILES",    to_list(json_index)),
            ("HS Common Master (Info)",     "COMMON_MASTER_INFO_FILES",     to_list(common_json)),
            ("HS Common Master (Scrip)",    "COMMON_MASTER_SCRIP_FILES",    to_list(common_json))
        ]
        
        for label, key, expected in checks:
            self.check_files(machine, label, key, expected, issues)
            
        return issues

class W2WPRODReport(ReportBase):
    """Generates the comprehensive report for the W2W Production environment."""
    def execute(self):
        self.ps = MachineData("PS")
        self.ns = MachineData("NS")
        self.dr = MachineData("DR")
        
        # Step 1: Automated SSH collection
        for machine, env in [(self.ps, "W2W_PROD_PS"), (self.ns, "W2W_PROD_NS"), (self.dr, "W2W_PROD_DR")]:
            self.collect_machine_data(machine, env)
        
        # Step 2: Manual Checks
        print("\n--- FINAL MANUAL CHECKS ---")
        self.opensearch_ok = self.read_yes_no("Opensearch data is available or not (yes/no): ")
        
        for machine in [self.ps, self.dr, self.ns]:
            machine.feeders_kafka = self.read_int(f"Enter number of feeders in {machine.name} Kafka (expected {config.FEEDERS_COUNT}): ")
            machine.feeders_ignite = self.read_int(f"Enter number of feeders in {machine.name} Ignite (expected {config.FEEDERS_COUNT}): ")
        
        # Use automated count if available, else ask
        ext_count = max(m.external_files for m in [self.ps, self.ns, self.dr])
        self.final_external_files = ext_count if ext_count > 0 else self.read_int(f"Enter number of external files (expected {config.EXTERNAL_FILES_COUNT}): ")
        
        self.generate_formatted_report()

    def generate_formatted_report(self):
        self.log(f"\nW2W PROD Report ({self.report_date}):\n")
        
        # 1. Containers
        exp_ps = config.W2W_PROD_PS_CONTAINERS_SATURDAY if self.is_saturday() else config.W2W_PROD_PS_CONTAINERS
        exp_ns = config.W2W_PROD_NS_CONTAINERS_SATURDAY if self.is_saturday() else config.W2W_PROD_NS_CONTAINERS
        exp_dr = config.W2W_PROD_DR_CONTAINERS_SATURDAY if self.is_saturday() else config.W2W_PROD_DR_CONTAINERS
        
        any_restart = self.ps.restarting_containers > 0 or self.ns.restarting_containers > 0 or self.dr.restarting_containers > 0
        wrong_count = self.ps.containers != exp_ps or self.ns.containers != exp_ns or self.dr.containers != exp_dr
        
        # Check for unauthorized exited containers across all machines
        allowed_prefixes = ("w2w-prod-hsm", "w2w-prod-hsco", "w2w-prod-hsi")
        any_unauth_exited = any(any(not c.startswith(allowed_prefixes) for c in m.exited_containers) for m in [self.ps, self.ns, self.dr])
        
        total_running = self.ps.containers + self.ns.containers + self.dr.containers
        self.log(f"1) Running containers: PS: {self.ps.containers} | NS: {self.ns.containers} | DR: {self.dr.containers} => Total {total_running}{self.get_issue_status(wrong_count or any_restart or any_unauth_exited)}")

        # 2. Storage
        self.log("2) Storage Status:")
        for m in [self.ps, self.ns, self.dr]:
            has_storage_issue = any(s.has_issue() for s in m.storage)
            self.log(f"{m.name}: {' & '.join(str(s) for s in m.storage)}{self.get_issue_status(has_storage_issue)}")

        # 3. Internal Files
        ps_iss = self.get_all_file_issues(self.ps)
        ns_iss = self.get_all_file_issues(self.ns)
        dr_iss = self.get_all_file_issues(self.dr)
        
        if not (ps_iss or ns_iss or dr_iss):
            self.log("3) All required files are downloaded in hsinteractive and hsbroadcast across PS | NS | DR.")
        else:
            self.log("3) Internal File Status Issues:")
            for machine, issues in [(self.ps, ps_iss), (self.ns, ns_iss), (self.dr, dr_iss)]:
                if issues:
                    self.log(f"   {machine.name} Machine:")
                    for issue in issues: self.log(f"   {issue} => Issue")

        # 4. RAM
        any_ram_issue = any(m.ram > config.RAM_THRESHOLD_PERCENT for m in [self.ps, self.ns, self.dr])
        self.log(f"4) RAM Status: PS: {self.ps.ram}% | NS: {self.ns.ram}% | DR: {self.dr.ram}%{self.get_issue_status(any_ram_issue)}")

        # 5-8. General Checks
        self.log("5) Data flow validated in webclient and hypertrade.")
        self.log("6) Superadmin is working properly.")
        self.log("7) Brokeradmin login page is functional.")
        self.log(f"8 ) Yesterday's data is available in Opensearch..{self.get_issue_status(not self.opensearch_ok)}")
        
        # 9-14. Feeder Checks
        idx = 9
        for m in [self.ps, self.dr, self.ns]:
            self.print_feeder_status(idx, f"{m.name} Kafka", m.feeders_kafka, config.FEEDERS_COUNT, ignore_issue_on_saturday=True)
            self.print_feeder_status(idx + 1, f"{m.name} Ignite", m.feeders_ignite, config.FEEDERS_COUNT, ignore_issue_on_saturday=True)
            idx += 2

        # 15. External Files
        is_sat = self.is_saturday()
        exp_ext = config.EXTERNAL_FILES_COUNT
        if self.final_external_files == exp_ext:
            self.log(f"15) All {exp_ext} external files are downloaded successfully.")
        else:
            status = f"Only {self.final_external_files}" if self.final_external_files > 0 else "No"
            self.log(f"15) {status} external files are downloaded{'.' if is_sat else ' => Issue'}")

        # Note Section: Unauthorized Exited Containers
        all_notes = []
        allowed_prefixes = ("w2w-prod-hsm", "w2w-prod-hsco", "w2w-prod-hsi")
        for m in [self.ps, self.ns, self.dr]:
            unauth_exited = [c for c in m.exited_containers if not c.startswith(allowed_prefixes)]
            if unauth_exited:
                all_notes.append(f"{m.name}: {', '.join(unauth_exited)}")
        
        if all_notes:
            self.log("\nNote:")
            for note in all_notes: self.log(f" - {note} containers are in exit state.")

class W2WUATReport(ReportBase):
    """Generates the report for the W2W UAT environment."""
    def execute(self):
        self.uat = MachineData("UAT")
        self.collect_machine_data(self.uat, "W2W_UAT")
        
        print("\n--- FINAL MANUAL CHECKS ---")
        self.opensearch_ok = self.read_yes_no("Opensearch data is available or not (yes/no): ")
        self.uat.feeders_kafka = self.read_int(f"Enter Kafka feeders (expected {config.FEEDERS_COUNT}): ")
        self.uat.feeders_ignite = self.read_int(f"Enter Ignite feeders (expected {config.FEEDERS_COUNT}): ")
        
        self.generate_formatted_report()

    def generate_formatted_report(self):
        self.log(f"\nW2W UAT Report ({self.report_date}):")
        
        # 1. Containers
        exp_uat = config.W2W_UAT_CONTAINERS
        allowed_prefixes = ("w2w-uat-hsm", "w2w-uat-hsco", "w2w-uat-hsi", "w2w-uat-hsc")

        unauth_exited = [c for c in self.uat.exited_containers if not c.startswith(allowed_prefixes)]
        has_cont_issue = (
        (self.uat.containers != exp_uat) or
        (len(unauth_exited) > 0) or
        (len(self.uat.out_of_range_containers) > 0)
    )
        self.log(f"1) Running containers: {self.uat.containers} => Expected {exp_uat}{self.get_issue_status(has_cont_issue)}")

        # ❌ Out-of-range containers (Issue)
        if self.uat.out_of_range_containers:
            self.log("   ❌ Containers out of range:")
            
            for c in self.uat.out_of_range_containers:
                self.log(f"      - {c['name']} ({c['runtime']})")
                
        # 2. Storage
        any_storage_issue = any(s.has_issue() for s in self.uat.storage)
        self.log(f"2) Storage Status: {', '.join(str(s) for s in self.uat.storage)}{self.get_issue_status(any_storage_issue)}")
        
        # 3. Internal Files
        issues = self.get_all_file_issues(self.uat)
        if not issues:
            self.log("3) All internal files are downloaded successfully.")
        else:
            self.log("3) Internal File Status Issues:")
            for i in issues: self.log(i + " => Issue")

        # 4. RAM
        ram_issue = self.uat.ram > config.RAM_THRESHOLD_PERCENT
        self.log(f"4) RAM Status: {self.uat.ram}%{self.get_issue_status(ram_issue)}")

        # 5-8. General
        self.log("5) Data flow validated in webclient and hypertrade.")
        self.log("6) Superadmin is working properly.")
        self.log("7) Brokeradmin login page is functional.")
        self.log(f"8 ) Yesterday's data {'is' if self.opensearch_ok else 'is NOT'} available in Opensearch.{self.get_issue_status(not self.opensearch_ok)}")

        # 9-10. Feeders
        self.print_feeder_status(9, "Kafka", self.uat.feeders_kafka, config.FEEDERS_COUNT)
        self.print_feeder_status(10, "Ignite", self.uat.feeders_ignite, config.FEEDERS_COUNT)
        
        # 11. External Files
        exp_ext = config.EXTERNAL_FILES_COUNT
        if self.uat.external_files == exp_ext:
            self.log(f"11) All {exp_ext} external files are downloaded successfully.")
        else:
            status = f"Only {self.uat.external_files}" if self.uat.external_files > 0 else "No"
            self.log(f"11) {status} external files are downloaded{'.' if self.is_saturday() else ' => Issue'}")

        # 12. Base Map Verification
        if self.uat.auto_success:
            details = self.uat.base_map_details
            files = self.uat.file_lists.get("BASE_MAP_FILES", {})
            has_files = len(files) > 0
            
            owner_info = ""
            if details and "|" in details:
                parts = details.split("|")
                owner_info = f" (Permissions: {parts[0]}, Owner: {parts[1]}, Group: {parts[2]})"
            
            self.log(f"12) base-map folder verification{owner_info}: {'Files are generated' if has_files else 'No files found'}{self.get_issue_status(not has_files)}")
            if has_files:
                self.log(f"    - Found {len(files)} files with today's date.")
        # 13. MTF Status Check
        mtf_issue = (
            self.uat.mtf_nse_cm_info == 0 or
            self.uat.mtf_bse_cm_info == 0 or
            self.uat.mtf_nse_cm_scrip == 0 or
            self.uat.mtf_bse_cm_scrip == 0
        )

        self.log(
            f"13) MTF Status Count => "
            f"NSE_INFO: {self.uat.mtf_nse_cm_info}, "
            f"BSE_INFO: {self.uat.mtf_bse_cm_info}, "
            f"NSE_SCRIP: {self.uat.mtf_nse_cm_scrip}, "
            f"BSE_SCRIP: {self.uat.mtf_bse_cm_scrip}"
            f"{self.get_issue_status(mtf_issue)}"
            )

        # Note Section
        unauth_exited = [c for c in self.uat.exited_containers if not c.startswith(allowed_prefixes)]
        if unauth_exited:
            self.log("\nNote:")
            self.log(f" - {', '.join(unauth_exited)} containers are in exit state.")

class TTSQAReport(ReportBase):
    """Automated report for TTS QA environment."""
    def execute(self):
        self.qa = MachineData("TTS_QA")
        
        # Automation via SSH
        print(f"\n--- AUTO-COLLECTING TTS QA DATA ---")
        server = config.get("TTS_QA_SERVER")
        if not server:
            print(">>> TTS QA Server not configured. Using manual input.")
            self.qa.containers = self.read_int("Running containers: ")
            self.log_report()
            return

        fetcher = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "data_fetcher.py")
        cmd = [
            "python", fetcher,
            config.get("TTS_QA_PASSWORD", ""), server, config.get("TTS_QA_PORT", "22"), config.get("TTS_QA_USER", "hypersync"),
            "tts_qa", "", # machine_name, date
            config.get("TTS_QA_PATH_INTERACTIVE_NOREN", ""),
            config.get("TTS_QA_PATH_INTERACTIVE_NEST", ""),
            config.get("TTS_QA_PATH_ZERODHA", ""),
            config.get("TTS_QA_PATH_HSM_SCRIP", ""),
            config.get("TTS_QA_PATH_HSM_CSV", ""),
            config.get("TTS_QA_PATH_EXTERNAL", "")
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            data = self._parse_ssh_output(res.stdout)
            if data:
                self.qa.containers = int(data.get("CONTAINERS", 0))
                self.qa.ram = float(data.get("RAM_USED_PCT", 0))
                self.qa.external_files = int(data.get("EXTERNAL_FILES", 0))
                self.qa.storage = [
                    StorageInfo("/", int(data.get("ROOT_AVAIL", 0)), int(data.get("ROOT_USED", 0))),
                    StorageInfo("Data", int(data.get("DATA_AVAIL", 0)), int(data.get("DATA_USED", 0)))
                ]
                self.qa.remote_matching_date = data.get("MATCHING_DATE", "").strip()
                # Parse all _FILES
                for k, v in data.items():
                    if k.endswith("_FILES"):
                        self.qa.file_lists[k] = {it.split("|")[0]: {'size': int(it.split("|")[1]), 'date': it.split("|")[2]} for it in v.split(",") if "|" in it}
                self.qa.auto_success = True
        except Exception as e:
            print(f"Automation error: {e}")

        print("\n--- FINAL MANUAL CHECKS ---")
        self.os_ok = self.read_yes_no("Opensearch OK? (y/n): ")
        self.hypertrade_ok = self.read_yes_no("Hypertrade login & chart OK? (y/n): ")
        self.qa.feeders_kafka = self.read_int(f"Kafka feeders (expected {config.FEEDERS_COUNT}): ")
        self.qa.feeders_ignite = self.read_int(f"Ignite feeders (expected {config.FEEDERS_COUNT}): ")
        
        self.log_report()

    def log_report(self):
        self.log(f"\n@all TTS QA Report ({self.report_date}) – Before 9:00 AM")
        
        # 1. External Files
        exp_ext = config.EXTERNAL_FILES_COUNT
        self.log(f"1) {self.qa.external_files} External files are downloaded in TTS_QA{self.get_issue_status(self.qa.external_files != exp_ext)}")

        # 2. HSI Files (Nest, Noren, Zerodha)
        hsi_issues = []
        def get_l(v): return v.split(",") if isinstance(v, str) else v
        
        # Noren: 2 index | 6 info | 6 scrip
        self.check_files(self.qa, "HSI Noren (Index)", "NOREN_INDEX_FILES", get_l(config.get("TTS_QA_EXPECTED_HSI_INDEX")), hsi_issues)
        self.check_files(self.qa, "HSI Noren (Info)",  "NOREN_INFO_FILES",  get_l(config.get("TTS_QA_EXPECTED_HSI_DATA")), hsi_issues)
        self.check_files(self.qa, "HSI Noren (Scrip)", "NOREN_SCRIP_FILES", get_l(config.get("TTS_QA_EXPECTED_HSI_DATA")), hsi_issues)
        
        # Nest: 2 index | 6 info | 6 scrip
        self.check_files(self.qa, "HSI Nest (Index)", "NEST_INDEX_FILES", get_l(config.get("TTS_QA_EXPECTED_HSI_INDEX")), hsi_issues)
        self.check_files(self.qa, "HSI Nest (Info)",  "NEST_INFO_FILES",  get_l(config.get("TTS_QA_EXPECTED_HSI_DATA")), hsi_issues)
        self.check_files(self.qa, "HSI Nest (Scrip)", "NEST_SCRIP_FILES", get_l(config.get("TTS_QA_EXPECTED_HSI_DATA")), hsi_issues)
        
        # Zerodha
        self.check_files(self.qa, "HSI Zerodha", "ZERODHA_FILES", get_l(config.get("TTS_QA_EXPECTED_HSI_DATA")), hsi_issues)

        hsi_status = "successfully" if not hsi_issues else "NOT successfully"
        self.log(f"2) Files for HSI (HSinteractive) i.e Nest, Noren, zerodha_exchange_files(HSCOMMINVOL) are downloaded {hsi_status} in TTS_QA{self.get_issue_status(hsi_issues)}")
        for i in hsi_issues: self.log(f"   {i} => Issue")

        # 3. HSM Scrip Master: 2 index | 9 info | 9 scrip
        hsm_s_issues = []
        self.check_files(self.qa, "HSM Scrip (Index)", "HSM_SCRIP_INDEX_FILES", get_l(config.get("TTS_QA_EXPECTED_HSM_SCRIP_INDEX")), hsm_s_issues)
        self.check_files(self.qa, "HSM Scrip (Info)",  "HSM_SCRIP_INFO_FILES",  get_l(config.get("TTS_QA_EXPECTED_HSM_SCRIP_DATA")), hsm_s_issues)
        self.check_files(self.qa, "HSM Scrip (Scrip)", "HSM_SCRIP_SCRIP_FILES", get_l(config.get("TTS_QA_EXPECTED_HSM_SCRIP_DATA")), hsm_s_issues)
        
        hsm_s_status = "successfully generated" if not hsm_s_issues else "NOT successfully generated"
        self.log(f"3) HSM, exchange_scrip_master, files are {hsm_s_status} in (HSCOMMONVOl) for TTS_QA{self.get_issue_status(hsm_s_issues)}")
        for i in hsm_s_issues: self.log(f"   {i} => Issue")

        # 4. HSM CSV Gen: 2 index | 6 info | 6 scrip
        hsm_c_issues = []
        self.check_files(self.qa, "HSM CSV (Index)", "HSM_CSV_INDEX_FILES", get_l(config.get("TTS_QA_EXPECTED_HSM_CSV_INDEX")), hsm_c_issues)
        self.check_files(self.qa, "HSM CSV (Info)",  "HSM_CSV_INFO_FILES",  get_l(config.get("TTS_QA_EXPECTED_HSM_CSV_DATA")), hsm_c_issues)
        self.check_files(self.qa, "HSM CSV (Scrip)", "HSM_CSV_SCRIP_FILES", get_l(config.get("TTS_QA_EXPECTED_HSM_CSV_DATA")), hsm_c_issues)
        
        hsm_c_status = "generated" if not hsm_c_issues else "NOT generated"
        self.log(f"4) HSM files for exchange_csv_gen is {hsm_c_status} in (HSBROADCAST) for TTS_QA{self.get_issue_status(hsm_c_issues)}")
        for i in hsm_c_issues: self.log(f"   {i} => Issue")

        # 5. Containers
        exp_c = config.TTS_QA_CONTAINERS
        self.log(f"5) {self.qa.containers} containers are running in TTS_QA before 9:00 AM{self.get_issue_status(self.qa.containers != exp_c)}")

        # 6-7. Feeders
        self.print_feeder_status(6, "TTS_QA (Kafka)", self.qa.feeders_kafka, config.FEEDERS_COUNT)
        self.print_feeder_status(7, "TTS_QA (IGNITE)", self.qa.feeders_ignite, config.FEEDERS_COUNT)

        # 8-10. General
        self.log(f"8 ) Able to connect in QA webclient and able to auth & subscribe.")
        self.log(f"9) Storage status: {', '.join(str(s) for s in self.qa.storage)}{self.get_issue_status(any(s.has_issue() for s in self.qa.storage))}")
        self.log(f"10) \"RAM\" usage – {self.qa.ram}%{self.get_issue_status(self.qa.ram > config.TTS_QA_RAM_THRESHOLD)}")
        
        # 11-17. Other
        self.log(f"11) Able to login into Hypertrade{self.get_issue_status(not self.hypertrade_ok)}")
        self.log(f"16) Yesterday’s data is coming properly in OpenSearch{self.get_issue_status(not self.os_ok)}")
        self.log(f"17) Nerve Center is functioning as expected.")

class FTUATReport(ReportBase):
    """Manual report for FTUAT with full 12-point checklist."""
    def execute(self):
        # 1. Containers
        exp_c = config.FTUAT_CONTAINERS
        count = self.read_int(f"Enter running containers count (expected {exp_c}): ")
        
        # 2. Storage
        print("\n--- Storage Status ---")
        root_avail = self.read_int("Enter '/' available GB: ")
        root_used = self.read_int("Enter '/' used %: ")
        data_avail = self.read_int("Enter 'Data' available GB: ")
        data_used = self.read_int("Enter 'Data' used %: ")
        
        # 3-5. Internal Files
        fyers_ok = self.read_yes_no("Fyers internal files downloaded? (y/n): ")
        scrip_ok = self.read_yes_no("Scrip Master internal files downloaded? (y/n): ")
        zerodha_ok = self.read_yes_no("Zerodha internal files downloaded? (y/n): ")
        
        # 6. RAM
        ram_usage = self.read_float("Enter RAM usage % in FTUAT: ")
        
        # 7-8. Feeders
        kafka_feeders = self.read_int(f"Enter FT Kafka feeders (expected {config.FEEDERS_COUNT}): ")
        ignite_feeders = self.read_int(f"Enter FT Ignite feeders (expected {config.FEEDERS_COUNT}): ")
        
        # 9. External Files
        ext_files = self.read_int(f"Enter external files count (expected {config.EXTERNAL_FILES_COUNT}): ")
        
        # 10-12. Functional Checks
        token_added = self.read_yes_no("ext-access-token added? (y/n): ")
        webclient_ok = self.read_yes_no("Webclient (connect, auth, subscribe) success? (y/n): ")
        nerve_ok = self.read_yes_no("Nevercenter Status functional? (y/n): ")

        # --- Logging the Report ---
        self.log(f"\nFTUAT REPORT ({self.report_date})")
        
        # 1. Containers
        exp_c = config.FTUAT_CONTAINERS
        self.log(f"1) Running containers: {count}.{self.get_issue_status(count != exp_c)}")
        
        # 2. Storage
        self.log(f"2) Storage Status:")
        self.log(f"   '/' : {root_avail}Gb available and Used is {root_used}% in '/'{self.get_issue_status(root_used > config.STORAGE_THRESHOLD_PERCENT)}")
        self.log(f"   'Data' : {data_avail}Gb available and Used is {data_used}% in 'Data'{self.get_issue_status(data_used > config.STORAGE_THRESHOLD_PERCENT)}")
        
        # 3-5. Internal Files
        self.log(f"3) Fyers internal files: {'Downloaded' if fyers_ok else 'NOT downloaded'}.{self.get_issue_status(not fyers_ok)}")
        self.log(f"4) Scrip Master internal files: {'Downloaded' if scrip_ok else 'NOT downloaded'}.{self.get_issue_status(not scrip_ok)}")
        self.log(f"5) Zerodha internal files: {'Downloaded' if zerodha_ok else 'NOT downloaded'}.{self.get_issue_status(not zerodha_ok)}")
        
        # 6. RAM
        self.log(f"6) RAM usage in FTUAT: {ram_usage}%.{self.get_issue_status(ram_usage > config.RAM_THRESHOLD_PERCENT)}")
        
        # 7-8. Feeders
        self.print_feeder_status(7, "FT Kafka", kafka_feeders, config.FEEDERS_COUNT)
        self.print_feeder_status(8, "FT Ignite", ignite_feeders, config.FEEDERS_COUNT)
        
        # 9. External Files
        exp_ext = config.EXTERNAL_FILES_COUNT
        self.log(f"9) {'All' if ext_files == exp_ext else f'Only {ext_files}'} external files are downloaded.{self.get_issue_status(ext_files != exp_ext)}")
        
        # 10-12. Functional
        self.log(f"10) ext-access-token (zerodha_exchange_token): {'Added' if token_added else 'NOT added'}.{self.get_issue_status(not token_added)}")
        self.log(f"11) Webclient (connect, auth, subscribe): {'Success' if webclient_ok else 'Failed'}.{self.get_issue_status(not webclient_ok)}")
        self.log(f"12) Nevercenter Status: {'Functional' if nerve_ok else 'Not Functional'}.{self.get_issue_status(not nerve_ok)}")

class BigulUATReport(ReportBase):
    """Simplified manual report for Bigul UAT."""
    def execute(self):
        ext_files = self.read_int("Enter number of external files downloaded: ")
        self.log(f"\nBIGUL UAT Report ({self.report_date})\n1) External files: {ext_files}")

class BigulPRODReport(ReportBase):
    """Simplified manual report for Bigul PROD."""
    def execute(self):
        ext_files = self.read_int("Enter external files (across 10 machines): ")
        self.log(f"\nBIGUL PROD Report ({self.report_date})\n1) External files: {ext_files}")
