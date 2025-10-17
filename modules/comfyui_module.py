#!/usr/bin/env python3
"""
ComfyUI Search Module for Dark Shodan
"""

import json
import os
from datetime import datetime

class ComfyUIModule:
    """
    ComfyUI search module with advanced filtering to find real ComfyUI instances
    while excluding Amazon/AWS infrastructure and other false positives.
    """
    
    def __init__(self):
        self.name = "comfyui"
        self.description = "Search for ComfyUI instances with advanced filtering"
    
    def execute(self, api, query="", max_results=100):
        """
        Main method for executing the ComfyUI search.
        
        Args:
            api: Shodan API object
            query: Additional search query (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of formatted ComfyUI instances
        """
        
        base_query = '''http.title:"ComfyUI" -http.title:"ComfyUI Login" -org:"Amazon.com Inc." -org:"Amazon Data Services" -org:"Amazon Technologies" -org:"A100 ROW" -org:"Amazon Corporate Services Pty Ltd" -org:"AWS Asia Pacific (Seoul) Region" -http.favicon.hash:1045696447 -http.favicon.hash:1592926977 -http.favicon.hash:2091717113 -http.favicon.hash:1924358485 -http.favicon.hash:1750461220 -http.favicon.hash:939607277 -http.favicon.hash:1750461220 -http.favicon.hash:-1439222863 -http.favicon.hash:-1750461220 -http.favicon.hash:444712798 "Python" "aiohttp" "Expires" -country:"CN"'''
        
        final_query = f"{base_query} {query}".strip() if query else base_query
        
        print(f"[+] Executing ComfyUI search: {final_query}")
        print(f"[+] Maximum results: {max_results}")
        
        try:
            results = api.search(final_query, limit=max_results)
            
            filtered_results = self._filter_results(results['matches'])
            
            self._display_results(filtered_results)
            
            self._save_results(filtered_results)
            
            return filtered_results
            
        except Exception as e:
            print(f"[!] Error during ComfyUI search: {e}")
            return []
    
    def _save_results(self, results):
        """
        Save search results to JSON file in results directory
        """
        if not results:
            return
            
        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comfyui-{timestamp}.json"
        filepath = os.path.join(results_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"[+] Results saved to: {filepath}")
    
    def _filter_results(self, results):
        """
        Filter ComfyUI search results to ensure quality.
        """
        filtered = []
        
        for result in results:
            if 'http' in result:
                filtered_result = {
                    'ip': result['ip_str'],
                    'port': result['port'],
                    'server': result['http'].get('server', 'Unknown'),
                    'title': result['http'].get('title', 'No title'),
                    'location': f"{result.get('country_name', 'Unknown')}/{result.get('city', 'Unknown')}",
                    'org': result.get('org', 'Unknown'),
                    'hostnames': result.get('hostnames', []),
                    'domains': result.get('domains', [])
                }
                
                if self._is_valid_comfyui_instance(filtered_result):
                    filtered.append(filtered_result)
        
        return filtered
    
    def _is_valid_comfyui_instance(self, result):
        """
        Verify if the result is a valid ComfyUI instance.
        """
        title = result['title'].lower()
        if 'comfyui' not in title and 'comfy ui' not in title:
            return False
        
        excluded_orgs = ['amazon', 'aws', 'google', 'microsoft', 'cloudflare']
        org = result['org'].lower()
        if any(excluded_org in org for excluded_org in excluded_orgs):
            return False
        
        return True
    
    def _display_results(self, results):
        """
        Display filtered ComfyUI results in a detailed format.
        """
        if not results:
            print("[!] No ComfyUI instances found after filtering")
            return
        
        print(f"\n[+] Found {len(results)} ComfyUI instances:")
        print("=" * 100)
        print("IP:Port          | Organization     | Location          | Title")
        print("-" * 100)
        
        for result in results:
            ip_port = f"{result['ip']}:{result['port']}"
            org = result['org'][:15] + "..." if len(result['org']) > 15 else result['org']
            location = result['location'][:15] + "..." if len(result['location']) > 15 else result['location']
            title = result['title'][:30] + "..." if len(result['title']) > 30 else result['title']
            
            print(f"{ip_port:<16} | {org:<15} | {location:<17} | {title}")
        
        print("=" * 100)
        print(f"[+] Search completed. Total ComfyUI instances found: {len(results)}")
        
        if results:
            print(f"\n[+] Statistics:")
            print(f"   - First result: {results[0]['ip']}:{results[0]['port']}")
            print(f"   - Last result: {results[-1]['ip']}:{results[-1]['port']}")
            
            # Count by country
            countries = {}
            for result in results:
                country = result['location'].split('/')[0]
                countries[country] = countries.get(country, 0) + 1
            
            print(f"   - By country: {', '.join([f'{k}: {v}' for k, v in countries.items()])}")

MODULE_INFO = """
=== COMFYUI MODULE INFORMATION ===

SEARCH QUERY:
http.title:"ComfyUI" -http.title:"ComfyUI Login" -org:"Amazon.com Inc." -org:"Amazon Data Services" -org:"Amazon Technologies" -org:"A100 ROW" -org:"Amazon Corporate Services Pty Ltd" -org:"AWS Asia Pacific (Seoul) Region" -http.favicon.hash:1045696447 -http.favicon.hash:1592926977 -http.favicon.hash:2091717113 -http.favicon.hash:1924358485 -http.favicon.hash:1750461220 -http.favicon.hash:939607277 -http.favicon.hash:1750461220 -http.favicon.hash:-1439222863 -http.favicon.hash:-1750461220 -http.favicon.hash:444712798 "Python" "aiohttp" "Expires" -country:"CN"

FILTERING:
- Excludes Amazon/AWS infrastructure
- Excludes specific favicon hashes (common false positives)
- Excludes Chinese locations
- Requires Python and aiohttp in response
- Requires "Expires" header

USAGE:
search comfyui    # Search for ComfyUI modules
use comfyui       # Select ComfyUI module
run               # Run with default query
run "port:8188"   # Run with custom port filter

OUTPUT:
- IP:Port combination
- Organization
- Geographic location
- Page title
- Additional statistics
"""

if __name__ == "__main__":
    print("ComfyUI Search Module for Dark Shodan")
    print(MODULE_INFO)