import paramiko
from math import ceil
import streamlit as st
import multiprocessing
from yaml import full_load
import plotly.graph_objects as go
from xml.etree import ElementTree
from plotly.subplots import make_subplots

def parse_ports(host):
  host = host.strip().split(':')
  if len(host) == 1:
    return [host[0], '22']
  return host

def plot_graphs(graph_data):
  cols = st.columns(2)
  left = False
  if graph_data is None:
    return
  for j, (host, results) in enumerate(graph_data.items()):
    with cols[int(left == True)]:
      with st.expander(host, True):
        for i, (gpu, data) in enumerate(results.items()):
          values = list(data.values())
          labels = list(data.keys())
          c = [config['figure_config']['colors'][label] for label in labels]
          text = list(map(lambda x: str(int(x)) + ' MB', values))
          fig = go.Figure(
            data=[
              go.Pie(
                labels=labels,
                values=values,
                text=text,
                title=gpu,
                **config['figure_config']['pie']
              )
            ]
          )
          fig.update(layout_showlegend=False)
          fig.update_traces(
            marker={'colors': c},
            **config['figure_config']['traces']
          )
          st.plotly_chart(fig, use_container_width=True)
    left = not left

def harvester(host):
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
  host_ip, port = host
  try:
    client.connect(host_ip, username=USER, password=PASS, port=port)
  except paramiko.ssh_exception.NoValidConnectionsError as e:
    print('Could not connect to', host_ip)
    return ('', [])
  except OSError as e:
    print('Could not connect to', host_ip)
    return ('', [])
  stdin, stdout, stderr = client.exec_command('nvidia-smi -x -q') 
  try:
    out = stdout.read().decode("utf8")
    root = ElementTree.fromstring(out)
  except:
    return ('', [])
  results = {}
  for i, gpu in enumerate(root.iter('gpu')):
    usage = {}
    gpu_name = gpu.find('product_name').text
    mem_use = gpu.find('fb_memory_usage')
    for attrib in mem_use:
      if attrib.tag != 'total':
        usage[attrib.tag] = float(attrib.text[:-4])
    results[f"[{str(i)}] {gpu_name}"] = usage
  
  stdin.close()
  stdout.close()
  stderr.close()
  client.close()
  return (host_ip, results)

def serial():
  my_bar = st.progress(0)
  results = [] 
  for i, host in enumerate(HOSTS):
    results.append(harvester(host))
    my_bar.progress((i + 1) / len(HOSTS))
  st.balloons()
  results = {host: data for (host, data) in results}
  if '' in results:
    del results['']
  plot_graphs(results)

def parallel():
  pool = multiprocessing.Pool(4)
  with st.spinner('Loading data...'):
    results = pool.map(harvester, HOSTS)
  st.success('Done!')
  pool.close()
  pool.join()
  results = {host: data for (host, data) in results}
  if '' in results:
    del results['']
  return results

if __name__ == '__main__':
  with open('config.yaml', 'r') as f:
    config = full_load(f)
    USER = config['ssh_config']['credentials']['USER'] 
    PASS = config['ssh_config']['credentials']['PASS']
    HOSTS = list(map(parse_ports, config['ssh_config']['hosts']))
    st.set_page_config(**config['page_config'])


  _, col, _ = st.columns([1,3,1])
  with col:
    st.image('images/logo.webp')
  body = '''
  ## GPU Monitor
  '''
  st.markdown(body, unsafe_allow_html=False)
  # st.button('Refresh', on_click=serial)
  results = parallel()
  plot_graphs(results)
