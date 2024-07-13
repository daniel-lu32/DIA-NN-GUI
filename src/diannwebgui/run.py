import subprocess
import os
import signal
import sys


def main():
    # Resolve the path to home.py
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "app.py"))

    # Run the Streamlit app with specified arguments
    process = subprocess.Popen(
        ["streamlit", "run", script_path],
    )

    def signal_handler(sig, frame):
        print('Terminating Streamlit process...')
        process.terminate()
        #process.wait(timeout=2)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    process.wait()


if __name__ == "__main__":
    main()
