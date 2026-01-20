# Use the official Python request
FROM python:3.9

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY ./app.py /code/app.py

# Copy the ML artifacts (You must upload these to the repo!)
# COPY ./model_obesity.joblib /code/model_obesity.joblib
# COPY ./model_diabetes.joblib /code/model_diabetes.joblib
# COPY ./standard_scaler.joblib /code/standard_scaler.joblib
# COPY ./encoders /code/encoders
# Or simply copy everything in the root:
COPY . /code

# Create a non-root user for security (required by some HF Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Expose the port (HF Spaces defaults to 7860)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
