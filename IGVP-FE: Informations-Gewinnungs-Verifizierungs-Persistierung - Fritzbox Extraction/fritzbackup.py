import argparse
import os
import sys
from datetime import datetime
import getpass

from fritzbox_connector import FritzboxConnector
from database_manager import DatabaseManager


def main():
    parser = argparse.ArgumentParser(
        description="Fritzbox Backup Tool: Sichert Konfigurationsdaten in eine SQLite-Datenbank."
    )
    parser.add_argument(
        "-n", "--name", default=None,
        help="Ein eindeutiger Name für die Sicherung (wird als Ordnername verwendet). Wird gefragt, wenn nicht angegeben."
    )
    parser.add_argument(
        "-u", "--user", default=None,
        help="Der Benutzername für den Fritzbox-Zugriff. Wird gefragt, wenn nicht angegeben (optional für ältere FritzOS)."
    )
    parser.add_argument(
        "-p", "--password", default=None,
        help="Das Passwort für den Fritzbox-Zugriff. Wird gefragt, wenn nicht angegeben (sichere Eingabe)."
    )
    parser.add_argument(
        "-i", "--ip", default=None,
        help="Optionale IP-Adresse der Fritzbox. Wenn nicht angegeben, wird automatisch gesucht oder interaktiv ausgewählt."
    )

    args = parser.parse_args()

    # --- Fritzboxen zuerst finden und anzeigen ---
    connector = FritzboxConnector()
    found_fbs = []

    # Führe die Suche nur durch, wenn keine IP per CLI-Argument übergeben wurde
    if not args.ip:
        print("Suche nach Fritzboxen im Netzwerk, bitte warten...")
        found_fbs = connector.find_fritzboxes()

        if not found_fbs:
            print(
                "\nEs konnten keine Fritzboxen im Netzwerk gefunden werden. Dies kann an Firewall-Einstellungen oder der Netzwerkkonfiguration liegen.")

            # --- NEU: Nach manueller IP-Eingabe fragen ---
            manual_ip_choice = input(
                "Möchten Sie die IP-Adresse der Fritzbox manuell eingeben? (j/n): ").strip().lower()
            if manual_ip_choice == 'j':
                args.ip = input("Bitte geben Sie die IP-Adresse der Fritzbox manuell ein: ").strip()
                if not args.ip:
                    print("Keine IP-Adresse eingegeben. Programm wird beendet.")
                    sys.exit(1)
            else:
                print("Programm wird beendet.")
                sys.exit(0)  # Exit-Code 0, da es kein Fehler des Programms ist
            # --- ENDE NEU ---
        else:
            print("\nFolgende Fritzbox(en) wurden im Netzwerk gefunden:")
            for i, fb in enumerate(found_fbs):
                print(f"[{i + 1}] {fb['ip']} ({fb.get('model_name', 'Unbekanntes Modell')})")
            print("-" * 40)  # Visuelle Trennung

    # Interaktive Abfrage für Sicherungsname
    backup_name = args.name
    while not backup_name:
        backup_name = input("Bitte geben Sie einen **Namen** für die Sicherung ein (z.B. 'Kunde_Datum'): ").strip()
        if not backup_name:
            print("Sicherungsname darf nicht leer sein.")

    # Interaktive Abfrage für Benutzer und Passwort
    username = args.user
    if not username:
        username_input = input(
            "Bitte geben Sie den Fritzbox-**Benutzernamen** ein (optional, Enter für leer lassen): ").strip()
        if username_input:
            username = username_input
        else:
            username = None

    password = args.password
    while not password:
        password = getpass.getpass(
            "Bitte geben Sie das Fritzbox-**Passwort** ein (wird nicht nicht angezeigt): ").strip()
        if not password:
            print("Passwort darf nicht leer sein.")

    # 1. Sicherungsverzeichnis erstellen
    base_backup_dir = "fritzbox_backups"
    if not os.path.exists(base_backup_dir):
        os.makedirs(base_backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_backup_folder_name = f"{backup_name}_{timestamp}"
    backup_path = os.path.join(base_backup_dir, full_backup_folder_name)

    # 2. Fritzbox-IPs für die Sicherung finalisieren
    fritzbox_ips_to_backup = []

    if args.ip:  # Wenn IP per Argument ODER manueller Eingabe übergeben wurde, diese nutzen
        fritzbox_ips_to_backup = [args.ip]
        print(f"\nSichere die angegebene Fritzbox unter {args.ip}...")
    elif len(found_fbs) == 1:  # Wenn nur eine im Netzwerk gefunden (und keine manuelle Eingabe erfolgte)
        fritzbox_ips_to_backup = [found_fbs[0]['ip']]
        print(f"Es wurde eine Fritzbox gefunden. Starte Sicherung für: {fritzbox_ips_to_backup[0]}")
    else:  # Wenn mehrere im Netzwerk gefunden, zur Auswahl auffordern
        print("[0] Alle gefundenen Fritzboxen sichern")
        while True:
            choice = input("Bitte wählen Sie die IP-Adresse zum Sichern (Nummer oder '0' für alle): ").strip()
            if choice == '0':
                fritzbox_ips_to_backup = [fb['ip'] for fb in found_fbs]
                print("Alle gefundenen Fritzboxen werden nacheinander gesichert.")
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(found_fbs):
                    fritzbox_ips_to_backup = [found_fbs[idx]['ip']]
                    print(f"Sichere: {fritzbox_ips_to_backup[0]}")
                    break
                else:
                    print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
            except ValueError:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")

    # 3. Sicherungsprozess für jede(n) ausgewählte(n) Fritzbox
    for ip in fritzbox_ips_to_backup:
        current_backup_path = backup_path
        if len(fritzbox_ips_to_backup) > 1:
            current_backup_path = os.path.join(backup_path, ip.replace('.', '_'))
            os.makedirs(current_backup_path, exist_ok=True)

        print(f"\n--- Starte Sicherung für Fritzbox: {ip} ---")

        try:
            fc = connector.connect_to_fritzbox(ip, username, password)
            if not fc:
                print(f"Fehler: Verbindung zur Fritzbox {ip} fehlgeschlagen. Überspringe diese Box.")
                continue

            db_manager = DatabaseManager(os.path.join(current_backup_path, "backup.db"))

            device_info = connector.get_device_info(fc)
            backup_meta_id = db_manager.insert_backup_metadata(
                backup_name, ip, username, device_info
            )

            if device_info:
                print(
                    f"  Gerät gefunden: {device_info.get('NewModelName')}, Firmware: {device_info.get('NewSoftwareVersion')}")
                db_manager.insert_raw_data(backup_meta_id, 'DeviceInfo', 'GetInfo', device_info)

            wlan_configs = connector.get_wlan_configurations(fc)
            if wlan_configs:
                print(f"  {len(wlan_configs)} WLAN-Konfigurationen gefunden.")
                for wlan_id, config in wlan_configs.items():
                    db_manager.insert_wlan_settings(backup_meta_id, config)
                    db_manager.insert_raw_data(backup_meta_id, f'WLANConfiguration{wlan_id}', 'GetInfo', config)

            connected_devices = connector.get_connected_devices(fc)
            if connected_devices:
                print(f"  {len(connected_devices)} verbundene Geräte gefunden.")
                for device in connected_devices:
                    db_manager.insert_connected_device(backup_meta_id, device)
                    db_manager.insert_raw_data(backup_meta_id, 'Hosts1', 'GetGenericHostEntry', device)

            print("  Sammle restliche Rohdaten (alle Dienste und Aktionen)...")
            all_raw_data = connector.get_all_services_and_actions_raw(fc)
            for item in all_raw_data:
                db_manager.insert_raw_data(
                    backup_meta_id,
                    item['service_name'],
                    item['action_name'],
                    item['data'],
                    item.get('error')
                )
            print(f"  {len(all_raw_data)} Rohdaten-Einträge gespeichert.")

            print(f"Sicherung für {ip} erfolgreich abgeschlossen in: {current_backup_path}")

        except Exception as e:
            print(f"Ein unerwarteter Fehler bei der Sicherung von {ip} aufgetreten: {e}")
            import traceback
            traceback.print_exc()

    print("\n--- Alle Sicherungsprozesse abgeschlossen ---")


if __name__ == "__main__":
    main()