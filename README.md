# Arhuaco

Arhuaco is a platform for Machine Learning based security data analysis.

# Install

## Linux

```bash
python3 setup.py install
```

## Docker

```bash
docker build -t arhuaco -f docker/Dockerfile .
```

# Run

For running the training step, a data directory is required. The data is located in:
/var/lib/arhuaco/data. The log information is stored in: /var/log/arhuaco.

```bash
docker run --name parsec-arhuaco -it -d -v /var/lib/arhuaco/data:/var/lib/arhuaco/data arhuaco /bin/bash
docker exec -i -t parsec-arhuaco /bin/bash
bin/arhuaco_train_cnn.sh <syscall/network>
```
