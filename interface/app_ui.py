
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import tensorflow as tf
from PIL import Image, UnidentifiedImageError

from interface.inference import decode_prediction, preprocess_image
from src.config import IMG_SIZE, MODELS_DIR


MODEL_PATH = MODELS_DIR / "smart_drug_model.keras"
RESULTS = PROJECT_ROOT / "results"
DOCS = PROJECT_ROOT / "docs"
MAX_IMAGE_BYTES = 10 * 1024 * 1024


st.set_page_config(
    page_title="Smart Drug AI | Ahmed Abdelmoula",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
:root {
    color-scheme: dark;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 90% 0%,
            #173f50 0%,
            transparent 42%
        ),
        #08111f;
    color: #edf7ff;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #142d40,
        #0b1728
    );
    border-right: 1px solid #2b4c5d;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1350px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    letter-spacing: -0.035em;
}

.hero {
    background: linear-gradient(
        120deg,
        #174657,
        #122c40 65%,
        #101e31
    );
    border: 1px solid #326677;
    border-radius: 24px;
    padding: 35px;
    margin-bottom: 24px;
    min-height: 210px;
}

.hero-label {
    color: #66e8db;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.hero h1 {
    color: white;
    font-size: clamp(30px, 3.3vw, 48px);
    font-weight: 850;
    line-height: 1.15;
    margin: 0 0 18px;
}

.hero p {
    color: #c0d6e2;
    font-size: 15px;
    line-height: 1.8;
    margin: 0;
}

.pill-graphic {
    height: 210px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: radial-gradient(
        circle,
        #23617a 0%,
        transparent 70%
    );
}

.pill-shape {
    width: 195px;
    height: 85px;
    border-radius: 85px;
    transform: rotate(-32deg);
    background: linear-gradient(
        90deg,
        #55e0d2 0%,
        #55e0d2 50%,
        #f1f8ff 50%
    );
    border: 7px solid #d9f8fb;
    box-shadow:
        0 18px 55px #37d7e055,
        inset 0 4px 15px #ffffff55;
}

.info-card {
    background: linear-gradient(
        140deg,
        #142e40,
        #102235
    );
    border: 1px solid #2d5265;
    border-radius: 18px;
    padding: 23px;
    min-height: 155px;
    margin-bottom: 15px;
    transition: transform .2s, border-color .2s;
}

.info-card:hover {
    transform: translateY(-3px);
    border-color: #53cdbf;
}

.card-icon {
    font-size: 27px;
    margin-bottom: 12px;
}

.card-title {
    color: white;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 8px;
}

.card-detail {
    color: #afc8d5;
    font-size: 13px;
    line-height: 1.6;
}

.result-card {
    background: linear-gradient(
        135deg,
        #14434d,
        #122b3e
    );
    border: 1px solid #397d82;
    border-radius: 20px;
    padding: 28px;
    margin: 12px 0;
}

.result-label {
    color: #86e7df;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.result-value {
    color: #ffffff;
    font-size: clamp(27px, 3vw, 42px);
    font-weight: 850;
    margin: 12px 0;
}

.result-description {
    color: #bed8df;
    font-size: 14px;
}

.warning-box {
    background: #302c1b;
    border: 1px solid #78682d;
    border-radius: 14px;
    padding: 16px 20px;
    color: #ffdfa2;
    line-height: 1.7;
    margin: 20px 0 28px;
}

.section-label {
    color: #72e5d9;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.image-information {
    background: #102638;
    border: 1px solid #305165;
    border-radius: 14px;
    padding: 18px;
    margin-top: 14px;
    line-height: 1.9;
}

[data-testid="stMetric"] {
    background: #143044;
    border: 1px solid #31586a;
    border-radius: 17px;
    padding: 22px;
}

[data-testid="stImage"] img {
    border-radius: 15px;
}

[data-testid="stFileUploader"] {
    border-radius: 15px;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 11px;
    border: 1px solid #398e95;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-radius: 18px;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 22px;
        min-height: auto;
    }

    .pill-graphic {
        height: 150px;
    }

    .pill-shape {
        transform: rotate(-32deg) scale(.75);
    }
}
</style>
""", unsafe_allow_html=True)


def card(icon, title, description):
    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-detail">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def hero(label, title, description, graphic=True):
    if graphic:
        left, right = st.columns([1.7, 1], gap="medium")

        with left:
            st.markdown(
                f"""
                <div class="hero">
                    <div class="hero-label">{label}</div>
                    <h1>{title}</h1>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with right:
            st.markdown(
                """
                <div class="pill-graphic">
                    <div class="pill-shape"></div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.markdown(
            f"""
            <div class="hero">
                <div class="hero-label">{label}</div>
                <h1>{title}</h1>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def research_warning():
    st.markdown(
        """
        <div class="warning-box">
            ⚠️ <b>Educational research only.</b>
            This model classifies visual patterns in images.
            Its output cannot verify medicine authenticity,
            effectiveness, ingredients, or safety.
            Never use its predictions to make medical
            or purchasing decisions.
        </div>
        """,
        unsafe_allow_html=True
    )


def read_json(path):
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, ValueError, TypeError):
        return None


@st.cache_resource(show_spinner="Loading trained AI model...")
def load_model(path):
    return tf.keras.models.load_model(
        path,
        compile=False
    )


def example_images():
    folder = RESULTS / "sample_predictions"

    if not folder.exists():
        return []

    images = []

    for extension in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        images.extend(folder.rglob(extension))

    return sorted(set(images))


def gallery():
    images = example_images()

    st.markdown("### 🖼️ Project Image Gallery")

    st.caption(
        "Saved prediction visualizations from the original "
        "Smart Drug Recognition project."
    )

    if not images:
        st.info(
            "No saved prediction visualizations were found."
        )
        return

    for index, path in enumerate(images[:6]):
        with st.container(border=True):
            st.markdown(
                f"**Prediction visualization {index + 1}**"
            )

            st.image(
                str(path),
                use_container_width=True
            )

            st.caption(
                path.stem.replace("_", " ").title()
            )


def pipeline():
    st.markdown("### ⚙️ How Our AI Works")

    steps = [
        (
            "📤",
            "01 — Image Upload",
            "Select a medicine package image."
        ),
        (
            "🖼️",
            "02 — Preprocessing",
            "Convert the image to RGB and resize it."
        ),
        (
            "🧠",
            "03 — CNN Analysis",
            "Analyze visual features with the trained model."
        ),
        (
            "📊",
            "04 — Prediction",
            "Display Original or Counterfeit."
        )
    ]

    cols = st.columns(4, gap="medium")

    for col, (icon, title, description) in zip(cols, steps):
        with col:
            card(icon, title, description)

    st.caption(
        "Image Upload → Preprocessing → CNN Inference → Prediction"
    )


def prediction_page():
    hero(
        "01 / AI IMAGE CLASSIFICATION",
        "Smart Drug Recognition",
        "Explore medicine package image classification "
        "using a trained deep-learning model."
    )

    a, b, c = st.columns(3)

    with a:
        card(
            "🖼️",
            "Image Analysis",
            "Upload and preview medicine package photographs."
        )

    with b:
        card(
            "🧠",
            "Deep Learning",
            "MobileNetV2-based CNN image classification."
        )

    with c:
        card(
            "📊",
            "Visual Results",
            "Explore saved results and prediction scores."
        )

    research_warning()

    st.markdown("## AI Classification Workspace")

    left, right = st.columns([1, 1], gap="large")

    image = None
    uploaded = None

    with left:
        st.markdown("#### 01 — Upload Image")

        uploaded = st.file_uploader(
            "Choose a medicine package image",
            type=["png", "jpg", "jpeg", "webp"],
            help="Maximum image size: 10 MB"
        )

        if uploaded is not None:
            if uploaded.size > MAX_IMAGE_BYTES:
                st.error(
                    "Please upload an image smaller than 10 MB."
                )
            else:
                try:
                    image = Image.open(uploaded)
                    image.load()

                    st.image(
                        image,
                        caption="Uploaded image preview",
                        width=360
                    )

                    st.markdown("##### Image Information")

                    width, height = image.size
                    size_kb = uploaded.size / 1024

                    st.markdown(
                        f"""
                        <div class="image-information">
                        <b>File:</b> {uploaded.name}<br>
                        <b>Dimensions:</b> {width} × {height} px<br>
                        <b>Size:</b> {size_kb:.1f} KB<br>
                        <b>Format:</b> {image.format or 'Unknown'}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except (UnidentifiedImageError, OSError, ValueError):
                    st.error(
                        "The uploaded file is not a readable image."
                    )

        else:
            st.info(
                "Upload a clear image to begin classification."
            )

    with right:
        st.markdown("#### 02 — Model Prediction")

        if image is None:
            st.markdown(
                """
                <div class="result-card">
                    <div class="result-label">MODEL STATUS</div>
                    <div class="result-value">Ready to analyze</div>
                    <div class="result-description">
                    Waiting for a valid image upload.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif not MODEL_PATH.is_file():
            st.error(
                "Model file missing: models/smart_drug_model.keras"
            )

        else:
            try:
                with st.spinner("Analyzing image..."):
                    model = load_model(str(MODEL_PATH))

                    features = preprocess_image(
                        image,
                        size=IMG_SIZE
                    )

                    output = model.predict(
                        features,
                        verbose=0
                    )

                    prediction = decode_prediction(
                        float(output.reshape(-1)[0])
                    )

                label = prediction["label"]
                score = float(prediction["score"])

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">
                        PREDICTED CATEGORY
                        </div>
                        <div class="result-value">{label}</div>
                        <div class="result-description">
                        Model score: {score:.1%}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.progress(
                    score,
                    text=f"Model score: {score:.1%}"
                )

                st.caption(
                    "This score is not a calibrated probability "
                    "of a medicine being genuine or counterfeit."
                )

                original_probability = float(
                    prediction["original_probability"]
                )

                counterfeit_probability = (
                    1.0 - original_probability
                )

                st.markdown("##### Model Output Details")

                a, b = st.columns(2)

                a.metric(
                    "Original score",
                    f"{original_probability:.1%}"
                )

                b.metric(
                    "Counterfeit score",
                    f"{counterfeit_probability:.1%}"
                )

                with st.expander("Technical prediction details"):
                    st.write(
                        f"Original score: {original_probability:.6f}"
                    )
                    st.write(
                        f"Counterfeit score: {counterfeit_probability:.6f}"
                    )
                    st.write("Decision threshold: 0.50")

            except Exception as exc:
                st.error(
                    "The model could not complete this prediction."
                )

                with st.expander("Technical error details"):
                    st.exception(exc)

    st.divider()

    pipeline()

    st.divider()

    gallery()


def performance_page():
    hero(
        "02 / MODEL EVALUATION",
        "Model Performance",
        "Explore historical test accuracy, confusion matrix, "
        "training curves, and classification metrics."
    )

    info = read_json(
        RESULTS
        / "confusion_matrix"
        / "evaluation_summary.json"
    )

    data = read_json(
        RESULTS
        / "dataset_summary"
        / "summary.json"
    )

    if isinstance(info, dict):
        matrix = info.get("confusion_matrix", [])

        valid_matrix = (
            isinstance(matrix, list)
            and len(matrix) == 2
            and all(
                isinstance(row, list) and len(row) == 2
                for row in matrix
            )
        )

        total = (
            sum(map(sum, matrix))
            if valid_matrix
            else None
        )

        correct = (
            matrix[0][0] + matrix[1][1]
            if valid_matrix
            else None
        )

        accuracy = info.get("test_accuracy")

        a, b, c = st.columns(3)

        a.metric(
            "Recorded Test Accuracy",
            f"{accuracy:.1%}"
            if isinstance(accuracy, (int, float))
            else "N/A"
        )

        b.metric(
            "Test Images",
            total if total is not None else "N/A"
        )

        c.metric(
            "Correct Classifications",
            correct if correct is not None else "N/A"
        )

        st.caption(
            "These are saved historical evaluation results, "
            "not a new independent test."
        )

    else:
        st.warning(
            "Evaluation summary is missing or invalid."
        )

    st.markdown("## Performance Visualizations")

    plots = [
        (
            "Confusion Matrix",
            RESULTS
            / "confusion_matrix"
            / "confusion_matrix.png"
        ),
        (
            "Accuracy History",
            RESULTS
            / "accuracy_loss_plots"
            / "accuracy.png"
        ),
        (
            "Training & Validation Loss",
            RESULTS
            / "accuracy_loss_plots"
            / "loss.png"
        )
    ]

    first, second = st.columns(2, gap="large")

    for index, (title, path) in enumerate(plots):
        col = first if index % 2 == 0 else second

        with col:
            with st.container(border=True):
                st.markdown(f"#### {title}")

                if path.is_file():
                    st.image(
                        str(path),
                        use_container_width=True
                    )
                else:
                    st.info(
                        f"{title} image is unavailable."
                    )

    st.markdown("## Classification Report")

    report = (
        RESULTS
        / "confusion_matrix"
        / "classification_report.txt"
    )

    if report.is_file():
        st.code(
            report.read_text(encoding="utf-8"),
            language="text"
        )
    else:
        st.info(
            "Classification report is unavailable."
        )

    if isinstance(data, dict):
        st.markdown("## Dataset Overview")

        counts = data.get("processed_counts", {})

        a, b, c = st.columns(3)

        a.metric(
            "Training Images",
            counts.get("train", {}).get("total", "N/A")
        )

        b.metric(
            "Validation Images",
            counts.get("validation", {}).get("total", "N/A")
        )

        c.metric(
            "Testing Images",
            counts.get("test", {}).get("total", "N/A")
        )

    research_warning()


def about_page():
    hero(
        "03 / PROJECT DOCUMENTATION",
        "Behind the AI",
        "Discover the architecture, technologies, "
        "processing workflow, and research limitations "
        "of the Smart Drug Recognition System."
    )

    st.markdown("## Project Overview")

    st.write(
        "Smart Drug Recognition System is an educational "
        "computer-vision project exploring binary image "
        "classification of medicine packaging. "
        "It uses a trained neural network to classify "
        "visual patterns as Original or Counterfeit."
    )

    st.markdown("## Technology Stack")

    a, b, c = st.columns(3)

    with a:
        card(
            "🐍",
            "Python",
            "Core application, data processing, and machine learning."
        )

    with b:
        card(
            "🧠",
            "TensorFlow / Keras",
            "Training and inference with a saved CNN."
        )

    with c:
        card(
            "🖥️",
            "Streamlit",
            "Interactive dashboard and image upload interface."
        )

    st.divider()

    pipeline()

    st.divider()

    st.markdown("## Research Limitations")

    st.write(
        "The system detects visual patterns in uploaded images. "
        "It cannot inspect medicine ingredients, authenticate "
        "serial numbers, verify manufacturers, or determine "
        "whether a real-world medicine is safe. "
        "Performance on unseen products may differ significantly "
        "from the recorded test accuracy."
    )

    st.markdown("## Project Documents")

    pdf_files = (
        sorted(DOCS.glob("*.pdf"))
        if DOCS.exists()
        else []
    )

    if pdf_files:
        cols = st.columns(2)

        for index, path in enumerate(pdf_files):
            with cols[index % 2]:
                with st.container(border=True):
                    st.markdown("### 📄 Project Document")
                    st.write(path.name)

                    st.download_button(
                        "Download PDF",
                        data=path.read_bytes(),
                        file_name=path.name,
                        mime="application/pdf",
                        key=str(path),
                        use_container_width=True
                    )
    else:
        st.info(
            "No PDF documents were found in the docs folder."
        )

    st.markdown("## Source & Reproducibility")

    st.info(
        "The repository includes the trained model, "
        "Python code, and saved evaluation outputs. "
        "The original image dataset is not included, "
        "so reproducing the training requires obtaining "
        "the dataset separately."
    )

    gallery()

    research_warning()


with st.sidebar:
    st.markdown("## 💊 Smart Drug AI")

    st.caption(
        "Image Intelligence Research Dashboard"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🔬 Prediction",
            "📊 Model Performance",
            "📘 About Project"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("**PROJECT INFORMATION**")

    st.caption("Architecture: MobileNetV2-based CNN")
    st.caption("Framework: TensorFlow / Keras")
    st.caption("Interface: Streamlit")

    st.divider()

    st.caption("Team research project")
    st.caption("GitHub edition — Ahmed Abdelmoula")


if page == "🔬 Prediction":
    prediction_page()

elif page == "📊 Model Performance":
    performance_page()

else:
    about_page()
