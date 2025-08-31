import asyncio
import logging
import string
from beeai_framework.backend import ChatModel, ChatModelParameters, UserMessage

class SimplePromptTemplate:
    """Simple prompt template using Python string formatting."""
    
    def __init__(self, template: str):
        self.template = template
    
    def render(self, variables: dict) -> str:
        """Render the template with provided variables."""
        # Replace mustache-style {{variable}} with Python format {variable}
        formatted_template = self.template
        for key, value in variables.items():
            formatted_template = formatted_template.replace(f"{{{{{key}}}}}", f"{{{key}}}")
        
        # Format the template with the variables
        return formatted_template.format(**variables)

async def prompt_template_example():
    llm = ChatModel.from_name("watsonx:ibm/granite-3-3-8b-instruct", ChatModelParameters(temperature=0))
    
    # Create a prompt template for data science project evaluation
    template_content = """
    You are a senior data scientist evaluating a machine learning project proposal.
    
    Project Details:
    - Project Name: {{project_name}}
    - Business Problem: {{business_problem}}
    - Available Data: {{data_description}}
    - Timeline: {{timeline}}
    - Success Metrics: {{success_metrics}}
    
    Please provide:
    1. Feasibility assessment (1-10 scale)
    2. Key technical challenges
    3. Recommended approach
    4. Risk mitigation strategies
    5. Expected outcomes
    
    Be specific and actionable in your recommendations.
    """
    
    # Create the prompt template
    prompt_template = SimplePromptTemplate(template_content)
    
    # Test with different project scenarios
    project_scenarios = [
        {
            "project_name": "Smart Inventory Optimization",
            "business_problem": "Reduce inventory costs while maintaining 95% product availability",
            "data_description": "2 years of sales data, supplier lead times, seasonal patterns, 500K records",
            "timeline": "3 months development, 1 month testing",
            "success_metrics": "15% cost reduction, maintain 95% availability, <2% forecast error"
        },
        {
            "project_name": "Fraud Detection System",
            "business_problem": "Detect fraudulent transactions in real-time with minimal false positives",
            "data_description": "1M transaction records, user behavior data, device fingerprints",
            "timeline": "6 months development, 2 months validation",
            "success_metrics": "95% fraud detection rate, <1% false positive rate, <100ms response time"
        }
    ]
    
    for i, scenario in enumerate(project_scenarios, 1):
        print(f"\n=== Project Evaluation {i}: {scenario['project_name']} ===")
        
        # Render the template with scenario data
        rendered_prompt = prompt_template.render(scenario)
        print("\n  Rendered prompt:")
        print(rendered_prompt)
        
        # Generate evaluation using create() method
        messages = [UserMessage(content=rendered_prompt)]
        response = await llm.create(messages=messages)
        
        print("### LLM response: ###\n")
        print(response.get_text_content())
        
async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL) # Suppress unwanted warnings
    await prompt_template_example()

if __name__ == "__main__":
    asyncio.run(main())


"""

Output::

=== Project Evaluation 1: Smart Inventory Optimization ===

  Rendered prompt:

    You are a senior data scientist evaluating a machine learning project proposal.
    
    Project Details:
    - Project Name: Smart Inventory Optimization
    - Business Problem: Reduce inventory costs while maintaining 95% product availability
    - Available Data: 2 years of sales data, supplier lead times, seasonal patterns, 500K records
    - Timeline: 3 months development, 1 month testing
    - Success Metrics: 15% cost reduction, maintain 95% availability, <2% forecast error
    
    Please provide:
    1. Feasibility assessment (1-10 scale)
    2. Key technical challenges
    3. Recommended approach
    4. Risk mitigation strategies
    5. Expected outcomes
    
    Be specific and actionable in your recommendations.
    
### LLM response: ###

1. Feasibility Assessment (1-10 scale): 8/10

The project appears feasible given the available data and clear objectives. The 3-month development timeline and 1-month testing period seem reasonable for a machine learning project of this scope. However, the success metrics, particularly the 15% cost reduction and less than 2% forecast error, are ambitious and might be challenging to achieve, which slightly lowers the feasibility score.

2. Key Technical Challenges:

- Handling seasonality and trends in sales data
- Accurately forecasting demand while accounting for supplier lead times
- Balancing inventory cost reduction with maintaining high product availability
- Ensuring the model generalizes well across different products and seasons
- Addressing potential data quality issues, such as missing or inconsistent data

3. Recommended Approach:

- Data Preprocessing: Clean and preprocess the data, handling missing values, and encoding categorical variables. Segment the data by product categories and seasons to capture seasonality and trends.
- Feature Engineering: Create relevant features, such as moving averages, lagged sales, and supplier lead time indicators. Consider external factors (e.g., promotions, holidays) that may impact sales.
- Model Selection: Experiment with various time-series forecasting models, such as ARIMA, SARIMA, Prophet, LSTM (Long Short-Term Memory), or hybrid models combining statistical and deep learning approaches.
- Inventory Optimization: Implement inventory control policies (e.g., (s, S) policy, periodic review systems) based on the forecasted demand to minimize costs while maintaining desired availability levels.
- Model Evaluation: Use appropriate metrics (e.g., Mean Absolute Percentage Error, Mean Absolute Error, and availability metrics) to evaluate model performance. Perform cross-validation and backtesting to ensure model robustness.
- Model Deployment: Develop a scalable and automated system for model retraining, forecasting, and inventory optimization.

4. Risk Mitigation Strategies:

- Data Quality: Implement data quality checks and monitoring to identify and address data issues early.
- Model Overfitting: Use regularization techniques, cross-validation, and early stopping to prevent overfitting.
- Model Drift: Continuously monitor model performance and retrain models periodically to adapt to changing patterns.
- Business Acceptance: Engage stakeholders throughout the project to ensure alignment with business objectives and address any concerns.

5. Expected Outcomes:

- Improved inventory forecasting accuracy, leading to reduced safety stock and lower inventory holding costs.
- Enhanced product availability, minimizing stockouts and lost sales.
- A robust, automated system for inventory optimization that can be scaled across different product categories and seasons.
- Insights into demand drivers and seasonality patterns, enabling better decision-making and strategic planning.

While the project has a high chance of success, it's essential to remain flexible and adapt the approach as needed based on ongoing evaluation and stakeholder feedback. Regular communication and collaboration with stakeholders will be crucial to ensure the project meets its objectives and addresses any unforeseen challenges.

=== Project Evaluation 2: Fraud Detection System ===

  Rendered prompt:

    You are a senior data scientist evaluating a machine learning project proposal.
    
    Project Details:
    - Project Name: Fraud Detection System
    - Business Problem: Detect fraudulent transactions in real-time with minimal false positives
    - Available Data: 1M transaction records, user behavior data, device fingerprints
    - Timeline: 6 months development, 2 months validation
    - Success Metrics: 95% fraud detection rate, <1% false positive rate, <100ms response time
    
    Please provide:
    1. Feasibility assessment (1-10 scale)
    2. Key technical challenges
    3. Recommended approach
    4. Risk mitigation strategies
    5. Expected outcomes
    
    Be specific and actionable in your recommendations.
    
### LLM response: ###

1. Feasibility Assessment (1-10 scale): 8

The project appears feasible given the available data and resources. With 1 million transaction records, user behavior data, and device fingerprints, there is a solid foundation for building a robust fraud detection system. The specified success metrics are ambitious but achievable with the right approach and resources. The main challenge will be balancing the high detection rate with minimal false positives while maintaining real-time performance.

2. Key Technical Challenges:

a. Imbalanced dataset: Fraudulent transactions are typically a small percentage of the total, leading to an imbalanced dataset that can negatively impact model performance.

b. Real-time processing: Ensuring the system can process transactions and provide results within 100ms is a significant challenge, especially as transaction volumes increase.

c. Minimizing false positives: Striking the right balance between detecting fraud and avoiding false alarms is crucial for maintaining user trust and minimizing operational disruptions.

d. Adapting to evolving fraud patterns: Fraudsters constantly adapt their tactics, requiring the system to learn and update continuously.

3. Recommended Approach:

a. Data Preprocessing: Address the class imbalance by using techniques like oversampling, undersampling, or generating synthetic samples (SMOTE). Feature engineering should focus on extracting meaningful patterns from user behavior and device fingerprints.

b. Model Selection: Employ a combination of supervised learning algorithms (e.g., Random Forest, XGBoost, or LightGBM) and unsupervised learning techniques (e.g., Isolation Forest or One-Class SVM) for anomaly detection. Ensemble methods can further improve performance.

c. Real-time Processing: Implement a scalable, distributed architecture using technologies like Apache Kafka, Apache Flink, or Spark Streaming for real-time data ingestion and processing. Leverage in-memory databases (e.g., Redis) or caching mechanisms to ensure low-latency responses.

d. Continuous Learning: Incorporate online learning or incremental learning techniques to adapt the model to new fraud patterns without retraining from scratch.

4. Risk Mitigation Strategies:

a. Regular Model Evaluation: Continuously monitor model performance using appropriate metrics (precision, recall, F1-score, AUC-ROC) and adjust thresholds as needed to maintain the desired balance between detection rate and false positives.

b. A/B Testing: Implement A/B testing to compare the performance of different models or configurations in a controlled environment before deploying them in production.

c. Data Drift Detection: Implement data drift detection mechanisms to identify when the underlying data distribution changes, prompting model retraining or adaptation.

d. Redundancy and Failover: Design the system with redundancy and failover mechanisms to ensure high availability and minimize downtime.

5. Expected Outcomes:

a. A real-time fraud detection system capable of processing transactions with minimal latency (<100ms).

b. Achieve a fraud detection rate of 95% while maintaining a false positive rate below 1%.

c. Continuous improvement in model performance through regular evaluation, A/B testing, and adaptation to evolving fraud patterns.

d. A scalable and robust system that can handle increasing transaction volumes and adapt to new fraud tactics.

e. Enhanced user trust and reduced operational disruptions due to minimized false positives.

"""