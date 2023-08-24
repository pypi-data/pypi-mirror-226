<img src="https://github.com/Solcast/solcast-api-python-sdk/blob/main/docs/img/logo.png?raw=true" width="100" align="right">

# Solcast API Python SDK

<em>simple Python SDK to access the Solcast API</em>

[![Docs](https://github.com/Solcast/solcast-api-python-sdk/actions/workflows/docs.yml/badge.svg)](https://github.com/Solcast/solcast-api-python-sdk/actions/workflows/docs.yml) [![Tests](https://github.com/Solcast/solcast-api-python-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/Solcast/solcast-api-python-sdk/actions/workflows/test.yml) [![Publish 📦 to PyPI](https://github.com/Solcast/solcast-api-python-sdk/actions/workflows/publish-to-test-pypi.yml/badge.svg)](https://github.com/Solcast/solcast-api-python-sdk/actions/workflows/publish-to-test-pypi.yml)

---

**Documentation**: <a href="https://solcast.github.io/solcast-api-python-sdk/" target="_blank">https://solcast.github.io/solcast-api-python-sdk/ </a>

## Install
```commandline
git clone https://github.com/Solcast/solcast-api-python-sdk.git
cd solcast-api-python-sdk
pip install .
# also pip install .[all] for the dev libs
```
## Basic Usage

```python
from solcast import live

df = live.radiation_and_weather(
    latitude=-33.856784,
    longitude=151.215297,
    output_parameters=['air_temp', 'dni', 'ghi']
).to_pandas()
```
---

## Contributing
```commandline
pytest tests
```
