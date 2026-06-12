"""
Módulo para gerenciar a fila local de telemetrias usando SQLite.
"""
import sqlite3
import json
from datetime import datetime
import os


class FilaLocal:
    """Classe responsável pela fila local de telemetrias"""
    
    def __init__(self, db_path):
        """Inicializa a fila local com o caminho do banco de dados"""
        self.db_path = db_path
        self._garantir_diretorio()
        self._criar_tabela()
    
    def _garantir_diretorio(self):
        """Garante que o diretório do banco de dados existe"""
        diretorio = os.path.dirname(self.db_path)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, mode=0o755)
    
    def _criar_tabela(self):
        """Cria a tabela de telemetrias se não existir"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS telemetrias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    machine_id TEXT NOT NULL,
                    percentual_uso_cpu REAL NOT NULL,
                    ram_utilizada_gb REAL NOT NULL,
                    coletado_em TEXT NOT NULL,
                    criado_em TEXT NOT NULL,
                    enviado INTEGER DEFAULT 0,
                    tentativas INTEGER DEFAULT 0
                )
            ''')
            
            # Criar índice para melhor performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_enviado_machine_id 
                ON telemetrias(enviado, machine_id)
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f'Erro ao criar tabela de telemetrias: {str(e)}')
    
    def adicionar_telemetria(self, machine_id, telemetria):
        """Adiciona uma telemetria à fila local"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO telemetrias 
                (machine_id, percentual_uso_cpu, ram_utilizada_gb, coletado_em, criado_em)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                machine_id,
                telemetria['percentual_uso_cpu'],
                telemetria['ram_utilizada_gb'],
                telemetria['coletado_em'],
                datetime.utcnow().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise Exception(f'Erro ao adicionar telemetria: {str(e)}')
    
    def obter_pendentes(self, machine_id, limite=100):
        """Obtém as telemetrias pendentes de envio"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM telemetrias 
                WHERE machine_id = ? AND enviado = 0 AND tentativas < 3
                ORDER BY id ASC
                LIMIT ?
            ''', (machine_id, limite))
            
            resultados = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in resultados]
        except Exception as e:
            raise Exception(f'Erro ao obter telemetrias pendentes: {str(e)}')
    
    def marcar_como_enviado(self, id):
        """Marca uma telemetria como enviada"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE telemetrias 
                SET enviado = 1, tentativas = tentativas + 1
                WHERE id = ?
            ''', (id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise Exception(f'Erro ao marcar como enviado: {str(e)}')
    
    def remover_telemetria(self, id):
        """Remove uma telemetria da fila (após sucesso no envio)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM telemetrias WHERE id = ?', (id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise Exception(f'Erro ao remover telemetria: {str(e)}')
    
    def limpar_antigas(self, dias=7):
        """Remove telemetrias antigas que já foram enviadas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            from datetime import timedelta
            data_limite = (datetime.utcnow() - timedelta(days=dias)).isoformat()
            
            cursor.execute('''
                DELETE FROM telemetrias 
                WHERE enviado = 1 AND criado_em < ?
            ''', (data_limite,))
            
            conn.commit()
            linhas_deletadas = cursor.rowcount
            conn.close()
            
            return linhas_deletadas
        except Exception as e:
            raise Exception(f'Erro ao limpar telemetrias antigas: {str(e)}')
