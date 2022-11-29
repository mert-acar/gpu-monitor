# GPU Utilization Monitor GUI
A [streamlit](https://streamlit.io) powered deamon for monitoring the GPU utilization of multiple ssh nodes with various number and models of GPUs. Developed for the use of my research group in National Magnetic Resonance Research Center, Ankara, Turkey. 

PRs and comments are welcome!

## Requirements
You need to install the following dependencies:
	
 - [streamlit](https://streamlit.io)
 - [paramiko](https://www.paramiko.org)
 - [plotly](https://plotly.com/python/getting-started/)

The dependencies can be installed easily with following instructions:

    # Setting up a virtual environment is recommended
    > python3 -m virtualenv venv
    > source venv/bin/activate
    
    # Installing the dependencies
    > pip install -r requirements.txt

## Usage

 1. In order to use the program first you need to specify a host list in *config.yaml* for the deamon to check. List the requested hosts in the form: `ip_address:port` (Most SSH configurations use port 22 by default).
 2. Then enter your credentials in *config.yaml* for the SSH connection. 
 3. Open a screen in the host machine and serve the streamlit app.
```
		> screen -R serve
		> streamlit run app.py
```
use CTRL+A+D to detach from the screen to let the program run in the background. You can reattach to this instance by:
```
		> screen -r serve
```
This will run your monitor instance on *localhost:8051* by default. You can specify a different port number by:

		    > streamlit run app.py --server.port YOUR_PORT

For more information on how to customize the configuration of streamlit visit [here](https://docs.streamlit.io/library/advanced-features/configuration).

Below you can see screenshots of the working app. The information displayed is static, however, you can refresh the graphs by pressing ***R*** anywhere on the screen.

![screenshot 1](/images/sample1.png "Screenshot 1")
![screenshot 2](/images/sample2.png "Screenshot 2")
