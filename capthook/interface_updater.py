import os
import json

from scrapli import Scrapli

DC_DEVICE_PLATFORM_MAP = {
    "leaf1": "arista_eos",
    "leaf2": "arista_eos",
    "leaf3": "cisco_nxos",
    "spine1": "arista_eos",
}

HOST_NAT_MAP = {
    "leaf1": 2221,
    "leaf2": 2222,
    "leaf3": 2223,
    "spine1": 2211,
}

def main():
    netbox_payload = json.loads(os.environ["PAYLOAD"])

    device_changed = netbox_payload["data"]["device"]["name"]
    intf_changed = netbox_payload["data"]["name"]
    new_descr = netbox_payload["data"]["description"]

    print(f"Device {device_changed} interface {intf_changed} description updated to '{new_descr}'")

    with Scrapli(
        host=device_changed,
        auth_username="admin",
        auth_password="admin",
        auth_strict_key=False,
        platform=DC_DEVICE_PLATFORM_MAP[device_changed],
        transport="paramiko",
        port=HOST_NAT_MAP[device_changed]
        ) as conn:
        
        current_intf_descr_result = conn.send_command(command=f"show run interface {intf_changed} | inc description")
        if current_intf_descr_result.result.strip() == new_descr:
            print("Current running config interface description matches intended description, nothing to do!")
            return
        conn.send_configs(configs=[f"interface {intf_changed}", f"description {new_descr}"])
        print("interface description updated!")

if __name__ == "__main__":
    main()
