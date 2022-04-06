### Installation

In order to install `filipid` please run `setup.py` script or use PIP.

```bash
python setup.py install
```

Using PIP

```bash
pip install filipid
```

### Example of usage

```python
from filipid import port

port = port.Port(port='/dev/cu.usbserial-A901A1JZ')
tmp = port.send([253, 252, 2, 3, 0], 0.04)
print(tmp)
tmp = port.send([253, 251, 2, 0], 0.02)
print(tmp)
tmp = port.send([255, 2], 0.02)
print(tmp)
```

### Utils tool

If you want to list all available ports

```bash
>>> list_ports

/dev/cu.SRS-XB10-CSRGAIA-1
/dev/cu.BoseQuietComfort35-SPPD-1
/dev/cu.usbserial-A901A1JZ

```