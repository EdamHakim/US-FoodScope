import pandas as pd
import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from rag_service import Chunk
from typing import List, Dict, Any

def row_to_text(row):
    """
    Transforms a single county row into a comprehensive textual profile,
    integrating both general metrics and risk analysis if available.
    """
    county = row.get('County', 'Unknown County')
    state = row.get('State', 'Unknown State')
    
    # --- DEMOGRAPHICS ---
    pop = row.get('Population', 'N/A')
    poverty = row.get('Poverty_Rate', 'N/A')
    income = row.get('Median_Income', 'N/A')
    
    # --- HEALTH ---
    obesity = row.get('Adult_Obesity_Rate13', 'N/A')
    diabetes = row.get('Adult_Diabetes_Rate13', 'N/A')
    
    # --- FOOD ACCESS & ENVIRONMENT ---
    grocery = row.get('Grocery_Stores_Per1000', 'N/A')
    farmers = row.get('Farmers_Markets_Count_16', 'N/A')
    insecurity = row.get('FOODINSEC_13_15', 'N/A')
    low_access = row.get('PCT_LACCESS_POP15', 'N/A')
    ff_restaurants = row.get('FFRPTH14', 'N/A')
    
    # --- PHYSICAL ACTIVITY ---
    gyms = row.get('GYMs_Per_1000_Count_14', 'N/A')
    
    text = f"Comprehensive Profile for {county}, {state}:\n"
    
    # Add Risk Analysis if available (from worst_cluster_counties)
    if pd.notna(row.get('composite_risk')):
        risk = row.get('composite_risk')
        cluster = row.get('Cluster')
        text += f"!!! ALERT: This county is identified as a Highest Composite Health Risk area (Cluster {cluster}).\n"
        text += f"- Composite Health Risk Score: {risk}.\n"

    text += f"- Demographics: Population: {pop}, Poverty Rate: {poverty}%, Median Income: ${income}.\n"
    text += f"- Health Outcomes: Adult Obesity Rate: {obesity}%, Adult Diabetes Rate: {diabetes}%.\n"
    text += f"- Food Environment: {grocery} grocery stores per 1k residents, {farmers} farmers markets. "
    text += f"Fast food density: {ff_restaurants}/1k residents.\n"
    text += f"- Food Security: Food insecurity: {insecurity}%. {low_access}% of pop. has low food access.\n"
    text += f"- Physical Activity: Gym density: {gyms}/1k residents.\n"
    
    # Add optional descriptions if available
    if pd.notna(row.get('Description')):
        text += f"- Environmental Context: {row.get('Description')}\n"
    if pd.notna(row.get('Rule_Description')):
        text += f"- Policy Context: {row.get('Rule_Description')}\n"
        
    return text

def generate_assets(main_csv="rag_df.csv", worst_csv="worst_cluster_counties.csv", output_index="faiss_index.bin", output_chunks="chunks.pkl"):
    print("Loading datasets...")
    df_main = pd.read_csv(main_csv)
    
    if os.path.exists(worst_csv):
        print(f"Merging risk data from {worst_csv}...")
        df_worst = pd.read_csv(worst_csv)
        # Merge on County and State to bring in composite_risk
        df_combined = pd.merge(
            df_main, 
            df_worst[['County', 'State', 'composite_risk']], 
            on=['County', 'State'], 
            how='left'
        )
    else:
        df_combined = df_main
    
    print(f"Generating unified profiles for {len(df_combined)} counties...")
    
    chunks = []
    texts = []
    
    for i, row in df_combined.iterrows():
        text = row_to_text(row)
        metadata = {
            "county": row.get('County'),
            "state": row.get('State'),
            "is_high_risk": pd.notna(row.get('composite_risk'))
        }
        chunks.append(Chunk(text=text, metadata=metadata, chunk_id=i))
        texts.append(text)
    
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print(f"Generating embeddings for {len(texts)} unified profiles...")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    faiss.normalize_L2(embeddings)
    
    print(f"Building FAISS index (dimension: {embeddings.shape[1]})...")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    
    print(f"Saving assets to {output_index} and {output_chunks}...")
    faiss.write_index(index, output_index)
    with open(output_chunks, 'wb') as f:
        pickle.dump(chunks, f)
    
    print(f"Success! RAG assets regenerated with {len(chunks)} unified county profiles.")

if __name__ == "__main__":
    generate_assets()
