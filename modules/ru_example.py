#!/usr/bin/env python3
"""
Пример модуля для Dark Shodan с документацией по созданию модулей

Этот модуль демонстрирует:
1. Структуру модуля
2. Алгоритм поиска
3. Систему фильтрации
4. Формат вывода результатов
"""

class ExampleModule:
    def __init__(self):
        self.name = "Example Module"
        self.description = "Демонстрационный модуль с документацией"
        
        # Документация по созданию модулей
        self.documentation = {
            'structure': {
                'class_name': "Должен наследоваться от object",
                'required_methods': ["__init__", "execute"],
                'required_attributes': ["name", "description"]
            },
            'search_algorithm': {
                'query_construction': "Использовать shodan.search() с фильтрами",
                'common_filters': ["port", "country", "os", "product"],
                'result_processing': "Обработка результатов через цикл"
            },
            'filter_system': {
                'optional': "Можно добавить методы фильтрации",
                'examples': ["по стране", "по порту", "по версии ПО"]
            },
            'output_format': {
                'standard': "Вывод в формате список строк",
                'recommended': "IP:Port - Информация",
                'extended': "Дополнительные данные через |"
            }
        }
    
    def execute(self, api, query=""):
        """
        Основной метод выполнения модуля
        
        Args:
            api: Объект Shodan API
            query: Поисковый запрос (опционально)
            
        Returns:
            list: Список найденных устройств
        """
        
        # Демонстрационный поисковый запрос
        search_query = query if query else "port:80 http"
        
        try:
            # Выполнение поиска через Shodan API
            results = api.search(search_query)
            
            # Обработка и фильтрация результатов
            filtered_devices = self._filter_results(results['matches'])
            
            # Форматирование вывода
            output = self._format_output(filtered_devices)
            
            # Добавление информации о модуле
            output.insert(0, f"=== {self.name} ===")
            output.insert(1, f"Запрос: {search_query}")
            output.insert(2, f"Найдено устройств: {len(filtered_devices)}")
            output.insert(3, "-" * 50)
            
            return output
            
        except Exception as e:
            return [f"Ошибка выполнения: {e}"]
    
    def _filter_results(self, devices):
        """
        Фильтрация результатов поиска
        
        Args:
            devices: Список устройств от Shodan
            
        Returns:
            list: Отфильтрованный список устройств
        """
        filtered = []
        
        for device in devices:
            # Пример фильтрации: только устройства с HTTP заголовками
            if 'http' in device and 'title' in device['http']:
                # Дополнительная фильтрация по желанию
                if self._is_interesting_device(device):
                    filtered.append(device)
        
        return filtered
    
    def _is_interesting_device(self, device):
        """
        Дополнительная проверка устройства
        
        Args:
            device: Данные устройства
            
        Returns:
            bool: True если устройство интересное
        """
        # Пример критериев отбора:
        # 1. Наличие определенного заголовка
        # 2. Конкретная версия ПО
        # 3. Географическое положение
        
        http_data = device.get('http', {})
        
        # Фильтр по заголовку сервера
        server_header = http_data.get('server', '').lower()
        interesting_servers = ['apache', 'nginx', 'iis']
        
        return any(server in server_header for server in interesting_servers)
    
    def _format_output(self, devices):
        """
        Форматирование вывода результатов
        
        Args:
            devices: Список устройств
            
        Returns:
            list: Отформатированные строки вывода
        """
        output = []
        
        for i, device in enumerate(devices, 1):
            ip = device['ip_str']
            port = device['port']
            
            # Основная информация
            info = f"{ip}:{port}"
            
            # Дополнительная информация
            http_data = device.get('http', {})
            if http_data:
                server = http_data.get('server', 'Unknown')
                title = http_data.get('title', 'No title')
                info += f" | Server: {server} | Title: {title}"
            
            # Географическая информация
            location = device.get('location', {})
            if location:
                country = location.get('country_name', 'Unknown')
                city = location.get('city', 'Unknown')
                info += f" | Location: {country}, {city}"
            
            output.append(info)
        
        return output
    
    def show_documentation(self):
        """
        Вывод документации по созданию модулей
        """
        docs = []
        docs.append("=== ДОКУМЕНТАЦИЯ ПО СОЗДАНИЮ МОДУЛЕЙ ===")
        
        for section, content in self.documentation.items():
            docs.append(f"\n--- {section.upper()} ---")
            
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, list):
                        docs.append(f"  {key}: {', '.join(value)}")
                    else:
                        docs.append(f"  {key}: {value}")
            else:
                docs.append(f"  {content}")
        
        return docs

# Пример использования документации
if __name__ == "__main__":
    module = ExampleModule()
    print("\n".join(module.show_documentation()))