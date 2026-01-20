# Use the official Python runtime
FROM python:3.9

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file
COPY ./requirement.txt /code/requirement.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirement.txt

# Copy the application code
COPY ./app.py /code/app.py

# Copy the ML artifacts
# COPY ./rf_foodinsecurity_predictor.pkl /code/rf_foodinsecurity_predictor.pkl
# COPY ./kmeans_food_access.pkl /code/kmeans_food_access.pkl
# COPY ./scaler_foodinsecurity.pkl /code/scaler_foodinsecurity.pkl
# COPY ./scaler_food_access.pkl /code/scaler_food_access.pkl
# COPY ./model_metadata.json /code/model_metadata.json
# COPY ./county_clusters.csv /code/county_clusters.csv
# Or simply copy everything in the root:
COPY . /code

# Create a non-root user for security (required by some HF Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Expose the port (HF Spaces defaults to 7860)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
