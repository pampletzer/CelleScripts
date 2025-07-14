import sqlite3
import json
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_tables()

    def _get_connection(self):
        """Stellt eine Verbindung zur Datenbank her."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Zugriff auf Spalten per Namen
        return conn

    def _create_tables(self):
        """Erstellt die notwendigen Datenbanktabellen."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # backup_metadata Tabelle
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS backup_metadata
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           backup_name
                           TEXT
                           NOT
                           NULL,
                           fritzbox_ip
                           TEXT
                           NOT
                           NULL,
                           username
                           TEXT,
                           firmware_version
                           TEXT,
                           device_name
                           TEXT,
                           backup_timestamp
                           TEXT
                           NOT
                           NULL
                       )
                       ''')

        # connected_devices Tabelle
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS connected_devices
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           backup_id
                           INTEGER
                           NOT
                           NULL,
                           mac_address
                           TEXT,
                           ip_address
                           TEXT,
                           device_name
                           TEXT,
                           active
                           BOOLEAN,
                           connection_type
                           TEXT,
                           lease_time_remaining
                           INTEGER,
                           FOREIGN
                           KEY
                       (
                           backup_id
                       ) REFERENCES backup_metadata
                       (
                           id
                       )
                           )
                       ''')

        # wlan_settings Tabelle
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS wlan_settings
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           backup_id
                           INTEGER
                           NOT
                           NULL,
                           ssid
                           TEXT,
                           channel
                           INTEGER,
                           encryption_method
                           TEXT,
                           enabled
                           BOOLEAN,
                           max_bit_rate
                           INTEGER,
                           mac_address_control_enabled
                           BOOLEAN,
                           FOREIGN
                           KEY
                       (
                           backup_id
                       ) REFERENCES backup_metadata
                       (
                           id
                       )
                           )
                       ''')

        # raw_data Tabelle (für alles, was nicht in spezialisierte Tabellen passt)
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS raw_data
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           backup_id
                           INTEGER
                           NOT
                           NULL,
                           service_name
                           TEXT,
                           action_name
                           TEXT,
                           data_json
                           TEXT,
                           error_message
                           TEXT,
                           timestamp
                           TEXT
                           NOT
                           NULL,
                           FOREIGN
                           KEY
                       (
                           backup_id
                       ) REFERENCES backup_metadata
                       (
                           id
                       )
                           )
                       ''')

        # Weitere Tabellen hier hinzufügen, z.B. call_logs, port_forwardings, system_logs etc.

        conn.commit()
        conn.close()

    def insert_backup_metadata(self, backup_name, fritzbox_ip, username, device_info=None):
        """Fügt Metadaten der Sicherung hinzu und gibt die ID zurück."""
        conn = self._get_connection()
        cursor = conn.cursor()
        firmware_version = device_info.get('NewSoftwareVersion') if device_info else None
        device_name = device_info.get('NewModelName') if device_info else None

        cursor.execute(
            '''INSERT INTO backup_metadata (backup_name, fritzbox_ip, username, firmware_version, device_name,
                                            backup_timestamp)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (backup_name, fritzbox_ip, username, firmware_version, device_name, datetime.now().isoformat())
        )
        backup_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return backup_id

    def insert_connected_device(self, backup_id, device_data):
        """Fügt Daten eines verbundenen Geräts hinzu."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO connected_devices (backup_id, mac_address, ip_address, device_name, active, connection_type,
                                              lease_time_remaining)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                backup_id,
                device_data.get('NewMACAddress'),
                device_data.get('NewIPAddress'),
                device_data.get('NewHostName'),
                device_data.get('NewActive') == '1',  # Fritzbox gibt '1' oder '0' zurück
                device_data.get('NewInterfaceType'),
                device_data.get('NewLeaseTimeRemaining')
            )
        )
        conn.commit()
        conn.close()

    def insert_wlan_settings(self, backup_id, wlan_data):
        """Fügt WLAN-Einstellungen hinzu."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO wlan_settings (backup_id, ssid, channel, encryption_method, enabled, max_bit_rate,
                                          mac_address_control_enabled)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                backup_id,
                wlan_data.get('NewSSID'),
                wlan_data.get('NewChannel'),
                wlan_data.get('NewX_AVM_DE_EncryptionMode'),
                wlan_data.get('NewEnable') == '1',
                wlan_data.get('NewMaxBitRate'),
                wlan_data.get('NewMACAddressControlEnabled') == '1'
            )
        )
        conn.commit()
        conn.close()

    def insert_raw_data(self, backup_id, service_name, action_name, data, error_message=None):
        """Fügt Rohdaten (als JSON) hinzu."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO raw_data (backup_id, service_name, action_name, data_json, error_message, timestamp)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (
                backup_id,
                service_name,
                action_name,
                json.dumps(data, indent=2, ensure_ascii=False) if data else None,  # Schön formatiertes JSON
                error_message,
                datetime.now().isoformat()
            )
        )
        conn.commit()
        conn.close()

    # Hier würden weitere insert-Methoden für andere spezialisierte Tabellen folgen
    # def insert_call_log_entry(self, backup_id, log_entry_data): ...
    # def insert_port_forwarding(self, backup_id, forwarding_data): ...