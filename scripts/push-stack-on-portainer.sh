#!/bin/bash

## Cores do Setup
amarelo="\e[33m"
verde="\e[32m"
branco="\e[97m"
bege="\e[93m"
vermelho="\e[91m"
reset="\e[0m"

# Função para exibir mensagens de erro
erro_msg() {
    echo -e "${vermelho}Erro:${reset} Ocorreu um erro durante a execução."
}

# Função para exibir logs em modo verboso
verbose_log() {
    [[ "$VERBOSE" == true ]] && echo -e "${branco}Verbose:${reset} $1"
}

# Função de uso
usage() {
    echo "Uso: $0 -r <url-portainer> -u <usuario-portainer> -p <senha-portainer> -s <nome-stack> -f <caminho-arquivo> [-v]"
    echo "  -r, --url           URL do Portainer"
    echo "  -u, --username      Nome de usuário do Portainer"
    echo "  -p, --password      Senha do Portainer"
    echo "  -s, --stack-name    Nome da stack"
    echo "  -f, --file-path     Caminho para o arquivo docker-compose.yaml da stack"
    
    echo "  -v, --verbose       Modo verboso"
    exit 1
}

# Função principal para implantar a stack
stack_deploy() {
    local portainer_url="$1"
    local username="$2"
    local password="$3"
    local stack_name="$4"
    local file_path="$5"
    local verbose="$6"

    # Ensure jq is installed
    if ! command -v jq &> /dev/null; then
        echo "jq is not installed. Please install jq."
        exit 1
    fi

    # Fetch auth token from Portainer
    local token=""
    local attempts=0
    local max_attempts=3

    while [[ -z "$token" || "$token" == "null" ]]; do
        token=$(curl -k -s -X POST -H "Content-Type: application/json" \
            -d "{\"username\":\"$username\",\"password\":\"$password\"}" \
            "https://$portainer_url/api/auth" | jq -r .jwt)

        ((attempts++))

        if [[ "$attempts" -ge "$max_attempts" ]]; then
            erro_msg
            echo "Failed to retrieve token after $max_attempts attempts."
            exit 1
        fi

        verbose_log "Attempt $attempts/$max_attempts to retrieve token."
        sleep 5
    done

    echo -e "Token retrieved: $bege$token$reset"

    # Obter ID do endpoint
    local ENDPOINT_ID
    ENDPOINT_ID=$(curl -k -s -X GET -H "Authorization: Bearer $token" \
        "https://$portainer_url/api/endpoints" | jq -r '.[] | select(.Name == "primary") | .Id')

    [[ -z "$ENDPOINT_ID" ]] && { echo "Erro ao obter ID do Portainer."; return; }
    echo -e "ID do Endpoint obtido: $bege$ENDPOINT_ID$reset"

    # Obter ID do Swarm
    local SWARM_ID
    SWARM_ID=$(curl -k -s -X GET -H "Authorization: Bearer $token" \
        "https://$portainer_url/api/endpoints/$ENDPOINT_ID/docker/swarm" | jq -r .ID)

    [[ -z "$SWARM_ID" ]] && { echo "Erro ao obter ID do Swarm."; return; }
    echo -e "ID do Swarm obtido: $bege$SWARM_ID$reset"

    # Arquivos temporários para capturar saída
    local erro_output
    erro_output=$(mktemp)
    local response_output
    response_output=$(mktemp)

    # Fazer deploy da stack pelo Portainer
    local http_code
    local url="https://$portainer_url/api/stacks/create/swarm/file"

    http_code=$(curl -s -o "$response_output" -w "%{http_code}" -k -X POST -H "Authorization: Bearer $token" \
        -F "Name=$stack_name" -F "file=@$file_path" -F "SwarmID=$SWARM_ID" -F "endpointId=$ENDPOINT_ID" "$url" 2> "$erro_output")

    local response_body
    response_body=$(cat "$response_output")

    if [[ "$http_code" -eq 200 && "$response_body" =~ "\"Id\"" ]]; then
        echo -e "Deploy da stack $bege$stack_name$reset feito com sucesso!"
    else
        echo -e "Erro ao efetuar deploy. Resposta HTTP: $http_code"
        echo "Mensagem de erro: $(cat "$erro_output")"
        echo "Detalhes: $(echo "$response_body" | jq .)"
        exit 1  # Exits with a status code of 1 (error)
    fi


    # Remover arquivos temporários
    rm "$erro_output" "$response_output"
}

## If script is executed directly, handle arguments and call main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    OPTS=$(getopt -o r:u:p:s:f:v -l url:,username:,password:,stack-name:,file-path:,verbose -n 'parse-options' -- "$@")
    if [ $? != 0 ]; then
        usage
    fi

    eval set -- "$OPTS"

    # Default value for verbose mode
    VERBOSE=false

    while true; do
        case "$1" in
        -r | --url )         portainer_url="$2"; shift 2 ;;
        -u | --username )    username="$2"; shift 2 ;;
        -p | --password )    password="$2"; shift 2 ;;
        -s | --stack-name )  stack_name="$2"; shift 2 ;;
        -f | --file-path )   file_path="$2"; shift 2 ;;
        -v | --verbose )     VERBOSE=true; shift ;;
        -- ) shift; break ;;
        * ) break ;;
        esac
    done

    # Check that required arguments are provided
    if [[ -z "$username" || -z "$password" || -z "$stack_name" || -z "$file_path" || -z "$portainer_url" ]]; then
        usage
    fi

    # Call the main function
    stack_deploy "$portainer_url" "$username" "$password" "$stack_name" "$file_path" "$VERBOSE"
fi

