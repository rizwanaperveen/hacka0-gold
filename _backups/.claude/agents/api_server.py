"""REST API server for the multi-agent system using Flask."""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from pathlib import Path
from agent_runner import AgentRunner


app = Flask(__name__)
CORS(app)

# Initialize agent runner
config_path = Path(__file__).parent / "config.json"
if config_path.exists():
    with open(config_path, 'r') as f:
        config = json.load(f)
    runner = AgentRunner(config)
else:
    runner = AgentRunner()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "multi-agent-system"})


@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List all available agents."""
    agents = {
        "ceo": "CEO Agent - Coordinates and oversees all agents",
        "personal": "Personal Agent - Manages personal tasks and schedules",
        "business": "Business Agent - Handles business operations",
        "social": "Social Agent - Manages social media and networking",
        "autonomous": "Autonomous Agent - Self-directed with independent goals"
    }
    return jsonify({"agents": agents})


@app.route('/api/agents/status', methods=['GET'])
def get_statuses():
    """Get status of all agents."""
    statuses = runner.get_all_statuses()
    return jsonify({"statuses": statuses})


@app.route('/api/tasks', methods=['POST'])
def run_task():
    """Run a single task."""
    try:
        task = request.get_json()

        if not task:
            return jsonify({"error": "No task data provided"}), 400

        if "agent_type" not in task:
            return jsonify({"error": "agent_type is required"}), 400

        result = runner.run_task(task)
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/tasks/batch', methods=['POST'])
def run_batch():
    """Run multiple tasks in batch."""
    try:
        data = request.get_json()
        tasks = data.get("tasks", [])

        if not tasks:
            return jsonify({"error": "No tasks provided"}), 400

        results = runner.run_batch(tasks)
        return jsonify({"results": results, "count": len(results)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ceo/delegate', methods=['POST'])
def delegate_task():
    """Delegate a task from CEO to another agent."""
    try:
        data = request.get_json()

        if not data or "task" not in data or "target_agent" not in data:
            return jsonify({"error": "task and target_agent are required"}), 400

        result = runner.delegate_from_ceo(data["task"], data["target_agent"])
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/results', methods=['GET'])
def get_results():
    """Get results from all agents."""
    agent_type = request.args.get('agent')

    if agent_type:
        if agent_type == "ceo":
            results = runner.ceo.get_results()
        elif agent_type in runner.agents:
            results = runner.agents[agent_type].get_results()
        else:
            return jsonify({"error": f"Unknown agent: {agent_type}"}), 404

        return jsonify({"agent": agent_type, "results": results})
    else:
        all_results = runner.get_all_results()
        return jsonify({"results": all_results})


@app.route('/api/results', methods=['DELETE'])
def clear_results():
    """Clear results from all agents."""
    runner.clear_all_results()
    return jsonify({"message": "All results cleared"})


@app.route('/api/autonomous/goals', methods=['POST'])
def set_autonomous_goal():
    """Set a goal for the autonomous agent."""
    try:
        data = request.get_json()
        goal = data.get("goal")

        if not goal:
            return jsonify({"error": "goal is required"}), 400

        runner.agents["autonomous"].set_goal(goal)
        return jsonify({"message": "Goal set successfully", "goal": goal})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/autonomous/goals', methods=['GET'])
def get_autonomous_goals():
    """Get all goals for the autonomous agent."""
    goals = runner.agents["autonomous"].goals
    return jsonify({"goals": goals})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


def main():
    """Run the API server."""
    print("=" * 60)
    print("Multi-Agent System API Server")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET  /health                    - Health check")
    print("  GET  /api/agents                - List agents")
    print("  GET  /api/agents/status         - Get agent statuses")
    print("  POST /api/tasks                 - Run a task")
    print("  POST /api/tasks/batch           - Run batch tasks")
    print("  POST /api/ceo/delegate          - Delegate from CEO")
    print("  GET  /api/results               - Get results")
    print("  DELETE /api/results             - Clear results")
    print("  POST /api/autonomous/goals      - Set autonomous goal")
    print("  GET  /api/autonomous/goals      - Get autonomous goals")
    print("\nServer starting on http://localhost:5000")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
