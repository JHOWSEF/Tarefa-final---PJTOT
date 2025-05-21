from minio import Minio
from minio.error import S3Error
import cv2
import numpy as np
import io


# Configurações do MinIO
S3_ENDPOINT = "localhost:9000"
S3_ACCESS_KEY = "admin"
S3_SECRET_KEY = "admin123"

# Buckets
BUCKET_INPUT = "input"
BUCKET_OUTPUT = "output"

# Inicializa cliente MinIO
client = Minio(
    S3_ENDPOINT,
    access_key=S3_ACCESS_KEY,
    secret_key=S3_SECRET_KEY,
    secure=False
)


def process_image(image_bytes):
    # Lê a imagem a partir dos bytes
    image_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if img is None:
        raise Exception("Erro ao decodificar a imagem")

    # PROCESSAMENTO COM OPENCV:
    # Exemplo: binarização (transforma em preto e branco)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Codifica novamente para PNG
    _, img_encoded = cv2.imencode('.png', binary)
    return img_encoded.tobytes()


def main():
    try:
        # Lista os objetos no bucket de input
        objects = client.list_objects(BUCKET_INPUT)

        for obj in objects:
            print(f"Processando {obj.object_name}...")

            # Baixa a imagem
            response = client.get_object(BUCKET_INPUT, obj.object_name)
            image_data = response.read()

            # Processa a imagem
            processed_image = process_image(image_data)

            # Salva no bucket de output
            client.put_object(
                BUCKET_OUTPUT,
                obj.object_name,
                io.BytesIO(processed_image),
                length=len(processed_image),
                content_type="image/png"
            )

            print(f"Imagem {obj.object_name} processada e salva no bucket 'output'.")

    except S3Error as e:
        print("Erro no MinIO:", e)


if __name__ == "__main__":
    main()
