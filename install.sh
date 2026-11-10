#!/usr/bin/env bash
#
# Instala a fechadura do clube Insabots no Raspberry Pi.
#
# Uso (dentro da pasta do projeto, como usuário normal, sem sudo):
#   ./install.sh
#
# O script pede a senha do sudo quando precisa. Pode ser rodado de novo
# com segurança (por exemplo, depois de um git pull): ele não apaga os
# usuários cadastrados.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_USER="$(id -un)"
SERVICE_NAME="smartlock"
SERVICE_SOURCE="$PROJECT_DIR/deploy/$SERVICE_NAME.service"
SERVICE_TARGET="/etc/systemd/system/$SERVICE_NAME.service"
CLI_TARGET="/usr/local/bin/smartlock"
VENV_DIR="$PROJECT_DIR/.venv"
USERS_FILE="$PROJECT_DIR/data/users.json"

step() {
    echo
    echo "==> $1"
}

fail() {
    echo "ERRO: $1" >&2
    exit 1
}

check_environment() {
    step "Verificando o ambiente"
    [ "$(id -u)" -ne 0 ] || fail "rode sem sudo: ./install.sh (o script pede a senha quando precisa)"
    [ "$(uname -s)" = "Linux" ] || fail "este script é para o Raspberry Pi (Linux)"
    command -v apt-get >/dev/null || fail "apt-get não encontrado; use o Raspberry Pi OS"
    [ -f "$SERVICE_SOURCE" ] || fail "não encontrei $SERVICE_SOURCE"
    echo "Usuário: $RUN_USER"
    echo "Pasta:   $PROJECT_DIR"
}

is_raspberry_pi_5() {
    grep -q "Raspberry Pi 5" /proc/device-tree/model 2>/dev/null
}

install_system_packages() {
    step "Instalando pacotes do sistema"
    local gpio_package="python3-rpi.gpio"
    if is_raspberry_pi_5; then
        # O RPi.GPIO original não funciona no Pi 5; o rpi-lgpio é compatível
        # e mantém o mesmo "import RPi.GPIO as GPIO".
        gpio_package="python3-rpi-lgpio"
        sudo apt-get remove -y python3-rpi.gpio >/dev/null 2>&1 || true
    fi
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-spidev "$gpio_package"
}

enable_spi() {
    step "Ativando o SPI (usado pelo leitor RFID)"
    if command -v raspi-config >/dev/null; then
        sudo raspi-config nonint do_spi 0
    else
        echo "AVISO: raspi-config não encontrado; ative o SPI manualmente."
    fi
    sudo usermod -aG gpio,spi "$RUN_USER"
}

create_virtualenv() {
    step "Criando o ambiente virtual"
    if [ ! -x "$VENV_DIR/bin/python" ]; then
        # --system-site-packages deixa o .venv enxergar o RPi.GPIO do apt.
        python3 -m venv --system-site-packages "$VENV_DIR"
    fi
    "$VENV_DIR/bin/pip" install --upgrade mfrc522
}

create_users_file() {
    step "Preparando o arquivo de usuários"
    mkdir -p "$(dirname "$USERS_FILE")"
    if [ -s "$USERS_FILE" ]; then
        echo "Já existe, mantendo os usuários cadastrados."
    else
        echo "[]" > "$USERS_FILE"
        echo "Criado vazio: $USERS_FILE"
    fi
    # Só o dono lê e escreve: o arquivo tem os UIDs que abrem a porta.
    chmod 700 "$(dirname "$USERS_FILE")"
    chmod 600 "$USERS_FILE"
}

install_service() {
    step "Instalando o serviço do systemd"
    # Troca usuário e caminhos do arquivo de referência pelos desta máquina.
    sed \
        -e "s|^User=.*|User=$RUN_USER|" \
        -e "s|^WorkingDirectory=.*|WorkingDirectory=$PROJECT_DIR|" \
        -e "s|^ExecStart=.*|ExecStart=$VENV_DIR/bin/python -u main.py|" \
        "$SERVICE_SOURCE" | sudo tee "$SERVICE_TARGET" >/dev/null
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    sudo systemctl restart "$SERVICE_NAME"
}

install_cli() {
    step "Instalando o comando smartlock"
    # Um script pequeno que entra na pasta do projeto antes de rodar a CLI,
    # para o caminho relativo data/users.json funcionar de qualquer lugar.
    sudo tee "$CLI_TARGET" >/dev/null <<EOF
#!/bin/sh
cd "$PROJECT_DIR" && exec "$VENV_DIR/bin/python" cli.py "\$@"
EOF
    sudo chmod 755 "$CLI_TARGET"
}

print_summary() {
    step "Pronto!"
    cat <<EOF
Comandos úteis:
  smartlock user list                ver os usuários
  smartlock user add --name N --uid U   cadastrar
  systemctl status $SERVICE_NAME          ver se o serviço está rodando
  journalctl -u $SERVICE_NAME -f          ver o que a fechadura imprime

Se foi a primeira instalação, reinicie o Pi (sudo reboot) para o SPI
e as permissões de gpio/spi valerem.
EOF
}

main() {
    check_environment
    install_system_packages
    enable_spi
    create_virtualenv
    create_users_file
    install_service
    install_cli
    print_summary
}

main
