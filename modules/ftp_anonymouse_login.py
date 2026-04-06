#!/usr/bin/env python3

import json
import os
from datetime import datetime


class ftp_anonymous_login:
    def __init__(self):
        self.name = "FTP Anonymous Login"
        self.description = "Search for FTP servers with anonymous login enabled."

    def execute(self, api, query="", max_results=50):
        base_query = '"220" "230 Login successful." port:21'
        final_query = f"{base_query} {query}".strip() if query else base_query

        try:
            print(f"[+] Executing FTP search: {final_query}")
            print(f"[+] Maximum results: {max_results}")
            results = api.search(final_query, limit=max_results)
            filtered = self._filter_results(results['matches'])
            self._display_results(filtered)
            self._save_results(filtered)
            return filtered
        except Exception as e:
            print(f"[!] Error: {e}")
            return []

    def _filter_results(self, matches):
        filtered = []
        for match in matches:
            filtered.append({
                'ip': match['ip_str'],
                'port': match['port'],
                'org': match.get('org', 'Unknown'),
                'location': f"{match.get('country_name', 'Unknown')}/{match.get('city', 'Unknown')}",
                'hostnames': match.get('hostnames', []),
                'timestamp': match.get('timestamp', 'Unknown')
            })
        return filtered

    def _display_results(self, devices):
        if not devices:
            print("[!] No FTP instances found with anonymous login enabled")
            return

        print(f"\n[+] Found {len(devices)} FTP instances:")
        print("=" * 100)
        print("IP:Port          | Organization     | Location")
        print("-" * 100)

        for d in devices:
            ip_port = f"{d['ip']}:{d['port']}"
            org = d['org'][:15] + "..." if len(d['org']) > 15 else d['org']
            location = d['location'][:15] + "..." if len(d['location']) > 15 else d['location']
            print(f"{ip_port:<16} | {org:<15} | {location}")

        print("=" * 100)
        print(f"[+] Search completed. Total MongoDB instances found: {len(devices)}")

        if devices:
            print(f"\n[+] Statistics:")
            print(f"   - First result: {devices[0]['ip']}:{devices[0]['port']}")
            print(f"   - Last result: {devices[-1]['ip']}:{devices[-1]['port']}")

            countries = {}
            for d in devices:
                country = d['location'].split('/')[0]
                countries[country] = countries.get(country, 0) + 1
            print(f"   - By country: {', '.join([f'{k}: {v}' for k, v in countries.items()])}")

    def _save_results(self, devices):
        if not devices:
            return

        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
        os.makedirs(results_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ftp_noauth-{timestamp}.json"
        filepath = os.path.join(results_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)

        print(f"[+] Results saved to: {filepath}")