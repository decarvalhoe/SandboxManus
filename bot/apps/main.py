"""
Point d'entrée principal du bot de trading Athena.
"""

import asyncio
import logging
import os
import signal
import sys
from pathlib import Path

import yaml
from bot.core.bot_manager import BotManager
from bot.monitoring.logger import setup_logging


class TradingBotApp:
    """Application principale du bot de trading."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.getenv("CONFIG_PATH", "bot_config.yaml")
        self.config = self._load_config()
        self.bot_manager = None
        self.running = False
        
        # Configuration du logging
        setup_logging(self.config.get("development", {}).get("log_level", "INFO"))
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> dict:
        """Charge la configuration depuis le fichier YAML."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.error(f"Fichier de configuration non trouvé: {self.config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            self.logger.error(f"Erreur de parsing YAML: {e}")
            sys.exit(1)
    
    def _setup_signal_handlers(self):
        """Configure les gestionnaires de signaux pour un arrêt propre."""
        def signal_handler(signum, frame):
            self.logger.info(f"Signal {signum} reçu, arrêt du bot...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def start(self):
        """Démarre le bot de trading."""
        self.logger.info("Démarrage du bot de trading Athena...")
        self.logger.info(f"Mode: {self.config['bot']['mode']}")
        
        try:
            # Initialisation du gestionnaire de bot
            self.bot_manager = BotManager(self.config)
            await self.bot_manager.initialize()
            
            # Configuration des gestionnaires de signaux
            self._setup_signal_handlers()
            
            # Boucle principale
            self.running = True
            while self.running:
                try:
                    await self.bot_manager.run_cycle()
                    await asyncio.sleep(1)  # Pause entre les cycles
                except Exception as e:
                    self.logger.error(f"Erreur dans le cycle principal: {e}")
                    if self.config['bot'].get('ops', {}).get('kill_switch', True):
                        self.logger.critical("Kill switch activé, arrêt du bot")
                        break
                    await asyncio.sleep(5)  # Pause plus longue en cas d'erreur
            
        except Exception as e:
            self.logger.critical(f"Erreur critique: {e}")
            raise
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Nettoyage et fermeture propre."""
        self.logger.info("Nettoyage en cours...")
        if self.bot_manager:
            await self.bot_manager.cleanup()
        self.logger.info("Bot arrêté proprement")


async def main():
    """Fonction principale."""
    app = TradingBotApp()
    await app.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\nArrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"Erreur fatale: {e}")
        sys.exit(1)
