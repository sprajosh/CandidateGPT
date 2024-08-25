def test_create_candidate(client):
    candidate_data = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "resume_url": "https://example.com/resume.pdf",
        "skills": ["Python", "FastAPI"],
    }

    response = client.post("/candidates/", json=candidate_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == candidate_data["name"]
    assert data["email"] == candidate_data["email"]
    assert data["resume_url"] == candidate_data["resume_url"]
    assert data["skills"] == candidate_data["skills"]
    assert "id" in data
    assert "created_at" in data


def test_get_candidate(client):
    candidate_data = {
        "name": "Jane Doe",
        "email": "johndoe2@example.com",
        "resume_url": "https://example.com/resume.pdf",
        "skills": ["Python", "FastAPI"],
    }

    response = client.post("/candidates/", json=candidate_data)
    assert response.status_code == 200
    created_candidate = response.json()

    response = client.get(f"/candidates/{created_candidate['id']}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == created_candidate["id"]
    assert data["name"] == candidate_data["name"]
    assert data["email"] == candidate_data["email"]
    assert data["resume_url"] == candidate_data["resume_url"]
    assert data["skills"] == candidate_data["skills"]


def test_get_candidate_not_found(client):
    response = client.get("/candidates/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Candidate not found"}


def test_update_candidate(client):
    candidate_data = {
        "name": "Jane Doe",
        "email": "janedoe3@example.com",
        "resume_url": "https://example.com/resume.pdf",
        "skills": ["Python", "FastAPI"],
    }

    response = client.post("/candidates/", json=candidate_data)
    assert response.status_code == 200
    created_candidate = response.json()

    update_data = {
        "name": "Jane Smith",
        "email": "janesmith@example.com",
        "resume_url": "https://example.com/new_resume.pdf",
        "skills": ["Python", "FastAPI", "Django"],
    }

    response = client.put(f"/candidates/{created_candidate['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == created_candidate["id"]
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]
    assert data["resume_url"] == update_data["resume_url"]
    assert data["skills"] == update_data["skills"]


def test_update_candidate_not_found(client):
    update_data = {
        "name": "Non Existent",
        "email": "nonexistent@example.com",
    }
    response = client.put("/candidates/999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Candidate not found"}


def test_delete_candidate(client):
    candidate_data = {
        "name": "Jane Doe",
        "email": "janedoe@example.com",
        "resume_url": "https://example.com/resume.pdf",
        "skills": ["Python", "FastAPI"],
    }

    response = client.post("/candidates/", json=candidate_data)
    assert response.status_code == 200
    created_candidate = response.json()

    response = client.delete(f"/candidates/{created_candidate['id']}")

    assert response.status_code == 200
    assert response.json() == {"message": "Candidate deleted"}

    response = client.get(f"/candidates/{created_candidate['id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Candidate not found"}


def test_delete_candidate_not_found(client):
    response = client.delete("/candidates/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Candidate not found"}
