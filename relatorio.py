import database as db
import re
from datetime import datetime

def gerar_relatorio_agendamentos(arquivo_saida="relatorio_agendamentos.txt"):
    try:
        agendamentos = db.listar_agendamentos()
        if not agendamentos:
            return False, "Nenhum agendamento encontrado."
        
        clientes = db.listar_clientes()
        clientes_com_com = [c for c in clientes if c[3] and re.search(r'\.com$', c[3], re.IGNORECASE)]
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RELATÓRIO DE AGENDAMENTOS\n")
            f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("LISTA DE AGENDAMENTOS:\n")
            f.write("-" * 60 + "\n")
            for ag in agendamentos:
                f.write(f"ID: {ag[0]} | Cliente: {ag[1]} | Data: {ag[2]} | Hora: {ag[3]} | Serviço: {ag[4]}\n")
            f.write("\n")
            
            f.write("CLIENTES COM EMAIL .COM (filtro regex):\n")
            f.write("-" * 60 + "\n")
            if clientes_com_com:
                for c in clientes_com_com:
                    f.write(f"ID: {c[0]} | Nome: {c[1]} | Email: {c[3]}\n")
            else:
                f.write("Nenhum cliente com email terminado em .com\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("FIM DO RELATÓRIO\n")
        
        return True, arquivo_saida
    except Exception as e:
        return False, f"Erro ao gerar relatório: {str(e)}"
