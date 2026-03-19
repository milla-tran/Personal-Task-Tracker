def inject_css():
    return """
    <style>
    .stApp {
        background-color: #D3A7B5;
        color: #1F1E1F;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1F1E1F;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #6A545B;
        margin-bottom: 1rem;
    }

    .cute-card {
        background: #F9E1DC;
        border-radius: 20px;
        padding: 1rem 1.2rem;
        box-shadow: 0 4px 12px rgba(31, 30, 31, 0.12);
        margin-bottom: 1rem;
    }

    .weather-card {
        background: #A0C6EC;
        border-radius: 20px;
        padding: 1rem 1.2rem;
        color: #1F1E1F;
        box-shadow: 0 4px 12px rgba(31, 30, 31, 0.12);
        margin-bottom: 1rem;
    }

    .reward-card {
        background: #FEAFC2;
        border-radius: 20px;
        padding: 1rem 1.2rem;
        box-shadow: 0 4px 12px rgba(31, 30, 31, 0.12);
        margin-bottom: 1rem;
    }

    div[data-testid="stCheckbox"] label p {
        font-size: 1rem;
    }
    </style>
    """