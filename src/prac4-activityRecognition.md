# Incomplete instructions - Practical 4: Activity recognition on the Capture24 dataset

## Setup instructions in the VMs
1. Load and initialize Anaconda. This needs to be done only once (you may not need to run this if you already see `(bash)` written in front of your prompt).

   ```bash
   module load Anaconda3
   conda init bash
   ```
   Exit and re-login so that the above takes effect.
3. Create an anaconda environment from the provided requirements YAML file:
   ```bash
   conda env create -f wearables-condaenv.yml
   ```
4. You are now ready to use the environment:
   ```bash
   conda activate wearables
   ```
   In future logins, you only need to run this last command.


## Datasets

The data required to run the notebooks can be found in
`/cdtshared/wearables/`. **Important:** Don't copy any data in there to own
devices. Also, avoid copying the data to your VM's `$HOME`.
Instead, change the absolute paths in the notebooks where necessary.
Or better, create a soft link:
```bash
ln -s /cdtshared/wearables/capture24/ capture24  # create shortcut in current location
```


## How to run Jupyter notebooks remotely

1. In your remote machine, launch a Jupyter notebook with a specified port, e.g. 9000:
   ```bash
   jupyter-notebook --no-browser --port=9000
   ```
   This will output something like:
   ```bash
   To access the notebook, open this URL:
   http://localhost:9000/?token=
   b3ee74d492a6348430f3b74b52309060dcb754e7bf3d6ce4
   ```

2. On your local machine, perform port-forwarding, e.g. the following forwards the remote port 9000 to the local port 8888:
   ```bash
   ssh -N -f -L localhost:8888:localhost:9000 username@remote_address
   ```
   Note: You can use the same port numbers for both local and remote.

3. Finally, copy the URL from step 1. Then in your local machine, open
Chrome and paste the URL, but change the port to the local port (or do nothing else if you used the same port).
You should be able see the notebooks now.
