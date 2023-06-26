def format_time(time_string):
    # Divide o tempo em horas, minutos, segundos e milissegundos (se disponível)
    parts = time_string.split(':')
    hours, minutes, seconds = parts[:3]
    
    # Verifica se o tempo contém milissegundos
    if len(parts) > 3:
        milliseconds = parts[3]
    else:
        milliseconds = '000'
    
    # Formata o tempo final
    formatted_time = f'{hours}:{minutes}:{seconds},{milliseconds}'
    
    return formatted_time

def calculate_end_time(start_time, next_start_time, text_length):
    # Divide o tempo inicial em horas, minutos, segundos e milissegundos
    hours, minutes, seconds = start_time.split(':')
    seconds, milliseconds = seconds.split(',')
    
    # Divide o tempo inicial da próxima linha em horas, minutos, segundos e milissegundos
    next_hours, next_minutes, next_seconds = next_start_time.split(':')
    next_seconds, next_milliseconds = next_seconds.split(',')
    
    # Calcula o tempo final baseado no tamanho do texto
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    milliseconds += text_length * 50
    seconds += milliseconds // 1000
    milliseconds %= 1000
    
    # Limita o tempo final entre 1 segundo e o tempo inicial da próxima linha
    next_seconds = int(next_seconds)
    next_milliseconds = int(next_milliseconds)
    next_total_milliseconds = next_seconds * 1000 + next_milliseconds
    seconds = max(1, min(seconds, next_total_milliseconds // 1000))
    
    # Calcula o tempo final
    end_time_seconds = seconds
    end_time_milliseconds = milliseconds + 750
    if end_time_milliseconds >= 1000:
        end_time_seconds += 1
        end_time_milliseconds %= 1000
    end_time = f'{hours}:{minutes}:{end_time_seconds:02d},{end_time_milliseconds:03d}'
    
    return end_time

def generate_subtitle_pattern(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        subtitle_number = 1
        i = 0
        while i < len(lines):
            start_time = format_time(lines[i].strip())
            text = lines[i+1].strip()

            # Divide o texto em linhas de até 40 caracteres
            text_lines = [text[j:j+40] for j in range(0, len(text), 40)]

            for line in text_lines:
                # Obtém o tempo inicial da próxima linha
                if i+2 < len(lines):
                    next_start_time = format_time(lines[i+2].strip())
                else:
                    next_start_time = "99:59:59,999"  # Define um tempo grande para a última linha
                
                # Calcula o tempo final baseado no tamanho do texto e no tempo inicial da próxima linha
                text_length = len(line)
                end_time = calculate_end_time(start_time, next_start_time, text_length)

                # Padrão de legendas para um novo arquivo
                file.write(f'{subtitle_number}\n')
                file.write(f'{start_time} --> {end_time}\n')
                file.write(f'{line}\n\n')

                start_time = end_time  # Atualiza o tempo de início para a próxima linha
                subtitle_number += 1

            i += 2

    print(f'Subtitle pattern generated and saved to {output_file}.')

input_file = 'visao_geral_ecs.txt'
output_file = 'visao_geral_ecs2.txt'

generate_subtitle_pattern(input_file, output_file)
