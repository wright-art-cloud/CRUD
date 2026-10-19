from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data model
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# Initial in-memory database list
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find an event by ID to avoid duplicate logic
def find_event_by_id(event_id):
    return next((event for event in events if event.id == event_id), None)

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    
    # Input validation: Check if JSON is provided and contains a title
    if not data or "title" not in data:
        return jsonify({"error": "Missing required field: 'title'"}), 400

    # Generate a new unique ID based on the last item (or 1 if list is empty)
    new_id = events[-1].id + 1 if events else 1
    
    # Create new Event instance and append to simulated database
    new_event = Event(id=new_id, title=data["title"])
    events.append(new_event)
    
    # Return the created resource with 201 Created status code
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<int:id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event_by_id(event_id)
    
    # Resource Not Found check
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' field for update"}), 400

    # Update event title
    event.title = data["title"]
    
    return jsonify(event.to_dict()), 200

# DELETE /events/<int:id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event_by_id(event_id)
    
    # Resource Not Found check
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Remove event from list
    events.remove(event)
    
    # Return 204 No Content on successful deletion (or success JSON message)
    return jsonify({"message": "Event successfully deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)