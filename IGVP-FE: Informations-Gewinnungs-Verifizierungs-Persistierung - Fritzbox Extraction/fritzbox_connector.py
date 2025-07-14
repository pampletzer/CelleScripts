from fritzconnection import FritzConnection
from fritzconnection.core.exceptions import FritzConnectionException, FritzServiceError


# Für eine robustere Discovery mehrerer Geräte könnte man Bibliotheken wie 'ssdp' oder 'upnpclient' verwenden.
# Für dieses Beispiel bleibt die fritzconnection.FritzConnection() Discovery im Fokus.

class FritzboxConnector:
    def __init__(self):
        self.fc = None

    def find_fritzboxes(self):
        """
        Versucht, Fritzboxen im lokalen Netzwerk zu finden.
        Gibt eine Liste von Dictionaries mit 'ip' und 'model_name' zurück.
        """
        found_devices = []

        # --- SIMULIERTE MEHRFACH-DISCOVERY (Für Testzwecke) ---
        # ERSETZE DIESEN BLOCK DURCH EINE ECHTE DISCOVERY-LOGIK FÜR MEHRERE BOXEN!
        # FritzConnection() alleine findet standardmäßig nur die erste antwortende Box.
        # Um wirklich mehrere zu finden, bräuchte man eine komplexere UPnP/SSDP-Logik
        # oder gezieltes Ausprobieren bekannter IPs.

        # Beispielhafte IPs in deinem Netzwerk, die du testen könntest
        test_ips = ['192.168.178.1', '192.168.1.1', '192.168.2.1']

        for ip in test_ips:
            try:
                # Kurzer Timeout für Discovery-Versuche
                fc_temp = FritzConnection(address=ip, timeout=0.5)
                model_name = "Unbekanntes Modell"
                try:
                    # Versuche, grundlegende Informationen abzurufen, um zu prüfen ob es eine Fritzbox ist
                    device_info = fc_temp.call_action('DeviceInfo1', 'GetInfo')
                    model_name = device_info.get('NewModelName', model_name)
                    found_devices.append({'ip': ip, 'model_name': model_name})
                except (FritzConnectionException, FritzServiceError):
                    pass  # Nicht erreichbar oder keine Fritzbox unter dieser IP
            except Exception:
                pass  # Weitere Fehler bei der Initialisierung ignorieren

        # --- ENDE DER SIMULATION ---

        # Fallback: Wenn die Simulation nichts findet oder für eine einzelne, schnelle Suche
        if not found_devices:
            try:
                # Standard FritzConnection Discovery (findet die erste im Netzwerk)
                fc_discovery = FritzConnection(timeout=5)  # Etwas längerer Timeout für die Discovery
                if fc_discovery.fc_host:
                    model_name = "Unbekanntes Modell"
                    try:
                        device_info = fc_discovery.call_action('DeviceInfo1', 'GetInfo')
                        model_name = device_info.get('NewModelName', model_name)
                    except (FritzConnectionException, FritzServiceError):
                        pass
                    found_devices.append({'ip': fc_discovery.fc_host, 'model_name': model_name})
            except FritzConnectionException:
                pass  # Keine Fritzbox gefunden über Standard-Discovery

        return found_devices

    def connect_to_fritzbox(self, ip, user, password):
        """
        Stellt eine Verbindung zur Fritzbox her.
        Gibt das FritzConnection-Objekt zurück oder None bei Fehler.
        Behandelt optionalen Benutzernamen.
        """
        try:
            # Wenn kein Benutzername angegeben, FritzConnection ohne User aufrufen
            if user is None or user == "":
                self.fc = FritzConnection(address=ip, password=password, timeout=10)
                print(f"Versuche, Verbindung zu {ip} ohne Benutzernamen herzustellen (für ältere FritzOS-Versionen).")
            else:
                self.fc = FritzConnection(address=ip, user=user, password=password, timeout=10)
                print(f"Versuche, Verbindung zu {ip} mit Benutzernamen '{user}' herzustellen.")

            # Eine kleine Abfrage, um die Verbindung zu testen
            self.fc.call_action('DeviceInfo1', 'GetInfo')
            print(f"Verbindung zu Fritzbox {ip} erfolgreich hergestellt.")
            return self.fc
        except FritzConnectionException as e:
            print(f"Verbindungsfehler zu {ip}: {e} (Falsche Zugangsdaten oder nicht erreichbar?)")
            return None
        except Exception as e:
            print(f"Unerwarteter Fehler bei der Verbindung zu {ip}: {e}")
            return None

    # Rest der Klasse bleibt unverändert (get_device_info, get_wlan_configurations, etc.)
    def get_device_info(self, fc):
        """Ruft allgemeine Geräteinformationen ab."""
        try:
            return fc.call_action('DeviceInfo1', 'GetInfo')
        except (FritzConnectionException, FritzServiceError) as e:
            print(f"Fehler beim Abrufen der Geräteinformationen: {e}")
            return None

    def get_wlan_configurations(self, fc):
        """Ruft WLAN-Konfigurationen ab (für alle WLANs)."""
        wlan_configs = {}
        for service_name in fc.services:
            if 'WLANConfiguration' in service_name:
                try:
                    wlan_id = int(service_name.replace('WLANConfiguration', ''))
                    config = fc.call_action(service_name, 'GetInfo')
                    wlan_configs[wlan_id] = config
                except (FritzConnectionException, FritzServiceError) as e:
                    print(f"Fehler beim Abrufen der WLAN-Konfiguration {service_name}: {e}")
                except ValueError:
                    pass
        return wlan_configs

    def get_connected_devices(self, fc):
        """Ruft Informationen über verbundene Geräte ab."""
        devices = []
        try:
            host_number = fc.call_action('Hosts1', 'GetHostNumberOfEntries')['NewHostNumberOfEntries']
            for i in range(host_number):
                host_entry = fc.call_action('Hosts1', 'GetGenericHostEntry', NewIndex=i)
                devices.append(host_entry)
        except (FritzConnectionException, FritzServiceError) as e:
            print(f"Fehler beim Abrufen verbundener Geräte: {e}")
        return devices

    def get_all_services_and_actions_raw(self, fc):
        """
        Versucht, alle verfügbaren Dienste und Aktionen aufzurufen
        und die Rohdaten zu sammeln. Für die 'raw_data'-Tabelle.
        """
        raw_data = []
        for service_name in fc.services:
            try:
                actions = fc.actions(service_name)
                for action_name in actions:
                    if action_name.startswith('Get') and not fc.arguments(service_name, action_name):
                        try:
                            result = fc.call_action(service_name, action_name)
                            raw_data.append({
                                'service_name': service_name,
                                'action_name': action_name,
                                'data': result
                            })
                        except (FritzConnectionException, FritzServiceError) as e:
                            raw_data.append({
                                'service_name': service_name,
                                'action_name': action_name,
                                'data': None,
                                'error': str(e)
                            })
                        except Exception as e:
                            raw_data.append({
                                'service_name': service_name,
                                'action_name': action_name,
                                'data': None,
                                'error': f"Unerwarteter Fehler: {str(e)}"
                            })
            except (FritzConnectionException, FritzServiceError) as e:
                raw_data.append({
                    'service_name': service_name,
                    'action_name': 'All',
                    'data': None,
                    'error': f"Fehler beim Auflisten der Aktionen: {str(e)}"
                })
        return raw_data