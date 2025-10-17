#!/usr/bin/env python3
"""
Example Module for Dark Shodan - English Version
This module serves as documentation and example for creating new modules.
"""

import json

class ExampleModule:
    """
    Example module demonstrating the structure and functionality of Dark Shodan modules.
    
    This module shows:
    1. Basic module structure
    2. Search algorithm implementation
    3. Result filtering system
    4. Standardized output format
    """
    
    def __init__(self):
        # Required attributes for module identification
        self.name = "example"
        self.description = "Example module demonstrating module creation and search algorithms"
    
    def execute(self, api, query="port:80 product:Apache", max_results=50):
        """
        Main method for executing the module.
        
        Args:
            api: Shodan API object
            query: Search query (default: "port:80 product:Apache")
            max_results: Maximum number of results to return
            
        Returns:
            List of formatted results
        """
        
        print(f"[+] Executing search: {query}")
        print(f"[+] Maximum results: {max_results}")
        
        try:
            # Perform search using Shodan API
            results = api.search(query, limit=max_results)
            
            # Filter and process results
            filtered_results = self._filter_results(results['matches'])
            
            # Display results
            self._display_results(filtered_results)
            
            return filtered_results
            
        except Exception as e:
            print(f"[!] Error during search: {e}")
            return []
    
    def _filter_results(self, results):
        """
        Filter search results based on specific criteria.
        
        This demonstrates optional filtering algorithms that can be added to modules.
        """
        filtered = []
        
        for result in results:
            # Basic filtering - only include results with HTTP data
            if 'http' in result:
                filtered_result = {
                    'ip': result['ip_str'],
                    'port': result['port'],
                    'server': result['http'].get('server', 'Unknown'),
                    'title': result['http'].get('title', 'No title'),
                    'location': f"{result.get('country_name', 'Unknown')}/{result.get('city', 'Unknown')}"
                }
                
                # Additional filtering - only include interesting servers
                interesting_servers = ['Apache', 'nginx', 'IIS', 'lighttpd']
                if any(server in filtered_result['server'] for server in interesting_servers):
                    filtered.append(filtered_result)
        
        return filtered
    
    def _display_results(self, results):
        """
        Display filtered results in a standardized format.
        
        This demonstrates the recommended output format for modules.
        """
        if not results:
            print("[!] No results found after filtering")
            return
        
        print(f"\n[+] Found {len(results)} devices:")
        print("=" * 80)
        print("IP:Port          | Server           | Title                    | Location")
        print("-" * 80)
        
        for result in results:
            ip_port = f"{result['ip']}:{result['port']}"
            server = result['server'][:15] + "..." if len(result['server']) > 15 else result['server']
            title = result['title'][:25] + "..." if len(result['title']) > 25 else result['title']
            
            print(f"{ip_port:<16} | {server:<16} | {title:<25} | {result['location']}")
        
        print("=" * 80)
        print(f"[+] Search completed. Total devices found: {len(results)}")

# Documentation for module developers
MODULE_DOCUMENTATION = """
=== MODULE CREATION GUIDE ===

1. BASIC STRUCTURE:
   - Each module must be a Python class
   - Required attributes: name, description
   - Required method: execute(api, query, max_results)

2. SEARCH ALGORITHM:
   - Use api.search(query, limit=max_results)
   - Handle exceptions properly
   - Return list of results

3. FILTERING SYSTEM (OPTIONAL):
   - Add _filter_results() method
   - Implement custom filtering logic
   - Return filtered results

4. OUTPUT FORMAT:
   - Use standardized display format
   - Include IP:Port, Server, Title, Location
   - Provide statistics and summary

5. EXAMPLE QUERIES:
   - "port:80 product:Apache"
   - "port:443 ssl:true"
   - "country:US product:nginx"
   - "city:New York port:8080"

6. BEST PRACTICES:
   - Add error handling
   - Include documentation
   - Use descriptive variable names
   - Follow PEP8 style guide
"""

if __name__ == "__main__":
    # Demo execution
    print("This is an example module. Import it in Dark Shodan to use.")
    print(MODULE_DOCUMENTATION)