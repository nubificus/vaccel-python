import argparse
from pathlib import Path

from vaccel import Resource, ResourceType, Session


def main():
    parser = argparse.ArgumentParser(description="Classify an image.")
    parser.add_argument(
        "image_file", type=str, help="Path to an image file to classify."
    )
    parser.add_argument(
        "-m",
        "--model-path",
        type=str,
        required=False,
        help="Path to the model to use for classification.",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        required=False,
        default=1,
        help="Number of iterations to run.",
    )
    args = parser.parse_args()

    session = Session()

    if args.model_path:
        resource = Resource(args.model_path, ResourceType.MODEL)
        resource.register(session)

    with Path(args.image_file).open("rb") as f:
        image = f.read()

    for _i in range(args.iterations):
        (prediction, _) = session.classify(image)
        print(f"Prediction: {prediction}")


if __name__ == "__main__":
    main()
