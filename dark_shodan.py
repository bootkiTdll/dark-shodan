#!/usr/bin/env python3

import os
import importlib
import json
import shodan
from colorama import init, Fore, Style

init()

class DarkShodan:
    def __init__(self):
        self.api_key = None
        self.api = None
        self.modules = {}
        self.current_module = None
        self.last_search_results = []
        self.language = 'eng'
        self.translations = {}
        self.config = {}
        self.load_config('config.json')
        self.load_language()
        self.load_modules()

    def load_language(self):
        try:
            lang_file = f"{self.language}.lng"
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
        except Exception as e:
            print(f"{Fore.RED}{self.t('errors.lang_load', e)}{Style.RESET_ALL}")

    def t(self, key, *args):
        value = self.translations
        for part in key.split('.'):
            value = value.get(part, {})
        if isinstance(value, str):
            return value.format(*args) if args else value
        return key

    def load_modules(self):
        modules_dir = os.path.join(os.path.dirname(__file__), self.config.get('modules_path', 'modules'))
        for file in os.listdir(modules_dir):
            if file.endswith('.py') and file != '__init__.py':
                module_name = file[:-3]
                try:
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(modules_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and hasattr(attr, 'execute'):
                            self.modules[attr.__name__.lower()] = attr()
                except Exception as e:
                    print(f"{Fore.RED}{self.t('errors.module_load', module_name, e)}{Style.RESET_ALL}")

    def connect(self):
        if not self.api_key:
            self.api_key = input(f"{Fore.YELLOW}{self.t('enter_api_key')} {Style.RESET_ALL}")
        try:
            self.api = shodan.Shodan(self.api_key)
            info = self.api.info()
            available_credits = info.get('query_credits', 0)
            min_requests = self.config.get('default:min_requests', 10)
            if available_credits < min_requests:
                print(f"{Fore.RED}{self.t('errors.no_suitable_keys', min_requests)}{Style.RESET_ALL}")
                self.api = None
                return False
            print(f"{Fore.GREEN}{self.t('success.connected')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{self.t('success.available_requests', available_credits)}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}{self.t('errors.connect', e)}{Style.RESET_ALL}")
            return False

    def autoconnect(self, file_path=None, min_requests=None):
        if file_path is None:
            file_path = self.config.get('autoconnect:api_key_file', 'api_keys.txt')
        if min_requests is None:
            min_requests = self.config.get('autoconnect:min_requests', 10)
        if not os.path.exists(file_path):
            print(f"{Fore.RED}{self.t('errors.file_not_found', file_path)}{Style.RESET_ALL}")
            return False
        try:
            with open(file_path, 'r') as f:
                api_keys = [line.strip() for line in f if line.strip()]
            print(f"{Fore.YELLOW}{self.t('errors.api_keys_found', len(api_keys))}{Style.RESET_ALL}")
            for api_key in api_keys:
                try:
                    test_api = shodan.Shodan(api_key)
                    info = test_api.info()
                    available_credits = info.get('query_credits', 0)
                    print(f"{Fore.CYAN}{self.t('errors.key_check', api_key[:10], available_credits)}{Style.RESET_ALL}")
                    if available_credits >= min_requests:
                        self.api_key = api_key
                        self.api = test_api
                        print(f"{Fore.GREEN}{self.t('errors.suitable_key', available_credits)}{Style.RESET_ALL}")
                        return True
                except Exception as e:
                    print(f"{Fore.RED}{self.t('errors.key_error', api_key[:10], e)}{Style.RESET_ALL}")
            print(f"{Fore.RED}{self.t('errors.no_suitable_keys', min_requests)}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}{self.t('errors.file_read_error', e)}{Style.RESET_ALL}")
            return False

    def show_banner(self):
        banner = f"""
{Fore.RED}
  ██████╗  █████╗ ██████╗ ██╗  ██╗    ███████╗██╗  ██╗ ██████╗ ██████╗  █████╗ ███╗   ██╗
  ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔══██╗████╗  ██║
  ██║  ██║███████║██████╔╝█████╔╝     ███████╗███████║██║   ██║██║  ██║███████║██╔██╗ ██║
  ██║  ██║██╔══██║██╔══██╗██╔═██╗     ╚════██║██╔══██║██║   ██║██║  ██║██╔══██║██║╚██╗██║
  ██████╔╝██║  ██║██║  ██║██║  ██╗    ███████║██║  ██║╚██████╔╝██████╔╝██║  ██║██║ ╚████║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
{Style.RESET_ALL}
        """
        print(banner)
        print(f"{Fore.CYAN}{self.t('banner')}{Style.RESET_ALL}")

    def search_modules(self, query):
        results_raw = [(n, m) for n, m in self.modules.items() if query.lower() in n.lower() or query.lower() in m.name.lower()]
        if results_raw:
            print(f"\n{Fore.CYAN}{self.t('search.results')}{Style.RESET_ALL}")
            self.last_search_results = []
            for idx, (name, module) in enumerate(results_raw, 1):
                print(f"{Fore.GREEN}[{idx}] {module.name} - {module.description}{Style.RESET_ALL}")
                self.last_search_results.append((idx, name, module))
        else:
            print(f"{Fore.YELLOW}{self.t('errors.module_not_found')}{Style.RESET_ALL}")
            self.last_search_results = []

    def use_module(self, identifier):
        if not self.last_search_results and not identifier.isdigit():
            print(f"{Fore.YELLOW}{self.t('errors.search_first')}{Style.RESET_ALL}")
            return
        if identifier.isdigit():
            index = int(identifier) - 1
            if 0 <= index < len(self.last_search_results):
                _, _, module = self.last_search_results[index]
                self.current_module = module
                print(f"{Fore.GREEN}{self.t('errors.module_used', module.name)}{Style.RESET_ALL}")
                self.run_module()
            else:
                print(f"{Fore.RED}{self.t('errors.invalid_module')}{Style.RESET_ALL}")
        else:
            if identifier in self.modules:
                self.current_module = self.modules[identifier]
                print(f"{Fore.GREEN}{self.t('errors.module_used', self.current_module.name)}{Style.RESET_ALL}")
                self.run_module()
            else:
                print(f"{Fore.RED}{self.t('errors.module_not_found_single')}{Style.RESET_ALL}")

    def run_module(self, query=""):
        if not self.current_module:
            print(f"{Fore.YELLOW}{self.t('errors.select_module_first')}{Style.RESET_ALL}")
            return
        if not self.api and not self.connect():
            return
        try:
            max_results = self.config.get('default:max_results', 50)
            result = self.current_module.execute(self.api, query, max_results)
            if hasattr(result, '__iter__') and not isinstance(result, str):
                print(f"{Fore.GREEN}{self.t('success.module_executed')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.WHITE}{result}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{self.t('errors.module_load', 'execution', e)}{Style.RESET_ALL}")

    def search_direct(self, query, filter_file=None):
        """
        Perform direct Shodan search without modules
        """
        if not self.api and not self.connect():
            return
        
        try:
            max_results = self.config.get('default:max_results', 50)
            print(f"{Fore.CYAN}{self.t('search.executing_direct', query)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{self.t('search.max_results', max_results)}{Style.RESET_ALL}")
            
            results = self.api.search(query, limit=max_results)
            
            filter_config = None
            if filter_file:
                filter_config = self._load_filter_config(filter_file)
            
            self._display_search_results(results['matches'], filter_config)
            
            self._save_search_results(results['matches'])
            
            return results['matches']
            
        except Exception as e:
            print(f"{Fore.RED}{self.t('errors.direct_search_error', e)}{Style.RESET_ALL}")
            return []
    
    def _load_filter_config(self, filter_file):
        """Load JSON filter configuration"""
        try:
            filter_path = os.path.join('filters', filter_file)
            if not os.path.exists(filter_path):
                filter_path = filter_file
            
            with open(filter_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"{Fore.YELLOW}{self.t('errors.filter_load_error', e)}{Style.RESET_ALL}")
            return None
    
    def _display_search_results(self, results, filter_config=None):
        """Display search results with optional filtering"""
        if not results:
            print(f"{Fore.YELLOW}{self.t('errors.no_results')}{Style.RESET_ALL}")
            return
        
        filtered_results = self._apply_filter(results, filter_config)
        
        if not filtered_results:
            print(f"{Fore.YELLOW}{self.t('errors.no_results_filtered')}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}{self.t('search.found_devices', len(filtered_results))}{Style.RESET_ALL}")
        print("=" * 100)
        
        print("-" * 100)
        
        for result in filtered_results:
            ip_port = f"{result.get('ip_str', 'N/A')}:{result.get('port', 'N/A')}"
            org = result.get('org', 'Unknown')[:20]
            country = result.get('location', {}).get('country_name', 'Unknown')[:15]
            city = result.get('location', {}).get('city', 'Unknown')[:15]
            product = result.get('product', 'Unknown')[:20]
            
            print(f"{ip_port:<16} | {org:<20} | {country:<15} | {city:<15} | {product:<20}")
        
        print("=" * 100)
        print(f"{Fore.GREEN}{self.t('search.completed', len(filtered_results))}{Style.RESET_ALL}")
    
    def _apply_filter(self, results, filter_config):
        """Apply filtering based on JSON configuration"""
        if not filter_config:
            return results
        
        filtered = []
        
        for result in results:
            org = result.get('org', '')
            if org and 'filters' in filter_config and 'exclude_orgs' in filter_config['filters']:
                if any(excluded_org.lower() in org.lower() for excluded_org in filter_config['filters']['exclude_orgs']):
                    continue
            
            country = result.get('location', {}).get('country_name', '')
            if country and 'filters' in filter_config:
                if (filter_config['filters'].get('include_countries') and 
                    country not in filter_config['filters']['include_countries']):
                    continue
                if (filter_config['filters'].get('exclude_countries') and 
                    country in filter_config['filters']['exclude_countries']):
                    continue
            
            port = result.get('port', 0)
            if 'filters' in filter_config:
                min_port = filter_config['filters'].get('min_port', 1)
                max_port = filter_config['filters'].get('max_port', 65535)
                if not (min_port <= port <= max_port):
                    continue
            
            filtered.append(result)
        
        return filtered
    
    def _save_search_results(self, results):
        """Save search results to JSON file"""
        if not results:
            return
            
        results_dir = os.path.join(os.path.dirname(__file__), 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"direct_search-{timestamp}.json"
        filepath = os.path.join(results_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"{Fore.GREEN}{self.t('search.results_saved', filepath)}{Style.RESET_ALL}")

    def show_help(self):
        help_order = [
            ('search <query>', 'commands.search'),
            ('find <query> <filter>', 'commands.find'),
            ('use <number/name>', 'commands.use'),
            ('connect', 'commands.connect'),
            ('autoconnect <file> <requests>', 'commands.autoconnect'),
            ('set lang <ru/eng>', 'commands.set_lang'),
            ('set cfg <filename>', 'commands.set_cfg'),
            ('clear', 'commands.clear'),
            ('help', 'commands.help'),
            ('exit', 'commands.exit')
        ]
        print(f"{Fore.CYAN}{self.t('commands.help')}{Style.RESET_ALL}")
        for cmd, key in help_order:
            print(f"{Fore.GREEN}{cmd.ljust(44)}{Fore.WHITE}- {self.t(key)}{Style.RESET_ALL}")

    def set_language(self, lang):
        if lang in ['ru', 'eng']:
            self.language = lang
            self.load_language()
            print(f"{Fore.GREEN}{self.t('errors.lang_changed', lang)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{self.t('errors.invalid_lang')}{Style.RESET_ALL}")

    def load_config(self, cfg_file):
        try:
            if not os.path.exists(cfg_file):
                print(f"{Fore.RED}{self.t('errors.file_not_found', cfg_file)}{Style.RESET_ALL}")
                return False
            with open(cfg_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            if 'language' in self.config:
                self.language = self.config['language']
                self.load_language()
            print(f"{Fore.GREEN}{self.t('success.config_loaded', cfg_file)}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}{self.t('errors.config_load', e)}{Style.RESET_ALL}")
            return False

    def start(self):
        self.show_banner()
        print(f"{Fore.YELLOW}{self.t('modules_loaded', len(self.modules))}{Style.RESET_ALL}")
        if self.config.get('autoconnect:enable', False):
            print(f"{Fore.YELLOW}{self.t('autoconnect.auto_connecting')}{Style.RESET_ALL}")
            self.autoconnect()
        while True:
            try:
                parts = input(f"{Fore.RED}{self.t('prompt')}{Style.RESET_ALL} ").strip().split()
                if not parts:
                    continue
                if parts[0] == 'search':
                    self.search_modules(' '.join(parts[1:]))
                elif parts[0] == 'use':
                    if len(parts) > 1:
                        self.use_module(parts[1])
                    else:
                        print(f"{Fore.YELLOW}{self.t('errors.specify_module')}{Style.RESET_ALL}")
                elif parts[0] == 'connect':
                    if len(parts) > 1:
                        self.api_key = parts[1]
                    self.connect()
                elif parts[0] == 'autoconnect' and len(parts) == 3:
                    try:
                        self.autoconnect(parts[1], int(parts[2]))
                    except ValueError:
                        print(f"{Fore.RED}{self.t('errors.invalid_requests')}{Style.RESET_ALL}")
                elif parts[0] == 'find' and len(parts) >= 2:
                    search_query = parts[1]
                    filter_file = parts[2] if len(parts) > 2 else None
                    self.search_direct(search_query, filter_file)
                elif parts[0] == 'set' and len(parts) > 2:
                    if parts[1] == 'lang':
                        self.set_language(parts[2])
                    elif parts[1] == 'cfg':
                        self.load_config(parts[2])
                elif parts[0] == 'help':
                    self.show_help()
                elif parts[0] == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif parts[0] == 'exit':
                    print(f"{Fore.YELLOW}{self.t('success.exit')}{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}{self.t('errors.unknown_command')}{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}{self.t('success.exit')}{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}{self.t('errors.generic', e)}{Style.RESET_ALL}")

if __name__ == '__main__':
    DarkShodan().start()