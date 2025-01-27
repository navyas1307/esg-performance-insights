from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# Function to load and prepare data
def load_and_prepare_data():
    data = pd.read_csv(r"C:\Users\NAVYA\Downloads\ESG\ESG_data_fixed.csv")
    features = ['totalEsg', 'environmentScore', 'socialScore', 'governanceScore', 'highestControversy']
    
    data = data.dropna(subset=features)  # Remove rows with missing values in key features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[features])
    return data, scaled_data, scaler

# Function to train the clustering model
def train_cluster_model(scaled_data, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    return kmeans, clusters

# Function to train the recommendation model
def train_recommendation_model(scaled_data):
    nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(scaled_data)
    return nbrs

# Function to get cluster description
def get_cluster_description(cluster, data, clusters):
    cluster_data = data[clusters == cluster]
    
    avg_esg = cluster_data['totalEsg'].mean()
    avg_env = cluster_data['environmentScore'].mean()
    avg_soc = cluster_data['socialScore'].mean()
    avg_gov = cluster_data['governanceScore'].mean()
    
    if avg_esg > 80:
        performance = "excellent"
    elif avg_esg > 60:
        performance = "good"
    else:
        performance = "moderate"
        
    strengths = []
    if avg_env > avg_soc and avg_env > avg_gov:
        strengths.append("environmental")
    if avg_soc > avg_env and avg_soc > avg_gov:
        strengths.append("social")
    if avg_gov > avg_env and avg_gov > avg_soc:
        strengths.append("governance")
    
    strength_text = " and ".join(strengths) if strengths else "balanced"
    
    return f"{performance} overall ESG performance with strong {strength_text} metrics"

# Function to analyze the company and provide results
def analyze_company(input_data, scaler, kmeans, nbrs, data, clusters):
    input_scaled = scaler.transform([input_data])
    cluster = kmeans.predict(input_scaled)[0]
    distances, indices = nbrs.kneighbors(input_scaled)
    
    # Get cluster description
    cluster_description = get_cluster_description(cluster, data, clusters)
    
    # Get peer companies
    peer_companies = data.iloc[indices[0]][['Ticker', 'totalEsg', 'environmentScore', 'socialScore', 'governanceScore', 'highestControversy']]
    
    # Generate detailed suggestions
    suggestions = []
    company_scores = {
        'Environment': input_data[1],
        'Social': input_data[2],
        'Governance': input_data[3]
    }
    
    peer_avg = {
        'Environment': peer_companies['environmentScore'].mean(),
        'Social': peer_companies['socialScore'].mean(),
        'Governance': peer_companies['governanceScore'].mean()
    }
    
    for category, score in company_scores.items():
        if score < peer_avg[category]:
            if category == 'Environment':
                suggestions.append(f"Improve environmental score (current: {score:.1f}, peer avg: {peer_avg[category]:.1f}) by enhancing sustainability initiatives and environmental reporting.")
            elif category == 'Social':
                suggestions.append(f"Strengthen social score (current: {score:.1f}, peer avg: {peer_avg[category]:.1f}) through improved employee programs and community engagement.")
            else:
                suggestions.append(f"Enhance governance score (current: {score:.1f}, peer avg: {peer_avg[category]:.1f}) with better board diversity and transparency measures.")
    
    if input_data[4] > 3:  # High controversy score
        suggestions.append("Work on reducing controversy exposure through better risk management and stakeholder engagement.")

    return cluster, cluster_description, peer_companies, suggestions

# Function to generate a cluster chart
def generate_cluster_chart(data, clusters):
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(
        x=data['totalEsg'], 
        y=data['environmentScore'], 
        hue=clusters, 
        palette='viridis', 
        s=100
    )
    plt.title('ESG Performance Clusters')
    plt.xlabel('Total ESG Score')
    plt.ylabel('Environment Score')
    
    # Add legend with cluster descriptions
    legend_labels = [f"Cluster {i}" for i in range(len(set(clusters)))]
    scatter.legend(title='Clusters', labels=legend_labels)
    
    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return image_base64

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get input data from the form
            input_data = [
                float(request.form['totalEsg']),
                float(request.form['environmentScore']),
                float(request.form['socialScore']),
                float(request.form['governanceScore']),
                float(request.form['highestControversy'])
            ]
            
            # Validate input ranges
            if not all(0 <= x <= 100 for x in input_data[:4]) or not (1 <= input_data[4] <= 5):
                return "Invalid input ranges. Please ensure scores are between 0-100 and controversy is between 1-5.", 400
            
            # Perform analysis
            cluster, cluster_description, peers, suggestions = analyze_company(
                input_data, scaler, kmeans, nbrs, data, clusters
            )

            # Generate cluster chart
            cluster_chart = generate_cluster_chart(data, clusters)

            # Create cluster descriptions dictionary
            cluster_descriptions = {cluster: cluster_description}

            # Render the results page
            return render_template(
                "results.html", 
                cluster=cluster,
                cluster_descriptions=cluster_descriptions,
                peers=peers.to_dict(orient='records'),
                suggestions=suggestions,
                cluster_chart=cluster_chart
            )
        except ValueError as e:
            return f"Invalid input: {str(e)}", 400
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    # Render the input form page
    return render_template("index.html")

@app.route("/privacy_policy")
def privacy_policy():
    return render_template("privacy_policy.html")

# Route for Terms of Service
@app.route("/terms_and_services")
def terms_and_services():
    return render_template("terms_and_services.html")


# Function to generate enhanced visualizations
def generate_enhanced_visualizations(data, clusters):
    visualizations = {}

    # 1. Sector-Wise ESG Performance
    sector_avg = data.groupby("peerGroup")["totalEsg"].mean().reset_index()
    fig1 = px.bar(
        sector_avg, x="peerGroup", y="totalEsg", 
        title="Sector-Wise Average ESG Performance",
        labels={"peerGroup": "Sector", "totalEsg": "Average ESG Score"},
        color="totalEsg"
    )
    fig1.update_layout(xaxis_tickangle=-45)
    visualizations["sector_esg"] = fig1.to_html(full_html=False)

    # 2. Controversy vs ESG Scores
    fig2 = px.scatter(
        data, x="highestControversy", y="totalEsg",
        size="peerCount", color="peerGroup",
        title="Controversy vs ESG Scores",
        labels={"highestControversy": "Highest Controversy Level", "totalEsg": "Total ESG Score", "peerGroup": "Sector"},
        hover_data={"Ticker": True, "totalEsg": True, "highestControversy": True}
    )
    visualizations["controversy_esg"] = fig2.to_html(full_html=False)

    # 3. ESG Component Analysis
    sample_peer = data.head(1)
    avg_components = data[["environmentScore", "socialScore", "governanceScore"]].mean()
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=[sample_peer["environmentScore"].values[0], sample_peer["socialScore"].values[0], sample_peer["governanceScore"].values[0]],
        theta=["Environment", "Social", "Governance"],
        fill="toself",
        name="Selected Company"
    ))
    radar_fig.add_trace(go.Scatterpolar(
        r=avg_components.values,
        theta=["Environment", "Social", "Governance"],
        fill="none",
        name="Sector Average"
    ))
    radar_fig.update_layout(title="ESG Component Analysis", polar=dict(radialaxis=dict(visible=True)))
    visualizations["esg_components"] = radar_fig.to_html(full_html=False)

    # 4. Industry Involvement Analysis
    involvement_columns = ["animalTesting",'militaryContract', "controversialWeapons"]
    involvement_counts = data[involvement_columns].sum().reset_index()
    involvement_counts.columns = ["Involvement Area", "Company Count"]
    fig4 = px.bar(
        involvement_counts, x="Involvement Area", y="Company Count", 
        title="Industry Involvement Analysis",
        labels={"Involvement Area": "Area", "Company Count": "Number of Companies"},
        color="Company Count"
    )
    visualizations["industry_involvement"] = fig4.to_html(full_html=False)

    # 5. Peer Benchmarking
    sample_peer = data.head(1)
    fig5 = px.bar(
        data, x="peerGroup", y="totalEsg", color="peerGroup",
        title="Peer Benchmarking for Selected Company",
        labels={"peerGroup": "Sector", "totalEsg": "ESG Score"},
        hover_data={"Ticker": True, "totalEsg": True}
    )
    visualizations["peer_benchmarking"] = fig5.to_html(full_html=False)

    return visualizations

@app.route("/visualizations")
def visualizations():
    # Generate visualizations
    enhanced_visuals = generate_enhanced_visualizations(data, clusters)
    return render_template("visualizations.html", figs=enhanced_visuals)



if __name__ == "__main__":
    # Load and prepare data
    data, scaled_data, scaler = load_and_prepare_data()

    # Train models
    kmeans, clusters = train_cluster_model(scaled_data)
    nbrs = train_recommendation_model(scaled_data)

    # Run the Flask app
    app.run(debug=True)