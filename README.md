# Tesseract Training Tutorial

This tutorial provides a detailed, step-by-step guide to training the Tesseract OCR engine with your custom dataset, enabling it to recognize specific languages or fonts.

## Introduction

Tesseract OCR is a widely used open-source Optical Character Recognition engine capable of recognizing text in multiple languages. This guide covers the installation, dataset preparation, training process, and troubleshooting.

---

## Installation

### Prerequisites

Before starting, ensure your environment is properly set up.

1. Install Tesseract and development libraries:

   ```bash
   sudo apt install tesseract-ocr
   sudo apt install libtesseract-dev
   ```

2. Set up Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

---

## Preparing the Dataset

### Dataset Requirements

1. **Model Name**: Decide on a three-letter code for your model based on [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). For example, use `vie` for Vietnamese.
2. **Directory Structure**:
   - Store ground truth data in `tesstrain/data/MODEL_NAME-ground-truth/`.
   - Ensure the directory contains both images and transcription files.
   ```bash
        tesstrain/data/
        ├── MODEL_NAME-ground-truth/
            ├── image1.tif
            ├── image1.gt.txt
            ├── image2.tif
            ├── image2.gt.txt
   ```
3. **File Formats**:
   - Images: TIFF (`.tif`) or PNG (`.png`, `.bin.png`, `.nrm.png`).
   - Transcriptions: Plain text files with the `.gt.txt` extension.
4. **Naming**: Each image file must have a corresponding transcription file with the same name (e.g., image1.tif and image1.gt.txt).

### Data generation

- Text Generation: Add your custom text to langdata/MODEL_NAME.training_text.
  You can use or modify text files from the [Tesseract langdata repository](https://github.com/tesseract-ocr/langdata)

- Pre-trained Data: Download pre-trained .traineddata files from the [Tesseract tessdata_best repository](https://github.com/tesseract-ocr/tessdata_best) and place them in tesseract/tessdata.

- Configurations: Ensure required configuration files (e.g., lstm.train) are in tesseract/tessdata/configs.
  You can find them in the [Tesseract tessconfigs repository](https://github.com/tesseract-ocr/tessconfigs/tree/3decf1c8252ba6dbeef0bf908f4b0aab7f18d113)

### Generate Dataset: Use a Python script to split training text into smaller files:

```python
python3 split_training_text.py
```

This script populates the tesstrain/data/MODEL_NAME-ground-truth directory.

### Validation Script: Ensure no files are missing or blank:

```python
python3 check_exsiting_file.py
```

This script removes incomplete pairs (e.g., missing .gt.txt or .box files).

## Training the Model

### Run the following command to start training:

```bash
TESSDATA_PREFIX=../tesseract/tessdata make training \
    MODEL_NAME=your_model_name \
    START_MODEL=base_model_name \
    TESSDATA=../tesseract/tessdata \
    MAX_ITERATIONS=100

```

#### Parameters:

- MODEL_NAME: Name of your model. It should match your ground-truth directory (e.g., MODEL_NAME-ground-truth).
- START_MODEL: Pre-trained model to fine-tune (e.g., vie for Vietnamese).
- MAX_ITERATIONS: Maximum training iterations.

### Example:

```bash
TESSDATA_PREFIX=../tesseract/tessdata make training \
    MODEL_NAME=vietnamese-ocr-model \
    START_MODEL=vie \
    TESSDATA=../tesseract/tessdata \
    MAX_ITERATIONS=100
```

### Adding a new language

```bash
sudo cp tesstrain/data/vietnamese-ocr-model.traineddata /usr/share/tesseract-ocr/4.00/tessdata # your own path to tessdata.
```

### Testing

```bash
tesseract vietnamese.dejavusans.exp10.tif output/a -l vietnamese-ocr-model
```

### Troubleshooting Common Errors:

Error: "Cannot load eng.traineddata during training."
Solution: Modify the Makefile to specify the correct language (-l MODEL_CODE):

```bash

%.lstmf: %.tif %.box
	tesseract "$<" $* --psm $(PSM) -l vie lstm.train

```
