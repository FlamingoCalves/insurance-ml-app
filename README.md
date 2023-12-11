
# Insurance Document Summarizer and QA

This Streamlit app provides an easy-to-use interface for summarizing insurance documents and answering questions about their content. It leverages powerful models from Hugging Face for natural language processing tasks.

## Models Used

- **Summarization**: The app uses the `facebook/bart-large-cnn` model from Hugging Face for summarizing text.
- **Question Answering**: For answering questions based on the context provided by the insurance document, the app uses the `deepset/roberta-base-squad2` model.

## Setup Instructions

To get the app up and running on your local machine, follow these steps:

1. Clone the repository.
2. Ensure you have Docker installed on your machine.
3. Build the Docker image with the provided `Dockerfile`.
4. Run the Docker container, ensuring you pass your Hugging Face API token as an environment variable.

Here's an example command to build and run the Docker container:

```sh
docker build -t ins_app_lite .
docker run -e "HUGGINGFACE_API_TOKEN=your_api_token" -p 8501:8501 ins_app_lite
```

Replace `your_api_token` with your actual Hugging Face API token.

## File Structure

```
clean_env_v1/
│
├── app.py               # Main application script
├── Dockerfile           # Dockerfile for building the Docker image
└── requirements_v1.txt  # Pip requirements file
```

## Testing the App

I've included three sample PDF documents that you can use to test the app's capabilities:

- `[SAMPLE] Blind Children's Vocational Discovery and Development Program.pdf`
- `[SAMPLE] Commercial_Insurance_Claim_Document.pdf`
- `[SAMPLE] Mock_Insurance_Claim_Document.pdf`

Simply upload one of these documents in the app's interface to see the summarization and question answering in action.

## Note on Virtual Environments

The virtual environment (`clean_env_v1`) is not included in the repository. Docker is used to create a consistent, isolated environment for running the app. The `requirements_v1.txt` file includes all necessary packages.

