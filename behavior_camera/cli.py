import click
import cv2
import yaml
import time
from .camera import Camera


@click.group()
def cli():
    """Behavior camera control CLI."""
    pass


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    default="config.yaml",
    help="Path to camera configuration file",
)
def preview(config):
    """Preview camera feed."""
    # Load configuration
    with open(config, "r") as f:
        cfg = yaml.safe_load(f)

    # Initialize camera
    camera = Camera(cfg)
    if not camera.initialize():
        click.echo("Failed to initialize camera")
        return

    click.echo("Press 'q' to quit")

    try:
        while True:
            timestamp, frame = camera.get_frame()

            if frame is not None:
                # Display frame info
                fps = camera.get_fps()
                cv2.putText(
                    frame,
                    f"FPS: {fps:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )

                # Show the frame
                cv2.imshow("Camera Preview", frame)

                # Break if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                click.echo("Failed to capture frame")
                time.sleep(0.1)

    finally:
        camera.release()
        cv2.destroyAllWindows()


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    default="config.yaml",
    help="Path to camera configuration file",
)
def test(config):
    """Test camera configuration."""
    # Load configuration
    with open(config, "r") as f:
        cfg = yaml.safe_load(f)

    # Initialize camera
    camera = Camera(cfg)
    if not camera.initialize():
        click.echo("Failed to initialize camera")
        return

    # Capture and analyze test frames
    click.echo("\nCapturing test frames...")
    for i in range(5):
        timestamp, frame = camera.get_frame()
        if frame is not None:
            click.echo(f"\nFrame {i + 1}:")
            click.echo(f"  Shape: {frame.shape}")
            click.echo(f"  Range: [{frame.min()}, {frame.max()}]")
            click.echo(f"  Mean: {frame.mean():.2f}")

            # Save test frame
            cv2.imwrite(f"test_frame_{i + 1}.png", frame)
            click.echo(f"  Saved as test_frame_{i + 1}.png")
        else:
            click.echo(f"\nFailed to capture frame {i + 1}")
        time.sleep(0.5)

    camera.release()


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    default="config.yaml",
    help="Path to camera configuration file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="recording.avi",
    help="Output video file path",
)
@click.option(
    "--duration", "-d", type=float, default=10.0, help="Recording duration in seconds"
)
def record(config, output, duration):
    """Record video from camera."""
    # Load configuration
    with open(config, "r") as f:
        cfg = yaml.safe_load(f)

    # Initialize camera
    camera = Camera(cfg)
    if not camera.initialize():
        click.echo("Failed to initialize camera")
        return

    # Get camera resolution
    width = cfg["resolution"]["width"]
    height = cfg["resolution"]["height"]

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output, fourcc, 30.0, (width, height))

    start_time = time.time()
    frame_count = 0

    try:
        click.echo(f"Recording for {duration} seconds...")
        while (time.time() - start_time) < duration:
            timestamp, frame = camera.get_frame()

            if frame is not None:
                # Write frame
                out.write(frame)
                frame_count += 1

                # Display progress
                elapsed = time.time() - start_time
                fps = frame_count / elapsed
                click.echo(f"\rRecorded {frame_count} frames ({fps:.1f} fps)", nl=False)
            else:
                click.echo("\nFailed to capture frame")
                time.sleep(0.1)

        click.echo("\nRecording complete")
        click.echo(f"Saved {frame_count} frames to {output}")
        click.echo(f"Average FPS: {frame_count / duration:.1f}")

    finally:
        out.release()
        camera.release()


if __name__ == "__main__":
    cli()
