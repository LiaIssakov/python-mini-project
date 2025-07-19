import subprocess, requests, json, webbrowser

API_KEY = "get your key from qualcomm"
URL = f"https://global.skyhookwireless.com/wps2/json/location?key={API_KEY}"

def scan_wifi_networks():
    try:
        results = subprocess.check_output(["netsh", "wlan", "show", "network", "bssid"])
        results = results.decode("ascii")
        results = results.replace("\r", "")
        print(results)

        ls = results.split("\n")
        # ssids = []
        bssids = []
        channels = []
        # for line in ls[4:]:  # SSID
        #     if line.strip() and line.strip().startswith('SSID'):
        #         ssid = line.split(':')[1].strip()
        #         ssids.append(ssid)
        for line in ls[8:]:  # BSSID
            if line.strip() and line.strip().startswith('BSSID'):
                bssid = line.split(':', 1)
                bssids.append(bssid[1].strip())
        for line in ls[12:]:  # Channel
            if line.strip() and line.strip().startswith('Channel'):
                channel = line.split(':')[1]
                if len(channel) < 6:
                    channels.append(channel)
        # return ssids
        return bssids, channels

    except Exception as e:
        print(f"Error during Wi-Fi scan: {e}")
        return []

def build_wifi_payload(bssids, channels):
    aps = []
    for i in range(0, len(channels)):
        aps.append({
            "macAddress": bssids[i]  # ,
            # "channel": int(channels[i])
        })
    payload_data = {"wifiAccessPoints": aps}
    return payload_data

def main():
    bssids, channels = scan_wifi_networks()
    payload = build_wifi_payload(bssids, channels)

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json"
    }

    print(payload)
    resp = requests.post(URL, json=payload)
    print("HTTP", resp.status_code)
    print(json.dumps(resp.json(), indent=2))

    if resp.status_code == 200:
        data = resp.json()
        lat = data["location"]["lat"]
        lng = data["location"]["lng"]
        acc = data["location"].get("accuracy")
        print(f"Location: {lat}, {lng} (+{acc} m)")
        webbrowser.open(f"https://www.google.com/maps/?q={lat},{lng}")
    else:
        print("Response text: ", resp.text)


available_bssids, available_channels = scan_wifi_networks()
print("Available Wi-Fi networks (SSIDs):", available_bssids, available_channels)


if __name__ == "__main__":
    main()
