from pathlib import Path

ARQUIVO_SERVICO = Path("/etc/systemd/system/monitor-energetico.service")
CONTEUDO_SERVICO = """[Unit]
Description=Agente Monitor Energetico
After=network.target

[Service]
User=root
WorkingDirectory=/opt/monitor-energetico
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
"""


def instalar_servico():
    ARQUIVO_SERVICO.write_text(CONTEUDO_SERVICO, encoding="utf-8")
    return [
        "systemctl daemon-reload",
        "systemctl enable monitor-energetico",
        "systemctl start monitor-energetico",
    ]
