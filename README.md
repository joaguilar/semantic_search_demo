# semantic_search_demo
A Small demo showing Semantic Search and text generation using both HF models and OpenAI models


## Installation

Create Environment:

```
conda create -p .\semantic python=3.10
conda activate .\semantic
pip install -r requirements.txt
```
For GPU CUDA support:

```
conda install cuda pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia/label/cuda-11.7.0
```

And check if it worked:
```
python -c "import torch; print(torch.cuda.is_available())"
```

Download and install Tesseract from [here](https://tesseract-ocr.github.io/tessdoc/Downloads.html).

Download and install Poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases/).



Run using:

```
set OPENAI_API_KEY=<YOU_OPENAI_API_KEY>
set OPENAI_API_ORG=<YOU_OPENAI_ORG_KEY>
set TESSERACT_LOCATION=<PATH_TO_TESSERACT_INSTALL>
set POPPLER_LOCATION=<PATH_TO_POPPLER_INSTALL>
set ELASTIC_HOST=<ELASTICSEARCH_HOST>
set ELASTIC_PORT=<ELASTICSEARCH_PORT>
set ELASTIC_SSL_ASSERT=<ELASTICSEARCH_SSL_ASSERT_FINGERPRINT>
set ELASTIC_USER=<ELASTICSEARCH_USERL>
set ELASTIC_PASSWORD=<ELASTICSEARCH_PASSWORD>
set ELASTIC_INDEX=<ELASTICSEARCH_INDEX>
python index_jsons.py
streamlit run webapp
```


## Troubleshooting

If you get an error with regards to `AttributeError: partially initialized module 'charset_normalizer' has no attribute 'md__mypyc' (most likely due to a circular import)`, run the following command to fix it:

```
pip install --force-reinstall charset-normalizer==3.1.0
```