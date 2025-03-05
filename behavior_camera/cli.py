import click
import sys
import time
from .camera import Camera
from .recorder import VideoRecorder
from .config import load_config


@click.group()
def cli():
    """Behavior camera control and recording."""
    pass


@cli.command()
@click.option("--config", required=True, help="Path to configuration file")
def record(config):
    """Start recording from the camera."""
    try:
        # Load configuration
        config_data = load_config(config)

        # Initialize camera
        camera = Camera()
        if not camera.initialize():
            click.echo("Failed to initialize camera", err=True)
            sys.exit(1)

        # Configure camera
        camera.configure(config_data["camera"])

        # Initialize recorder
        recorder = VideoRecorder(
            config_data["recording"]["output_directory"], config_data
        )

        # Start recording
        recorder.start_recording()
        click.echo("Recording started. Press Ctrl+C to stop.")

        try:
            while True:
                timestamp, frame = camera.get_frame()
                if frame is not None:
                    recorder.record_frame(frame, timestamp)
                time.sleep(1 / config_data["camera"]["framerate"])

        except KeyboardInterrupt:
            click.echo("\nStopping recording...")

        finally:
            recorder.stop_recording()
            camera.release()
            click.echo("Recording finished.")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
