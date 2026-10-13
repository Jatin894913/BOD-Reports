import os

class ReportConfig:
    _data = {}

    @classmethod
    def load(cls, env_file_path):
        if not os.path.exists(env_file_path):
            print(f"Warning: {env_file_path} not found. Using defaults.")
            return

        with open(env_file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    cls._data[key.strip()] = value.strip()

    @classmethod
    def get(cls, key, default=None):
        return cls._data.get(key, default)

    @classmethod
    def get_int(cls, key, default=0):
        val = cls.get(key)
        try:
            return int(val) if val is not None else default
        except ValueError:
            return default

    @classmethod
    def get_float(cls, key, default=0.0):
        val = cls.get(key)
        try:
            return float(val) if val is not None else default
        except ValueError:
            return default

    # Flock Notification
    @property
    def FLOCK_WEBHOOK_URL(self):
        return self.get("FLOCK_WEBHOOK_URL")

    # Thresholds
    @property
    def STORAGE_THRESHOLD_PERCENT(self): return self.get_int("STORAGE_THRESHOLD", 75)
    
    @property
    def RAM_THRESHOLD_PERCENT(self): return self.get_int("RAM_THRESHOLD", 75)
    
    @property
    def FEEDERS_COUNT(self): return self.get_int("FEEDERS_COUNT", 8)
    
    @property
    def EXTERNAL_FILES_COUNT(self): return self.get_int("EXTERNAL_FILES_COUNT", 17)
    
    @property
    def SSH_PASSWORD(self): return self.get("SSH_PASSWORD")

    @property
    def SCREENSHOT_BASE_PATH(self): return self.get("SCREENSHOT_BASE_PATH", "../../BOD Screenshots")

    @property
    def ENABLE_FOLDER_CREATION(self): return self.get("ENABLE_FOLDER_CREATION", "true").lower() == "true"

    # W2W PROD EXPECTATIONS
    @property
    def W2W_PROD_PS_CONTAINERS(self): return self.get_int("W2W_PROD_PS_CONTAINERS", 71)
    @property
    def W2W_PROD_NS_CONTAINERS(self): return self.get_int("W2W_PROD_NS_CONTAINERS", 67)
    @property
    def W2W_PROD_DR_CONTAINERS(self): return self.get_int("W2W_PROD_DR_CONTAINERS", 67)

    @property
    def W2W_PROD_PS_CONTAINERS_SATURDAY(self): return self.get_int("W2W_PROD_PS_CONTAINERS_SATURDAY", 59)
    @property
    def W2W_PROD_NS_CONTAINERS_SATURDAY(self): return self.get_int("W2W_PROD_NS_CONTAINERS_SATURDAY", 55)
    @property
    def W2W_PROD_DR_CONTAINERS_SATURDAY(self): return self.get_int("W2W_PROD_DR_CONTAINERS_SATURDAY", 55)

    # W2W UAT EXPECTATIONS
    @property
    def W2W_UAT_CONTAINERS(self): return self.get_int("W2W_UAT_CONTAINERS", 86)

    # FTUAT EXPECTATIONS
    @property
    def FTUAT_CONTAINERS(self): return self.get_int("FTUAT_CONTAINERS", 52)
    @property
    def FTUAT_FYERS_FILES(self): return self.get_int("FTUAT_FYERS_FILES", 5)
    @property
    def FTUAT_SCRIP_MASTER_EXPECTED(self): return self.get("FTUAT_SCRIP_MASTER_EXPECTED", "2/9/9")
    @property
    def FTUAT_ZERODHA_FILES(self): return self.get_int("FTUAT_ZERODHA_FILES", 6)

    # BIGUL UAT EXPECTATIONS
    @property
    def BIGUL_UAT_194_CONTAINERS(self): return self.get_int("BIGUL_UAT_194_CONTAINERS", 60)
    @property
    def BIGUL_UAT_195_CONTAINERS(self): return self.get_int("BIGUL_UAT_195_CONTAINERS", 27)
    @property
    def BIGUL_UAT_RAM_THRESHOLD(self): return self.get_float("BIGUL_UAT_RAM_THRESHOLD", 65.54)

    # BIGUL PROD EXPECTATIONS
    @property
    def BIGUL_PROD_WS_SRV1_CONTAINERS(self): return self.get_int("BIGUL_PROD_WS_SRV1_CONTAINERS", 25)
    @property
    def BIGUL_PROD_WS_SRV23_CONTAINERS(self): return self.get_int("BIGUL_PROD_WS_SRV23_CONTAINERS", 24)
    @property
    def BIGUL_PROD_DB_PRIMARY_CONTAINERS(self): return self.get_int("BIGUL_PROD_DB_PRIMARY_CONTAINERS", 20)
    @property
    def BIGUL_PROD_DB_BACKUP_CONTAINERS(self): return self.get_int("BIGUL_PROD_DB_BACKUP_CONTAINERS", 18)
    @property
    def BIGUL_PROD_BUS12_CONTAINERS(self): return self.get_int("BIGUL_PROD_BUS12_CONTAINERS", 14)
    @property
    def BIGUL_PROD_BUS3_CONTAINERS(self): return self.get_int("BIGUL_PROD_BUS3_CONTAINERS", 6)
    @property
    def BIGUL_PROD_OMS_CONN1_CONTAINERS(self): return self.get_int("BIGUL_PROD_OMS_CONN1_CONTAINERS", 6)
    @property
    def BIGUL_PROD_OMS_CONN23_CONTAINERS(self): return self.get_int("BIGUL_PROD_OMS_CONN23_CONTAINERS", 5)
    @property
    def BIGUL_PROD_EXCHANGE_FEED_CONTAINERS(self): return self.get_int("BIGUL_PROD_EXCHANGE_FEED_CONTAINERS", 15)
    @property
    def BIGUL_PROD_RAM_THRESHOLD(self): return self.get_int("BIGUL_PROD_RAM_THRESHOLD", 65)

    # TTS QA EXPECTATIONS
    @property
    def TTS_QA_CONTAINERS(self): return self.get_int("TTS_QA_CONTAINERS", 85)
    @property
    def TTS_QA_RAM_THRESHOLD(self): return self.get_float("TTS_QA_RAM_THRESHOLD", 80.0)

    # TTS QA FILE LISTS
    @property
    def TTS_QA_EXPECTED_HSI_INDEX(self): return self.get("TTS_QA_EXPECTED_HSI_INDEX", "").split(",")
    @property
    def TTS_QA_EXPECTED_HSI_DATA(self): return self.get("TTS_QA_EXPECTED_HSI_DATA", "").split(",")
    @property
    def TTS_QA_EXPECTED_HSM_SCRIP_INDEX(self): return self.get("TTS_QA_EXPECTED_HSM_SCRIP_INDEX", "").split(",")
    @property
    def TTS_QA_EXPECTED_HSM_SCRIP_DATA(self): return self.get("TTS_QA_EXPECTED_HSM_SCRIP_DATA", "").split(",")
    @property
    def TTS_QA_EXPECTED_HSM_CSV_INDEX(self): return self.get("TTS_QA_EXPECTED_HSM_CSV_INDEX", "").split(",")
    @property
    def TTS_QA_EXPECTED_HSM_CSV_DATA(self): return self.get("TTS_QA_EXPECTED_HSM_CSV_DATA", "").split(",")

    # --- MACHINE SPECIFIC PATHS ---
    @property
    def TTS_QA_PATH_INTERACTIVE_NOREN(self): return self.get("TTS_QA_PATH_INTERACTIVE_NOREN", "/Data/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/")
    @property
    def TTS_QA_PATH_INTERACTIVE_NEST(self): return self.get("TTS_QA_PATH_INTERACTIVE_NEST", "/Data/ttsvolume/hsinteractivevol/data/exch_csv_gen_nest/")
    @property
    def TTS_QA_PATH_ZERODHA(self): return self.get("TTS_QA_PATH_ZERODHA", "/Data/ttsvolume/hscommonvol/data/zerodha_exchange_files/")
    @property
    def TTS_QA_PATH_HSM_SCRIP(self): return self.get("TTS_QA_PATH_HSM_SCRIP", "/Data/ttsvolume/hscommonvol/data/exch_scrip_master/")
    @property
    def TTS_QA_PATH_HSM_CSV(self): return self.get("TTS_QA_PATH_HSM_CSV", "/Data/ttsvolume/hsbroadcastvol/data/exch_csv_gen/")
    @property
    def TTS_QA_PATH_EXTERNAL(self): return self.get("TTS_QA_PATH_EXTERNAL", "/Data/ttsvolume/hscommonvol/data/exch_scrip_master/exchangefiles/")
    @property
    def EXPECTED_CSV_FILES(self): return self.get("EXPECTED_CSV_FILES", "").split(",")
    @property
    def EXPECTED_JSON_FILES(self): return self.get("EXPECTED_JSON_FILES", "").split(",")
    @property
    def EXPECTED_COMMON_JSON(self): return self.get("EXPECTED_COMMON_JSON", "").split(",")
    @property
    def EXPECTED_INDEX_CSV(self): return self.get("EXPECTED_INDEX_CSV", "").split(",")
    @property
    def EXPECTED_INDEX_JSON(self): return self.get("EXPECTED_INDEX_JSON", "").split(",")

    # --- MACHINE SPECIFIC EXPECTATIONS ---
    # PS
    @property
    def PS_EXPECTED_CSV(self): return self.get("PS_EXPECTED_CSV", self.get("EXPECTED_CSV_FILES", "")).split(",")
    @property
    def PS_EXPECTED_JSON(self): return self.get("PS_EXPECTED_JSON", self.get("EXPECTED_JSON_FILES", "")).split(",")
    @property
    def PS_EXPECTED_INDEX_CSV(self): return self.get("PS_EXPECTED_INDEX_CSV", self.get("EXPECTED_INDEX_CSV", "")).split(",")
    @property
    def PS_EXPECTED_INDEX_JSON(self): return self.get("PS_EXPECTED_INDEX_JSON", self.get("EXPECTED_INDEX_JSON", "")).split(",")
    
    # NS
    @property
    def NS_EXPECTED_CSV(self): return self.get("NS_EXPECTED_CSV", self.get("EXPECTED_CSV_FILES", "")).split(",")
    @property
    def NS_EXPECTED_JSON(self): return self.get("NS_EXPECTED_JSON", self.get("EXPECTED_JSON_FILES", "")).split(",")
    @property
    def NS_EXPECTED_INDEX_CSV(self): return self.get("NS_EXPECTED_INDEX_CSV", self.get("EXPECTED_INDEX_CSV", "")).split(",")
    @property
    def NS_EXPECTED_INDEX_JSON(self): return self.get("NS_EXPECTED_INDEX_JSON", self.get("EXPECTED_INDEX_JSON", "")).split(",")
    
    # DR
    @property
    def DR_EXPECTED_CSV(self): return self.get("DR_EXPECTED_CSV", self.get("EXPECTED_CSV_FILES", "")).split(",")
    @property
    def DR_EXPECTED_JSON(self): return self.get("DR_EXPECTED_JSON", self.get("EXPECTED_JSON_FILES", "")).split(",")
    @property
    def DR_EXPECTED_INDEX_CSV(self): return self.get("DR_EXPECTED_INDEX_CSV", self.get("EXPECTED_INDEX_CSV", "")).split(",")
    @property
    def DR_EXPECTED_INDEX_JSON(self): return self.get("DR_EXPECTED_INDEX_JSON", self.get("EXPECTED_INDEX_JSON", "")).split(",")
    
    # UAT
    @property
    def UAT_EXPECTED_CSV(self): return self.get("UAT_EXPECTED_CSV", self.get("EXPECTED_CSV_FILES", "")).split(",")
    @property
    def UAT_EXPECTED_JSON(self): return self.get("UAT_EXPECTED_JSON", self.get("EXPECTED_JSON_FILES", "")).split(",")
    @property
    def UAT_EXPECTED_INDEX_CSV(self): return self.get("UAT_EXPECTED_INDEX_CSV", self.get("EXPECTED_INDEX_CSV", "")).split(",")
    @property
    def UAT_EXPECTED_INDEX_JSON(self): return self.get("UAT_EXPECTED_INDEX_JSON", self.get("EXPECTED_INDEX_JSON", "")).split(",")

    # --- MACHINE SPECIFIC PATHS ---
    @property
    def PS_PATH_INTERACTIVE(self): return self.get("PS_PATH_INTERACTIVE", "/data/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/,/data1/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/,/data/solute/hsinteractivevol/data/exch_csv_gen_noren/")
    @property
    def PS_PATH_BROADCAST(self): return self.get("PS_PATH_BROADCAST", "/data/ttsvolume/hsbroadcastvol/data/exch_scrip_master/,/data1/ttsvolume/hsbroadcastvol/data/exch_scrip_master/")
    @property
    def PS_PATH_BROADCAST_CSV(self): return self.get("PS_PATH_BROADCAST_CSV", "/data/ttsvolume/hsbroadcastvol/data/exch_csv_gen/,/data1/ttsvolume/hsbroadcastvol/data/exch_csv_gen/")
    @property
    def PS_PATH_COMMON(self): return self.get("PS_PATH_COMMON", "/data/ttsvolume/hscommonvol/data/exch_scrip_master/,/data1/ttsvolume/hscommonvol/data/exch_scrip_master/")
    
    @property
    def NS_PATH_INTERACTIVE(self): return self.get("NS_PATH_INTERACTIVE", "/data/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/,/data1/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/,/data/solute/hsinteractivevol/data/exch_csv_gen_noren/")
    @property
    def NS_PATH_BROADCAST(self): return self.get("NS_PATH_BROADCAST", "/data/ttsvolume/hsbroadcastvol/data/exch_scrip_master/,/data1/ttsvolume/hsbroadcastvol/data/exch_scrip_master/")
    @property
    def NS_PATH_BROADCAST_CSV(self): return self.get("NS_PATH_BROADCAST_CSV", "/data/ttsvolume/hsbroadcastvol/data/exch_csv_gen/,/data1/ttsvolume/hsbroadcastvol/data/exch_csv_gen/")
    @property
    def NS_PATH_COMMON(self): return self.get("NS_PATH_COMMON", "/data/ttsvolume/hscommonvol/data/exch_scrip_master/,/data1/ttsvolume/hscommonvol/data/exch_scrip_master/")
    
    @property
    def DR_PATH_INTERACTIVE(self): return self.get("DR_PATH_INTERACTIVE", "/data/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/,/data1/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/,/data/solute/hsinteractivevol/data/exch_csv_gen_noren/")
    @property
    def DR_PATH_BROADCAST(self): return self.get("DR_PATH_BROADCAST", "/data/ttsvolume/hsbroadcastvol/data/exch_scrip_master/,/data1/ttsvolume/hsbroadcastvol/data/exch_scrip_master/")
    @property
    def DR_PATH_BROADCAST_CSV(self): return self.get("DR_PATH_BROADCAST_CSV", "/data/ttsvolume/hsbroadcastvol/data/exch_csv_gen/,/data1/ttsvolume/hsbroadcastvol/data/exch_csv_gen/")
    @property
    def DR_PATH_COMMON(self): return self.get("DR_PATH_COMMON", "/data/ttsvolume/hscommonvol/data/exch_scrip_master/,/data1/ttsvolume/hscommonvol/data/exch_scrip_master/")
    
    @property
    def UAT_PATH_INTERACTIVE(self): return self.get("UAT_PATH_INTERACTIVE", "/data/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/,/data1/ttsvolume/hsinteractivevol/data/exch_csv_gen_noren/,/data/solute/hsinteractivevol/data/exch_csv_gen_noren/")
    @property
    def UAT_PATH_BROADCAST(self): return self.get("UAT_PATH_BROADCAST", "/data/ttsvolume/hsbroadcastvol/data/exch_scrip_master/,/data1/ttsvolume/hsbroadcastvol/data/exch_scrip_master/")
    @property
    def UAT_PATH_BROADCAST_CSV(self): return self.get("UAT_PATH_BROADCAST_CSV", "/data/ttsvolume/hsbroadcastvol/data/exch_csv_gen/,/data1/ttsvolume/hsbroadcastvol/data/exch_csv_gen/")
    @property
    def UAT_PATH_COMMON(self): return self.get("UAT_PATH_COMMON", "/data/ttsvolume/hscommonvol/data/exch_scrip_master/,/data1/ttsvolume/hscommonvol/data/exch_scrip_master/")

    # CONTAINER LISTS
    @property
    def ALLOWED_EXITED_CONTAINER_SUFFIXES(self): return self.get("ALLOWED_EXITED_CONTAINER_SUFFIXES", "").split(",")

config = ReportConfig()
