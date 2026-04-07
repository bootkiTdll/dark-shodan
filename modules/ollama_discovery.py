#!/usr/bin/env python3

import json
import os
import requests
from datetime import datetime

class ollama_discovery:
    def __init__(self):
        self.name = "Ollama Instances Discovery"
        self.description = "Search for exposed Ollama AI instances and verify their availability."

    def execute(self, api, query="", max_results=50):
        base_query = 'port:11434 http.html:"Ollama is running"'
        final_query = f"{base_query} {query}".strip() if query else base_query

        try:
            print(f"[+] Executing Shodan search")
            print(f"[+] Maximum results: {max_results}")
            results = api.search(final_query, limit=max_results)
            
            verified_devices = self._verify_instances(results['matches'])
            
            self._display_results(verified_devices)
            self._save_results(verified_devices)
            
            return verified_devices
        except Exception as e:
            print(f"[!] Shodan API Error: {e}")
            return []

    def _verify_instances(self, matches):
        verified = []
        print(f"[+] Found {len(matches)} potential instances. Starting verification...")
        
        for match in matches:
            ip = match['ip_str']
            port = match['port']
            url = f"http://{ip}:{port}/api/generate"
            payload = {
                "model": "llama3.2",
                "prompt": "Why is the sky blue?"
            }

            try:
                print(f"[*] Testing {ip}:{port}...", end="\r")
                response = requests.post(url, json=payload, timeout=5)
                if response.status_code == 200:
                    print(f"[V] Valid response from {ip}:{port}                     ")
                    verified.append({
                        'ip': ip,
                        'port': port,
                        'org': match.get('org', 'Unknown'),
                        'location': f"{match.get('country_name', 'Unknown')}/{match.get('city', 'Unknown')}",
                        'status': 'Verified',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                else:
                    print(f"[X] Invalid status {response.status_code} from {ip}:{port}   ")
            except requests.exceptions.RequestException:
                pass
                
        return verified

    def _display_results(self, devices):
        if not devices:
            print("[!] No verified Ollama instances found")
            return

        print(f"\n[+] Found {len(devices)} verified Ollama instances:")
        print("=" * 100)
        print("IP:Port          | Organization     | Location          | Status")
        print("-" * 100)

        for d in devices:
            ip_port = f"{d['ip']}:{d['port']}"
            org = d['org'][:16] + "..." if len(d['org']) > 16 else d['org']
            location = d['location'][:19] + "..." if len(d['location']) > 19 else d['location']
            print(f"{ip_port:<16} | {org:<19} | {location:<22} | {d['status']}")

        print("=" * 100)
        print(f"[+] Verification completed. Total verified: {len(devices)}")

    def _save_results(self, devices):
        if not devices:
            return

        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
        os.makedirs(results_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ollama_discovery-{timestamp}.json"
        filepath = os.path.join(results_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)

        print(f"[+] Detailed results saved to: {filepath}")
