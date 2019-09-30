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

# Run Arhuaco

For running the training step, a data directory is required. The data is located in:
/var/lib/arhuaco/data. The log information is stored in: /var/log/arhuaco.

Running the training phase:

```bash
bin/arhuaco_container_ctl.sh start
docker exec -i -t parsec-arhuaco /bin/bash
bin/arhuaco_train_cnn.sh <syscall/network>
```
Running the online detection:

```bash
# without the container
bin/arhuaco_sensor_ctl.sh start
bin/arhuaco_ctl.sh start

# with the container
bin/arhuaco_container_run.sh start
docker exec -i -t parsec-arhuaco /bin/bash
bin/arhuaco_ctl.sh start
```
The Arhuaco sensor service cannot be executed inside the container
if the sysdig source is utilized, due to permisions for accessing
the Linux kernel.
