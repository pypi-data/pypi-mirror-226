# CarbonTracer API Python Client

This is a Python client for CarbonTracer. It is a wrapper around the [CarbonTracer](https://carbontracer.uni-graz.at/) REST API, which allows you to calculate CO2 equivalents for personal transport.

## Installation

```bash
pip install git+https://kumig.it/kumitterer/pycarbontracer.git
```

## Usage

```python
from pycarbontracer import CarbonTracer

# Create a new CarbonTracer instance

ct = CarbonTracer("YOUR_API_KEY")

# Or use CarbonTracer.from_config() if you have a config.ini in the format of config.dist.ini

# Calculate the CO2 equivalents for a train trip from Graz to Vienna

result = ct.routing("train", "8010 Graz", "1010 Wien")

# Print the result

print(f"CO2 equivalents: {result["response"]["data"]["co2eq"]} {result["response"]["data"]["unitco2eq"]}")
```

The `CarbonTracer` class also has methods for the `location`, `address` and `co2only` endpoints, as documented in the [CarbonTracer API documentation](https://carbontracer.uni-graz.at/api-doc). The documentation also includes information about the input and output parameters, so make sure to check it out.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
