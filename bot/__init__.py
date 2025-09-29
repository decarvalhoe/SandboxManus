"""
Bot de Trading Athena
=====================

Bot de trading automatisé avec gestion des risques et monitoring intégré.

Architecture:
- apps/: Applications FastAPI et interfaces
- core/: Logique métier (signaux, sizing, risque, exécution)
- exchanges/: Adaptateurs pour les exchanges (ccxt)
- data/: Ingestion et stockage des données
- backtest/: Moteur de backtest
- paper/: Simulation de trading en temps réel
- monitoring/: Métriques et alertes
"""

__version__ = "1.0.0"
__author__ = "Trading Team"
__email__ = "trading@example.com"

# Configuration par défaut
DEFAULT_CONFIG = {
    "bot": {
        "name": "athena_trading_bot",
        "version": __version__,
        "mode": "paper"
    }
}
