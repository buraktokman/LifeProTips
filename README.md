# LifeProTips [![GitHub stars](https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Stars)](https://github.com/buraktokman/LifeProTips/)

[![Travis](https://img.shields.io/travis/rust-lang/rust.svg)](https://github.com/buraktokman/LifeProTips)
[![Repo](https://img.shields.io/badge/source-GitHub-303030.svg?maxAge=3600&style=flat-square)](https://github.com/buraktokman/LifeProTips)
[![Requires.io](https://img.shields.io/requires/github/celery/celery.svg)](https://requires.io/github/buraktokman/LifeProTips/requirements/?branch=master)
[![Scrutinizer](https://img.shields.io/scrutinizer/g/filp/whoops.svg)](https://github.com/buraktokman/LifeProTips)
[![DUB](https://img.shields.io/dub/l/vibe-d.svg)](https://choosealicense.com/licenses/mit/)
[![Donate with Bitcoin](https://img.shields.io/badge/Donate-BTC-orange.svg)](https://blockchain.info/address/17dXgYr48j31myKiAhnM5cQx78XBNyeBWM)
[![Donate with Ethereum](https://img.shields.io/badge/Donate-ETH-blue.svg)](https://etherscan.io/address/91dd20538de3b48493dfda212217036257ae5150)

Tips that improve your life in one way or another. This software downloads life tips from [reddit.com/r/LifeProTips](https://www.reddit.com/r/LifeProTips/top/) and tweets the most upvoted tips.

------
### Warning
Before using, modify account credentials in **inc** folder.

------
### Instructions

0. Fork, clone or download this repository.

1. Navigate to the directory.

2. Install requirements.

3. Run the script.

    ```bash
    git clone https://github.com/buraktokman/LifeProTips.git
    cd LifeProTips
    pip3 install -r requirements.txt
    python3 bot.py
    ```

------
### System Design

![system-design.drawio](docs/system-design.drawio.png)

------

### Versions

**0.1.3 beta (WIP)**

```
- [ ] WIP
- [x] History check on DynamoDB improved
```

**0.1.2 beta**

```
- [ ] WIP
- [x] Using Twitter threads for longer tips and for tips with added content
- [x] History check moved from S3 object storage to DynamoDB table
- [x] Lambda Layer creation bash script added to repository
- [x] Created dynamic structure for configuration load
- [x] First version of system design diagram added to documentation
- [x] Refactoring done
```

**0.1.1 beta**

- [x] Fetching via PRAW done.
- [x] Twitter API integration done.
- [x] AWS S3 integration done.
- [x] AWS Lambda functionality done.

---

### License

MIT License
