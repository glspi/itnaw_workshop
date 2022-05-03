import asyncio

import httpx


async def main():
    ips_to_fetch = [1, 2, 3, 4]
    devices_to_fetch = [1, 2, 3, 4, 5, 6]

    base_url = "http://ryan-netbox.workshop/api"
    headers = {"Authorization": "Token 0bb0966c2544d6580a804c21acc3eebc5afd491a"}

    async with httpx.AsyncClient(headers=headers) as client:
         ip_coros = [client.get(f"{base_url}/ipam/ip-addresses/{ip_id}/") for ip_id in ips_to_fetch]
         device_coros = [client.get(f"{base_url}/dcim/devices/{device_id}/") for device_id in devices_to_fetch]

         all_results = await asyncio.gather(*ip_coros, *device_coros)

    ips = [r.json() for r in all_results[:len(ips_to_fetch)]]
    devices = [r.json() for r in all_results[-len(devices_to_fetch):]]

    print(f"Fetched IPs:\n{ips}")
    print(f"Fetched Devices:\n{devices}")


if __name__ == "__main__":
    asyncio.run(main())

