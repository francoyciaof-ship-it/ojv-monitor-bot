import json
import os
from scraper import OJVScraper
from github import Github

def create_github_issue(repo, titulo, cuerpo, labels=None):
    """Create a GitHub issue with the given title and body"""
    try:
        issue = repo.create_issue(
            title=titulo,
            body=cuerpo,
            labels=labels or []
        )
        print(f"Issue creado: {issue.html_url}")
        return issue
    except Exception as e:
        print(f"Error creando issue: {e}")
        return None

def format_causa_details(causa):
    """Format a single causa for display"""
    return f"""
**Sala:** {causa['sala']}
**Número en Tabla:** {causa['numero_tabla']}
**RIT/ROL:** {causa['rit_rol']}
**Relator:** {causa['relator']}
**Detectado:** {causa['timestamp']}
"""

def main():
    """Main execution"""
    print("=" * 50)
    print("OJV MONITOR BOT - Iniciando...")
    print("=" * 50)
    
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    rits_to_monitor = config.get('rits_to_monitor', [])
    github_token = os.environ.get('GITHUB_TOKEN', config.get('github_token'))
    
    if not rits_to_monitor:
        print("❌ No RITs configured for monitoring. Update config.json")
        return
    
    print(f"📋 RITs a monitorear: {', '.join(rits_to_monitor)}")
    
    # Initialize scraper
    scraper = OJVScraper()
    resultado = scraper.run(rits_to_monitor)
    
    if 'error' in resultado:
        print(f"❌ Error: {resultado['error']}")
        return
    
    print(f"✅ Total de causas encontradas: {resultado['total_causas']}")
    
    # Process changes
    cambios = resultado['cambios']
    nuevas = cambios['nuevas']
    desaparecidas = cambios['desaparecidas']
    
    # Create GitHub issues for new causas
    if nuevas:
        print(f"\n🆕 {len(nuevas)} NUEVAS CAUSA(S) ENCONTRADA(S)!")
        
        if github_token:
            try:
                g = Github(github_token)
                repo = g.get_user().get_repo('ojv-monitor-bot')
                
                for causa in nuevas:
                    titulo = f"⚠️ NUEVA CAUSA EN TABLA: {causa['rit_rol']}"
                    
                    cuerpo = f"""
## 🚨 Nueva Causa Detectada en Tabla

Una causa que estabas monitoreando ha aparecido en la tabla de la Oficina Judicial Virtual.

{format_causa_details(causa)}

---
**Acción recomendada:** Revisa la [Oficina Judicial Virtual](https://oficinajudicialvirtual.pjud.cl/indexN.php#) para más detalles.
"""
                    
                    create_github_issue(repo, titulo, cuerpo, labels=['causa-en-tabla', 'notificacion'])
                    print(f"  ✓ Issue creado para {causa['rit_rol']}")
            
            except Exception as e:
                print(f"⚠️ No se pudo conectar a GitHub: {e}")
        else:
            print("⚠️ GITHUB_TOKEN no configurado. Causas no registradas en issues.")
    else:
        print("\n✅ No hay nuevas causas en tabla")
    
    if desaparecidas:
        print(f"\n❌ {len(desaparecidas)} CAUSA(S) DESAPARECIDA(S) DE LA TABLA")
        for causa in desaparecidas:
            print(f"  • {causa['rit_rol']}")
    
    print("\n" + "=" * 50)
    print("Chequeo completado ✓")
    print("=" * 50)

if __name__ == "__main__":
    main()