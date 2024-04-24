import requests

base_url = "http://127.0.0.1:5000"

test_data = {
  "question": "What is our pricing model?",
  "documents": [
      "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240314_104111.txt",
      "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240315_104111.txt",
      "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240316_104111.txt"
  ],
}

def test_submit_question_and_documents():
    response = requests.post(f"{base_url}/submit_question_and_documents", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Submitted successfully"}

def test_get_latest_question_and_facts():
    response = requests.get(f"{base_url}/get_latest_question_and_facts")
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "facts" in data
    assert "status" in data

if __name__ == "__main__":
    test_submit_question_and_documents()
    test_get_latest_question_and_facts()
    print("All tests passed successfully.")