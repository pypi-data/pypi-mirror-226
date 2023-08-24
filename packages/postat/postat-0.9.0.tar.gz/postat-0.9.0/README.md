# Python wrapper for Austrian Post web services

This is a Python wrapper for web services provided by [Austrian Post](https://www.post.at/).

Currently, it only supports looking up shipment details by tracking number.

Groundwork for services requiring authentication is laid out, but not working
yet. If you want to contribute, please feel free to do so.

## Installation

```bash
pip install git+https://kumig.it/kumitterer/postat.git
```

## Usage

```python
from postat.classes.api import PostAPI

api = PostAPI()

# Get shipment details

shipment_details = api.get_shipment_details("123456789012345678901234567890")

shipment = shipment["data"]["einzelsendung"]

# Get latest event

latest_event = shipment["sendungsEvents"][-1]
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.