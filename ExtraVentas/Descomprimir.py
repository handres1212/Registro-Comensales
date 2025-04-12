import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zipfile

def send_email(subject, body, sender, recipients, password):
    """Envía un correo electrónico."""
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
           smtp_server.login(sender, password)
           smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Correo electrónico enviado correctamente!")
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {e}")

def unzip_and_delete_files(local_path):
    """Descomprime archivos ZIP en la carpeta local y luego borra los ZIP."""
    unzipped_files = []
    for filename in os.listdir(local_path):
        if filename.endswith(".zip"):
            zip_filepath = os.path.join(local_path, filename)
            try:
                with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                    zip_ref.extractall(local_path)
                print(f"Descomprimido: {filename} en {local_path}")
                os.remove(zip_filepath)
                print(f"Archivo ZIP eliminado: {filename}")
                unzipped_files.append(filename)
            except Exception as e:
                print(f"Error al descomprimir o eliminar {filename}: {e}")
    return unzipped_files

# Directorio local
local_directory = "C:/Users/User/Desktop/Python/descargas_sftp"

# Credenciales de correo electrónico (Gmail)
email_sender = "granaceros@gmail.com"  # Correo de envío
email_recipients = ["andres.reyes@divinaprovidencia.com.co"]  # Correo de recepción
email_password = "snsn tpdy jjas cdah"  # Contraseña de aplicación

# Descomprimir archivos ZIP y eliminarlos
unzipped_files = unzip_and_delete_files(local_directory)

# Construir el cuerpo del correo
email_body = "Proceso de descompresión de archivos completado.\n\n"
if unzipped_files:
    email_body += "Archivos descomprimidos:\n"
    for file in unzipped_files:
        email_body += f"- {file}\n"
else:
    email_body += "No se encontraron archivos ZIP para descomprimir.\n"

# Enviar el correo electrónico
send_email("Descompresión de archivos completada", email_body, email_sender, email_recipients, email_password)

print("Proceso finalizado.")