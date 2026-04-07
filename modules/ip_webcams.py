#!/usr/bin/env python3

import json
import os
from datetime import datetime

class ip_webcams:
    def __init__(self):
        self.name = "IP Webcams"
        self.description = "Search for IP Webcams with screenshot availability."

    def execute(self, api, query="", max_results=50):
        base_query = 'has_screenshot:true IP Webcam'
        final_query = f"{base_query} {query}".strip() if query else base_query

        try:
            print(f"[+] Executing IP Webcam search: {final_query}")
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
                'title': match.get('http', {}).get('title', 'Unknown')
            })
        return filtered

    def _display_results(self, devices):
        if not devices:
            print("[!] No IP Webcams found")
            return

        print(f"\n[+] Found {len(devices)} IP Webcams:")
        print("=" * 100)
        print("IP:Port          | Organization     | Location          | Title")
        print("-" * 100)

        for d in devices:
            ip_port = f"{d['ip']}:{d['port']}"
            org = d['org'][:16] + "..." if len(d['org']) > 16 else d['org']
            location = d['location'][:19] + "..." if len(d['location']) > 19 else d['location']
            title = d['title'][:15] + "..." if len(d['title']) > 15 else d['title']
            print(f"{ip_port:<16} | {org:<19} | {location:<22} | {title}")

        print("=" * 100)
        print(f"[+] Search completed. Total devices found: {len(devices)}")

    def _save_results(self, devices):
        if not devices:
            return

        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
        os.makedirs(results_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ip_webcams-{timestamp}.json"
        filepath = os.path.join(results_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)

        print(f"[+] Results saved to: {filepath}")
