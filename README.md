# 💊 Smart Drug Recognition System

**CNN-based drug-package image classification | Team project repository maintained by Ahmed Abdelmoula**

This academic deep-learning project classifies uploaded medicine-package images as **Original** or **Counterfeit** using transfer learning with **MobileNetV2** (a CNN architecture). It includes training, evaluation, a saved Keras model, and a Streamlit demonstration interface.

> **Important:** This is a research/educational demonstration, not a verified medicine-authentication tool. Its predictions and confidence scores must **not** be used to decide whether a medicine is safe, genuine, or suitable for use.

## Project attribution

This project was developed collaboratively as a team. This repository is **Ahmed Abdelmoula's copy of the shared team project**, published on his GitHub profile. The shared code, trained model, and existing evaluation results are team work; hosting this copy does not imply sole authorship.

**Repository owner / team contributor:** Ahmed Abdelmoula  
**University:** Istanbul Arel University, Faculty of Engineering  
**Course:** LEEN364 – Deep Learning and Classification Techniques

Other team members and individual contributions can be added here when confirmed.

## Highlights

- Prepares a two-class dataset and splits it into train, validation and test sets.
- Uses ImageNet-pretrained MobileNetV2 with transfer learning and fine-tuning.
- Provides a Streamlit upload interface to display the predicted class and model score.
- Includes the saved trained model and evaluation plots.

## Recorded evaluation (existing project outputs)

| Metric | Recorded value |
|---|---:|
| Test set | 100 images (64 original, 36 counterfeit) |
| Test accuracy | **97.0%** (97/100) |
| Test loss | 0.0833 |
| Confusion matrix (actual rows, predicted columns) | `[[34, 2], [1, 63]]` |

These are metrics recorded in the bundled evaluation files, **not a new independent run**. Performance on new packaging, lighting, manufacturers, and unseen distribution shifts is not established.

![Confusion matrix](results/confusion_matrix/confusion_matrix.png)

![Training accuracy](results/accuracy_loss_plots/accuracy.png)

## Project structure

```text
interface/app_ui.py                 Streamlit UI
models/smart_drug_model.keras       Trained Keras model
src/config.py                       Project paths, image size and random seed
src/data_preprocessing/             Dataset preparation script
src/training/                       Training script
src/evaluation/                     Evaluation script
results/                             Plots, summaries and example predictions
docs/                                Original team report and presentation PDFs
requirements.txt                    Python dependencies
.gitignore                          Local environment and dataset exclusions
```

## Team report and presentation

- [Project report (PDF)](docs/LEEN364__Smart_Drug_Recognition.pdf)
- [Team presentation (PDF)](docs/PRESENTATION_Smart_Drug_Recogniton.pdf)

These documents are retained from the shared team archive. Their original authorship and attribution should be respected.

## Dataset

Dataset referenced by the team: [Fake vs Real Medicine Dataset (Kaggle)](https://www.kaggle.com/datasets/surajkumarjha1/fake-vs-real-medicine-datasets-images).

The original images and prepared splits **are not included** in this repository. The previously generated dataset summary records 661 raw images: 421 original and 240 counterfeit. Check the dataset source, license and exact folder layout before attempting to retrain.

For data preparation, provide raw images under `dataset/raw/original/` and `dataset/raw/counterfeit/` and run:

```bash
python -m src.data_preprocessing.prepare_dataset --clean-processed --skip-corrupt
```

## Run the saved model demo

Create a virtual environment (Use Python 3.11; dependency compatibility still needs confirmation on your computer):

```bash
python -m venv .venv
```

Activate it:

```powershell
# PowerShell on Windows
.venv\Scripts\Activate.ps1
```

```bash
# Linux/macOS
source .venv/bin/activate
```

Install requirements and launch from the repository root:

```bash
python -m pip install -r requirements-demo.txt
python scripts/check_project.py
python -m unittest discover -s tests -v
streamlit run interface/app_ui.py
```

Open the local link shown in the terminal, upload a package image, and inspect the demonstration result. The `.keras` model is included, but a complete end-to-end launch was **not verified** when this GitHub copy was prepared.

## Reproduce training and evaluation

After downloading and placing the dataset into the expected directory structure:

```bash
python -m src.data_preprocessing.prepare_dataset --clean-processed --skip-corrupt
python -m src.training.train_model
python -m src.evaluation.evaluate_model
```

Training can take substantial time and will overwrite the saved model/outputs; keep a copy if you want to retain the existing artifact.

## Limitations and future work

- Dataset and its precise provenance/licensing are not packaged with this repository.
- Dependency versions are bounded for Python 3.11 but not independently validated against the saved model in a clean TensorFlow runtime.
- Prediction interface has not been smoke-tested on a clean environment as part of this copy.
- A validation study with genuinely unseen medicine packages and more diverse capture conditions would be needed.
- Unit tests and file integrity checks are included; full model inference and clean-environment deployment are still unverified.
- A contribution breakdown and real UI screenshots can be added after checking with teammates.

## Pre-publish quality checks

```bash
python scripts/check_project.py
python -m unittest discover -s tests -v
python -m compileall -q interface src tests scripts
```

The tests check image tensor formatting and class mapping without changing the trained model. **They do not prove the model runs on your machine**; manually launch Streamlit and upload a sample image to confirm that. For training dependencies, install `requirements.txt` instead of `requirements-demo.txt`. The documented evaluation is historical and was not rerun here.

## Release checklist

- [x] Shared project source, saved `.keras` model, recorded plots, report and presentation included
- [x] `requirements.txt`, minimal demo requirements, `.gitignore`, smoke checks and unit tests
- [x] Portable paths in recorded machine-readable summaries
- [ ] End-to-end TensorFlow / Streamlit launch with a real image on the target computer
- [ ] Confirm dataset download instructions, distribution rights and split reproducibility
- [ ] Verify publication consent for report/presentation and exact team credit
- [ ] Capture real UI screenshots and optionally deploy demo

Note: The project uses a dataset of photographs and a classification model. It cannot reliably authenticate pharmaceutical products or replace pharmacist/manufacturer verification.


## Dashboard navigation

The Streamlit dashboard provides three sections:

- **Prediction** — upload a package image and inspect the saved classifier's output.
- **Model Performance** — inspect *historical* accuracy, loss plots, confusion matrix, and classification report already in `results/`.
- **About Project** — read a brief workflow overview and download the existing project documentation.

Run from the repository root with Python 3.11:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-demo.txt
.\.venv\Scripts\python.exe -m streamlit run interface/app_ui.py
```

The model scores are not calibrated probabilities of authenticity; this is a research demonstration, not a medicine-verification service.
