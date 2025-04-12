import paramiko
import os
import stat
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def connect_to_sftp(host, username, password, port=22):
    """Se conecta al servidor SFTP y devuelve un objeto de conexión."""
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        transport.set_keepalive(30)
        sftp = transport.open_sftp_client()
        print("Conexión SFTP exitosa!")
        return sftp, transport
    except Exception as e:
        print(f"Error en la conexión SFTP: {e}")
        return None, None

def download_files(sftp, remote_path, local_path):
    """Descarga archivos nuevos o modificados de un directorio remoto a uno local."""
    os.makedirs(local_path, exist_ok=True)
    downloaded_files = []
    skipped_files = []

    try:
        for entry in sftp.listdir_attr(remote_path):
            remotepath = remote_path + "/" + entry.filename
            localpath = os.path.join(local_path, entry.filename)

            if stat.S_ISREG(entry.st_mode):
                if not os.path.exists(localpath):
                    print(f"Descargando (NUEVO): {remotepath} a {localpath}")
                    sftp.get(remotepath, localpath)
                    downloaded_files.append(entry.filename)
                else:
                    remote_mtime = entry.st_mtime
                    local_mtime = os.path.getmtime(localpath)

                    if remote_mtime > local_mtime:
                        print(f"Descargando (ACTUALIZADO): {remotepath} a {localpath}")
                        sftp.get(remotepath, localpath)
                        downloaded_files.append(entry.filename)
                    else:
                        print(f"Saltando (YA DESCARGADO): {remotepath}")
                        skipped_files.append(entry.filename)
            else:
                print(f"Saltando: {remotepath} (no es un archivo)")

        return downloaded_files, skipped_files

    except Exception as e:
        print(f"Error en la descarga de archivos: {e}")
        return [], []

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

# Credenciales SFTP
sftp_host = "mtu01-sftp-prod.ohrc.oracleindustry.com"
sftp_username = "SFTP_IGA1"
sftp_password = "_8TACdoqHBz44u"
sftp_port = 22

# Directorios
remote_directory = "/SFTP_IGA/StandardGL"
local_directory = "C:/Users/User/Desktop/Python/descargas_sftp"

# Credenciales de correo electrónico (Gmail)
email_sender = "granaceros@gmail.com"  # Correo de envío CORRECTO
email_recipients = ["andres.reyes@divinaprovidencia.com.co"]  # Correo de recepción
email_password = "snsn tpdy jjas cdah"  #  USA LA CONTRASEÑA DE APLICACIÓN

# Crear el directorio local si no existe
os.makedirs(local_directory, exist_ok=True)

# Conectarse al SFTP y descargar archivos
sftp, transport = connect_to_sftp(sftp_host, sftp_username, sftp_password, sftp_port)

if sftp:
    downloaded_files, skipped_files = download_files(sftp, remote_directory, local_directory)
    sftp.close()
    transport.close()

    # Construir el cuerpo del correo
    email_body = "Proceso de descarga de archivos completado.\n\n"
    if downloaded_files:
        email_body += "Archivos descargados:\n"
        for file in downloaded_files:
            email_body += f"- {file}\n"
    else:
        email_body += "No se descargaron archivos nuevos.\n"

    if skipped_files:
        email_body += "\nArchivos omitidos (ya descargados):\n"
        for file in skipped_files:
            email_body += f"- {file}\n"

    # Enviar el correo electrónico
    send_email("Descarga de archivos SFTP completada", email_body, email_sender, email_recipients, email_password)

    print("Descarga de archivos completa.")
else:
    print("No se pudo conectar al servidor SFTP. Revisa las credenciales y la conexión.")

print("Proceso finalizado.")