def test_create_opportunity(client):
    opportunity_data = {
        "title": "Software Engineer",
        "description": "Develop and maintain software applications.",
        "location": "New York",
        "required_skills": ["Python", "FastAPI", "SQL"],
    }

    response = client.post("/opportunities/", json=opportunity_data)
    # import ipdb

    # ipdb.set_trace()
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == opportunity_data["title"]
    assert data["description"] == opportunity_data["description"]
    assert data["location"] == opportunity_data["location"]
    assert data["required_skills"] == opportunity_data["required_skills"]
    assert "id" in data
    assert "created_at" in data


def test_get_opportunities(client):
    opportunity_data1 = {
        "title": "Software Engineer",
        "description": "Develop and maintain software applications.",
        "location": "New York",
        "required_skills": ["Python", "FastAPI"],
    }
    opportunity_data2 = {
        "title": "Data Scientist",
        "description": "Analyze and interpret complex data.",
        "location": "San Francisco",
        "required_skills": ["Python", "Machine Learning"],
    }

    client.post("/opportunities/", json=opportunity_data1)
    client.post("/opportunities/", json=opportunity_data2)

    response = client.get("/opportunities/")

    assert response.status_code == 200
    data = response.json()

    assert len(data) >= 2
    assert any(opportunity["title"] == "Software Engineer" for opportunity in data)
    assert any(opportunity["title"] == "Data Scientist" for opportunity in data)
    assert all("required_skills" in opportunity for opportunity in data)


def test_get_opportunity(client):
    opportunity_data = {
        "title": "Software Engineer",
        "description": "Develop and maintain software applications.",
        "location": "New York",
        "required_skills": ["Python", "FastAPI"],
    }

    response = client.post("/opportunities/", json=opportunity_data)
    assert response.status_code == 200
    created_opportunity = response.json()

    response = client.get(f"/opportunities/{created_opportunity['id']}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == created_opportunity["id"]
    assert data["title"] == opportunity_data["title"]
    assert data["description"] == opportunity_data["description"]
    assert data["location"] == opportunity_data["location"]
    assert data["required_skills"] == opportunity_data["required_skills"]


def test_get_opportunity_not_found(client):
    response = client.get("/opportunities/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Opportunity not found"}


def test_update_opportunity(client):
    opportunity_data = {
        "title": "Software Engineer",
        "description": "Develop and maintain software applications.",
        "location": "New York",
        "required_skills": ["Python", "FastAPI"],
    }

    response = client.post("/opportunities/", json=opportunity_data)
    assert response.status_code == 200
    created_opportunity = response.json()

    update_data = {
        "title": "Senior Software Engineer",
        "description": "Lead software development projects.",
        "location": "New York",
        "required_skills": ["Python", "FastAPI", "Leadership"],
    }

    response = client.put(
        f"/opportunities/{created_opportunity['id']}", json=update_data
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == created_opportunity["id"]
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["location"] == update_data["location"]
    assert data["required_skills"] == update_data["required_skills"]


def test_update_opportunity_not_found(client):
    update_data = {
        "title": "Non Existent Opportunity",
        "description": "This opportunity does not exist.",
    }
    response = client.put("/opportunities/999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Opportunity not found"}


def test_delete_opportunity(client):
    opportunity_data = {
        "title": "Software Engineer",
        "description": "Develop and maintain software applications.",
        "location": "New York",
        "required_skills": ["Python", "FastAPI"],
    }

    response = client.post("/opportunities/", json=opportunity_data)
    assert response.status_code == 200
    created_opportunity = response.json()

    response = client.delete(f"/opportunities/{created_opportunity['id']}")

    assert response.status_code == 200
    assert response.json() == {"message": "Opportunity deleted"}

    response = client.get(f"/opportunities/{created_opportunity['id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Opportunity not found"}


def test_delete_opportunity_not_found(client):
    response = client.delete("/opportunities/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Opportunity not found"}
