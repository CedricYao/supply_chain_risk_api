### **Design Document: "Port Watch" (1-Day Hackathon Edition)**

Project Name: "Port Watch" – Rapid Prototype  
Target Audience: Schwarz Group Supply Chain Coordinators  
Status: 1-Day Hackathon / Proof of Concept

### ---

**1\. Executive Summary**

This is an ultra-simplified version of the Proactive Supply Chain Risk Agent designed to be built and demonstrated in a single day.  
The Goal: Prove that Gemini can bridge the gap between unstructured external data (news text) and structured internal data (shipment rows) to identify specific supply chain risks.  
**The Shift:** Instead of building live API integrations, we will simulate the "world" to focus entirely on the AI reasoning capability.

### **2\. Scope: The "Micro Slice"**

We are removing all external plumbing (News APIs, BigQuery, email servers) to focus on the core logic.

* **Trigger (Simulated):** The user manually pastes a text snippet (simulating a news article) into a simple interface.  
* **Data (Simulated):** A hardcoded list of 10 "Active Shipments" (JSON/Dictionary) representing the SAP environment.  
* **Action:** The system outputs a text alert identifying exactly which Shipment IDs are affected by the pasted text.

**Out of Scope:**

* Live News API connections (replaced by manual paste).  
* Database setup (replaced by hardcoded list).  
* Complex risk calculations (replaced by simple "Match/No Match" logic).

### **3\. User Experience (UX) Flow**

**Interface:** A simple **Google Colab Notebook** or a bare-bones **Streamlit app**.

1. **Input:** User pastes a paragraph of text:*"Labor unions have announced a 48-hour walkout at the Port of Rotterdam starting this Friday due to stalled wage negotiations."*  
2. **Processing:**  
   * **Step A (Gemini):** Extracts {"location": "Port of Rotterdam", "event": "Strike", "severity": "High"}.  
   * **Step B (Code):** Filters the hardcoded shipment list for Destination \== "Rotterdam".  
3. **Output:** The system displays:  
   * **🔴 ALERT: High Severity Disruption Detected**  
   * **Reason:** Strike at Port of Rotterdam.  
   * **Affected Shipments:**  
     * *Shipment \#SCH-9001* (Bananas) \- Arrival: Friday.  
     * *Shipment \#SCH-9004* (Coffee) \- Arrival: Saturday.

### **4\. Technical Architecture (1-Day Build)**

* **Environment:** Python (local or Google Colab).  
* **LLM:** **Vertex AI SDK (Gemini 1.5 Flash)**. *Flash is chosen for speed and low latency in a demo.*  
* **Data Structure:** A Python List of Dictionaries simulating SAP data.  
  Python  
  shipments \= \[  
      {"id": "SCH-9001", "contents": "Bananas", "destination": "Rotterdam", "value": 15000},  
      {"id": "SCH-9002", "contents": "Electronics", "destination": "Hamburg", "value": 50000},  
      ...  
  \]

### **5\. Success Metrics (1-Day)**

| Metric | Target |
| :---- | :---- |
| **Extraction Accuracy** | Correctly identifies the port name from 3 different test news snippets (e.g., Hamburg, Rotterdam, Valencia). |
| **Logic Accuracy** | Correctly filters the shipment list (e.g., if news says "Hamburg", only Hamburg shipments appear). |
| **Build Time** | Functional demo ready in \< 6 hours. |

### **6\. 1-Day Development Roadmap**

**09:00 \- 10:30: Setup & Data (The "Mock" World)**

* Initialize Vertex AI SDK credentials.  
* Create the shipments mock dataset (Python list) with diverse ports and goods.  
* Curate 3 "test snippets" of text (one strike, one weather delay, one irrelevant news story).

**10:30 \- 12:30: The Brain (Prompt Engineering)**

* Develop the Gemini prompt.  
  * *Input:* Unstructured news text.  
  * *Task:* Extract entities into a strict JSON format: {"port\_name": str, "event\_type": str, "is\_disruption": bool}.  
* Test against the 3 snippets to ensure JSON outputs are consistent.

**13:30 \- 15:30: The Logic (Integration)**

* Write the Python function check\_impact(news\_text).  
  * Calls Gemini to get the JSON.  
  * Loops through shipments.  
  * Returns a list of matching Shipment IDs.

**15:30 \- 17:00: Interface & Polish**

* Wrap the logic in a simple loop or Streamlit UI (st.text\_area for input, st.dataframe for output).  
* Add a final Gemini call to generate a 1-sentence "Mitigation Advice" for the display (e.g., *"Suggest rerouting to Antwerp."*).

**17:00:** **Demo Ready.**