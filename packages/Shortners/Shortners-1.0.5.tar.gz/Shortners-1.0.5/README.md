<p align="center">
    PYTHON URL SHORTNER © 2023
</p>

<p align="center">
   <a href="https://telegram.dog/clinton_abraham"><img src="https://img.shields.io/badge/𝑪𝒍𝒊𝒏𝒕𝒐𝒏 𝑨𝒃𝒓𝒂𝒉𝒂𝒎-30302f?style=flat&logo=telegram" alt="telegram badge"/a>
   <a href="https://telegram.dog/Space_x_bots"><img src="https://img.shields.io/badge/Sᴘᴀᴄᴇ ✗ ʙᴏᴛꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/a>
   <a href="https://telegram.dog/sources_codes"><img src="https://img.shields.io/badge/Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/a>
</p>

## INSTALLATION
```bash
pip install shortners
```

```python

import asyncio
from Shortners import Shortners

shortner_api = "a1cgsja52iey3j53mg"
shortner_url = "https://tnshort.net/api"
contents_url = "https://github.com/Clinton-Abraham"

core = Shortners(shortner_api, shortner_url)

async def test():
    o = await core.shortlink(contents_url)
    print(o)

asyncio.run(test())

```
