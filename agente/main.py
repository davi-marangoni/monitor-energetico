#!/usr/bin/env python3
"""
Agente de Monitoramento Energético
Script principal para executar o agente
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servico.agente import main


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nAgente interrompido pelo usuário')
        sys.exit(0)
    except Exception as e:
        print(f'Erro fatal: {str(e)}')
        sys.exit(1)
