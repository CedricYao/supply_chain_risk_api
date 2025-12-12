# User Stories for "Port Watch" (1-Day Hackathon Prototype)

## Context
**Project:** Port Watch (Proactive Supply Chain Risk Agent Prototype)  
**Goal:** Build a functional proof-of-concept in < 6 hours that demonstrates using Gemini to bridge unstructured news data with structured shipment data.  
**Primary Persona:** Supply Chain Coordinator (Schwarz Group)

---

## Story 1: Manual Risk Intelligence Input

### Description
**As a** Supply Chain Coordinator,  
**I want** to manually paste text snippets describing potential supply chain disruptions (e.g., news about strikes or weather),  
**So that** I can test the system's analysis capabilities on specific scenarios without relying on live API integrations.

### INVEST Analysis
*   **Independent:** Yes, this is the entry point of the application workflow.
*   **Negotiable:** Yes, the UI could be a text box, a file upload, or a pre-set selection. We are settling on a text paste for speed.
*   **Valuable:** Essential for the "Simulated Trigger" scope of the hackathon.
*   **Estimable:** Low effort (standard UI input).
*   **Small:** Fits easily into the "Interface & Polish" phase.
*   **Testable:** Verification is straightforward (can text be entered?).

### Acceptance Criteria
*   **Scenario: Valid Text Input**
    *   **Given** the Port Watch application is open
    *   **When** I paste a paragraph of text into the "News Snippet" input field
    *   **And** I click the "Analyze Risk" button
    *   **Then** the system should accept the input and begin processing.
*   **Scenario: Empty Input**
    *   **Given** the input field is empty
    *   **When** I click the "Analyze Risk" button
    *   **Then** the system should display a prompt asking me to enter text first.

---

## Story 2: AI-Powered Event Extraction

### Description
**As a** Supply Chain Coordinator,  
**I want** the system to automatically identify the *Port Name*, *Event Type*, and *Disruption Severity* from the unstructured text I provided,  
**So that** the raw news text is converted into structured data that can be compared against my shipment records.

### INVEST Analysis
*   **Independent:** Can be developed and tested in the "Prompt Engineering" phase using the console before UI integration.
*   **Negotiable:** The specific JSON structure can be adjusted, but the core entities are fixed.
*   **Valuable:** This is the core "AI Reasoning" value proposition of the prototype.
*   **Estimable:** Medium effort (prompt engineering required).
*   **Small:** Focused solely on extraction, not matching.
*   **Testable:** Can be tested against the 3 curated snippets defined in the roadmap.

### Acceptance Criteria
*   **Scenario: Clear Port Disruption**
    *   **Given** the input text matches the test snippet: "Labor unions have announced a 48-hour walkout at the Port of Rotterdam..."
    *   **When** the system processes this text
    *   **Then** it should extract: `{"port_name": "Rotterdam", "event_type": "Strike", "is_disruption": true}`.
*   **Scenario: No Location Found**
    *   **Given** the input text contains no specific geographic location
    *   **When** the system processes this text
    *   **Then** it should return a standardized "Unknown" or null value for the location field.
*   **Scenario: Irrelevant News**
    *   **Given** the input text is a general news story with no supply chain impact
    *   **When** the system processes this text
    *   **Then** it should flag `is_disruption` as `false`.

---

## Story 3: Shipment Impact Analysis

### Description
**As a** Supply Chain Coordinator,  
**I want** the system to filter the active shipment list to show only those goods destined for the impacted port,  
**So that** I can immediately identify which specific orders (e.g., Bananas, Electronics) are at risk of delay.

### INVEST Analysis
*   **Independent:** Depends on Story 2 for input, but the logic can be built with mock inputs first.
*   **Negotiable:** The matching logic is simplified (exact string match vs fuzzy match).
*   **Valuable:** Connects the external event to internal business value.
*   **Estimable:** Low effort (standard list filtering).
*   **Small:** Core logic is a simple loop.
*   **Testable:** Can be verified against the hardcoded `shipments` list.

### Acceptance Criteria
*   **Scenario: Matching Logic**
    *   **Given** the system has extracted "Rotterdam" as the impacted port
    *   **And** the hardcoded shipment list contains shipments for "Rotterdam", "Hamburg", and "Valencia"
    *   **When** the impact analysis runs
    *   **Then** only the "Rotterdam" shipments (e.g., ID SCH-9001) should be returned.
*   **Scenario: No Impact**
    *   **Given** the system has extracted "London" as the impacted port
    *   **And** no shipments in the list are destined for "London"
    *   **When** the impact analysis runs
    *   **Then** the system should return an empty list or a "No Shipments Affected" message.

---

## Story 4: Intelligent Mitigation Advice

### Description
**As a** Supply Chain Coordinator,  
**I want** the system to provide a one-sentence recommendation based on the event details (e.g., "Suggest rerouting to Antwerp"),  
**So that** I have an immediate starting point for resolving the disruption rather than just staring at a problem.

### INVEST Analysis
*   **Independent:** Can be developed as a separate Gemini call.
*   **Negotiable:** The complexity of the advice can range from generic to highly specific.
*   **Valuable:** demonstrative of "Generative" AI capabilities beyond just extraction.
*   **Estimable:** Low effort (prompt engineering).
*   **Small:** Single API call.
*   **Testable:** Subjective quality check, but can be verified that *some* advice is generated.

### Acceptance Criteria
*   **Scenario: Mitigation Generation**
    *   **Given** a "Strike" event at "Rotterdam"
    *   **When** the system generates advice
    *   **Then** the output should be a coherent sentence offering a logistical alternative or action (e.g., rerouting or contacting the carrier).
*   **Scenario: Non-Disruptive Event**
    *   **Given** the event is not a disruption (`is_disruption: false`)
    *   **When** the system processes the advice step
    *   **Then** it should output "No action required."

---

## Story 5: Integrated Risk Dashboard

### Description
**As a** Supply Chain Coordinator,  
**I want** to see a consolidated view showing the Alert Details, List of Affected Shipments, and Mitigation Advice on one screen,  
**So that** I can assess the situation efficiently without toggling between tools or logs.

### INVEST Analysis
*   **Independent:** Combines the outputs of previous stories.
*   **Negotiable:** UI layout is flexible (Streamlit text area vs dataframe).
*   **Valuable:** Provides the actual user experience.
*   **Estimable:** Low to Medium effort (Streamlit assembly).
*   **Small:** Focusing on a single-page view.
*   **Testable:** Visual verification of the UI elements.

### Acceptance Criteria
*   **Scenario: Full Disruption Display**
    *   **Given** a valid risk scenario has been processed
    *   **Then** the dashboard should display:
        1.  A clear "Red" or "High" severity indicator.
        2.  The reason for the alert (e.g., "Strike at Port of Rotterdam").
        3.  A table or list of the specific affected Shipment IDs.
        4.  The generated mitigation advice text.
