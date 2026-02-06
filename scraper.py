import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import re

class OJVScraper:
    def __init__(self):
        self.base_url = "https://oficinajudicialvirtual.pjud.cl/indexN.php#"
        self.data_file = "data/causas_data.json"
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def fetch_ojv_page(self) -> str:
        """Fetch the OJV website"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.base_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching OJV page: {e}")
            return None
    
    def parse_causas_table(self, html: str) -> List[Dict]:
        """Parse the causas table from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            causas = []
            
            # Find the table containing causas
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        causa = {
                            'sala': cols[0].text.strip(),
                            'numero_tabla': cols[1].text.strip(),
                            'rit_rol': cols[2].text.strip(),
                            'relator': cols[3].text.strip(),
                            'timestamp': datetime.now().isoformat()
                        }
                        causas.append(causa)
            
            return causas
        except Exception as e:
            print(f"Error parsing table: {e}")
            return []
    
    def load_previous_data(self) -> Dict[str, List[Dict]]:
        """Load previously stored causas data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading previous data: {e}")
            return {}
    
    def save_causas_data(self, causas: List[Dict]):
        """Save causas data to file"""
        try:
            data = self.load_previous_data()
            timestamp = datetime.now().isoformat()
            data[timestamp] = causas
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def compare_causas(self, current: List[Dict], rits_to_monitor: List[str]) -> Dict:
        """Compare current causas with previous data and identify new ones"""
        previous_data = self.load_previous_data()
        
        if not previous_data:
            return {'nuevas': current, 'desaparecidas': []}
        
        # Get the last stored causas
        last_causas = list(previous_data.values())[-1] if previous_data else []
        
        # Filter by monitored RITs
        current_filtered = [c for c in current if c['rit_rol'] in rits_to_monitor]
        last_filtered = [c for c in last_causas if c['rit_rol'] in rits_to_monitor]
        
        # Create sets for comparison
        current_rits = {c['rit_rol'] for c in current_filtered}
        last_rits = {c['rit_rol'] for c in last_filtered}
        
        # Find new and disappeared causas
        nuevas_rits = current_rits - last_rits
        desaparecidas_rits = last_rits - current_rits
        
        nuevas = [c for c in current_filtered if c['rit_rol'] in nuevas_rits]
        desaparecidas = [c for c in last_filtered if c['rit_rol'] in desaparecidas_rits]
        
        return {
            'nuevas': nuevas,
            'desaparecidas': desaparecidas
        }
    
    def run(self, rits_to_monitor: List[str]) -> Dict:
        """Main execution method"""
        print("Iniciando scraping de OJV...")
        
        html = self.fetch_ojv_page()
        if not html:
            return {'error': 'No se pudo obtener la página de OJV'}
        
        causas = self.parse_causas_table(html)
        print(f"Se encontraron {len(causas)} causas en la tabla")
        
        self.save_causas_data(causas)
        
        cambios = self.compare_causas(causas, rits_to_monitor)
        
        return {
            'total_causas': len(causas),
            'causas': causas,
            'cambios': cambios
        }