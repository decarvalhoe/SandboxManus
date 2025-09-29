# Bot de Trading Athena

Bot de trading automatisé avec gestion des risques intégrée, monitoring en temps réel et architecture modulaire pour les marchés de cryptomonnaies.

## Architecture du Projet

Le projet suit une architecture modulaire organisée selon les meilleures pratiques de développement de systèmes de trading automatisés. L'ensemble du système est conçu pour être robuste, sécurisé et facilement extensible.

### Structure des Dossiers

```
bot/
├── apps/           # Applications FastAPI et interfaces utilisateur
├── core/           # Logique métier (signaux, sizing, risque, exécution)
├── exchanges/      # Adaptateurs pour les exchanges (ccxt)
├── data/           # Ingestion et stockage des données de marché
├── backtest/       # Moteur de backtest et validation des stratégies
├── paper/          # Simulation de trading en temps réel
├── monitoring/     # Métriques, alertes et dashboards
├── configs/        # Fichiers de configuration
├── tests/          # Tests unitaires et d'intégration
└── docs/           # Documentation technique
```

## Fonctionnalités Principales

### Gestion des Risques

Le système intègre plusieurs niveaux de protection pour minimiser les pertes et protéger le capital. La gestion des risques comprend des limites d'exposition par symbole, des plafonds de pertes journalières et un système de kill-switch automatique en cas de conditions de marché défavorables.

### Stratégies de Trading

Le bot supporte actuellement les stratégies de mean reversion basées sur l'indicateur RSI, avec la possibilité d'étendre facilement vers d'autres approches comme le momentum trading ou le market making. Chaque stratégie est configurable via des paramètres YAML.

### Monitoring et Alertes

L'infrastructure de monitoring utilise Prometheus pour la collecte de métriques et Grafana pour la visualisation. Le système peut envoyer des alertes via Telegram en cas d'événements critiques ou de conditions de marché particulières.

## Configuration Rapide

### Prérequis Système

Le projet nécessite Python 3.11 ou supérieur, Docker et Docker Compose pour l'infrastructure de données. Les dépendances Python incluent ccxt pour la connectivité aux exchanges, pandas pour l'analyse de données et FastAPI pour l'interface de contrôle.

### Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/decarvalhoe/SandboxManus.git
   cd SandboxManus
   ```

2. **Configurer l'environnement**
   ```bash
   cp .env.example .env
   # Éditer .env avec vos clés API testnet
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Démarrer l'infrastructure**
   ```bash
   docker-compose up -d timescaledb redis prometheus grafana
   ```

### Configuration du Bot

Le fichier `bot_config.yaml` contient toute la configuration du bot. Les paramètres principaux incluent la sélection des exchanges, les symboles à trader, les paramètres de stratégie et les limites de risque.

**Exemple de configuration pour débuter :**

```yaml
bot:
  name: "athena_trading_bot_v1"
  mode: "paper"
  exchanges:
    - name: "binance"
      market: "futures"
      symbols: ["BTCUSDT", "ETHUSDT"]
  strategy:
    type: "mean_reversion"
    entry:
      rsi_low: 28
    exit:
      rsi_high: 68
  risk:
    daily_loss_cap_pct: 2.0
    max_position_per_symbol_pct: 20
```

## Utilisation

### Mode Paper Trading

Le mode paper trading permet de tester les stratégies sans risquer de capital réel. Toutes les fonctionnalités sont disponibles, mais les ordres sont simulés.

```bash
python -m bot.apps.main
```

### Mode Live Trading

**⚠️ Attention :** Le mode live utilise de l'argent réel. Assurez-vous d'avoir testé votre configuration en mode paper avant de passer en live.

```bash
# Modifier bot_config.yaml : mode: "live"
python -m bot.apps.main
```

### Interface de Monitoring

Les dashboards Grafana sont accessibles sur `http://localhost:3000` (admin/admin par défaut). Ils affichent les métriques de performance, l'exposition du portefeuille et les signaux générés en temps réel.

## Sécurité et Bonnes Pratiques

### Gestion des Clés API

Les clés API ne doivent jamais être stockées en dur dans le code. Utilisez le fichier `.env` pour les variables d'environnement et configurez des clés avec des permissions limitées (trading uniquement, pas de retrait).

### Kill Switch

Le système dispose d'un kill switch automatique qui s'active en cas de pertes excessives ou d'erreurs répétées. Un bouton d'arrêt d'urgence manuel est également disponible via l'API.

### Audit et Logging

Toutes les décisions de trading sont loggées avec horodatage précis pour permettre l'audit et l'analyse post-mortem. Les logs incluent les signaux générés, les ordres exécutés et les métriques de performance.

## Développement et Extension

### Ajouter une Nouvelle Stratégie

Pour implémenter une nouvelle stratégie de trading, créez une classe héritant de `BaseStrategy` dans le module `bot/core/strategies/`. La stratégie doit implémenter les méthodes `generate_signals()` et `validate_signal()`.

### Tests et Validation

Le projet inclut une suite de tests complète couvrant les composants critiques. Exécutez les tests avant de déployer des modifications :

```bash
pytest bot/tests/ -v --cov=bot
```

### Backtest des Stratégies

Le moteur de backtest permet de valider les stratégies sur des données historiques avec des coûts de transaction réalistes :

```bash
python -m bot.backtest.runner --config backtest_config.yaml
```

## Support et Contribution

### Signalement de Bugs

Pour signaler un bug ou demander une fonctionnalité, ouvrez une issue sur GitHub avec une description détaillée et les étapes de reproduction.

### Contribution au Code

Les contributions sont les bienvenues. Assurez-vous de suivre les conventions de code (Black, flake8) et d'inclure des tests pour les nouvelles fonctionnalités.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Avertissement

Le trading automatisé comporte des risques financiers importants. Ce logiciel est fourni à des fins éducatives et de recherche. Les utilisateurs sont responsables de leurs décisions d'investissement et des pertes potentielles.
