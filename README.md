# Tarefa-final---PJTOT
# MinIO OpenCV Image Processor

Pipeline de processamento de imagens utilizando MinIO e OpenCV.

## 📦 Descrição

Este projeto realiza a leitura de imagens de um bucket no MinIO, aplica um processamento simples utilizando OpenCV (binarização preto e branco) e salva o resultado em outro bucket.

## 🚀 Tecnologias

- Python
- MinIO
- OpenCV
- NumPy

## ⚙️ Como executar

1. Configure o MinIO rodando localmente ou em container.
2. Configure os buckets `input` e `output`.
3. Execute o script:

```bash
pip install -r requirements.txt
python main.py
