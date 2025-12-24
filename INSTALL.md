
1. Atualizar sistema

sudo apt update
sudo apt upgrade -y

2. Instalar Python e ferramentas básicas

sudo apt install -y python3 python3-pip python3-venv build-essential git

3. Atualizar pip, e instalar o pip streamlit

pip install --upgrade pip
pip install streamlit

4. Instalar requeriment

pip install -r requirements.txt
 
5 Criar usuário de serviço e dá permissão
sudo adduser streamlit
sudo usermod -aG sudo streamlit

6- Acessar o home de streamlit e baixar a aplicação do github
cd ~
git clone https://github.com/tailanttt/nocbot.git
cd nocbot
git pull

7 - Criar e ativar ambiente venv

python3 -m venv venv
source venv/bin/activate

8 - Executar aplicação e trocar a porta se necessário

nohup streamlit run app.py &
nohup streamlit run app.py --server.address=0.0.0.0 --server.port=8501

9 - Verificar atualização diáriamente do repositorio do github
sudo -u streamlit crontab -l
0 0 * * * cd /home/streamlit/nocbot && git pull && /usr/bin/systemctl restart streamlit.service

10- Rodar o app.py sempre no boot

10.1 - Crie o arquivo /etc/systemd/system/streamlit.service com este conteúdo

sudo nano /etc/systemd/system/streamlit.service

[Unit]
Description=Streamlit Nocbot Service
After=network.target

[Service]
User=streamlit
WorkingDirectory=/home/streamlit/nocbot
ExecStart=/home/streamlit/venv/bin/python -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

10.2 - Ativar no boot

sudo systemctl daemon-reload
sudo systemctl enable streamlit.service
sudo systemctl start streamlit.service

11- Validar se o serviço está no ar
systemctl status streamlit.service

