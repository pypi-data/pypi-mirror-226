# Gitea Actions Webscraper

```py
from gitea_actions_webscraper import GiteaActionsWebscraper
import json

gitea_actions_webscraper = GiteaActionsWebscraper('https://codeberg.org', 'User/Repository', 'YOUR_i_like_gitea_COOKIE')
actions = gitea_actions_webscraper.getFirstActionsPage()
lastAction = actions[0]
print(lastAction.commitTitle)
print(json.dumps(lastAction.getArtifacts(), indent = 4))
print(json.dumps(lastAction.getLogs(), indent = 4))
messages = '\n'.join([stepLog['message'] for stepLog in lastAction.getStepLogs(0)])
print(messages)
```
