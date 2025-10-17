#!/usr/bin/env python3

class YourModuleName:
    def __init__(self):
        self.name = "Easy Example" # place name of module here
        self.description = "the easy example module" # place description of module here

    def execute(self, api, query=""): # execute method
        try:
            results = api.search(query or 'here is a query') # place query here
            filtered = self._filter_results(results['matches'])
            output = self._format_output(filtered)
            output.insert(0, f"=== {self.name} ===")
            output.insert(1, f"Query: {query}")
            output.insert(2, f"Found: {len(filtered)}")
            output.insert(3, "-" * 50)
            return output
        except Exception as e:
            return [f"Error: {e}"]

    def _format_output(self, devices): # simple format output data
        output = []
        for d in devices:
            line = f"{d['ip_str']}:{d['port']}"
            output.append(line)
        return output