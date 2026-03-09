import sys
import os

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from jules_tools import JulesUIDTTools
except ImportError:
    print("CRITICAL: jules_tools not found. Ensure it is in the root directory.")
    sys.exit(1)

def verify_task():
    tools = JulesUIDTTools()

    # Verify 2+2=4
    # Expected: 4
    # Tolerance: 1e-14
    success = tools.mpmath_tool('2+2', 4, 1e-14)

    if not success:
        print("Verification failed!")
        sys.exit(1)

    # Generate commit message
    # Summary: "Verify 2+2=4"
    # Type: "chore"
    # Evidence: "A" (Analytically Proven)
    msg = tools.commit_tool("Verify 2+2=4", "chore", "A")

    # Write the commit message to a file for the next step to read
    # Write to current working directory (root)
    with open('commit_message.txt', 'w') as f:
        f.write(msg)

if __name__ == "__main__":
    verify_task()
