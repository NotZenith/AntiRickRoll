"""Command-line interface for fingerprint management."""

import argparse
import logging
import sys
from pathlib import Path
from antirickroll.detection.generator.service import FingerprintGenerator
from antirickroll.detection.database.manager import FingerprintDatabase

def setup_cli_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    setup_cli_logging()
    parser = argparse.ArgumentParser(description="AntiRickRoll Fingerprint Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate fingerprint from audio file")
    gen_parser.add_argument("input", type=str, help="Path to input audio file")
    gen_parser.add_argument("--name", type=str, required=True, help="Song name")
    gen_parser.add_argument("--artist", type=str, default="Unknown", help="Artist name")
    gen_parser.add_argument("--output", type=str, default="plugins/fingerprints", help="Output directory")

    # List command
    subparsers.add_parser("list", help="List installed fingerprints")

    args = parser.parse_args()

    if args.command == "generate":
        input_path = Path(args.input)
        output_dir = Path(args.output)

        generator = FingerprintGenerator()
        package = generator.generate_from_file(
            input_path, name=args.name, artist=args.artist
        )

        if package:
            db = FingerprintDatabase(output_dir)
            saved_path = db.save_package(package)
            print(f"Successfully generated fingerprint: {saved_path}")
        else:
            print("Failed to generate fingerprint.")
            sys.exit(1)

    elif args.command == "list":
        db = FingerprintDatabase(Path("plugins/fingerprints"))
        db.load_all()
        print(f"Installed fingerprints ({len(db.packages)}):")
        for pkg in db.packages.values():
            print(f"- {pkg.metadata.name} by {pkg.metadata.artist} (ID: {pkg.metadata.id})")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
