# EKS Scaling Diagram with Keda and Karpenter

This repo generates a diagram illustrating EKS scaling with Keda and Karpenter based on the number of messages in an SQS queue for the blog post.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required Python libraries:

    ```sh
    pip install pillow diagrams graphviz
    ```

4. Ensure `graphviz` is installed on your system. You can install it using your package manager. For example, on Ubuntu:

    ```sh
    sudo apt-get install graphviz
    ```

    On macOS, you can use Homebrew:

    ```sh
    brew install graphviz
    ```

## Usage

1. Ensure you have the images `keda.png` and `karpenter.png` in the project directory.
2. Run the script to generate the diagram:

    ```sh
    python3 diagram.py
    ```

## Output

The script will generate a diagram showing the EKS scaling setup with Keda and Karpenter.

## Notes

- The images `keda.png` and `karpenter.png` will be resized to 300x300 pixels before being used in the diagram.

