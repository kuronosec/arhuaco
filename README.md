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
bin/arhuaco_train_cnn.sh <syscall|network>

# For training the the generative method with a RNN
bin/arhuaco_train_rnn.sh network
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

# Publications

*  A. Gomez Ramirez, C. Lara, U. Kebschull for the ALICE Collaboration. Intrusion Prevention and Detection in Grid computing - The ALICE Case, Journal of Physics: Conference Series (JPCS). http://iopscience.iop.org/article/10.1088/1742-6596/664/6/062017.
*  A. Gomez Ramirez, M. Martinez Pedreira, C. Grigoras, L. Betev, C. Lara and U. Kebschull for the ALICE Collaboration. A Security Monitoring Framework For Virtualization Based HEP Infrastructures. Journal of Physics: Conference Series, 898(10):102004, 2017. https://arxiv.org/abs/1704.04782.
*  A. Gomez Ramirez, C. Lara, L. Betev, D. Bilanovic, U. Kebschull for the ALICE Collaboration. Arhuaco: Deep Learning and Isolation Based Security for Distributed High-Throughput Computing. https://arxiv.org/abs/1801.04179.

# In the media

*  https://www.scientificamerican.com/article/worlds-most-powerful-particle-collider-taps-ai-to-expose-hack-attacks/
