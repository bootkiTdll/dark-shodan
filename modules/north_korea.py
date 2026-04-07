#!/usr/bin/env python3

import json
import os
from datetime import datetime

class north_korea:
    def __init__(self):
        self.name = "Everything in North Korea"
        self.description = "Search for all internet-exposed resources in North Korean network ranges."

    def execute(self, api, query="", max_results=50):
        base_query = 'net:175.45.176.0/22,210.52.109.0/24,77.94.35.0/24'
        final_query = f"{base_query} {query}".strip() if query else base_query

        try:
            print(f"[+] Executing North Korea search: {final_query}")
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
                'timestamp': match.get('timestamp', 'Unknown'),
                'content': match.get('data', 'No data')[:100].replace('\n', ' ')
            })
        return filtered

    def _display_results(self, devices):
        if not devices:
            print("[!] No resources found in North Korea")
            return

        print(f"\n[+] Found {len(devices)} resources in North Korea:")
        print("=" * 100)
        print("IP:Port          | Organization     | Location          | Snippet")
        print("-" * 100)

        for d in devices:
            ip_port = f"{d['ip']}:{d['port']}"
            org = d['org'][:16] + "..." if len(d['org']) > 16 else d['org']
            location = d['location'][:19] + "..." if len(d['location']) > 19 else d['location']
            snippet = d['content'][:15] + "..." if len(d['content']) > 15 else d['content']
            print(f"{ip_port:<16} | {org:<19} | {location:<22} | {snippet}")

        print("=" * 100)
        print(f"[+] Search completed. Total resources found: {len(devices)}")

    def _save_results(self, devices):
        if not devices:
            return

        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
        os.makedirs(results_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"north_korea-{timestamp}.json"
        filepath = os.path.join(results_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)

        print(f"[+] Results saved to: {filepath}")
